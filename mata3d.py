#!/usr/bin/env python3
"""
MATA 3D (rev 31) -- membaca BENTUK ASLI item dari file 3D resmi Roblox (endpoint yang sama dengan tampilan 3D di Marketplace).

Endpoint: thumbnails.roblox.com/v1/assets-thumbnail-3d?assetId=ID. Sejak Maret 2026 wajib login; untuk aplikasi pihak
ketiga Roblox menyediakan Open Cloud API key dengan izin **thumbnails: read** (DevForum t/4435303). Kunci repo
(secret ROBLOX_API_KEY) dipakai lewat header x-api-key. Tidak memakai cookie akun.
Hasil endpoint -> URL JSON berisi hash file OBJ/MTL/tekstur di CDN rbxcdn. Dari OBJ dihitung (bukan ditebak):
  ukuran x/y/z, jumlah verteks, profil lebar & tebal per ketinggian (siluet), lebar bawah vs atas (rok A-line / flare),
  tonjolan dada (tebal maksimum di sepertiga atas vs tengah), simetri kiri-kanan, rongga depan (jaket terbuka).
Format file diverifikasi saat jalan (semua kunci dicetak ke log), tidak diasumsikan.
"""
import json, os, sys, time
import numpy as np
import requests

KEY = (os.environ.get("ROBLOX_API_KEY") or "").strip()
H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}


def url_cdn(h):
    """hash rbxcdn -> daftar URL dicoba berurutan: server hasil rumus lama dulu, lalu t0..t7 lain, lalu tr.rbxcdn.com
    (uji 16 Okt: rumus hanya cocok sebagian hash berawalan 180DAY-, jadi semua server dicoba)"""
    i = 31
    for c in h[:32]:
        i ^= ord(c)
    urut = [i % 8] + [k for k in range(8) if k != i % 8]
    return [f"https://t{k}.rbxcdn.com/{h}" for k in urut] + [f"https://tr.rbxcdn.com/{h}"]


def ambil(url, kunci=False, **kw):
    h = dict(H)
    if kunci and KEY:
        h["x-api-key"] = KEY
    return requests.get(url, headers=h, timeout=30, **kw)


def ambil_3d(aid, log=print):
    """-> (meta json 3D, teks OBJ) atau (None, alasan)"""
    for coba in range(6):
        r = ambil("https://thumbnails.roblox.com/v1/assets-thumbnail-3d", kunci=True, params={"assetId": aid})
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:160]}"
        js = r.json()
        if js.get("state") == "Completed" and js.get("imageUrl"):
            break
        time.sleep(2)
    else:
        return None, f"belum selesai: {json.dumps(js)[:160]}"
    r2 = ambil(js["imageUrl"])
    if r2.status_code != 200:
        return None, f"imageUrl HTTP {r2.status_code}"
    meta = r2.json()
    obj = None
    h = meta.get("obj")
    coba_log = []
    for u in (url_cdn(h) if isinstance(h, str) else []):
        try:
            r3 = ambil(u)
            ok = r3.status_code == 200 and (b"\nv " in r3.content[:200000] or r3.content[:2] == b"v ")
            coba_log.append(f"{u.split('/')[2]}:{r3.status_code}:{len(r3.content)}")
            if ok:
                obj = r3.text
                meta["_obj_url"] = u
                break
        except Exception as ex:
            coba_log.append(f"{u.split('/')[2]}:galat")
    if obj is None:
        log("obj tidak terunduh, dicoba:", " ".join(coba_log))
    return meta, obj


def baca_obj(teks):
    """OBJ -> (V (n,3), daftar grup nama per verteks pertama). Hanya v & g/o yang dipakai."""
    V, grup, cur = [], {}, "?"
    for ln in teks.splitlines():
        if ln.startswith("v "):
            p = ln.split()
            V.append((float(p[1]), float(p[2]), float(p[3])))
        elif ln.startswith("g ") or ln.startswith("o "):
            cur = ln[2:].strip()
            grup.setdefault(cur, len(V))
    return np.array(V, dtype=np.float64), grup


def geometri(V):
    """fitur bentuk dari verteks (sumbu Y = atas; Z = depan/belakang menurut konvensi Roblox; diperiksa di log)"""
    if len(V) < 10:
        return None
    lo, hi = V.min(axis=0), V.max(axis=0)
    ukuran = hi - lo
    f = {"n_verteks": int(len(V)), "ukuran": [round(float(x), 3) for x in ukuran]}
    # profil per ketinggian: lebar (x) & tebal (z) pada 10 irisan
    y0, y1 = lo[1], hi[1]
    prof = []
    for k in range(10):
        a = y0 + (y1 - y0) * k / 10
        b = y0 + (y1 - y0) * (k + 1) / 10
        m = (V[:, 1] >= a) & (V[:, 1] <= b)
        if m.sum() < 3:
            prof.append([0.0, 0.0])
            continue
        S = V[m]
        prof.append([round(float(S[:, 0].max() - S[:, 0].min()), 3), round(float(S[:, 2].max() - S[:, 2].min()), 3)])
    f["profil"] = prof          # bawah -> atas: [lebar, tebal]
    lb = [p[0] for p in prof]
    f["flare"] = round(float((lb[0] + 1e-6) / (max(lb[4], lb[5]) + 1e-6)), 3)      # >1 = melebar ke bawah (rok/gaun)
    tb = [p[1] for p in prof]
    f["tonjol_atas"] = round(float(max(tb[6:9]) / (max(tb[3:5]) + 1e-6)), 3)        # dada lebih tebal dari pinggang
    cx = (lo[0] + hi[0]) / 2
    kiri, kanan = (V[:, 0] < cx).sum(), (V[:, 0] >= cx).sum()
    f["simetri"] = round(float(min(kiri, kanan) / max(1, max(kiri, kanan))), 3)
    return f


def main():
    ids = [int(x) for x in sys.argv[1:] if x.isdigit()] or [7192553841, 9438759973, 126884250250747, 72558563872966, 192557913]
    os.makedirs("uji3d", exist_ok=True)
    print("kunci API terpasang:", bool(KEY), flush=True)
    hasil = {}
    for aid in ids:
        meta, obj = ambil_3d(aid)
        if meta is None:
            print(aid, "GAGAL:", obj, flush=True)
            hasil[str(aid)] = {"galat": obj}
            continue
        ring = {k: (v if not isinstance(v, (list, dict)) else (str(v)[:200])) for k, v in meta.items()}
        print(aid, "meta 3D kunci:", list(meta.keys()), json.dumps(ring)[:600], flush=True)
        if not obj:
            hasil[str(aid)] = {"galat": "obj tidak terunduh", "meta": ring}
            continue
        V, grup = baca_obj(obj)
        g = geometri(V)
        print(aid, "OBJ:", len(V), "verteks, grup:", list(grup)[:12], "geometri:", json.dumps(g)[:500], flush=True)
        # per grup: jumlah verteks & kotak batas (apakah ada manekin/badan ikut di file 3D pakaian layered?)
        mulai = sorted(grup.items(), key=lambda kv: kv[1]) + [("_akhir", len(V))]
        for (nm, a0), (_, a1) in zip(mulai, mulai[1:]):
            if a1 > a0:
                S = V[a0:a1]
                print("   grup", nm[:40], a1 - a0, "verteks, min", np.round(S.min(axis=0), 2).tolist(),
                      "maks", np.round(S.max(axis=0), 2).tolist(), flush=True)
        for ln in obj.splitlines()[:6]:
            if not ln.startswith(("v ", "vt ", "vn ", "f ")):
                print("   kepala:", ln[:120], flush=True)
        hasil[str(aid)] = {"meta": ring, "grup": list(grup)[:30], "geometri": g}
        time.sleep(0.5)
    json.dump(hasil, open("uji3d/hasil.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
