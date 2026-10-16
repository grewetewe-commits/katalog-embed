#!/usr/bin/env python3
"""
MOTIF DIUKUR DARI PIKSEL (rev 33) -- corak kain dibaca dari thumbnail resmi 420 px, bukan ditebak dari nama/CLIP.

Masalah lama: kartu `pola` = CLIP zero-shot + nama (cocok dengan nama hanya 44-55%), dan map memakai NAMA saja
(VisualOutfitKit MOTIF/polosNama). Baju bergaris tanpa kata "striped" dianggap polos -> generator salah menilai ramai.

Yang diukur per wilayah kain (warna Lab, piksel manekin/latar dibuang):
  kontras   : simpangan warna (dE) seluruh kain
  tepi      : kerapatan tepi tajam (dE antar piksel berjarak 2 > 18) -- corak punya tepi, lipatan/shading lembut tidak
  warna     : jumlah warna nyata (k-means Lab, gugus dE<12 digabung, pangsa >= 5%) + pangsa warna dominan
  ulang X/Y : autokorelasi 2D bertopeng (FFT) -> puncak berulang searah x / y (garis, kotak) dan keseragaman searah
              sumbu lain (garis mendatar seragam searah x)
  taburan   : gugus warna minor (jauh dari warna dominan) -> banyak bercak kecil padat sejenis (polkadot, hati, bintang)
  sebaran   : tepi di tengah vs pinggir -> gambar/logo terpusat di atas dasar polos (grafis) vs corak penuh (ramai)
Label: polos | garis | kotak | taburan | grafis | ramai  (+ "lemah" bila bukti tipis -> tidak diklaim).

2D klasik (baju 11 / celana 12): manekin & kamera tetap (lihat bentuk2d.py) -> wilayah badan depan, lengan, kaki.
3D (64-72): item sendiri di latar transparan, cahaya & lipatan -> kecerahan dilewatkan high-pass; tetap dievaluasi
terpisah dan hanya dipakai bila lolos uji (LAPORAN_MOTIF.md).
"""
import io, json, os, sys, time, re, random, gzip
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bentuk2d as B2

VERSI_MOTIF = 1
WIL2D = {   # (x0, y0, x1, y1) gambar 420 -- muka depan saja (bidang datar, cahaya rata)
    11: {"badan": (154, 130, 254, 236), "lenganL": (120, 128, 150, 226), "lenganR": (262, 132, 322, 232)},
    12: {"kaki": (160, 242, 262, 334)},
}


def lab(rgb):
    c = np.clip(rgb, 0, 255) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = (c @ M.T) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def _kmeans(P, k=5, it=10, seed=0):
    """k-means kecil (Lab) -> pusat, pangsa; gugus berjarak dE < 12 digabung"""
    rng = np.random.default_rng(seed)
    if len(P) > 4000:
        P = P[rng.choice(len(P), 4000, replace=False)]
    # inisialisasi: kuantil kecerahan (stabil, tanpa acak)
    o = np.argsort(P[:, 0])
    C = P[o[np.linspace(0, len(P) - 1, k).astype(int)]].copy()
    for _ in range(it):
        d = ((P[:, None, :] - C[None]) ** 2).sum(-1)
        a = d.argmin(1)
        for j in range(k):
            m = a == j
            if m.any():
                C[j] = P[m].mean(0)
    d = ((P[:, None, :] - C[None]) ** 2).sum(-1)
    a = d.argmin(1)
    w = np.bincount(a, minlength=k).astype(float)
    # gabung gugus mirip
    grup = list(range(k))
    for i in range(k):
        for j in range(i + 1, k):
            if w[i] > 0 and w[j] > 0 and np.sqrt(((C[i] - C[j]) ** 2).sum()) < 12:
                gi, gj = grup[i], grup[j]
                grup = [gi if g == gj else g for g in grup]
    pusat, pangsa = [], []
    for g in sorted(set(grup)):
        idx = [j for j in range(k) if grup[j] == g and w[j] > 0]
        if not idx:
            continue
        ww = w[idx].sum()
        pusat.append((C[idx] * w[idx, None]).sum(0) / ww)
        pangsa.append(ww / len(P))
    o = np.argsort(pangsa)[::-1]
    return np.array(pusat)[o], np.array(pangsa)[o]


def _autokor(X, M):
    """autokorelasi 2D bertopeng (vektor Lab, rata-rata dibuang). Kembalikan A(dy,dx) ternormalisasi & jumlah pasangan."""
    h, w = M.shape
    H2, W2 = 2 * h, 2 * w
    Fm = np.fft.rfft2(M.astype(float), (H2, W2))
    cnt = np.fft.irfft2(Fm * np.conj(Fm), (H2, W2))
    num = np.zeros((H2, W2))
    for c in range(X.shape[-1]):
        Fx = np.fft.rfft2(X[..., c] * M, (H2, W2))
        num += np.fft.irfft2(Fx * np.conj(Fx), (H2, W2))
    var = (X[M] ** 2).sum(-1).mean()
    A = num / np.maximum(cnt, 1) / max(var, 1e-6)
    return A, cnt


def _ulang(p, dmin, dmax):
    """profil autokorelasi 1D -> (puncak, jarak, celah): puncak ulang setelah lembah (osilasi nyata).
    Puncak tertinggi dipilih; bila beberapa hampir sama (kelipatan periode), jarak terkecil."""
    best = (0.0, 0, 0.0)
    for L in range(dmin, min(dmax, len(p) - 2) + 1):
        if p[L] < p[L - 1] or p[L] < p[L + 1]:
            continue
        lembah = float(p[1:L].min())
        cel = float(p[L]) - lembah
        if p[L] >= 0.25 and cel >= 0.25 and float(p[L]) > best[0] + 0.05:
            best = (float(p[L]), L, cel)
    return best


def analisa(L3, M, highpass=False):
    """L3: Lab (h,w,3) ; M: topeng kain (h,w) bool -> dict fitur wilayah (None bila kain terlalu sedikit)"""
    n = int(M.sum())
    if n < 300:
        return None
    X = L3.astype(np.float64).copy()
    if highpass:
        # 3D: cahaya/lipatan mengubah kecerahan pelan -> buang komponen halus (rata-rata lokal bertopeng)
        from scipy.ndimage import uniform_filter
        k = max(9, int(0.18 * min(M.shape)))
        mm = uniform_filter(M.astype(float), k)
        for c in (0,):
            X[..., c] = X[..., c] - uniform_filter(X[..., c] * M, k) / np.maximum(mm, 1e-3) + X[..., c][M].mean()
    P = X[M]
    mu = P.mean(0)
    s = float(np.sqrt(((P - mu) ** 2).sum(1).mean()))
    C, w = _kmeans(P)
    nyata = int((w >= 0.05).sum())
    # tepi tajam: jarak 2 piksel, dua arah, hanya pasangan di dalam kain
    def dE(a, b):
        return np.sqrt(((a - b) ** 2).sum(-1))
    mx = M[:, 2:] & M[:, :-2]
    my = M[2:, :] & M[:-2, :]
    ex = dE(X[:, 2:], X[:, :-2]) > 18
    ey = dE(X[2:, :], X[:-2, :]) > 18
    npas = mx.sum() + my.sum()
    tepi = float(((ex & mx).sum() + (ey & my).sum()) / max(1, npas))
    tepiX = float((ex & mx).sum() / max(1, mx.sum()))   # tepi saat bergeser searah x (garis TEGAK)
    tepiY = float((ey & my).sum() / max(1, my.sum()))   # garis MENDATAR
    # sebaran tepi: tengah vs pinggir (gambar terpusat)
    E = np.zeros(M.shape, bool)
    E[:, 1:-1] |= (ex & mx)
    E[1:-1, :] |= (ey & my)
    # blok warna: piksel -> warna k-means terdekat -> komponen terhubung besar (>= 5% kain). Tepi di antara dua blok besar
    # = batas blok (kaos dua warna, sepatu dilukis), bukan corak; tepi yang menyentuh bagian kecil = detail/corak.
    from scipy.ndimage import label as cc_label
    seg = (((X[..., None, :] - C[None, None]) ** 2).sum(-1)).argmin(-1)
    besarPx = np.zeros(M.shape, bool)
    nblok = 0
    for j in range(len(C)):
        lj, nj = cc_label(M & (seg == j))
        if nj:
            luas = np.bincount(lj.ravel())[1:]
            for q in np.nonzero(luas >= 0.05 * n)[0]:
                besarPx |= lj == (q + 1)
                nblok += 1
    detX = ex & mx & ~(besarPx[:, 2:] & besarPx[:, :-2])
    detY = ey & my & ~(besarPx[2:, :] & besarPx[:-2, :])
    tepiDet = float((detX.sum() + detY.sum()) / max(1, npas))
    cakBlok = float(besarPx.sum() / n)
    h, w_ = M.shape
    yy, xx = np.mgrid[0:h, 0:w_]
    ry, rx = (yy - (h - 1) / 2) / (h / 2), (xx - (w_ - 1) / 2) / (w_ / 2)
    tengah = (np.abs(ry) < 0.55) & (np.abs(rx) < 0.55) & M
    pinggir = ((np.abs(ry) > 0.7) | (np.abs(rx) > 0.7)) & M
    eT = float(E[tengah].mean()) if tengah.sum() > 30 else 0.0
    eP = float(E[pinggir].mean()) if pinggir.sum() > 30 else 0.0
    # pengulangan
    Xc = X - mu
    A, cnt = _autokor(Xc, M)
    ok = cnt >= 0.35 * n
    Ax = np.array([A[0, d] if ok[0, d] else np.nan for d in range(w_)])
    Ay = np.array([A[d, 0] if ok[d, 0] else np.nan for d in range(h)])
    def prof(p):
        p = np.nan_to_num(p, nan=0.0)
        return p
    Ax, Ay = prof(Ax), prof(Ay)
    pkx, Lx, cx = _ulang(Ax, 3, int(w_ / 2.2))
    pky, Ly, cy = _ulang(Ay, 3, int(h / 2.2))
    ux = float(np.mean(Ax[1:max(3, w_ // 3)]))   # seragam searah x (garis mendatar -> tinggi)
    uy = float(np.mean(Ay[1:max(3, h // 3)]))
    # taburan: piksel jauh dari warna dominan -> komponen terhubung
    d0 = np.sqrt(((X - C[0]) ** 2).sum(-1))
    minor = M & (d0 > 20)
    pm = float(minor.sum() / n)
    lab_, nk = cc_label(minor)
    bercak = 0
    luas_med = 0.0
    padat = 0.0
    if nk:
        luas = np.bincount(lab_.ravel())[1:]
        kecil = (luas >= 4) & (luas <= 0.03 * n)
        bercak = int(kecil.sum())
        if bercak:
            luas_med = float(np.median(luas[kecil]) / n)
            # kepadatan bercak: luas / kotak pembatas (bulat/kotak padat ~0.6-1, garis tipis memanjang rendah)
            from scipy.ndimage import find_objects
            obj = find_objects(lab_)
            pd = []
            for j, sl in enumerate(obj):
                if sl is None or not kecil[j]:
                    continue
                bh, bw = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
                if max(bh, bw) <= 2 * min(bh, bw):
                    pd.append(luas[j] / (bh * bw))
                else:
                    pd.append(0.0)
            padat = float(np.mean(pd)) if pd else 0.0
        besar = float(luas.max() / n)
    else:
        besar = 0.0
    return {"n": n, "s": round(s, 1), "warna": nyata, "dom": round(float(w[0]), 3), "tepi": round(tepi, 4),
            "tepiX": round(tepiX, 4), "tepiY": round(tepiY, 4), "tepiDet": round(tepiDet, 4), "blok": nblok,
            "cakBlok": round(cakBlok, 3), "eT": round(eT, 4), "eP": round(eP, 4),
            "pkx": round(pkx, 3), "Lx": Lx, "cx": round(cx, 3), "pky": round(pky, 3), "Ly": Ly, "cy": round(cy, 3),
            "ux": round(ux, 3), "uy": round(uy, 3), "minor": round(pm, 3), "bercak": bercak,
            "luasBercak": round(luas_med, 4), "padat": round(padat, 3), "besar": round(besar, 3)}


def label_wilayah(f):
    """fitur wilayah -> (label, kekuatan 0..100). Ambang dari uji (LAPORAN_MOTIF.md); 'lemah' = tidak diklaim.
    Urutan: corak BERULANG dulu (garis/kotak/taburan), lalu polos/blok warna, lalu gambar terpusat vs corak penuh."""
    if f is None:
        return None, 0
    perX = f["pkx"] >= 0.3 and f["cx"] >= 0.3
    perY = f["pky"] >= 0.3 and f["cy"] >= 0.3
    tabur = f["bercak"] >= 6 and f["padat"] >= 0.45 and 0.03 <= f["minor"] <= 0.4 and f["besar"] <= 0.05
    if perX and perY and f["tepi"] >= 0.03:
        if tabur:
            return "taburan", 85
        if f["ux"] >= 0.85 or f["uy"] >= 0.85:
            return "garis", 80
        return "kotak", int(100 * min(1.0, (f["pkx"] + f["pky"]) / 2 + 0.2))
    if perY and f["ux"] >= 0.5 and f["tepiY"] >= 0.03:
        return "garis", int(100 * min(1.0, f["pky"] + 0.2))      # mendatar
    if perX and f["uy"] >= 0.5 and f["tepiX"] >= 0.03:
        return "garis", int(100 * min(1.0, f["pkx"] + 0.2))      # tegak
    if f["tepiDet"] < 0.02:
        if f["tepi"] < 0.02 or f["blok"] <= 1:
            return "polos", 90 if f["tepi"] < 0.012 else 75
        return "blok", 75                                          # 2-3 bidang warna rata, tanpa corak
    if tabur and f["eP"] >= 0.03:
        return "taburan", 65
    if f["eT"] >= 0.06 and f["eP"] <= 0.03 and f["eT"] >= 2.5 * max(f["eP"], 0.005):
        return "grafis", 70
    if f["tepiDet"] >= 0.05 and f["eP"] >= 0.04:
        return "ramai", int(min(100, 40 + 400 * f["tepiDet"]))
    if f["tepiDet"] >= 0.035:
        return ("grafis" if f["eT"] > 1.8 * f["eP"] else "ramai"), 40
    return "lemah", 20


def ukur(im, t):
    """PIL RGBA thumbnail 420 -> {"v", "wil": {nama: fitur}, "label", "p"}"""
    if im.size != (420, 420):
        im = im.resize((420, 420), Image.BILINEAR)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] > 200
    L3 = lab(rgb)
    out = {"v": VERSI_MOTIF, "wil": {}}
    if t in WIL2D:
        man = B2.manekin(rgb) & al
        kain = al & ~man
        for nm, (x0, y0, x1, y1) in WIL2D[t].items():
            f = analisa(L3[y0:y1, x0:x1], kain[y0:y1, x0:x1])
            if f:
                out["wil"][nm] = f
    else:
        from scipy.ndimage import binary_erosion
        m = binary_erosion(al, iterations=3)
        ys, xs = np.nonzero(m)
        if len(ys) > 400:
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            # bagian tengah item (bidang depan terbesar), tepi siluet dibuang
            hy, hx = (y1 - y0), (x1 - x0)
            yy0, yy1 = y0 + int(0.15 * hy), y1 - int(0.15 * hy)
            xx0, xx1 = x0 + int(0.2 * hx), x1 - int(0.2 * hx)
            f = analisa(L3[yy0:yy1, xx0:xx1], m[yy0:yy1, xx0:xx1], highpass=True)
            if f:
                out["wil"]["item"] = f
    lab_w = {k: label_wilayah(f) for k, f in out["wil"].items()}
    out["labelWil"] = {k: v[0] for k, v in lab_w.items()}
    out["label"], out["p"] = gabung(t, lab_w, out["wil"])
    return out


URUT = {"garis": 6, "kotak": 6, "taburan": 5, "ramai": 4, "grafis": 3, "blok": 2, "polos": 1, "lemah": 0, None: -1}
POLOSAN = ("polos", "blok")


def gabung(t, lab_w, wil):
    """label item dari label wilayah. Baju: badan diutamakan; corak berulang di KEDUA lengan juga dihitung (overall/rompi
    di atas kaos bergaris). Badan ramai tapi kedua lengan polos = gambar/tulisan di badan (kaos bergambar) -> grafis."""
    if not lab_w:
        return None, 0
    if t == 11:
        b = lab_w.get("badan", (None, 0))
        lg = [lab_w[k] for k in ("lenganL", "lenganR") if k in lab_w]
        if b[0] in ("garis", "kotak", "taburan"):
            return b
        ul = [x for x in lg if x[0] in ("garis", "kotak", "taburan")]
        if len(ul) == 2 and ul[0][0] == ul[1][0]:
            return ul[0][0], min(ul[0][1], ul[1][1]) - 10
        if b[0] == "ramai" and len(lg) == 2 and all(x[0] in POLOSAN for x in lg):
            return "grafis", 70
        if b[0] in POLOSAN and len(lg) == 2 and all(x[0] in ("ramai", "taburan") for x in lg):
            return "ramai", 50                                     # lengan bercorak, badan depan polos (jaket terbuka)
        return b if b[0] else (lg[0] if lg else (None, 0))
    return max(lab_w.values(), key=lambda x: (URUT.get(x[0], -1), x[1]))


# --------------------------------------------------------------------------- uji (GitHub Actions)
KELAS_NAMA = {
    "garis": r"\b(stripe|stripes|striped|stripped|pinstripe|pinstriped)\b",
    "kotak": r"\b(plaid|tartan|flannel|checkered|checker|checkerboard|gingham)\b",
    "taburan": r"\b(polka|polkadot|polkadots|dots|dotted)\b",
    "ramai": r"\b(camo|camouflage|leopard|cheetah|zebra|floral|hawaiian|paisley|tie dye|tiedye)\b",
    "polos": r"\b(plain|solid|basic|blank)\b",
}
WARNA_KATA = set("black white red blue green pink purple yellow orange brown grey gray beige cream navy dark light baby "
                 "pastel maroon olive tan khaki lilac lavender mint teal cyan nude charcoal".split())
JENIS_KATA = set("tee tees t shirt shirts tshirt polo tank top tops jeans jean pants pant trousers sweatpants joggers jogger "
                 "shorts hoodie sweater sweatshirt longsleeve sleeve sleeves vneck crewneck long short".split())


def kelas_nama(n):
    n = (n or "").lower()
    hit = [k for k, rx in KELAS_NAMA.items() if re.search(rx, n)]
    if len(hit) == 1:
        return hit[0]
    if not hit:
        w = re.findall(r"[a-z]+", n)
        if 1 <= len(w) <= 4 and any(x in JENIS_KATA for x in w) and all(x in WARNA_KATA or x in JENIS_KATA for x in w):
            return "polos"
    return None


def ambil(ids, folder, ukuran="420x420"):
    """thumbnail resmi (publik) -> cache PNG per id (actions/cache), dipakai ulang antar uji"""
    os.makedirs(folder, exist_ok=True)
    perlu = [i for i in ids if not os.path.exists(f"{folder}/{i}.png")]
    print(f"thumbnail: {len(ids) - len(perlu)} dari cache, ambil {len(perlu)}", flush=True)
    for a in range(0, len(perlu), 100):
        got = B2.thumb(perlu[a:a + 100], ukuran, 0.3)
        for i, im in got.items():
            im.save(f"{folder}/{i}.png")
    out = {}
    for i in ids:
        p = f"{folder}/{i}.png"
        if os.path.exists(p):
            try:
                out[i] = Image.open(p).convert("RGBA")
            except Exception:
                pass
    return out


def lembar(judul, sel, jalur, font, kol=8, sw=150, sh=150):
    """sel: [(gambar PIL, [teks...])] -> JPEG kecil (lembar ditimpa tiap uji; repo tetap ringan)"""
    from PIL import ImageDraw
    th = 38
    baris = (len(sel) + kol - 1) // kol
    kan = Image.new("RGB", (kol * sw, 22 + baris * (sh + th)), (245, 245, 245))
    d = ImageDraw.Draw(kan)
    d.text((6, 5), judul, fill=(0, 0, 0), font=font)
    for k, (im, teks) in enumerate(sel):
        x, y = (k % kol) * sw, 22 + (k // kol) * (sh + th)
        if im is not None:
            alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
            alas.alpha_composite(im)
            kan.paste(alas.convert("RGB").resize((sw - 4, sh - 4)), (x + 2, y))
        for q, tx in enumerate(teks[:3]):
            d.text((x + 3, y + sh - 2 + q * 12), tx[:int(sw / 6)], fill=(0, 0, 0) if q else (20, 20, 160), font=font)
    kan.save(jalur, quality=82, optimize=True)


def potong_2d(im, t):
    """untuk lembar: wilayah yang diukur saja (diperbesar) supaya corak terlihat"""
    if t == 11:
        return im.crop((112, 120, 330, 240))
    if t == 12:
        return im.crop((150, 236, 272, 340))
    return im


def main():
    from PIL import ImageFont
    rng = random.Random(20261017)
    meta = json.load(gzip.open("data/panen.json.gz", "rt", encoding="utf-8"))["meta"]
    BATAS_KELAS = int(os.environ.get("MOTIF_PER_KELAS", "120"))
    ACAK = int(os.environ.get("MOTIF_ACAK", "150"))
    kelompok = {"2D baju": (11,), "2D celana": (12,), "3D atas": (64, 65, 66, 67, 68), "3D bawah": (69, 72)}
    sampel = {}
    for g, ts in kelompok.items():
        per = {}
        semua = []
        for k, v in meta.items():
            if int(v.get("t") or 0) in ts:
                semua.append(int(k))
                c = kelas_nama(v.get("n"))
                if c:
                    per.setdefault(c, []).append(int(k))
        pilih = []
        bk = BATAS_KELAS if g.startswith("2D") else BATAS_KELAS // 2
        for c, ids in sorted(per.items()):
            ids.sort()
            pilih += rng.sample(ids, min(bk, len(ids)))
        semua.sort()
        pilih += rng.sample(semua, min(ACAK if g.startswith("2D") else ACAK // 2, len(semua)))
        sampel[g] = sorted(set(pilih))
    try:
        for i, t in json.load(open("uji2d/sampel.json"))["sampel"]:
            if t in (11, 12) and str(i) in meta:
                g = "2D baju" if t == 11 else "2D celana"
                sampel[g] = sorted(set(sampel[g]) | {int(i)})
    except Exception as ex:
        print("sampel emas gagal:", ex, flush=True)
    ids = sorted({i for v in sampel.values() for i in v})
    gambar = ambil(ids, "cache_motif")
    hasil = {}
    for g, daftar in sampel.items():
        for i in daftar:
            im = gambar.get(i)
            if im is None:
                continue
            t = int(meta[str(i)].get("t") or 0)
            try:
                hasil[i] = ukur(im, t)
            except Exception as ex:
                print("gagal ukur", i, ex, flush=True)
    # evaluasi: label terukur vs kelas nama (hanya nama yang menunjuk tepat satu kelas)
    kelas = ["polos", "blok", "garis", "kotak", "taburan", "ramai", "grafis", "lemah"]
    lap = ["# Laporan motif diukur (rev 33)", "",
           "Label dari PIKSEL thumbnail (motif.py), dibandingkan dengan kata di NAMA item (bukan kebenaran mutlak: nama bisa",
           "menyebut motif yang hanya kecil, atau bohong). Baris = kelas menurut nama, kolom = hasil ukur.", ""]
    ringkas = {}
    for g, daftar in sampel.items():
        tab = {}
        for i in daftar:
            if i not in hasil:
                continue
            c = kelas_nama(meta[str(i)].get("n"))
            tab.setdefault(c or "-", {}).setdefault(hasil[i]["label"] or "-", 0)
            tab[c or "-"][hasil[i]["label"] or "-"] += 1
        lap += [f"## {g}", "", "| nama \\ ukur | " + " | ".join(kelas + ["-"]) + " | n | cocok |",
                "|---" * (len(kelas) + 4) + "|"]
        for c in ["polos", "garis", "kotak", "taburan", "ramai", "-"]:
            row = tab.get(c, {})
            n = sum(row.values())
            if not n:
                continue
            cocok = row.get(c, 0)
            if c == "ramai":
                cocok = row.get("ramai", 0) + row.get("taburan", 0)
            pct = f"{round(100 * cocok / max(1, n - row.get('lemah', 0)))}%" if c != "-" else ""
            lap.append(f"| {c} | " + " | ".join(str(row.get(k, 0)) for k in kelas + ["-"]) + f" | {n} | {pct} |")
            ringkas[f"{g}/{c}"] = pct
        # presisi per label ukur (dari item yang namanya berkelas)
        lap.append("")
        for k in ["polos", "garis", "kotak", "taburan"]:
            tot = sum(tab.get(c, {}).get(k, 0) for c in tab if c != "-")
            ben = tab.get(k, {}).get(k, 0)
            if tot:
                lap.append(f"- presisi `{k}` (vs nama): {ben}/{tot} = {round(100 * ben / tot)}%")
        lap.append("")
    try:
        font = ImageFont.load_default(size=10)
    except TypeError:
        font = ImageFont.load_default()
    os.makedirs("kartu/lembar", exist_ok=True)
    PER_LABEL = int(os.environ.get("MOTIF_LEMBAR", "8"))
    UK = {"2D baju": (6, 218, 120), "2D celana": (8, 160, 136), "3D atas": (8, 150, 150), "3D bawah": (8, 150, 150)}
    for g, daftar in sampel.items():
        ada = [i for i in daftar if i in hasil]
        sel = []
        for k in ["polos", "blok", "garis", "kotak", "taburan", "ramai", "grafis", "lemah"]:
            pil = sorted(i for i in ada if hasil[i]["label"] == k)
            for i in rng.sample(pil, min(PER_LABEL, len(pil))):
                t = int(meta[str(i)].get("t") or 0)
                lw = hasil[i].get("labelWil", {})
                sel.append((potong_2d(gambar[i], t), [f"{k.upper()} {hasil[i]['p']} nm:{kelas_nama(meta[str(i)].get('n')) or '-'}",
                                                     (meta[str(i)].get("n") or "?"),
                                                     " ".join(f"{a[:2]}:{(b or '-')[:4]}" for a, b in lw.items())]))
        kol, sw, sh = UK[g]
        lembar(f"Motif terukur {g}: {PER_LABEL} contoh acak per label (baris biru = hasil ukur, nm = kata di nama)", sel,
               f"kartu/lembar/motif_{g.replace(' ', '_').lower()}.jpg", font, kol, sw, sh)
    # label emas manual (uji2d/emas.json, dinilai mata 16 Okt) -> kelas ukur
    try:
        emas = json.load(open("uji2d/emas.json"))
        smp = json.load(open("uji2d/sampel.json"))["sampel"]
        PETA = {"polos": "polos", "garis": "garis", "kotak": "kotak", "polkadot": "taburan", "bunga": "ramai", "loreng": "ramai",
                "motif_hewan": "ramai", "grafis": "grafis", "tulisan": "grafis", "denim": "polos", "kulit": "polos"}
        pos = {}
        for i, t in smp:
            pos.setdefault(str(t), []).append(i)
        lap += ["## Label emas (dinilai mata)", "", "| t | id | emas | ukur | wilayah |", "|---|---|---|---|---|"]
        benar = tot = 0
        for t in ("11", "12"):
            for k, i in enumerate(pos.get(t, [])):
                e = emas[t]["pola"][k] if k < len(emas[t]["pola"]) else None
                if e is None or e not in PETA or i not in hasil:
                    continue
                u = hasil[i]["label"]
                ok_ = u == PETA[e] or (PETA[e] == "polos" and u == "blok") or (PETA[e] == "ramai" and u == "taburan")
                tot += 1
                benar += ok_
                lap.append(f"| {t} | {i} | {e} | {u}{'' if ok_ else ' X'} | {hasil[i].get('labelWil')} |")
        lap += ["", f"**Emas: {benar}/{tot} cocok**", ""]
    except Exception as ex:
        lap.append(f"(emas gagal: {ex})")
    with open("LAPORAN_MOTIF.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lap) + "\n")
    simpan = {str(i): {"t": int(meta[str(i)].get("t") or 0), "nm": kelas_nama(meta[str(i)].get("n")), "l": h["label"],
                       "p": h["p"], "w": h["wil"]} for i, h in hasil.items()}
    with open("uji2d/motif_fitur.json", "w") as f:
        json.dump(simpan, f, separators=(",", ":"))
    print("\n".join(lap[:80]), flush=True)


if __name__ == "__main__":
    main()
