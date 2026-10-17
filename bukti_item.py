#!/usr/bin/env python3
"""
BUKTI ITEM (rev 31) -- tema & gender item dari BUKTI, bukan tebakan satu sumber.

Sumber bukti (semuanya gratis, data sudah ada di repo):
  nama      : kata kunci tema/gender di nama item (pembuat menamai itemnya)
  unsur     : unsur yang TERLIHAT di gambar (subjek: labu/tengkorak/mahkota..., jenis: topi koboi/zirah/tanduk..., pola: loreng...)
              -- CLIP jauh lebih andal untuk BENDA daripada untuk gaya abstrak
  gaya      : tema gaya menurut gambar saja (CLIP; paling lemah, hanya 1 poin)
  pemakaian : 73 rb outfit buatan MANUSIA (data/panen.json.gz): item dipakai bersama item bertema/bergender apa
Tema diputuskan hanya bila poin cukup; kurang bukti = tidak bertema khusus (bukan dipaksa menebak).
Gender: propagasi pemakaian dari item yang namanya jelas bergender (uji nama-tersembunyi 16 Okt: 94% benar, vs skor
CLIP otak 78%). Peta sambungan tema (PMI) dipelajari dari outfit manusia yang item-itemnya bertema kuat.
"""
import collections, math, re
import numpy as np

# indeks kolom kartu (lihat kartu_item.bangun)
K_KEL, K_JENIS, K_JENISP, K_T1, K_P1, K_T2, K_P2, K_S1, K_SP1, K_S2, K_SP2, K_POLA, K_POLAP = range(13)
K_TGAMBAR, K_FUNGSI = 17, 18

# --------------------------------------------------------------------------------------------------------------
# UNSUR TEMA: (facet, label, kuat?) -- kuat = benda yang hampir selalu berarti tema itu (2 poin, p>=40), lemah = 1 poin (p>=50)
UNSUR = {
    "halloween": [("subjek", "labu", 1), ("subjek", "kelelawar", 1), ("subjek", "hantu", 1), ("subjek", "laba_laba", 1)],
    "horor": [("subjek", "tengkorak", 0), ("subjek", "mata", 0), ("jenis", "topeng_kepala", 0)],
    "koboi": [("jenis", "topi_koboi", 1)],
    "bajak_laut": [("jenis", "penutup_mata", 1), ("subjek", "tengkorak", 0)],
    "ksatria": [("jenis", "zirah", 1), ("jenis", "zirah_bawah", 1), ("jenis", "helm", 0)],
    "kerajaan": [("jenis", "mahkota", 1), ("subjek", "mahkota", 0)],   # gambar mahkota di baju sering = warna emas saja
    "militer": [("pola", "loreng", 1)],
    "maid": [("pola", "renda", 0), ("jenis", "pita_bando", 0)],
    "gothic": [("subjek", "salib", 0), ("pola", "renda", 0), ("jenis", "korset", 0)],
    "punk": [("subjek", "rantai", 0), ("jenis", "tindik", 0), ("pola", "kotak", 0)],
    "kawaii": [("subjek", "kucing", 0), ("subjek", "kelinci", 0), ("subjek", "beruang", 0), ("subjek", "hati", 0),
               ("pola", "polkadot", 0)],
    "coquette": [("subjek", "pita", 0), ("jenis", "pita_bando", 0), ("pola", "renda", 0)],
    "y2k": [("pola", "kilau", 0), ("pola", "pelangi", 0)],
    "peri": [("jenis", "sayap", 0), ("subjek", "kupu_kupu", 0), ("subjek", "bunga", 0)],
    "malaikat": [("jenis", "halo", 1), ("jenis", "sayap", 0)],
    "iblis": [("jenis", "tanduk", 1), ("jenis", "ekor", 0)],
    "vampir": [("jenis", "jubah_belakang", 0)],
    "musim_dingin": [("jenis", "syal", 0), ("jenis", "kupluk", 0), ("pola", "bulu", 0)],
    "anime": [("subjek", "wajah_anime", 1)],
    "kostum_hewan": [("jenis", "telinga", 0), ("jenis", "ekor", 0), ("jenis", "kostum_penuh", 0), ("pola", "bulu", 0)],
    "novelty": [("subjek", "makanan", 0), ("subjek", "kartun", 0)],
    "tradisional": [("jenis", "jubah", 0)],
    "ninja": [("jenis", "penutup_kain", 0), ("jenis", "senjata", 0)],
    "superhero": [("jenis", "jubah_belakang", 0)],
    "antariksa": [("subjek", "bintang", 0), ("subjek", "bulan", 0)],
    "sporty": [("jenis", "jersey", 1), ("jenis", "topi_baseball", 0), ("jenis", "jogger", 0)],
    "formal": [("jenis", "jas", 1), ("jenis", "celana_kain", 0), ("jenis", "topi_formal", 0), ("jenis", "kemeja", 0)],
    "gaun_elegan": [("jenis", "gaun", 0), ("jenis", "bawahan_gaun", 0), ("jenis", "rok_panjang", 0)],
    "sekolah": [("jenis", "seragam", 0)],
    "polisi": [("jenis", "seragam", 0)],
    "streetwear": [("jenis", "hoodie", 0), ("jenis", "kargo", 0), ("subjek", "logo", 0)],
}
POIN_KUAT, POIN_SEDANG = 4, 3
SUMBER_NAMA, SUMBER_UNSUR, SUMBER_GAYA, SUMBER_PAKAI = 1, 2, 4, 8

# --------------------------------------------------------------------------------------------------------------
# GENDER dari nama (sama semangat dengan GenderKit di map; berlaku semua slot untuk benih propagasi)
PRIA = {"male", "man", "men", "mens", "boy", "boys", "cowo", "pria", "guy", "dude", "bro", "masculine", "beard", "mustache",
        "moustache", "goatee", "stubble", "sideburns"}
WANITA = {"female", "woman", "women", "womens", "girl", "girls", "cewe", "wanita", "lady", "ladies", "miss", "mrs", "feminine",
          "skirt", "skirts", "dress", "dresses", "blouse", "corset", "bustier", "cami", "camisole", "bikini", "bra", "lashes",
          "eyelashes", "lipstick", "gown", "miniskirt", "pigtails", "ponytails", "dolly", "diva", "baddie"}
JENIS_CEWE = {("bawah", "rok_pendek"), ("bawah", "rok_panjang"), ("bawah", "bawahan_gaun"), ("atas", "gaun"), ("atas", "korset")}
JENIS_COWO = {("wajah", "kumis_jenggot")}


def tok(s):
    return set(re.findall(r"[a-z]+", (s or "").lower()))


def gender_nama(nama):
    t = tok(nama)
    if "unisex" in t:
        return 0.0
    if "dress" in t and "shirt" in t:
        t = t - {"dress"}
    f, m = bool(t & WANITA), bool(t & PRIA)
    if f and not m:
        return 1.0
    if m and not f:
        return -1.0
    return 0.0


def daftar_outfit(st):
    """outfit buatan manusia di data panen -> daftar list id (minimal 2 item)"""
    out = []
    for o in (st.get("outfit") or {}).values():
        ids = [o[k] for k in ("Sh", "Pa", "Gt") if o.get(k)] + [a[0] for a in (o.get("A") or []) if a]
        ids = list({int(i) for i in ids if isinstance(i, (int, float)) and i > 0})
        if len(ids) >= 2:
            out.append(ids)
    return out


def _konteks(nilai, outs):
    """rata-rata nilai item LAIN dalam outfit yang sama, dirata-rata atas semua outfit item -> (dict ctx, Counter n)"""
    acc, n = collections.defaultdict(float), collections.Counter()
    for ids in outs:
        v = [nilai.get(i, 0.0) for i in ids]
        tot = sum(v)
        k = len(ids) - 1
        for i, x in zip(ids, v):
            acc[i] += (tot - x) / k
            n[i] += 1
    return {i: acc[i] / n[i] for i in acc}, n


def gender_bukti(kartu, meta, outs, label, sembunyi=None, iters=2, benih_bentuk=None, sumber_bentuk=None):
    """-> {id: (skor -1 cowo .. +1 cewe, jumlah outfit)} ; sembunyi = set id yang benih namanya disembunyikan (uji);
    benih_bentuk = {id: nilai} dari BENTUK 2D DIUKUR (leher rendah / bahu terbuka / crop: 98-99% dipakai cewek, data 16 Okt)"""
    benih, src = {}, {}
    for i, b in kartu.items():
        m = meta.get(str(i)) or {}
        g = 0.0 if (sembunyi and i in sembunyi) else gender_nama(m.get("n"))
        sb = 1 if g else 0                               # 1 nama
        if g == 0.0 and benih_bentuk and i in benih_bentuk:
            g = benih_bentuk[i]
            sb = (sumber_bentuk or {}).get(i, 2)         # 2 bentuk diukur (2D/3D), 4 kategori resmi
        if g == 0.0 and b[K_JENIS] >= 0 and b[K_JENISP] >= 50:
            kel = label["kelompok"][b[K_KEL]]
            jn = label["jenis"].get(kel, [])
            nmj = jn[b[K_JENIS]] if b[K_JENIS] < len(jn) else None
            if (kel, nmj) in JENIS_CEWE:
                g, sb = 0.5, 4
            elif (kel, nmj) in JENIS_COWO:
                g, sb = -0.5, 4
        if g:
            benih[i] = g
            src[i] = sb
    cur = dict(benih)
    ctx, n = {}, collections.Counter()
    for _ in range(iters):
        ctx, n = _konteks(cur, outs)
        cur = {i: (benih[i] if i in benih else ctx.get(i, 0.0)) for i in set(benih) | set(ctx)}
    hasil = {}
    for i in kartu:
        c = ctx.get(i)
        g0 = benih.get(i, 0.0)
        if c is None and g0 == 0.0:
            continue
        s = (0.6 * g0 + 0.4 * (c or 0.0)) if g0 else (c or 0.0)
        sb = src.get(i, 0) | (8 if n.get(i, 0) >= 2 and c is not None else 0)   # 8 pemakaian (>= 2 outfit manusia)
        hasil[i] = (max(-1.0, min(1.0, s)), n.get(i, 0) + (2 if abs(g0) >= 1 else 0), sb)
    return hasil


def uji_gender(kartu, meta, outs, label, seed=0, benih_bentuk=None):
    """uji jujur: benih nama 20% item berlabel disembunyikan, lalu ditebak dari pemakaian saja"""
    lab = [i for i in kartu if gender_nama((meta.get(str(i)) or {}).get("n")) != 0.0]
    rng = np.random.default_rng(seed)
    rng.shuffle(lab)
    uji = set(lab[:len(lab) // 5])
    h = gender_bukti(kartu, meta, outs, label, sembunyi=uji, benih_bentuk=benih_bentuk)
    out = []
    for amb in (0.10, 0.15, 0.25):
        ok = nn = 0
        for i in uji:
            s = h.get(i, (0.0, 0))[0]
            if abs(s) <= amb:
                continue
            nn += 1
            ok += (s > 0) == (gender_nama((meta.get(str(i)) or {}).get("n")) > 0)
        out.append((amb, ok, nn, len(uji)))
    return out


# --------------------------------------------------------------------------------------------------------------
def _indeks_unsur(label, tema_list):
    """UNSUR dengan nama label -> indeks: {tema_idx: [(facet, kel|None, idx, kuat)]}"""
    out = {}
    ti = {t: k for k, t in enumerate(tema_list)}
    for tema, lst in UNSUR.items():
        if tema not in ti:
            continue
        rows = []
        for facet, lab, kuat in lst:
            if facet == "subjek":
                if lab in label["subjek"]:
                    rows.append(("subjek", None, label["subjek"].index(lab), kuat))
            elif facet == "pola":
                if lab in label["pola"]:
                    rows.append(("pola", None, label["pola"].index(lab), kuat))
            else:
                for kel, jn in label["jenis"].items():
                    if lab in jn:
                        rows.append(("jenis", kel, jn.index(lab), kuat))
        out[ti[tema]] = rows
    return out


def _poin_unsur(p, kuat):
    """unsur kuat: 2 poin bila gambar yakin (>=60), 1 bila sedang (>=40); unsur lemah: 1 poin bila >=60"""
    if kuat:
        return 2 if p >= 60 else (1 if p >= 40 else 0)
    return 1 if p >= 60 else 0


def _poin_sendiri(b, kel, nama_hits, iu, T):
    """poin & sumber per tema dari bukti ITEM itu sendiri (nama, unsur gambar, gaya gambar)"""
    poin = np.zeros(T)
    sumber = np.zeros(T, dtype=np.int64)
    kuat_yakin = np.zeros(T, dtype=bool)   # benda khas tema terlihat jelas (unsur kuat, gambar >= 60)
    for t in nama_hits:
        poin[t] += 2 if len(nama_hits) == 1 else 1
        sumber[t] |= SUMBER_NAMA
    for t, rows in iu.items():
        p = 0
        for facet, k, idx, kuat in rows:
            q = 0
            if facet == "subjek":
                for c, cp in ((K_S1, K_SP1), (K_S2, K_SP2)):
                    if b[c] == idx:
                        q += _poin_unsur(b[cp], kuat)
            elif facet == "pola":
                if b[K_POLA] == idx:
                    q += _poin_unsur(b[K_POLAP], kuat)
            elif k == kel and b[K_JENIS] == idx:
                q += _poin_unsur(b[K_JENISP], kuat)
            if kuat and q >= 2:
                kuat_yakin[t] = True
            p += q
        if p:
            poin[t] += min(3, p)
            sumber[t] |= SUMBER_UNSUR
    tg = b[K_TGAMBAR]
    if 0 <= tg < T:
        poin[tg] += 1
        sumber[tg] |= SUMBER_GAYA
    return poin, sumber, kuat_yakin


def tema_bukti(kartu, meta, outs, label, tema_kata, ada_kata, token):
    """-> {id: (temaB idx | -1, poin, sumber bitmask, temaCocok idx | -1)}; tema_kata = TEMA (kunci, desk, kata)"""
    tema_list = [t[0] for t in tema_kata]
    T = len(tema_list)
    BIASA = tema_list.index("biasa")
    iu = _indeks_unsur(label, tema_list)
    sendiri = {}
    for i, b in kartu.items():
        kel = label["kelompok"][b[K_KEL]]
        nm = (meta.get(str(i)) or {}).get("n") or ""
        nl, tk = nm.lower(), token(nm)
        hits = [j for j, lab in enumerate(tema_kata) if j != BIASA and lab[2] and ada_kata(nl, tk, lab[2])]
        sendiri[i] = _poin_sendiri(b, kel, hits, iu, T)
    # tahap 1: tema dari bukti sendiri saja (benih pemakaian)
    t1 = {}
    for i, (poin, _, _) in sendiri.items():
        poin = poin.copy()
        poin[BIASA] = -1
        t = int(np.argmax(poin))
        if poin[t] >= POIN_SEDANG:
            t1[i] = t
    # tahap 2: pemakaian = proporsi item lain di outfit yang sama yang bertema t (tahap 1)
    share, dukung, nOut = collections.defaultdict(lambda: np.zeros(T)), collections.defaultdict(lambda: np.zeros(T)), collections.Counter()
    for ids in outs:
        th = [t1.get(i, -1) for i in ids]
        cnt = collections.Counter(t for t in th if t >= 0)
        k = len(ids) - 1
        for i, t in zip(ids, th):
            c = cnt.copy()
            if t >= 0:
                c[t] -= 1
            nOut[i] += 1
            v = share[i]
            d = dukung[i]
            for tt, x in c.items():
                if x > 0:
                    v[tt] += x / k
                    d[tt] += x
    hasil = {}
    for i, (poin, sumber, kuat_yakin) in sendiri.items():
        poin = poin.copy()
        sumber = sumber.copy()
        cocok = -1
        if i in share:
            s = share[i] / max(1, nOut[i])
            d = dukung[i]
            tb = int(np.argmax(s))
            if s[tb] >= 0.25 and d[tb] >= 2:
                cocok = tb
            for t in range(T):
                if s[t] >= 0.4 and d[t] >= 4:
                    poin[t] += 2
                    sumber[t] |= SUMBER_PAKAI
                elif s[t] >= 0.25 and d[t] >= 2:
                    poin[t] += 1
                    sumber[t] |= SUMBER_PAKAI
        poin[BIASA] = -1
        t = int(np.argmax(poin))
        sendiri_t = sumber[t] & (SUMBER_NAMA | SUMBER_UNSUR | SUMBER_GAYA)
        # unsur & gaya sama-sama dari GAMBAR (CLIP) -> tidak saling bebas: klaim yang hanya dari gambar butuh poin kuat
        # kecuali benda khas tema terlihat jelas (labu, tanduk, mahkota, topi koboi... gambar >= 60) DAN gaya gambar setuju
        hanya_gambar = (sumber[t] & (SUMBER_NAMA | SUMBER_PAKAI)) == 0
        gambar_jelas = kuat_yakin[t] and (sumber[t] & SUMBER_GAYA)
        ok = poin[t] >= POIN_KUAT or (poin[t] >= POIN_SEDANG and sendiri_t and (not hanya_gambar or gambar_jelas))
        hasil[i] = (t if ok else -1, int(min(9, max(0, poin[t]))), int(sumber[t]) if ok else 0, cocok)
    return hasil


def graf_tema(tb, outs, tema_list, min_pasang=5):
    """PMI antar tema dari outfit manusia (hanya item bertema kuat/sedang) -> {tema: [[tema2, pmi, n], ...]}"""
    cnt, pair, nO = collections.Counter(), collections.Counter(), 0
    for ids in outs:
        ts = sorted({tb[i][0] for i in ids if i in tb and tb[i][0] >= 0})
        if not ts:
            continue
        nO += 1
        for t in ts:
            cnt[t] += 1
        for a in range(len(ts)):
            for b in range(a + 1, len(ts)):
                pair[(ts[a], ts[b])] += 1
    g = collections.defaultdict(list)
    for (a, b), c in pair.items():
        if c < min_pasang:
            continue
        p = math.log((c * nO) / (cnt[a] * cnt[b]))
        g[tema_list[a]].append([tema_list[b], round(p, 3), c])
        g[tema_list[b]].append([tema_list[a], round(p, 3), c])
    return {"n_outfit": nO, "n_tema": {tema_list[t]: c for t, c in cnt.items()},
            "sambung": {t: sorted(v, key=lambda x: -x[1]) for t, v in g.items()}}
