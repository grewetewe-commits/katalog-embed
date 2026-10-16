#!/usr/bin/env python3
"""
BENTUK 3D (rev 32) -- dari deskriptor mesh resmi (mata3d.py, fisik3d/bentuk3d.json.gz) ke FITUR dan LABEL yang bisa dibaca.
fitur(): angka turunan (stud / persen), tidak menebak. baca(): label HANYA untuk fitur yang lolos uji pemisahan di
LAPORAN_3D.md (uji_bentuk3d.py: kata nama & gender pemakaian sebagai pembanding). Ambang ditulis bersama angka ujinya.
Sumbu: Y atas, depan -Z, |x| dari garis tengah. Pakaian layered dibuat di sekitar manekin acuan yang sama.
"""
import numpy as np

ATAS = {64, 65, 67, 68}
BAWAH = {66, 69, 72}
SEPATU = {70, 71}
# stud; sebaran 17 Okt (kerangka wajar): pinggul celana panjang bernama jelas p1 1,05 (n 778), versi berskala kecil 0,16-0,64;
# dada atasan bernama jelas p1 0,76 (atasan ketat ~0,73), mantel berskala kecil ~0,4
LEBAR_MIN_PINGGUL = 0.9
LEBAR_MIN_DADA = 0.7


def fitur(f, rk=None):
    """rk = fakta map (fisik3d/rangka.json): ro = letak manekin acuan (WrapLayer.ReferenceOrigin) di bingkai mesh ->
    KERANGKA BADAN: yb/yt = tinggi ujung bawah/atas pakaian terhadap pusat manekin (stud). Diukur 16 Okt pada 8.133 mesh:
    celana panjang berujung di -2,73 (mata kaki), atasan di +1,9 (bahu), pinggang celana +0,6. TIDAK semua kreator memakai
    titik asal manekin yang sama (cek lembar 17 Okt: hoodie asli terbaca ujung atas +0,85 / +3,8) -> baca() memakai kerangka
    hanya bila letaknya wajar."""
    if not isinstance(f, dict) or "prof" not in f:
        return {}
    pr = f["prof"]
    w = [p[0] / 100 for p in pr]
    d = [p[1] / 100 for p in pr]
    fr = [p[2] / 100 for p in pr]
    gap = [p[4] for p in pr]
    ada = [k for k in range(len(pr)) if pr[k][0] > 0]
    o = {"W": f["W"] / 100, "H": f["H"] / 100, "D": f["D"] / 100, "nv": f.get("nv", 0), "ntex": f.get("ntex", 0)}
    o["kakiCelah"] = float(np.mean(gap[0:4]))
    o["kakiCelahMax"] = float(max(gap[0:4]))
    top = [w[k] for k in (9, 10, 11) if w[k] > 0]
    o["flare"] = (np.mean([w[0], w[1]]) / max(1e-3, np.mean(top))) if top else None
    o["lebarBawah"] = w[0]
    for j, q in enumerate(("09", "11", "13")):
        fr_, lo_, hi_ = f["luar"][j]
        o["luar" + q] = fr_
        o["luar" + q + "Bawah"] = lo_ if lo_ >= 0 else 100
    ld = f.get("leher") or [-1, -1, -1]
    if ld[0] >= 0:
        o["leherDepan"] = ld[0] / 100       # turunnya garis leher depan dari puncak pakaian (stud)
    if ld[0] >= 0 and ld[2] >= 0:
        o["leherDalam"] = (ld[0] - ld[2]) / 100
    if ld[0] >= 0 and ld[1] >= 0:
        o["tudung"] = (ld[0] - ld[1]) / 100
    up = [fr[k] for k in (7, 8, 9) if pr[k][0] > 0]
    mid = [fr[k] for k in (3, 4, 5) if pr[k][0] > 0]
    if up and mid:
        o["dadaTonjol"] = max(up) - float(np.median(mid))
        o["dadaRasio"] = max(up) / max(1e-3, max(mid))
    o["tebalRata"] = float(np.mean([d[k] for k in ada])) if ada else None
    o["depanTerbuka"] = f.get("depanTerbuka", 0)
    # rev 32b: PENUTUP BADAN tanpa kerangka -- ada baris yang kainnya melintasi garis tengah (6 dari 24 kolom tengah,
    # depan+belakang). Kuku/sarung tangan/penghangat lengan/gelang = dua potong terpisah, pusatnya selalu kosong.
    o["pusatTertutup"] = any(p[0] > 0 and p[4] <= 2 for p in pr)
    ro = (rk or {}).get("ro") if isinstance(rk, dict) else None
    if isinstance(ro, list) and len(ro) == 3:
        ry = ro[1] / 100
        o["rx"] = abs(ro[0] / 100)        # pusat manekin jauh dari pusat mesh = barang satu sisi (pegangan tangan, satu kaki)
        o["yb"], o["yt"] = -o["H"] / 2 - ry, o["H"] / 2 - ry
        # tebal kain di garis tengah per tinggi badan: lebar baris pada ketinggian y (stud, kerangka badan) | None
        def lebar_di(y):
            k = int((y - o["yb"]) / o["H"] * 12) if o["H"] > 0 else -1
            return pr[k][0] / 100 if 0 <= k < 12 and pr[k][0] > 0 else None
        o["wLengan"] = lebar_di(1.55)                       # lebar setinggi lengan atas (badan saja ~0,9; berlengan >= 1,2)
        fr_, lo_, hi_ = f["luar"][0]
        o["yUjungLengan"] = (o["yb"] + lo_ / 100 * o["H"]) if lo_ >= 0 and fr_ > 0 else None
        pinggul = [pr[k][4] for k in range(12) if pr[k][0] >= 60 and -0.3 <= o["yb"] + (k + 0.5) / 12 * o["H"] <= 0.45]
        o["pinggulTertutup"] = bool(pinggul) and min(pinggul) <= 2

        def lebar_maks(lo, hi):
            ws = [pr[k][0] / 100 for k in range(12) if pr[k][0] > 0 and lo <= o["yb"] + (k + 0.5) / 12 * o["H"] <= hi]
            return max(ws) if ws else None
        o["wPinggul"] = lebar_maks(-0.3, 0.45)              # skala: pinggul celana asli selebar badan
        o["wDada"] = lebar_maks(0.9, 1.4)                   # skala: dada atasan asli selebar badan
    return o


def kerangka_wajar(o, t):
    """rev 32b: mesh berskala kecil (sebagian kreator membuat pakaian kecil yang dibesarkan sangkar manekinnya) membuat
    letak & ukuran mentah menyesatkan. Kerangka dianggap wajar hanya bila lebar pinggul (bawahan) / dada (atasan) setidaknya
    selebar badan manekin (ambang dari sebaran pakaian bernama jelas, LAPORAN_3D.md)."""
    if t in BAWAH:
        return (o.get("wPinggul") or 0) >= LEBAR_MIN_PINGGUL
    if t in ATAS:
        return (o.get("wDada") or 0) >= LEBAR_MIN_DADA
    return True


def baca(o, t):
    """label terbaca dari fitur; HANYA yang lolos uji (rev 32b, 17 Okt, 11.559 mesh; pembanding kata nama yang berisik,
    ukur ulang: python uji_bentuk3d.py -> LAPORAN_3D.md):
      BUKAN PENUTUP (bukanPenutup): barang bertipe baju/celana yang tidak menutup badan --
        atas: tak ada baris yang kainnya melintasi garis tengah, atau pusat manekin > 0,5 stud dari pusat mesh
              (kuku, sarung tangan, penghangat lengan, gelang, barang pegangan: 94% tertangkap; atasan asli salah 0,1%)
        bawah: dengan kerangka badan, tak ada kain di pinggul (-0,3..+0,45) DAN ujung atas di bawah -0,6 (sepatu, kaus kaki,
              penghangat kaki, gelang kaki: 89% tertangkap; bawahan asli salah 0,1%)
      KERANGKA BADAN dipakai hanya bila wajar: atasan ujung atas +1,25..+3,0; bawahan -1,0..+3,0 (sebagian kreator memakai
        titik asal manekin lain -> letak bergeser; tanpa syarat ini hoodie terbaca "di perut").
      bawahan  potong  kategori resmi Roblox (72 rok/gaun, 66 celana, 69 celana pendek); gaun = ujung atas >= +1,2.
               panjang ujung bawah <= -2,2 panjang, <= -0,9 selutut/sedang, selain itu pendek; tanpa kerangka dari tinggi.
               melebar ke bawah: rok/gaun dengan lebar bawah >= 1,4x lebar pinggang
      atasan   lengan  (hanya kerangka wajar) panjang = kain di luar badan (|x| > 0,9) turun sampai <= +0,6; tanpa = lebar
                       setinggi lengan atas (+1,55) < 1,2 stud atau tak ada kain di sana; selain itu pendek.
      Ketepatan saat MENGKLAIM (17 Okt, nama sebagai pembanding berisik): lengan panjang 93%, pendek 74%, tanpa 82%;
      celana panjang 93%, celana pendek 71%; potong dari tipe resmi 98-99%. Sisanya TIDAK diklaim (kerangka tak wajar).
      sepatu   bot bila tinggi >= 0,65 stud
      atasan   (rev 32c, hanya kerangka wajar) crop / bahu terbuka / leher rendah -- ambang & uji di badan fungsi.
    Belum lolos uji (TIDAK diklaim): tudung, jaket terbuka, tebal/puffer, bentuk dada."""
    out = {}
    if not o:
        return out
    yb, yt = o.get("yb"), o.get("yt")
    if t in ATAS:
        if not o.get("pusatTertutup", True) or (o.get("rx") or 0) > 0.5:
            out["bukanPenutup"] = True
            return out
    if t in BAWAH and yt is not None and not o.get("pinggulTertutup", True) and yt < -0.6:
        out["bukanPenutup"] = True
        out["ukurBadan"] = True
        return out
    if t in BAWAH:
        # potongan: KATEGORI RESMI Roblox (72 DressSkirt, 66 Pants, 69 Shorts -- fakta katalog, bukan tebakan; kata nama
        # "skirt/dress" 97% bertipe 72, "pants/jeans" 96% bertipe 66)
        rok = t == 72
        out["potong"] = "rok" if rok else "celana"
        # PANJANG hanya dengan kerangka badan yang wajar (rev 32b: tanpa kerangka / kerangka bergeser / mesh berskala kecil =
        # TIDAK diklaim; dulu dari tinggi mesh mentah -> joggers berskala kecil terbaca "selutut")
        if yb is not None and -1.0 <= yt <= 3.0 and kerangka_wajar(o, t):
            # ujung bawah <= -2,2 = sampai mata kaki (celana panjang 93% tepat), <= -0,9 = sekitar lutut, selain itu pendek
            out["panjang"] = "panjang" if yb <= -2.2 else (("sedang" if rok else "selutut") if yb <= -0.9 else "pendek")
            out["ukurBadan"] = True
            if rok and yt >= 1.2:
                out["potong"] = "gaun"      # menutup badan atas (nama gaun 97%, nama rok 91% tepat)
        if rok and (o.get("flare") or 0) >= 1.4:
            out["mengembang"] = True        # rasio lebar bawah/pinggang -- tak bergantung skala
    elif t in ATAS:
        # LENGAN hanya dengan kerangka badan yang wajar (ujung atas di bahu); tanpa itu TIDAK diklaim (rev 32b: mantel
        # berskala kecil dulu terbaca "tanpa lengan" dari lebar mentah)
        if yt is not None and 1.25 <= yt <= 3.0 and kerangka_wajar(o, t):
            yl, wl = o.get("yUjungLengan"), o.get("wLengan")
            if yl is not None and yl <= 0.6:
                out["lengan"] = "panjang"
            elif (wl is None and yt < 1.55) or (wl is not None and wl < 1.2):
                out["lengan"] = "tanpa"
            else:
                out["lengan"] = "pendek"
            out["ukurBadan"] = True
            # rev 32c: BAGIAN BADAN YANG TERBUKA (pembeda gender yang terlihat), diuji 17 Okt pada 897 atasan bergender
            # (nama / pemakaian): perut terbuka = ujung bawah >= +0,8 (di atas pinggang celana +0,6): 92 cewek, 0 cowok;
            # bahu terbuka = ujung atas < +1,5 (bahu +1,9), depan tidak terbuka, lebar < 3,5: 46 cewek, 0 cowok;
            # leher rendah = garis leher depan turun >= 0,4 stud, depan tidak terbuka (< 10%): 25 cewek, 0 cowok.
            dT = o.get("depanTerbuka", 0)
            if yb is not None and yb >= 0.8:
                out["crop"] = True
            if yt < 1.5 and dT < 30 and o["W"] < 3.5:
                out["bahuTerbuka"] = True
            if (o.get("leherDepan") or 0) >= 0.4 and dT < 10:
                out["leherRendah"] = True
    elif t in SEPATU:
        out["tinggi"] = "bot" if o["H"] >= 0.65 else "rendah"
    return out
