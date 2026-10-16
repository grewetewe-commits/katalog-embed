#!/usr/bin/env python3
"""uji bentuk2d.py pada sampel beku uji2d (175 item, label emas) -> uji2d/bentuk.json + lembar overlay bentuk"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bentuk2d as B
from PIL import Image, ImageDraw, ImageFont

sampel = [(int(i), int(t)) for i, t in json.load(open("uji2d/sampel.json"))["sampel"]]
emas = json.load(open("uji2d/emas.json"))
gb = B.thumb([i for i, _ in sampel])
per = collections.defaultdict(list)
for i, t in sampel:
    per[t].append(i)
hasil = {}
for i, t in sampel:
    if i in gb and t in (11, 12):
        f = B.ukur(gb[i])
        hasil[str(i)] = {"t": t, "f": f, "baca": B.baca(f, t)}
json.dump(hasil, open("uji2d/bentuk.json", "w"), ensure_ascii=False)
# penilaian terhadap label emas (jenis & fungsi)
TANPA_LENGAN = {"tanktop", "korset", "crop"}
PENDEK = {"celana_pendek", "rok_pendek"}
PANJANG = {"jeans", "kargo", "jogger", "celana_kain", "legging", "rok_panjang"}
rep = []
for t in (11, 12):
    g = emas[str(t)]
    c = collections.Counter()
    for k, i in enumerate(per[t]):
        h = hasil.get(str(i))
        if not h:
            continue
        b = h["baca"]
        j, fu = g["jenis"][k], g["fungsi"][k]
        if fu:
            c["fungsi_n"] += 1
            c["fungsi_ok"] += int((b.get("fungsi") == "badan") == (fu == "badan"))
        if t == 11 and j:
            if j in ("crop",):
                c["crop_n"] += 1
                c["crop_ok"] += int(bool(b.get("crop")))
            if j in TANPA_LENGAN:
                c["tanpa_n"] += 1
                c["tanpa_ok"] += int(b.get("lengan") == "tanpa" or bool(b.get("crop")) or b.get("bahu") == "terbuka")
            if j in ("lengan_panjang", "hoodie", "sweater", "jaket", "jas"):
                c["panjang_n"] += 1
                c["panjang_ok"] += int(b.get("lengan") == "panjang")
            if j in ("kaos",):
                c["kaos_n"] += 1
                c["kaos_ok"] += int(b.get("lengan") == "pendek")
        if t == 12 and j:
            if j in PENDEK:
                c["pendek_n"] += 1
                c["pendek_ok"] += int(b.get("panjang") == "pendek")
            if j in PANJANG:
                c["pjg_n"] += 1
                c["pjg_ok"] += int(b.get("panjang") == "panjang")
            if j in ("kostum_bawah", "overall"):
                c["badan_n"] += 1
                c["badan_ok"] += int(b.get("badan") == "tertutup")
    rep.append((t, dict(c)))
    print(t, dict(c), flush=True)
json.dump(rep, open("uji2d/bentuk_nilai.json", "w"))
try:
    font = ImageFont.load_default(size=13)
except TypeError:
    font = ImageFont.load_default()
for t, nm in ((11, "baju"), (12, "celana")):
    ids = per[t]
    kol, sel = 6, 230
    bar = (len(ids) + kol - 1) // kol
    kan = Image.new("RGB", (kol * sel, bar * (sel + 34)), (245, 245, 245))
    dr = ImageDraw.Draw(kan)
    for k, i in enumerate(ids):
        if i not in gb:
            continue
        im = gb[i]
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        x, y = (k % kol) * sel, (k // kol) * (sel + 34)
        kan.paste(bg.convert("RGB").resize((sel - 10, sel - 10)), (x + 5, y))
        b = hasil.get(str(i), {}).get("baca", {})
        dr.text((x + 4, y + sel - 8), f"#{k + 1} " + " ".join(f"{a}={v}" for a, v in b.items())[:44], fill=(160, 20, 20), font=font)
        dr.text((x + 4, y + sel + 8), (emas[str(t)]["jenis"][k] or "-"), fill=(20, 20, 160), font=font)
    kan.save(f"uji2d/bentuk_{nm}.png", optimize=True)
print("selesai")
