#!/usr/bin/env python3
"""
CEK LEMBAR 3D -- alat periksa mata (bukan dipakai server): thumbnail katalog resmi (thumbnails.roblox.com/v1/assets, publik)
untuk daftar id di uji3d/cek_ids.json [{"id", "ukur", "nama"}], dengan angka ukur 3D (kerangka badan) di bawahnya.
Keluaran: uji3d/cek_lembar.png. Dipakai untuk memastikan bacaan kerangka badan (letak pakaian di manekin) sesuai gambar.
"""
import io, json, time
import requests
from PIL import Image, ImageDraw, ImageFont

H = {"User-Agent": "KatalogPraktis-cek3d/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
SEL, KOL, TEKS = 260, 4, 54


def thumb(ids, bundle=False):
    out = {}
    for a in range(0, len(ids), 50):
        p = ids[a:a + 50]
        for _ in range(3):
            try:
                if bundle:
                    r = requests.get("https://thumbnails.roblox.com/v1/bundles/thumbnails", headers=H, timeout=30,
                                     params={"bundleIds": ",".join(map(str, p)), "size": "420x420", "format": "Png",
                                             "isCircular": "false"})
                else:
                    r = requests.get("https://thumbnails.roblox.com/v1/assets", headers=H, timeout=30,
                                     params={"assetIds": ",".join(map(str, p)), "returnPolicy": "PlaceHolder",
                                             "size": "420x420", "format": "Png", "isCircular": "false"})
                pending = False
                for e in r.json().get("data", []):
                    if e.get("state") == "Completed" and e.get("imageUrl"):
                        b = requests.get(e["imageUrl"], headers=H, timeout=30).content
                        im = Image.open(io.BytesIO(b)).convert("RGBA")
                        alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
                        alas.alpha_composite(im)
                        out[int(e["targetId"])] = alas.convert("RGB")
                    elif e.get("state") == "Pending":
                        pending = True
                if not pending:
                    break
            except Exception as ex:
                print("thumbnail gagal:", ex, flush=True)
            time.sleep(2)
    return out


def main():
    daftar = json.load(open("uji3d/cek_ids.json", encoding="utf-8"))
    # {"bundle": true} pada entri = thumbnail bundle (badan avatar), selain itu aset
    gb = thumb([d["id"] for d in daftar if not d.get("bundle")])
    gb.update(thumb([d["id"] for d in daftar if d.get("bundle")], bundle=True))
    baris = (len(daftar) + KOL - 1) // KOL
    kanvas = Image.new("RGB", (KOL * SEL, baris * (SEL + TEKS)), (255, 255, 255))
    dr = ImageDraw.Draw(kanvas)
    try:
        f = ImageFont.truetype("DejaVuSans.ttf", 12)
    except Exception:
        f = ImageFont.load_default()
    for k, d in enumerate(daftar):
        x, y = (k % KOL) * SEL, (k // KOL) * (SEL + TEKS)
        im = gb.get(d["id"])
        if im:
            kanvas.paste(im.resize((SEL, SEL)), (x, y))
        dr.text((x + 3, y + SEL + 2), f"{k + 1}. {d['id']}", fill=(0, 0, 0), font=f)
        dr.text((x + 3, y + SEL + 18), d.get("ukur", "")[:44], fill=(160, 0, 0), font=f)
        dr.text((x + 3, y + SEL + 34), "".join(c for c in d.get("nama", "") if ord(c) < 0x2000)[:40], fill=(0, 0, 160), font=f)
    kanvas.save("uji3d/cek_lembar.png", optimize=True)
    print("lembar:", len(daftar), "item,", len(gb), "thumbnail")


if __name__ == "__main__":
    main()
