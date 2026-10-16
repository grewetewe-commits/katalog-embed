#!/usr/bin/env python3
"""
BENTUK 2D DARI PIKSEL (rev 31) -- mengukur, bukan menebak, potongan baju/celana klasik 2D dari thumbnail resmi 420 px.

Thumbnail baju/celana klasik Roblox SELALU memakai manekin kotak (R6) dengan pose & kamera yang sama (diperiksa di
uji2d/mentah: 12 gambar, posisi kepala/badan/lengan/kaki identik). Bagian yang TIDAK tertutup pakaian menampakkan warna
manekin abu (#abaca7: r~g, b sedikit lebih rendah; sama dengan otak.py w2_manekin). Maka per wilayah badan kita ukur
berapa persen tertutup pakaian:
  leher   : kedalaman bukaan leher dari bawah dagu (V/scoop rendah sering cewek; kerah tinggi/crew menyentuh leher)
  bahu    : bahu terbuka (off-shoulder / tank)
  lengan  : panjang lengan (tanpa / pendek / panjang) dari pita atas->bawah
  crop    : perut terbuka
  kaki    : panjang celana/rok (pendek / selutut / panjang)
  badan   : celana yang menutup badan (overall / kostum penuh)
  cakupan : total tertutup -> lapisan kulit / aksesori dilukis (bukan pakaian)
Koordinat wilayah dalam piksel gambar 420x420 (dicek dengan overlay di lembar uji).
"""
import io, json, os, sys, time
import numpy as np
import requests
from PIL import Image

H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
VERSI_BENTUK = 1
W = {  # (x0, y0, x1, y1) inklusif-eksklusif, gambar 420
    "leher": (182, 136, 226, 200),
    "leher_lebar": (160, 136, 248, 146),
    "bahuL": (152, 128, 180, 146),
    "bahuR": (228, 128, 256, 146),
    "badan": (152, 128, 256, 238),
    "crop": (160, 206, 250, 236),
    "lenganL": (104, 124, 150, 230),
    "lenganR": (258, 130, 336, 268),
    "kaki": (160, 240, 262, 336),
}
TINGGI_BADAN = 238 - 128


def manekin(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    gs = np.maximum(g, 1e-6)
    rg, bg = r / gs, b / gs
    return (g >= 60) & (g <= 240) & (rg >= 0.98) & (rg <= 1.015) & (bg >= 0.95) & (bg <= 0.99)


def _box(m, k):
    x0, y0, x1, y1 = W[k]
    return m[y0:y1, x0:x1]


def ukur(im):
    """PIL RGBA 420 -> dict fitur 0..100 (persen) ; None bila ukuran tak sesuai"""
    if im.size != (420, 420):
        im = im.resize((420, 420), Image.BILINEAR)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] > 128
    man = manekin(rgb) & al
    kain = al & ~man

    def cak(k):
        o = _box(al, k)
        n = o.sum()
        return float(_box(kain, k).sum() / n) if n > 0 else 0.0

    def pita(k, nb):
        """cakupan per pita horizontal atas->bawah"""
        x0, y0, x1, y1 = W[k]
        out = []
        for j in range(nb):
            ya = y0 + (y1 - y0) * j // nb
            yb = y0 + (y1 - y0) * (j + 1) // nb
            o = al[ya:yb, x0:x1]
            n = o.sum()
            out.append(float(kain[ya:yb, x0:x1].sum() / n) if n > 0 else 0.0)
        return out

    def hist(k, j, nb):
        """histogram warna kasar (4x4x4) piksel pakaian pada pita j dari nb pita"""
        x0, y0, x1, y1 = W[k]
        ya = y0 + (y1 - y0) * j // nb
        yb = y0 + (y1 - y0) * (j + 1) // nb
        m = kain[ya:yb, x0:x1]
        px = rgb[ya:yb, x0:x1][m]
        if len(px) < 20:
            return None
        q = (np.clip(px, 0, 255) // 64).astype(np.int64)
        h = np.bincount(q[:, 0] * 16 + q[:, 1] * 4 + q[:, 2], minlength=64).astype(np.float64)
        return h / h.sum()

    def lanjut_warna(k, nb, cs, amb=0.5):
        """sampai pita ke berapa pakaian BERWARNA SAMA dengan pita teratas yang tertutup (kaus kaki/stoking/kulit dilukis
        di bawah celana pendek/rok tidak dihitung sebagai celana panjang)"""
        mulai = next((j for j, c in enumerate(cs) if c >= amb), None)
        if mulai is None:
            return 0.0
        h0 = hist(k, mulai, nb)
        akhir = mulai
        for j in range(mulai + 1, nb):
            if cs[j] < amb:
                break
            hj = hist(k, j, nb)
            if h0 is None or hj is None or np.minimum(h0, hj).sum() < 0.35:
                break
            akhir = j
        return (akhir + 1) / nb

    def bawah(cs, amb=0.5):
        """pita terbawah yang masih tertutup (celana/rok: sampai mana ke bawah)"""
        j = -1
        for k, c in enumerate(cs):
            if c >= amb:
                j = k
        return (j + 1) / len(cs)

    def panjang(cs, amb=0.5):
        n = 0
        for c in cs:
            if c >= amb:
                n += 1
            else:
                break
        return n / len(cs)

    # leher: baris demi baris dari bawah dagu, berapa dalam manekin masih terlihat di tengah dada
    x0, y0, x1, y1 = W["leher"]
    dalam = 0
    for y in range(y0, y1):
        o = al[y, x0:x1]
        n = o.sum()
        if n == 0:
            break
        fm = man[y, x0:x1].sum() / n
        if fm >= 0.35:
            dalam += 1
        else:
            break
    lL, lR = pita("lenganL", 5), pita("lenganR", 5)
    kk = pita("kaki", 5)
    f = {
        "v": VERSI_BENTUK,
        "leher": int(round(100 * dalam / TINGGI_BADAN)),
        "leherLebar": int(round(100 * (1 - cak("leher_lebar")))),
        "bahu": int(round(100 * (1 - (cak("bahuL") + cak("bahuR")) / 2))),
        "badan": int(round(100 * cak("badan"))),
        "crop": int(round(100 * (1 - cak("crop")))),
        "lengan": int(round(100 * max(panjang(lL, 0.3), panjang(lR, 0.3)))),
        "lenganCak": int(round(100 * (sum(lL) + sum(lR)) / 10)),
        "kaki": int(round(100 * bawah(kk))),
        "kakiWarna": int(round(100 * lanjut_warna("kaki", 5, kk))),
        "lenganWarna": int(round(100 * (lanjut_warna("lenganL", 5, lL) + lanjut_warna("lenganR", 5, lR)) / 2)),
        "kakiCak": int(round(100 * sum(kk) / 5)),
    }
    f["pita"] = [int(round(100 * c)) for c in lL + lR + kk]   # cakupan per pita: lengan kiri(5), kanan(5), kaki(5)
    tot = al[128:338, 104:336].sum()
    f["cakupan"] = int(round(100 * kain[128:338, 104:336].sum() / max(1, tot)))
    return f


def baca(f, t):
    """fitur -> label yang bisa dibaca map/manusia. t = tipe aset (11 baju, 12 celana)."""
    out = {}
    if t == 11:
        if f["cakupan"] < 12 or (f["badan"] < 15 and f["lenganCak"] < 15):
            out["fungsi"] = "badan"            # hampir tak menutup: shading/riasan/tekstur kulit
        pl = f["lengan"]  # lengan: cakupan saja (lenganWarna = info; corak manset sering memutus warna)
        out["lengan"] = "tanpa" if f["lenganCak"] < 20 else ("pendek" if pl < 80 else "panjang")
        out["leher"] = "tinggi" if f["leher"] <= 6 else ("sedang" if f["leher"] <= 22 else "rendah")
        if f["bahu"] >= 60 and f["badan"] >= 30:
            out["bahu"] = "terbuka"
        if f["crop"] >= 55 and f["badan"] >= 25:
            out["crop"] = True
    elif t == 12:
        if f["kakiCak"] < 10 and f["badan"] < 15:
            out["fungsi"] = "badan"
        pk = min(f["kaki"], f.get("kakiWarna", f["kaki"]))
        out["panjang"] = "pendek" if pk <= 40 else ("selutut" if pk <= 60 else "panjang")
        if pk <= 60 and f["kaki"] >= 80:
            out["kakiBawah"] = "kaus kaki/stoking/kulit dilukis"
        if f["badan"] >= 60:
            out["badan"] = "tertutup"           # overall / kostum / setelan badan
    return out


def thumb(ids, ukuran="420x420", jeda=0.4):
    out = {}
    for a in range(0, len(ids), 50):
        p = ids[a:a + 50]
        for coba in range(3):
            try:
                r = requests.get("https://thumbnails.roblox.com/v1/assets", headers=H, timeout=30,
                                 params={"assetIds": ",".join(map(str, p)), "returnPolicy": "PlaceHolder", "size": ukuran,
                                         "format": "Png", "isCircular": "false"})
                for e in r.json().get("data", []):
                    if e.get("state") == "Completed" and e.get("imageUrl"):
                        try:
                            b = requests.get(e["imageUrl"], headers=H, timeout=30).content
                            out[int(e["targetId"])] = Image.open(io.BytesIO(b)).convert("RGBA")
                        except Exception:
                            pass
                break
            except Exception as ex:
                print("thumbnail gagal:", ex, flush=True)
                time.sleep(3)
        time.sleep(jeda)
    return out
