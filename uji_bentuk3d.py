#!/usr/bin/env python3
"""
UJI BENTUK 3D (rev 32) -- apakah ukuran dari mesh resmi (fisik3d/bentuk3d.json.gz) benar-benar memisahkan jenis potongan?
Label pembanding (lemah, hanya untuk MENGUJI, bukan memutuskan): kata di nama item (shorts vs pants, skirt, long sleeve vs
tank, crop, puffer, off shoulder) dan gender pemakaian dari kartu (kolom gender, >= 4 outfit). Keluaran: LAPORAN_3D.md
(median per label + AUC tiap fitur). Fitur yang AUC-nya rendah tidak boleh dipakai map.
"""
import gzip, json, re, sys
import numpy as np

sys.path.insert(0, ".")
import bentuk3d as B3


def auc(pos, neg):
    """peluang nilai acak kelompok pos > kelompok neg (0,5 = tak memisahkan)"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) < 5 or len(neg) < 5:
        return None
    x = np.concatenate([pos, neg])
    r = x.argsort().argsort().astype(float) + 1
    # rata-rata peringkat untuk nilai kembar
    _, inv, cnt = np.unique(x, return_inverse=True, return_counts=True)
    jum = np.bincount(inv, weights=r)
    r = (jum / cnt)[inv]
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


KATA = {
    "celana_panjang": r"\b(pants|jeans|trousers|cargo|joggers?|sweatpants|slacks|flare[sd]?|baggy|leggings?)\b",
    "celana_pendek": r"\b(shorts|trunks|bermuda)\b",
    "rok": r"\b(skirt|skort)\b",
    "gaun": r"\b(dress|gown)\b",
    "lengan_panjang": r"\b(long ?sleeves?|hoodie|sweater|cardigan|jacket|coat|blazer|turtleneck)\b",
    "lengan_pendek": r"\b(short ?sleeves?|tee|t-shirt|tshirt|polo)\b",
    "tanpa_lengan": r"\b(tank|sleeveless|tube|cami|camisole|halter|strapless|bandeau|corset)\b",
    "crop": r"\bcrop(ped)?\b",
    "puffer": r"\b(puffer|puffy|down jacket|bomber)\b",
    "oversized": r"\b(oversized?|baggy)\b",
    "bahu_terbuka": r"\b(off[- ]?shoulders?|strapless|tube)\b",
}


def main():
    import mata3d
    H3 = mata3d.muat_hasil()
    RK = mata3d.muat_rangka()
    with gzip.open("data/panen.json.gz", "rt", encoding="utf-8") as f:
        meta = json.load(f).get("meta", {})
    kartu = {}
    for s in range(8):
        try:
            kartu.update(json.load(open(f"kartu/kartu_{s}.json"))["d"])
        except Exception:
            pass
    rows = []
    for i, f in H3.items():
        if not isinstance(f, dict) or "prof" not in f:
            continue
        nm = ((meta.get(i) or {}).get("n") or "").lower()
        fit = B3.fitur(f, RK.get(i))
        lab = {k for k, rx in KATA.items() if re.search(rx, nm)}
        b = kartu.get(i)
        g = None
        if b and len(b) > 20 and b[19] >= 0 and b[20] >= 4:
            g = (b[19] - 100) / 100
        rows.append((i, int(f.get("t", 0)), nm, fit, lab, g))
    out = [f"# Uji bentuk 3D (mesh resmi) — {len(rows)} item diukur", ""]
    kelompok = {"bawah (66 celana, 69 shorts, 72 rok/gaun)": {66, 69, 72},
                "atas (64 kaos, 65 kemeja, 67 jaket, 68 sweater)": {64, 65, 67, 68}}
    uji = {
        "bawah": [("celana_panjang", "celana_pendek"), ("celana_panjang", "rok"), ("celana_pendek", "rok"), ("gaun", "rok")],
        "atas": [("lengan_panjang", "tanpa_lengan"), ("lengan_panjang", "lengan_pendek"), ("lengan_pendek", "tanpa_lengan"),
                 ("crop", None), ("puffer", None), ("oversized", None), ("bahu_terbuka", None)],
    }
    for judul, tipe in kelompok.items():
        R = [r for r in rows if r[1] in tipe]
        k = "bawah" if "bawah" in judul else "atas"
        out += [f"## {judul}: {len(R)} item", ""]
        nama_fitur = sorted({n for r in R for n in r[3]})
        for a, b in uji[k]:
            A = [r for r in R if a in r[4]]
            Bk = [r for r in R if (b in r[4] if b else a not in r[4])]
            out.append(f"### {a} (n={len(A)}) vs {b or 'lainnya'} (n={len(Bk)})")
            out.append("| fitur | median " + a + " | median " + (b or "lain") + " | AUC |")
            out.append("|---|---|---|---|")
            for nf in nama_fitur:
                pa = [r[3][nf] for r in A if r[3].get(nf) is not None]
                pb = [r[3][nf] for r in Bk if r[3].get(nf) is not None]
                u = auc(pa, pb)
                if u is None:
                    continue
                out.append(f"| {nf} | {np.median(pa):.2f} | {np.median(pb):.2f} | {u:.2f} |")
            out.append("")
        # gender pemakaian
        A = [r for r in R if r[5] is not None and r[5] >= 0.25]
        Bk = [r for r in R if r[5] is not None and r[5] <= -0.25]
        out.append(f"### dipakai cewek (n={len(A)}) vs dipakai cowok (n={len(Bk)}) — gender dari pemakaian, bukan nama")
        out.append("| fitur | median cewek | median cowok | AUC |")
        out.append("|---|---|---|---|")
        for nf in nama_fitur:
            pa = [r[3][nf] for r in A if r[3].get(nf) is not None]
            pb = [r[3][nf] for r in Bk if r[3].get(nf) is not None]
            u = auc(pa, pb)
            if u is not None:
                out.append(f"| {nf} | {np.median(pa):.2f} | {np.median(pb):.2f} | {u:.2f} |")
        out.append("")
        # label hasil baca (bentuk3d.baca) vs kata nama
        out.append("### Hasil baca (bentuk3d.baca) per kata nama")
        hit = {}
        for r in R:
            lb = B3.baca(r[3], r[1])
            for kk in r[4]:
                for kl, v in lb.items():
                    hit.setdefault((kk, kl), {}).setdefault(str(v), 0)
                    hit[(kk, kl)][str(v)] += 1
        for (kk, kl), d in sorted(hit.items()):
            if sum(d.values()) >= 5:
                out.append(f"- {kk} → {kl}: " + ", ".join(f"{v} {n}" for v, n in sorted(d.items(), key=lambda x: -x[1])))
        out.append("")
    open("LAPORAN_3D.md", "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out[:400]))


if __name__ == "__main__":
    main()
