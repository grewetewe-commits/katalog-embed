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


def fitur(f, rk=None):
    """rk = fakta map (fisik3d/rangka.json): ro = letak manekin acuan (WrapLayer.ReferenceOrigin) di bingkai mesh ->
    KERANGKA BADAN: yb/yt = tinggi ujung bawah/atas pakaian terhadap pusat manekin (stud). Diukur 16 Okt pada 8.133 mesh:
    celana panjang berujung di -2,73 (mata kaki), atasan di +1,9 (bahu), pinggang celana +0,6 -> kerangka konsisten."""
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
    ro = (rk or {}).get("ro") if isinstance(rk, dict) else None
    if isinstance(ro, list) and len(ro) == 3:
        ry = ro[1] / 100
        o["yb"], o["yt"] = -o["H"] / 2 - ry, o["H"] / 2 - ry
    return o


def baca(o, t):
    """label terbaca dari fitur; HANYA yang lolos uji 16 Okt (4.044 mesh, pembanding kata nama yang berisik):
      bawahan  potong  kategori resmi Roblox (72 rok/gaun, 66 celana, 69 celana pendek); gaun bila menutup badan atas
                       (ujung atas >= +1,2 stud di kerangka badan). Tanpa tipe: tebal >= 0,95 & dua kaki tidak terpisah.
               panjang celana: < 1,7 stud pendek, < 2,6 selutut, sisanya panjang (celana panjang 78%, pendek 68% tepat)
                       rok/gaun: < 1,35 pendek, < 2,9 sedang, sisanya panjang
               melebar ke bawah: rok/gaun dengan lebar bawah >= 1,4x lebar pinggang (ukuran langsung)
      atasan   lengan  tanpa = tak ada kain di luar badan & lebar < 1,5; panjang = kain di luar badan sampai 20% terbawah
                       & lebar >= 2,3; selain itu pendek (benar: panjang 85%, pendek 69%, tanpa 90%)
      sepatu   bot bila tinggi >= 0,65 stud (bot median 0,78 vs sneaker 0,37; n kecil 11/24)
    Belum lolos uji (TIDAK diklaim): crop, bahu terbuka, tudung, jaket terbuka, tebal/puffer, bentuk dada -- mesh resmi
    dipusatkan tanpa badan, jadi letak terhadap badan belum diketahui."""
    out = {}
    if not o:
        return out
    if t in BAWAH:
        h = o["H"]
        if t not in (66, 69, 72) and h < 1.0 and 0.85 <= o["D"] < 0.95 and o["kakiCelahMax"] == 0:
            # sangat pendek & tebal tanggung: rok mini ketat dan celana pendek tak terbedakan -> tidak mengklaim potongan
            out["panjang"] = "pendek"
            return out
        # potongan: KATEGORI RESMI Roblox dulu (72 DressSkirt, 66 Pants, 69 Shorts -- fakta katalog, bukan tebakan; kata nama
        # "skirt/dress" 97% bertipe 72, "pants/jeans" 96% bertipe 66). Geometri (tebal & celah kaki) hanya bila tipe tak tersedia.
        if t == 72:
            rok = True
        elif t in (66, 69):
            rok = False
        else:
            rok = o["D"] >= 0.95 and o["kakiCelah"] < 1.5 and not (h >= 2.6 and o["kakiCelahMax"] >= 1)
        out["potong"] = "rok" if rok else "celana"
        yb, yt = o.get("yb"), o.get("yt")
        if yb is not None:
            # KERANGKA BADAN (uji 16 Okt, kata nama sebagai pembanding): ujung bawah <= -2,2 = sampai mata kaki
            # (celana panjang 93% tepat, maxi 79%), <= -0,9 = sekitar lutut, selain itu pendek (mini 93%, celana pendek 70%)
            out["panjang"] = "panjang" if yb <= -2.2 else (("sedang" if rok else "selutut") if yb <= -0.9 else "pendek")
            out["ukurBadan"] = True
            if rok and yt is not None and yt >= 1.2:
                out["potong"] = "gaun"      # menutup badan atas (gaun 96%, rok 90% tepat)
        elif rok:
            out["panjang"] = "pendek" if h < 1.35 else ("sedang" if h < 2.9 else "panjang")
        else:
            out["panjang"] = "pendek" if h < 1.7 else ("selutut" if h < 2.6 else "panjang")
        if rok and (o.get("flare") or 0) >= 1.4:
            out["mengembang"] = True
    elif t in ATAS:
        if o["luar09"] <= 1 and o["W"] < 1.5:
            out["lengan"] = "tanpa"
        elif o["luar09Bawah"] <= 20 and o["W"] >= 2.3:
            out["lengan"] = "panjang"
        else:
            out["lengan"] = "pendek"
    elif t in SEPATU:
        out["tinggi"] = "bot" if o["H"] >= 0.65 else "rendah"
    return out
