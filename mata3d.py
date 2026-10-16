#!/usr/bin/env python3
"""
MATA 3D (rev 32) -- membaca BENTUK ASLI item dari file 3D resmi Roblox (endpoint yang sama dengan tampilan 3D di Marketplace).

Endpoint: thumbnails.roblox.com/v1/assets-thumbnail-3d?assetId=ID, header x-api-key (Open Cloud API key dengan izin
**thumbnail:read**, secret ROBLOX_API_KEY; tanpa cookie akun). Hasilnya JSON berisi hash OBJ/MTL/tekstur di CDN rbxcdn.
Diverifikasi 16 Okt: OBJ satu grup "Handle1" (pakaian saja, tanpa manekin), sumbu Y = atas, DEPAN = -Z (kamera thumbnail
selalu di sisi -Z). Pakaian layered dibuat di sekitar manekin acuan yang sama -> ukuran stud bisa dibandingkan antar item.

Yang dihitung (DIUKUR dari permukaan mesh, bukan ditebak): sampel titik merata di permukaan (bobot luas segitiga), lalu
  W/H/D        : lebar, tinggi, tebal (stud)
  prof         : 12 irisan bawah->atas: [lebar, tebal, tonjol depan, tonjol belakang, celah tengah 0..6]
                 (celah tengah di irisan bawah = dua kaki terpisah -> celana; menyatu -> rok/gaun)
  luar         : titik di luar badan (|x| > 0,9 / 1,1 / 1,3 stud): [porsi %, y terendah %, y tertinggi %] -> lengan
  leher        : tinggi titik tertinggi tengah-depan & tengah-belakang & bahu (cm dari puncak) -> bukaan leher, tudung
  depanTerbuka : porsi irisan tengah tanpa kain di tengah-depan -> jaket terbuka
  nv/nf/ntex   : jumlah verteks/segitiga/tekstur (4 tekstur = PBR)
Mesh mentah TIDAK disimpan (hak kreator); hanya angka turunan.
"""
import gzip, json, os, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import requests

KEY = (os.environ.get("ROBLOX_API_KEY") or "").strip()
H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
VERSI_3D = 1
P_HASIL = "fisik3d/bentuk3d.json.gz"
_lok = threading.Lock()
STAT = {"ok": 0, "pending": 0, "galat": 0, "429": 0, "tanpa_obj": 0}


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


def ambil_3d(aid, log=print, coba_pending=6):
    """-> (meta json 3D, teks OBJ) | (None, alasan). alasan diawali 'pending' bila Roblox belum selesai merender."""
    js = None
    for coba in range(coba_pending):
        for ulang in range(4):
            r = ambil("https://thumbnails.roblox.com/v1/assets-thumbnail-3d", kunci=True, params={"assetId": aid})
            if r.status_code != 429:
                break
            with _lok:
                STAT["429"] += 1
            time.sleep(8 * (ulang + 1))
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:160]}"
        js = r.json()
        if js.get("state") == "Completed" and js.get("imageUrl"):
            break
        time.sleep(2)
    else:
        return None, f"pending: {json.dumps(js)[:120]}"
    r2 = ambil(js["imageUrl"])
    if r2.status_code != 200:
        return None, f"imageUrl HTTP {r2.status_code}"
    meta = r2.json()
    obj = None
    coba_log = []
    h = meta.get("obj")
    for u in (url_cdn(h) if isinstance(h, str) else []):
        try:
            r3 = ambil(u)
            ok = r3.status_code == 200 and (b"\nv " in r3.content[:200000] or r3.content[:2] == b"v ")
            coba_log.append(f"{u.split('/')[2]}:{r3.status_code}:{len(r3.content)}")
            if ok:
                obj = r3.text
                meta["_obj_url"] = u
                break
        except Exception:
            coba_log.append(f"{u.split('/')[2]}:galat")
    if obj is None:
        log("obj tidak terunduh, dicoba:", " ".join(coba_log))
    return meta, obj


def baca_obj(teks):
    """OBJ -> (V (n,3), F (m,3) indeks segitiga 0-based, grup {nama: verteks pertama}). Poligon dipecah kipas."""
    V, F, grup, cur = [], [], {}, "?"
    for ln in teks.splitlines():
        if ln.startswith("v "):
            p = ln.split()
            V.append((float(p[1]), float(p[2]), float(p[3])))
        elif ln.startswith("f "):
            idx = []
            for tok in ln.split()[1:]:
                a = int(tok.split("/")[0])
                idx.append(a - 1 if a > 0 else len(V) + a)
            for k in range(1, len(idx) - 1):
                F.append((idx[0], idx[k], idx[k + 1]))
        elif ln.startswith("g ") or ln.startswith("o "):
            cur = ln[2:].strip()
            grup.setdefault(cur, len(V))
    return np.array(V, dtype=np.float64), np.array(F, dtype=np.int64).reshape(-1, 3), grup


def sampel_permukaan(V, F, n=6000, seed=7):
    """titik merata di permukaan (bobot luas segitiga); tanpa segitiga -> verteks apa adanya"""
    if len(F) == 0:
        return V
    F = F[(F >= 0).all(axis=1) & (F < len(V)).all(axis=1)]
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    luas = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    if luas.sum() <= 0:
        return V
    rng = np.random.default_rng(seed)
    pilih = rng.choice(len(F), size=n, p=luas / luas.sum())
    u, v = rng.random(n), rng.random(n)
    balik = u + v > 1
    u[balik], v[balik] = 1 - u[balik], 1 - v[balik]
    return a[pilih] + u[:, None] * (b[pilih] - a[pilih]) + v[:, None] * (c[pilih] - a[pilih])


def cm(x):
    return int(round(float(x) * 100))


def ukur3d(V, F):
    """deskriptor bentuk (lihat docstring modul). Satuan cm (stud x100) atau persen."""
    if len(V) < 10:
        return None
    lo, hi = V.min(axis=0), V.max(axis=0)
    W, Hh, D = (hi - lo).tolist()
    P = sampel_permukaan(V, F)
    X = P[:, 0] - (lo[0] + hi[0]) / 2
    Y = (P[:, 1] - lo[1]) / max(Hh, 1e-6)          # 0 bawah .. 1 atas
    Z = P[:, 2] - (lo[2] + hi[2]) / 2               # depan = negatif
    nb = 12
    prof = []
    for k in range(nb):
        m = (Y >= k / nb) & ((Y < (k + 1) / nb) if k < nb - 1 else (Y <= 1.0))
        if m.sum() < 8:
            prof.append([0, 0, 0, 0, 0])
            continue
        x, z = X[m], Z[m]
        h, _ = np.histogram(x, bins=24, range=(-W / 2, W / 2))
        prof.append([cm(x.max() - x.min()), cm(z.max() - z.min()), cm(-z.min()), cm(z.max()), int((h[9:15] == 0).sum())])
    luar = []
    ax = np.abs(X)
    for q in (0.9, 1.1, 1.3):
        m = ax > q
        luar.append([int(round(100 * m.mean())), int(round(100 * Y[m].min())) if m.any() else -1,
                     int(round(100 * Y[m].max())) if m.any() else -1])

    def puncak(m):
        return cm((1 - Y[m].max()) * Hh) if m.any() else -1     # cm di bawah puncak pakaian

    leher = [puncak((ax < 0.15) & (Z < 0)), puncak((ax < 0.15) & (Z > 0)), puncak((ax > 0.4) & (ax < 0.8))]
    tengah = [k for k in range(3, 10)]
    kosong = 0
    for k in tengah:
        m = (Y >= k / nb) & (Y < (k + 1) / nb)
        if m.sum() >= 8 and not ((ax[m] < 0.12) & (Z[m] < 0)).any():
            kosong += 1
    return {"v": VERSI_3D, "W": cm(W), "H": cm(Hh), "D": cm(D), "prof": prof, "luar": luar, "leher": leher,
            "depanTerbuka": int(round(100 * kosong / len(tengah))), "nv": int(len(V)), "nf": int(len(F))}


def satu(aid, t):
    meta, obj = ambil_3d(aid, log=lambda *a: None, coba_pending=2)
    if meta is None:
        with _lok:
            STAT["pending" if str(obj).startswith("pending") else "galat"] += 1
        return aid, None, obj
    if not obj:
        with _lok:
            STAT["tanpa_obj"] += 1
        return aid, None, "obj"
    V, F, _ = baca_obj(obj)
    f = ukur3d(V, F)
    if f is None:
        return aid, None, "kosong"
    f["t"] = int(t)
    tx = meta.get("textures")
    f["ntex"] = len(tx) if isinstance(tx, list) else 0
    with _lok:
        STAT["ok"] += 1
    return aid, f, None


def muat_hasil():
    try:
        with gzip.open(P_HASIL, "rt", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def simpan_hasil(hasil):
    os.makedirs(os.path.dirname(P_HASIL), exist_ok=True)
    with gzip.open(P_HASIL + ".tmp", "wt", encoding="utf-8") as f:
        json.dump(hasil, f, separators=(",", ":"))
    os.replace(P_HASIL + ".tmp", P_HASIL)


def calon_panen(hasil, jenis):
    """item bertipe `jenis` dari data panen otak, paling difavoritkan dulu, yang belum diukur versi ini"""
    with gzip.open("data/panen.json.gz", "rt", encoding="utf-8") as f:
        meta = json.load(f).get("meta", {})
    c = [(int(m.get("f") or 0), int(i), int(m.get("t") or 0)) for i, m in meta.items()
         if int(m.get("t") or 0) in jenis and (hasil.get(i) or {}).get("v") != VERSI_3D]
    c.sort(reverse=True)
    return [(i, t) for _, i, t in c]


def panen(menit, batas, jenis, pekerja=4):
    hasil = muat_hasil()
    calon = calon_panen(hasil, jenis)[:batas]
    print(f"calon {len(calon)} (sudah diukur {len(hasil)}), pekerja {pekerja}, batas {menit} mnt", flush=True)
    t0 = time.time()
    selesai = 0
    with ThreadPoolExecutor(pekerja) as ex:
        it = iter(calon)
        aktif = set()
        for _ in range(pekerja * 2):
            nx = next(it, None)
            if nx:
                aktif.add(ex.submit(satu, *nx))
        while aktif:
            done = next(as_completed(aktif))
            aktif.discard(done)
            try:
                aid, f, err = done.result()
                if f:
                    hasil[str(aid)] = f
            except Exception as e:
                with _lok:
                    STAT["galat"] += 1
            selesai += 1
            if selesai % 200 == 0:
                print(f"  {selesai} | {json.dumps(STAT)} | {time.time() - t0:.0f} dtk", flush=True)
                simpan_hasil(hasil)
            if time.time() - t0 < menit * 60:
                nx = next(it, None)
                if nx:
                    aktif.add(ex.submit(satu, *nx))
    simpan_hasil(hasil)
    print(f"selesai: {json.dumps(STAT)} | total diukur {len(hasil)} | {time.time() - t0:.0f} dtk", flush=True)


def main():
    print("kunci API terpasang:", bool(KEY), flush=True)
    if "--panen" in sys.argv:
        jenis = {int(x) for x in (os.environ.get("JENIS_3D") or "64,65,66,67,68,69,70,71,72").split(",") if x.strip()}
        panen(float(os.environ.get("MENIT_3D") or 40), int(os.environ.get("BATAS_3D") or 4000), jenis,
              int(os.environ.get("PEKERJA_3D") or 4))
        return
    ids = [int(x) for x in sys.argv[1:] if x.isdigit()] or [7192553841, 9438759973, 126884250250747, 72558563872966, 192557913]
    os.makedirs("uji3d", exist_ok=True)
    hasil = {}
    for aid in ids:
        meta, obj = ambil_3d(aid)
        if meta is None or not obj:
            print(aid, "GAGAL:", obj if meta is None else "obj tidak terunduh", flush=True)
            hasil[str(aid)] = {"galat": str(obj)[:200]}
            continue
        V, F, grup = baca_obj(obj)
        f = ukur3d(V, F)
        print(aid, "OBJ:", len(V), "verteks,", len(F), "segitiga, grup:", list(grup)[:6], flush=True)
        print("   ", json.dumps(f)[:900], flush=True)
        hasil[str(aid)] = f
        time.sleep(0.3)
    json.dump(hasil, open("uji3d/hasil.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
