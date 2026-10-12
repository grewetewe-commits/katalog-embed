"""Import verified public outfit compositions into the existing local training pipeline."""
import copy
import json
import math
from pathlib import Path

PARTS = ("Head", "Torso", "LeftArm", "RightArm", "LeftLeg", "RightLeg")

def valid_id(value):
    return type(value) is int and 0 < value < 2**53

def import_ready(st, filename="bank/ready_outfits.json"):
    p = Path(filename)
    if not p.exists():
        return 0
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("seeds"), list) or len(data["seeds"]) > 4000:
        raise ValueError("Invalid public outfit bank")
    added = 0
    for seed in data["seeds"]:
        if not isinstance(seed, dict) or seed.get("S") not in ("marketplace_look", "public_saved_outfit"):
            continue
        h = seed.get("H")
        if not isinstance(h, str) or len(h) != 16 or any(c not in "0123456789abcdef" for c in h):
            continue
        a, bp, sc = seed.get("A"), seed.get("BP"), seed.get("SC")
        if not isinstance(a, list) or len(a) > 20 or not all(isinstance(x, list) and len(x) == 2 and valid_id(x[0]) and type(x[1]) is int and 1 <= x[1] <= 19 for x in a):
            continue
        if not isinstance(bp, dict) or not all(type(bp.get(k)) is int and (bp[k] == 0 or valid_id(bp[k])) for k in PARTS):
            continue
        if not isinstance(sc, list) or len(sc) != 6 or not all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 2 and (i >= 4 or v > 0) for i, v in enumerate(sc)):
            continue
        if seed.get("R") not in ("R6", "R15") or any(k in seed and not valid_id(seed[k]) for k in ("Sh", "Pa", "Gt", "F")):
            continue
        origin = seed.get("Origin") or {}
        value = copy.deepcopy(seed)
        value["K"] = "ready:" + str(origin.get("creatorHash") or origin.get("outfitId") or h)
        if h not in st["outfit"]:
            added += 1
        st["outfit"][h] = value
    # Names and sale snapshots are observations. The existing metadata worker refreshes stale prices.
    for key, meta in data.get("meta", {}).items():
        if not key.isdecimal() or not valid_id(int(key)) or not isinstance(meta, dict):
            continue
        if not isinstance(meta.get("n"), str) or type(meta.get("t")) is not int or type(meta.get("w")) is not int:
            continue
        old = st["meta"].get(key)
        if not old or old.get("w", 0) < meta["w"]:
            st["meta"][key] = copy.deepcopy(meta)
    return added
