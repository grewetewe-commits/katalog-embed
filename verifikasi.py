#!/usr/bin/env python3
"""
PENGOREKSI (verifikasi) hasil embed.py -- tidak percaya pada klaim, hanya pada angka.

Pertanyaan yang dijawab:
  1. Apakah hasilnya sehat? (tidak ada NaN, tidak runtuh jadi satu titik, tidak banyak gambar placeholder/duplikat)
  2. Apakah sidik jari visual benar-benar membawa informasi tentang KESERASIAN?
     Alat ukurnya adalah label yang SUDAH kita punya dari data nyata (labels.json):
       - tema   : item yang berasal dari tema yang sama (mis. Angel & Divine) seharusnya lebih mirip,
                  termasuk LINTAS slot (baju vs topi) -- itu yang relevan untuk menyusun outfit.
       - kreator: item dari satu kreator (satu set) seharusnya lebih mirip.
     Ukuran: AUC = peluang pasangan "satu tema" lebih mirip daripada pasangan "beda tema".
             0,5 = sama saja dengan acak, 1,0 = sempurna.
  3. Apakah tag zero-shot (gaya/atribut) masuk akal terhadap tema yang sudah kita ketahui?

Keluaran: out/LAPORAN.md, out/verifikasi.json, dan (di GitHub Actions) ringkasan di halaman jalannya workflow.
Kode keluar 1 hanya untuk kegagalan keras (NaN / terlalu banyak thumbnail gagal pada jalan penuh / data kosong).
"""
import json
import os
import random
import sys

import numpy as np

from embed import pusatkan_per_slot

OUT = "out"
LABELS = "labels.json"
N_PASANGAN = 8000
MIN_JALAN_PENUH = 500  # di bawah ini dianggap uji kecil: AUC belum bermakna


def muat():
    p = os.path.join(OUT, "raw.npz")
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=False)
    ids = d["ids"].astype("int64")
    emb = d["emb"].astype("float32")
    slot = np.array([str(s) for s in d["slot"].tolist()])
    return ids, emb, slot


def norm_baris(x):
    n = np.linalg.norm(x, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return x / n


def auc(pos, neg):
    pos = np.asarray(pos, dtype="float64")
    neg = np.asarray(neg, dtype="float64")
    if len(pos) < 30 or len(neg) < 30:
        return None
    semua = np.concatenate([pos, neg])
    urut = np.argsort(semua, kind="mergesort")
    nilai = semua[urut]
    peringkat_terurut = np.arange(1, len(semua) + 1, dtype="float64")
    i = 0
    n = len(nilai)
    while i < n:  # rata-ratakan peringkat untuk nilai kembar
        j = i
        while j + 1 < n and nilai[j + 1] == nilai[i]:
            j += 1
        if j > i:
            peringkat_terurut[i:j + 1] = (i + 1 + j + 1) / 2.0
        i = j + 1
    peringkat = np.empty(n)
    peringkat[urut] = peringkat_terurut
    r_pos = peringkat[:len(pos)].sum()
    return float((r_pos - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def ambil_pasangan(label_dari, slot, rng, lintas_slot, n, sama):
    """Ambil n pasangan (a,b). sama=True: label sama; sama=False: label beda. Hanya item berlabel."""
    idx_label = [i for i, l in enumerate(label_dari) if l is not None]
    per_label = {}
    for i in idx_label:
        per_label.setdefault(label_dari[i], []).append(i)
    pasangan = []
    coba = 0
    while len(pasangan) < n and coba < n * 60:
        coba += 1
        a = rng.choice(idx_label)
        if sama:
            kandidat = per_label[label_dari[a]]
            if len(kandidat) < 2:
                continue
            b = rng.choice(kandidat)
        else:
            b = rng.choice(idx_label)
        if a == b:
            continue
        if (label_dari[a] == label_dari[b]) != sama:
            continue
        if lintas_slot and slot[a] == slot[b]:
            continue
        if (not lintas_slot) and slot[a] != slot[b]:
            continue
        pasangan.append((a, b))
    return pasangan


def sim_pasangan(e, pasangan):
    if not pasangan:
        return np.array([])
    a = np.array([p[0] for p in pasangan])
    b = np.array([p[1] for p in pasangan])
    return (e[a] * e[b]).sum(axis=1)


def presisi_tetangga(e, slot, label_dari, rng, k=5, maks_sumber=400):
    """Dari tetangga terdekat LINTAS slot: berapa persen yang satu label? Dibanding tetangga acak lintas slot."""
    n = len(e)
    idx = [i for i in range(n) if label_dari[i] is not None]
    rng.shuffle(idx)
    idx = idx[:maks_sumber]
    sim = e @ e.T
    hit = tot = hit_acak = tot_acak = 0
    for a in idx:
        mask = (slot != slot[a]) & np.array([label_dari[j] is not None for j in range(n)])
        kandidat = np.where(mask)[0]
        if len(kandidat) < k * 2:
            continue
        urut = kandidat[np.argsort(-sim[a][kandidat])[:k]]
        hit += sum(1 for j in urut if label_dari[j] == label_dari[a])
        tot += len(urut)
        acak = rng.sample(list(kandidat), k)
        hit_acak += sum(1 for j in acak if label_dari[j] == label_dari[a])
        tot_acak += len(acak)
    if tot == 0:
        return None
    return {"presisi": hit / tot, "dasar_acak": hit_acak / max(1, tot_acak), "sumber": len(idx)}


def label_penilaian(a):
    if a is None:
        return "belum bisa dinilai"
    if a >= 0.75:
        return "KUAT"
    if a >= 0.65:
        return "SEDANG"
    if a >= 0.58:
        return "LEMAH"
    return "TIDAK INFORMATIF"


def main():
    laporan = []
    hasil = {"peringatan": [], "gagal_keras": []}

    def tulis(s=""):
        laporan.append(s)
        print(s, flush=True)

    data = muat()
    if data is None:
        print("out/raw.npz tidak ada. Jalankan embed.py dulu.")
        sys.exit(1)
    ids, emb, slot = data
    n = len(ids)
    info = {}
    if os.path.exists(os.path.join(OUT, "info.json")):
        info = json.load(open(os.path.join(OUT, "info.json")))
    gagal = []
    if os.path.exists(os.path.join(OUT, "gagal.json")):
        gagal = json.load(open(os.path.join(OUT, "gagal.json")))
    total_coba = n + len(gagal)
    jalan_penuh = n >= MIN_JALAN_PENUH

    tulis("# Laporan verifikasi sidik jari visual")
    tulis()
    tulis(f"- Item berhasil: **{n}** | gagal (thumbnail/placeholder): **{len(gagal)}** | model: `{info.get('model', '?')}`")
    tulis(f"- Mode: **{'JALAN PENUH' if jalan_penuh else 'UJI KECIL (angka kemiripan belum bermakna)'}**")
    if info.get("stub"):
        tulis("- **PERINGATAN: ini hasil STUB (model palsu), bukan CLIP asli.**")
    tulis()

    # ---------- 1. Kesehatan ----------
    tulis("## 1. Kesehatan data")
    if not np.isfinite(emb).all():
        hasil["gagal_keras"].append("ada NaN/Inf pada embedding")
        tulis("- **GAGAL**: ada NaN/Inf pada embedding.")
    e_raw = norm_baris(emb)
    rata_sim = None
    if n >= 3:
        acak_idx = np.random.default_rng(0).choice(n, size=min(n, 400), replace=False)
        sub = e_raw[acak_idx]
        s = sub @ sub.T
        iu = np.triu_indices(len(sub), 1)
        rata_sim = float(s[iu].mean())
        _, sv, _ = np.linalg.svd(sub - sub.mean(axis=0), full_matrices=False)
        pr = float((sv ** 2).sum() ** 2 / ((sv ** 4).sum() + 1e-12))
        dup = float((s[iu] > 0.999).mean())
        tulis(f"- Rata-rata kemiripan antar item acak (mentah): {rata_sim:.3f} (CLIP wajar 0,4 sampai 0,8; di atas 0,95 = runtuh)")
        tulis(f"- Dimensi efektif (participation ratio): {pr:.1f} (di bawah 3 = hampir satu titik)")
        tulis(f"- Pasangan hampir identik (>0,999): {dup:.2%}")
        if rata_sim > 0.95 or pr < 3:
            hasil["gagal_keras"].append("embedding runtuh (hampir semua item sama)")
        if dup > 0.02:
            hasil["peringatan"].append(f"{dup:.1%} pasangan item hampir identik: kemungkinan banyak gambar placeholder")
    if jalan_penuh and total_coba > 0 and len(gagal) / total_coba > 0.30:
        hasil["gagal_keras"].append(f"{len(gagal) / total_coba:.0%} item gagal diambil thumbnail-nya")
        tulis(f"- **GAGAL**: {len(gagal) / total_coba:.0%} item gagal diambil thumbnail-nya.")
    elif total_coba > 0:
        tulis(f"- Tingkat gagal thumbnail: {len(gagal) / total_coba:.1%}")
    tulis()

    # ---------- 2. Informasi keserasian ----------
    tulis("## 2. Apakah sidik jari ini membawa informasi keserasian?")
    ringkas = {}
    if not os.path.exists(LABELS):
        tulis("- labels.json tidak ada: bagian ini dilewati.")
    elif not jalan_penuh:
        tulis("- Uji kecil: terlalu sedikit item untuk menghitung AUC. Jalankan dengan batas = 0 (semua item).")
    else:
        lab = json.load(open(LABELS, encoding="utf-8"))
        indeks = {int(i): k for k, i in enumerate(ids.tolist())}
        tema_dari = [None] * n
        for nama, daftar in lab["tema"].items():
            for i in daftar:
                if int(i) in indeks:
                    tema_dari[indeks[int(i)]] = nama
        kreator_dari = [None] * n
        for nama, daftar in lab["kreator"].items():
            for i in daftar:
                if int(i) in indeks:
                    kreator_dari[indeks[int(i)]] = nama
        n_tema = sum(1 for t in tema_dari if t)
        n_kr = sum(1 for t in kreator_dari if t)
        tulis(f"- Item berlabel tema: {n_tema} | berlabel kreator (grup >= 3 item): {n_kr}")
        rng = random.Random(42)
        e_gaya = pusatkan_per_slot(emb, slot.tolist())
        reps = {"mentah (CLIP apa adanya)": e_raw, "gaya (slot dinetralkan)": e_gaya}
        tulis()
        tulis("| Ukuran | Representasi | AUC | Penilaian |")
        tulis("|---|---|---|---|")
        for nama_rep, e in reps.items():
            for judul, lab_dari, lintas in (
                ("Tema, LINTAS slot (relevan untuk outfit)", tema_dari, True),
                ("Tema, dalam slot yang sama", tema_dari, False),
                ("Kreator/set, LINTAS slot", kreator_dari, True),
            ):
                ps = ambil_pasangan(lab_dari, slot, rng, lintas, N_PASANGAN, True)
                pn = ambil_pasangan(lab_dari, slot, rng, lintas, N_PASANGAN, False)
                a = auc(sim_pasangan(e, ps), sim_pasangan(e, pn))
                ringkas[(judul, nama_rep)] = a
                tulis(f"| {judul} | {nama_rep} | {('%.3f' % a) if a is not None else '-'} | {label_penilaian(a)} |")
        tulis()
        p_gaya = presisi_tetangga(e_gaya, slot, tema_dari, rng)
        p_mentah = presisi_tetangga(e_raw, slot, tema_dari, rng)
        for nama_p, p in (("gaya", p_gaya), ("mentah", p_mentah)):
            if p:
                lipat = p["presisi"] / max(p["dasar_acak"], 1e-9)
                tulis(f"- Tetangga terdekat lintas slot ({nama_p}): {p['presisi']:.1%} se-tema vs {p['dasar_acak']:.1%} bila acak (**{lipat:.1f}x** lebih baik dari acak)")
        hasil["presisi"] = {"gaya": p_gaya, "mentah": p_mentah}

        # keputusan memakai ukuran paling relevan: tema lintas slot, representasi terbaik
        kunci_tema = "Tema, LINTAS slot (relevan untuk outfit)"
        a_best = max([v for (j, r), v in ringkas.items() if j == kunci_tema and v is not None] or [None])
        a_kr = max([v for (j, r), v in ringkas.items() if j.startswith("Kreator") and v is not None] or [None])
        hasil["auc_tema_lintas_slot_terbaik"] = a_best
        hasil["auc_kreator_lintas_slot_terbaik"] = a_kr
        tulis()
        tulis("## 3. Keputusan")
        if a_best is None:
            tulis("- Data berlabel tidak cukup untuk memutuskan.")
        elif a_best >= 0.75:
            tulis(f"- **LAYAK DIPAKAI**: AUC tema lintas slot = {a_best:.2f} (kuat). Lanjut ke integrasi ke penilai di Roblox.")
        elif a_best >= 0.65:
            tulis(f"- **LAYAK DENGAN SYARAT**: AUC tema lintas slot = {a_best:.2f} (sedang). Pakai sebagai salah satu sinyal berbobot kecil, gabungkan dengan warna dan kreator, dan WAJIB dikalibrasi dengan penilaianmu.")
        else:
            tulis(f"- **BELUM LAYAK**: AUC tema lintas slot = {a_best:.2f}. Sidik jari ini belum cukup memisahkan tema. Jangan diintegrasikan; kita pakai jalur lain (warna asli, kreator, penilaianmu).")
        if a_kr is not None:
            tulis(f"- Kesamaan kreator/set (AUC lintas slot terbaik): {a_kr:.2f}")

    # ---------- 4. Tag zero-shot ----------
    tulis()
    tulis("## 4. Tag zero-shot (gaya) terhadap tema yang sudah diketahui")
    p_tag = os.path.join(OUT, "tags.json")
    if os.path.exists(p_tag) and os.path.exists(LABELS) and jalan_penuh:
        tags = json.load(open(p_tag, encoding="utf-8"))
        lab = json.load(open(LABELS, encoding="utf-8"))
        harap = {
            "Angel & Divine": ["angel"],
            "Horror": ["horror", "gothic", "demon"],
            "Anime": ["kawaii", "y2k"],
            "Ancient Egypt": ["royal", "fantasy"],
            "Assassin": ["military", "gothic"],
        }
        semua_id = [str(i) for i in ids.tolist()]
        punya_tag = sum(1 for i in semua_id if tags.get(i, {}).get("gaya"))
        tulis(f"- Item dengan minimal 1 tag gaya (>=12%): {punya_tag}/{len(semua_id)} ({punya_tag / max(1, len(semua_id)):.0%})")
        baris = []
        for tema, tag_harap in harap.items():
            ids_t = [str(i) for i in lab["tema"].get(tema, []) if str(i) in tags]
            if len(ids_t) < 20:
                continue

            def frek(daftar_id):
                c = 0
                for i in daftar_id:
                    nama_tag = {t for t, _ in tags.get(i, {}).get("gaya", [])}
                    if nama_tag & set(tag_harap):
                        c += 1
                return c / max(1, len(daftar_id))
            f_tema, f_semua = frek(ids_t), frek(semua_id)
            baris.append((tema, "/".join(tag_harap), f_tema, f_semua, f_tema / max(f_semua, 1e-9)))
        if baris:
            tulis()
            tulis("| Tema | Tag yang diharapkan | Di tema itu | Di semua item | Lipat |")
            tulis("|---|---|---|---|---|")
            for t, g, a, b, l in baris:
                tulis(f"| {t} | {g} | {a:.0%} | {b:.0%} | {l:.1f}x |")
            tulis("- Lipat di atas 1,5 berarti tag itu memang lebih sering muncul di tema yang sesuai (tanda tag masuk akal).")
    else:
        tulis("- Dilewati (uji kecil atau berkas tidak lengkap).")

    # ---------- penutup ----------
    tulis()
    if hasil["peringatan"]:
        tulis("## Peringatan")
        for p in hasil["peringatan"]:
            tulis(f"- {p}")
    if hasil["gagal_keras"]:
        tulis("## KEGAGALAN KERAS")
        for p in hasil["gagal_keras"]:
            tulis(f"- {p}")
    tulis()
    tulis("_Catatan jujur: label tema berasal dari hasil pencarian per-tema (bukan penilaian manusia), jadi AUC tinggi berarti_")
    tulis("_sidik jari menangkap kesamaan tema/gaya; belum membuktikan outfit hasil susunan itu enak dipandang. Itu tetap diuji dengan penilaianmu._")

    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "LAPORAN.md"), "w", encoding="utf-8").write("\n".join(laporan) + "\n")
    hasil_ser = {k: v for k, v in hasil.items()}
    hasil_ser["ringkas_auc"] = {f"{j} | {r}": v for (j, r), v in ringkas.items()}
    json.dump(hasil_ser, open(os.path.join(OUT, "verifikasi.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    ringkasan = os.environ.get("GITHUB_STEP_SUMMARY")
    if ringkasan:
        open(ringkasan, "a", encoding="utf-8").write("\n".join(laporan) + "\n")
    if hasil["gagal_keras"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
