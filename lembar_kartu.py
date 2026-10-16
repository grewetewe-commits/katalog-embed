#!/usr/bin/env python3
"""
LEMBAR KARTU -- lembar kontak untuk MEMERIKSA kartu item dengan mata (pemilik, Codex, Claude).
Tiap sel: thumbnail item (thumbnails.roblox.com/v1/assets, publik, sama dengan otak.py) + nama + kartu (jenis/tema/subjek/pola).
Sampel acak tetap (seed) per kelompok + item uji. Keluaran: kartu/lembar/*.png + kartu/lembar/daftar.json (id per sel, untuk
label emas manual). Tidak dipakai server; hanya alat periksa.
"""
import os, sys, io, json, random, time
import requests
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kartu_item as KI

H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
SEL, KOL = 170, 6
TINGGI_TEKS = 64


def thumb(ids):
    out = {}
    for a in range(0, len(ids), 50):
        p = ids[a:a + 50]
        try:
            r = requests.get("https://thumbnails.roblox.com/v1/assets", headers=H, timeout=30,
                             params={"assetIds": ",".join(map(str, p)), "returnPolicy": "PlaceHolder", "size": "150x150",
                                     "format": "Png", "isCircular": "false"})
            for e in r.json().get("data", []):
                if e.get("state") == "Completed" and e.get("imageUrl"):
                    b = requests.get(e["imageUrl"], headers=H, timeout=30).content
                    im = Image.open(io.BytesIO(b)).convert("RGBA")
                    alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
                    alas.alpha_composite(im)
                    out[int(e["targetId"])] = alas.convert("RGB")
        except Exception as ex:
            print("thumbnail gagal:", ex, flush=True)
        time.sleep(0.5)
    return out


def ringkas(kel, b):
    L = KI
    def nm(lst, j):
        return lst[j][0] if 0 <= j < len(lst) else "-"
    baris = []
    if kel in L.JENIS and b[1] >= 0:
        baris.append(f"J:{nm(L.JENIS[kel], b[1])} {b[2]}")
    baris.append(f"T:{nm(L.TEMA, b[3])} {b[4]}/{nm(L.TEMA, b[5])} {b[6]}")
    if b[7] >= 0:
        baris.append(f"S:{nm(L.SUBJEK, b[7])} {b[8]}/{nm(L.SUBJEK, b[9])} {b[10]}")
    if b[11] >= 0:
        baris.append(f"P:{nm(L.POLA, b[11])} {b[12]}")
    return baris


def lembar(judul, item, gambar, meta, kartu, jalur, font):
    n = len(item)
    baris_n = (n + KOL - 1) // KOL
    W, Hh = KOL * SEL, 28 + baris_n * (SEL + TINGGI_TEKS)
    kanvas = Image.new("RGB", (W, Hh), (245, 245, 245))
    d = ImageDraw.Draw(kanvas)
    d.text((6, 6), judul, fill=(0, 0, 0), font=font)
    for k, i in enumerate(item):
        x, y = (k % KOL) * SEL, 28 + (k // KOL) * (SEL + TINGGI_TEKS)
        im = gambar.get(i)
        if im:
            kanvas.paste(im.resize((SEL - 20, SEL - 20)), (x + 10, y))
        m = meta.get(str(i)) or {}
        kel = KI.ASET_KE_KEL.get(int(m.get("t") or 0), "?")
        teks = [f"#{k + 1} {(m.get('n') or '?')[:26]}"] + (ringkas(kel, kartu[i]) if i in kartu else ["(tanpa kartu)"])
        for q, t in enumerate(teks[:5]):
            d.text((x + 4, y + SEL - 18 + q * 13), t, fill=(0, 0, 0) if q else (20, 20, 160), font=font)
    kanvas.save(jalur, optimize=True)


def main():
    uji = [int(x) for x in sys.argv[1:] if x.isdigit()]
    kartu = {}
    for s in range(KI.SHARD):
        for k, v in json.load(open(f"kartu/kartu_{s}.json", encoding="utf-8"))["d"].items():
            kartu[int(k)] = v
    import gzip
    with gzip.open(KI.P_STATE, "rt", encoding="utf-8") as f:
        meta = json.load(f).get("meta", {})
    try:
        font = ImageFont.load_default(size=11)
    except TypeError:
        font = ImageFont.load_default()
    os.makedirs("kartu/lembar", exist_ok=True)
    rng = random.Random(20261016)
    per = {}
    for i, b in kartu.items():
        per.setdefault(KI.KELOMPOK[b[0]], []).append(i)
    daftar = {"uji": uji}
    for kel in KI.KELOMPOK:
        ids = sorted(per.get(kel, []))
        daftar[kel] = rng.sample(ids, min(36, len(ids)))
    semua = [i for v in daftar.values() for i in v]
    gambar = thumb(semua)
    for nama, item in daftar.items():
        if item:
            lembar(f"Kartu item - {nama} ({len(item)} item, sampel acak seed 20261016)", item, gambar, meta, kartu,
                   f"kartu/lembar/{nama}.png", font)
    json.dump(daftar, open("kartu/lembar/daftar.json", "w"), indent=0)
    print("lembar selesai:", {k: len(v) for k, v in daftar.items()}, flush=True)


if __name__ == "__main__":
    main()
