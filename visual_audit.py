"""Compare garment features on cached human outfits; never export a runtime model.

The target is held out co-occurrence, not a claim about human beauty ratings.
All profiles use the same creator split, training examples and test candidates.
"""
import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np

from otak import (
    ASET_KE_SLOT, W2_SLOT_2D, muat_emb, muat_state, muat_w2,
    slot_item_seed, warna_desain,
)


def creator_key(outfit_hash, outfit):
    return str(outfit.get("K") or outfit_hash)


def held_out(key):
    return int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % 5 == 0


def normalized(vector):
    v = np.asarray(vector, dtype=np.float32)
    if v.shape != (512,) or not np.isfinite(v).all():
        raise ValueError("Invalid 512-dimensional feature")
    norm = float(np.linalg.norm(v))
    if norm <= 1e-6:
        raise ValueError("Empty feature")
    return v / norm


def build_features(original, cropped, slots, weight):
    rows, counts = [], {slot: [0, 0] for slot in W2_SLOT_2D}
    for item_id in sorted(original):
        v = normalized(original[item_id])
        slot = slots[item_id]
        if slot in counts:
            counts[slot][1] += 1
            if item_id in cropped:
                counts[slot][0] += 1
                if weight:
                    v = normalized((1 - weight) * v + weight * normalized(cropped[item_id]))
        rows.append(v)
    return np.stack(rows), counts


def negative_items(pool, used, rng, count):
    # Bounded sampling also covers a slot whose entire catalog is in the outfit.
    # Returning None lets the caller skip that target without hanging the runner.
    valid = pool[~np.isin(pool, list(used))]
    if not len(valid):
        return None
    return rng.choice(valid, size=count, replace=len(valid) < count).astype(np.int64)


def make_training(outfits, pools):
    training = []
    pool_sets = {slot: set(pool.tolist()) for slot, pool in pools.items()}
    for key, items in outfits:
        used = set(i for i, _ in items)
        targets = [k for k, (_, slot) in enumerate(items)
                   if len(pools[slot]) > len(used & pool_sets[slot])]
        if targets:
            training.append((key, items, targets))
    if len(training) < 60:
        raise RuntimeError("Fewer than 60 eligible training outfits; no model comparison")
    return training


def make_questions(outfits, pools, item_info, ids, seed=811, limit=4000):
    rng = np.random.default_rng(seed)
    questions, per_creator = [], {}
    for key, items in outfits:
        if per_creator.get(key, 0) >= 20:
            continue
        used = set(i for i, _ in items)
        for k in rng.permutation(len(items)):
            target, slot = items[k]
            random_neg = negative_items(pools[slot], used, rng, 7)
            if random_neg is None or len(set(random_neg.tolist())) < 7:
                continue
            context = [i for j, (i, _) in enumerate(items) if j != k]
            info = item_info.get(ids[target])
            hard_neg = None
            if info:
                color, gender = info
                hard_pool = np.array([i for i in pools[slot]
                    if item_info.get(ids[i]) == (color, gender)], dtype=np.int64)
                if len(hard_pool) >= 8:
                    hard_neg = negative_items(hard_pool, used, rng, 7)
                    if hard_neg is not None and len(set(hard_neg.tolist())) < 7:
                        hard_neg = None
            questions.append(dict(creator=key, target=target, slot=slot, context=context,
                random=[target] + random_neg.tolist(),
                hard=[target] + hard_neg.tolist() if hard_neg is not None else None))
            per_creator[key] = per_creator.get(key, 0) + 1
            if len(questions) >= limit:
                return questions
            if per_creator[key] >= 20:
                break
    return questions


def train(features, training, pools, slot_array, steps=500, seed=29):
    import torch
    torch.manual_seed(seed)
    torch.set_num_threads(min(2, max(1, os.cpu_count() or 1)))
    rng = np.random.default_rng(seed)
    # Means only use training items. Held out creators do not influence centering.
    seen = sorted(set(i for _, items, _ in training for i, _ in items))
    means = {s: features[[i for i in seen if slot_array[i] == s]].mean(axis=0)
             for s in pools if any(slot_array[i] == s for i in seen)}
    x = features - np.stack([means.get(s, np.zeros(512, np.float32)) for s in slot_array])
    x /= np.maximum(np.linalg.norm(x, axis=1, keepdims=True), 1e-6)
    xt = torch.from_numpy(x)
    model = torch.nn.Sequential(torch.nn.Linear(512, 128), torch.nn.GELU(),
                                torch.nn.Linear(128, 32))
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.0001)
    started = time.monotonic()
    for step in range(steps):
        contexts, positives, negatives = [], [], []
        for _ in range(64):
            _, items, targets = training[int(rng.integers(len(training)))]
            k = int(rng.choice(targets))
            target, slot = items[k]
            used = set(i for i, _ in items)
            negative = negative_items(pools[slot], used, rng, 12)
            if negative is None:
                raise AssertionError("Training eligibility changed")
            contexts.append([i for j, (i, _) in enumerate(items) if j != k])
            positives.append(target)
            negatives.append(negative.tolist())
        all_ids = sorted(set(positives + [i for c in contexts for i in c]
                             + [i for n in negatives for i in n]))
        position = {i: k for k, i in enumerate(all_ids)}
        z = torch.nn.functional.normalize(model(xt[all_ids]), dim=1)
        c = torch.nn.functional.normalize(torch.stack([
            z[[position[i] for i in context]].mean(dim=0) for context in contexts]), dim=1)
        positive = z[[position[i] for i in positives]]
        negative = z[[[position[i] for i in n] for n in negatives]]
        logits = torch.cat([(c * positive).sum(-1, keepdim=True),
                            torch.einsum("bd,bkd->bk", c, negative)], dim=1) / 0.07
        loss = torch.nn.functional.cross_entropy(logits, torch.zeros(64, dtype=torch.long))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if time.monotonic() - started > 240:
            raise RuntimeError("Equal-step audit exceeded CPU deadline; comparison not released")
    model.eval()
    vectors = []
    with torch.no_grad():
        for first in range(0, len(xt), 1024):
            vectors.append(torch.nn.functional.normalize(model(xt[first:first + 1024]), dim=1).numpy())
    return np.concatenate(vectors), dict(steps=steps, seconds=round(time.monotonic() - started, 2))


def evaluate(vectors, questions, candidates, only_2d=False):
    correct, rows = 0, []
    for q in questions:
        options = q[candidates]
        if options is None or (only_2d and q["slot"] not in W2_SLOT_2D):
            continue
        context = vectors[q["context"]].mean(axis=0)
        context /= max(float(np.linalg.norm(context)), 1e-6)
        scores = vectors[options] @ context
        # Tie must not count as a successful prediction of the first option.
        good = bool(scores[0] > np.max(scores[1:]))
        correct += int(good)
        rows.append((q["creator"], good))
    return dict(correct=correct, questions=len(rows),
                accuracy=correct / len(rows) if rows else None), rows


def paired_difference(base, candidate, seed=491):
    if len(base) != len(candidate) or not base:
        return None
    per_creator = {}
    for (key, a), (key_b, b) in zip(base, candidate):
        if key != key_b:
            raise AssertionError("Different test cases between profiles")
        total, count = per_creator.get(key, (0, 0))
        per_creator[key] = (total + int(b) - int(a), count + 1)
    values = np.asarray(list(per_creator.values()), dtype=np.float64)
    rng = np.random.default_rng(seed)
    deltas = []
    for _ in range(500):
        bag = values[rng.integers(len(values), size=len(values))]
        deltas.append(float(bag[:, 0].sum() / bag[:, 1].sum()))
    return dict(delta=float(values[:, 0].sum() / values[:, 1].sum()),
                creator_bootstrap_ci95=np.quantile(deltas, [0.025, 0.975]).tolist(),
                creators=len(values))


def main():
    state = muat_state()
    original, _ = muat_emb()
    _, _, cropped = muat_w2()
    if len(original) < 5000 or len(cropped) < 1000:
        raise RuntimeError("Full training cache missing; local sample cannot support this audit")
    slots = {}
    for outfit in state["outfit"].values():
        for item_id, slot in slot_item_seed(outfit):
            slots.setdefault(item_id, slot)
    for key, metadata in state["meta"].items():
        slot = ASET_KE_SLOT.get(metadata.get("t"))
        if slot:
            slots.setdefault(int(key), slot)
    original = {i: v for i, v in original.items() if i in slots and slots[i] != "Alis"}
    ids = sorted(original)
    position = {i: k for k, i in enumerate(ids)}
    slot_array = np.asarray([slots[i] for i in ids])
    pools = {s: np.where(slot_array == s)[0] for s in set(slot_array.tolist())}
    train_outfits, test_outfits = [], []
    for h, outfit in sorted(state["outfit"].items(),
                           key=lambda pair: hashlib.sha256(pair[0].encode()).digest()):
        items, seen = [], set()
        for i, s in slot_item_seed(outfit):
            if i in position and i not in seen:
                items.append((position[i], s))
                seen.add(i)
        if len(items) >= 3:
            key = creator_key(h, outfit)
            target = test_outfits if held_out(key) else train_outfits
            if len(target) < (3000 if held_out(key) else 9000):
                target.append((key, items))
    training = make_training(train_outfits, pools)
    train_creators = {k for k, _, _ in training}
    test_creators = {k for k, _ in test_outfits}
    if train_creators & test_creators:
        raise AssertionError("Creator leakage")
    item_info = {}
    for shard in sorted(Path("model").glob("item_*.json")):
        for item_id, row in json.loads(shard.read_text(encoding="utf-8"))["d"].items():
            color, _, _ = warna_desain(row[2])
            g = row[1]
            if color != 15:
                item_info[int(item_id)] = (color, 0 if g < 35 else 2 if g > 65 else 1)
    questions = make_questions(test_outfits, pools, item_info, ids)
    if len(questions) < 150:
        raise RuntimeError("Insufficient held out test questions")
    report = dict(runtime_changed=False, purpose="Cached garment feature experiment",
        limitations=["Co-occurrence test is not a human beauty rating",
            "CPU audit head differs from the production network",
            "No assembled 3D collision or motif semantics guarantee",
            "No automatic runtime replacement from this report"],
        train_outfits=len(training), test_outfits=len(test_outfits),
        train_creators=len(train_creators), test_creators=len(test_creators),
        creator_overlap=0, items=len(ids), profiles={})
    results = {}
    for name, weight in [("original", 0), ("half_crop", 0.5), ("crop", 1)]:
        features, coverage = build_features(original, cropped, slots, weight)
        vectors, timing = train(features, training, pools, slot_array)
        scores, rows_by_metric = {}, {}
        for candidates in ("random", "hard"):
            for only_2d in (False, True):
                metric = candidates + ("_2d" if only_2d else "_all")
                scores[metric], rows_by_metric[metric] = evaluate(vectors, questions, candidates, only_2d)
        results[name] = rows_by_metric
        report["profiles"][name] = dict(weight=weight, coverage=coverage, timing=timing, scores=scores)
        if name != "original":
            report["profiles"][name]["paired_vs_original"] = {
                m: paired_difference(results["original"][m], rows_by_metric[m]) for m in scores}
        print(name, json.dumps(report["profiles"][name]), flush=True)
        del features, vectors
    Path("visual-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Pembandingan fitur pakaian", "", "Model map tidak diganti oleh audit ini.", "",
             "| Fitur | FITB acak | FITB sulit | FITB sulit pakaian 2D |", "|---|---:|---:|---:|"]
    for name, profile in report["profiles"].items():
        def value(metric):
            score = profile["scores"][metric]
            return (f"{score['accuracy']:.4f} ({score['questions']} soal)"
                    if score["accuracy"] is not None else "Tidak cukup data")
        lines.append(f"| {name} | {value('random_all')} | {value('hard_all')} | {value('hard_2d')} |")
    lines += ["", "Kandidat sulit memiliki slot, kelompok warna dan skor gender yang sama.",
              "Split per kreator; bootstrap selisih berpasangan per kreator ada di JSON.",
              "Hasil mengukur prediksi item yang dipakai bersama, belum penilaian keindahan manusia."]
    Path("visual-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
