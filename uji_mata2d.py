#!/usr/bin/env python3
"""
UJI MATA 2D -- membandingkan cara MEMBACA baju/celana/kaos klasik 2D sebelum dipakai di kartu (bukan bagian pipeline).

Masalah: kartu fase 1 membaca 2D dari thumbnail 150 px (manekin kotak) -> jenis/pola/tema 2D paling lemah.
Varian pada sampel acak tetap (seed) yang SAMA, semua dinilai nanti dengan LABEL EMAS manual (bukan nama):
  b32_150     : embedding lama (cache otak.py, thumbnail 150 px utuh) + kalimat manekin   -- garis dasar kartu fase 1
  b32_k150    : potongan pakaian lama (cache emb2d, 150 px)                               -- dipakai kartu untuk jenis/pola
  b32_utuh    : CLIP B/32, thumbnail 420 px utuh
  b32_kain    : CLIP B/32, 420 px, manekin & latar dibuang -> potongan pakaian saja
  fc_kain     : FashionCLIP (patrickjohncyh/fashion-clip), potongan pakaian 420
  l14_kain    : CLIP ViT-L/14 (openai/clip-vit-large-patch14), potongan pakaian 420
  probe_150   : regresi softmax di atas embedding lama, dilatih dari NAMA puluhan ribu item lain (pengawasan lemah;
                sampel uji dikeluarkan dari latihan). Murah: tidak perlu unduh gambar baru bila menang.
Keluaran (uji2d/): logit.npz (logit tiap varian/facet), prediksi.json (top-3), lembar_*.png (potongan 420 untuk label emas).
"""
import os, sys, io, json, random, time
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kartu_item as KI

H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
N_PER = int(os.environ.get("N_PER", "60"))   # per tipe aset (Shirt, Pants, TShirt)
MODEL = {"b32": "openai/clip-vit-base-patch32", "fc": "patrickjohncyh/fashion-clip", "l14": "openai/clip-vit-large-patch14"}
KAL_KAIN = ["a photo of {d} {n}", "{d} {n}, product photo on white background", "a {n}: {d}"]
NOUN = {11: "shirt", 12: "pants", 2: "t-shirt graphic"}
KEL = {11: "atas", 12: "bawah", 2: "atas"}
# kata nama untuk pengawasan lemah 2D: "shirt" ada di hampir semua nama aset Shirt -> bukan bukti kaos
KATA_2D = {("atas", "kaos"): ["tee", "t-shirt", "tshirt", "kaos"]}


def manekin(rgb):
    """sama dengan otak.py w2_manekin: manekin abu katalog #abaca7 (r~g, b 1-5% lebih rendah)"""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    gs = np.maximum(g, 1e-6)
    rg, bg = r / gs, b / gs
    return (g >= 60) & (g <= 240) & (rg >= 0.98) & (rg <= 1.015) & (bg >= 0.95) & (bg <= 0.99)


def potong_kain(im):
    """RGBA 420 -> (utuh di latar putih, potongan pakaian saja persegi 224 atau None)"""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] > 128
    alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
    alas.alpha_composite(im.convert("RGBA"))
    utuh = alas.convert("RGB")
    kain = al & ~manekin(rgb)
    if kain.sum() < 400:
        return utuh, None
    ys, xs = np.where(kain)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    kanvas = np.full(rgb.shape, 255, dtype=np.uint8)
    kanvas[kain] = rgb[kain].astype(np.uint8)
    pot = kanvas[y0:y1, x0:x1]
    h, w = pot.shape[:2]
    s = max(h, w) + 8
    kotak = np.full((s, s, 3), 255, dtype=np.uint8)
    kotak[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = pot
    return utuh, Image.fromarray(kotak).resize((224, 224), Image.BICUBIC)


def thumb(ids, ukuran="420x420"):
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
                        b = requests.get(e["imageUrl"], headers=H, timeout=30).content
                        out[int(e["targetId"])] = Image.open(io.BytesIO(b)).convert("RGBA")
                break
            except Exception as ex:
                print("thumbnail gagal:", ex, flush=True)
                time.sleep(3)
        time.sleep(0.4)
    return out


class Model:
    def __init__(self, mid):
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self.torch = torch
        self.m = CLIPModel.from_pretrained(mid).eval()
        self.p = CLIPProcessor.from_pretrained(mid)

    def gambar(self, ims):
        out = []
        with self.torch.no_grad():
            for i in range(0, len(ims), 16):
                f = self.m.get_image_features(**self.p(images=ims[i:i + 16], return_tensors="pt"))
                f = f / f.norm(dim=-1, keepdim=True)
                out.append(f.cpu().numpy().astype("float32"))
        return np.concatenate(out)

    def teks(self, kal):
        with self.torch.no_grad():
            f = self.m.get_text_features(**self.p(text=kal, return_tensors="pt", padding=True))
            f = f / f.norm(dim=-1, keepdim=True)
        return f.cpu().numpy().astype("float32")


def mat_label(model, labels, noun, kal):
    out = []
    for lab in labels:
        v = model.teks([t.format(d=d, n=noun) for d in lab[1] for t in kal]).mean(axis=0)
        out.append(v / np.linalg.norm(v))
    return np.stack(out)


def top3(L):
    return np.argsort(-L, axis=1)[:, :3].tolist()


def kata(kel, lab):
    return KATA_2D.get((kel, lab[0]), lab[2])


def label_nama(labels, kel, nama_l, tok):
    hit = [j for j, lab in enumerate(labels) if kata(kel, lab) and KI.ada_kata(nama_l, tok, kata(kel, lab))]
    return hit[0] if len(hit) == 1 else None


def latih_probe(X, y, ncls, iters=400, lr=0.05, l2=1e-4):
    """regresi softmax seimbang kelas (Adam, numpy). X (N,D) ternormalisasi, y (N,) -> W (D+1, C)"""
    N, D = X.shape
    Xb = np.hstack([X * 10.0, np.ones((N, 1), dtype=np.float32)])
    cnt = np.bincount(y, minlength=ncls).astype(np.float32)
    wk = np.where(cnt > 0, 1.0 / np.sqrt(np.maximum(cnt, 1)), 0.0)
    ws = wk[y]
    ws = ws / ws.sum()
    W = np.zeros((D + 1, ncls), dtype=np.float32)
    m = np.zeros_like(W)
    v = np.zeros_like(W)
    Y = np.zeros((N, ncls), dtype=np.float32)
    Y[np.arange(N), y] = 1
    for t in range(1, iters + 1):
        Z = Xb @ W
        Z -= Z.max(axis=1, keepdims=True)
        P = np.exp(Z)
        P /= P.sum(axis=1, keepdims=True)
        G = Xb.T @ ((P - Y) * ws[:, None]) + l2 * W
        m = 0.9 * m + 0.1 * G
        v = 0.999 * v + 0.001 * G * G
        W -= lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
    return W


def pakai_probe(W, X):
    return np.hstack([X * 10.0, np.ones((X.shape[0], 1), dtype=np.float32)]) @ W


def main():
    rng = random.Random(20261016)
    ids_all, E, e2, meta = KI.muat()
    emb_ids = ids_all.tolist()
    pos = {int(i): k for k, i in enumerate(emb_ids)}
    sampel = []
    for t in (11, 12, 2):
        calon = sorted(i for i in emb_ids if int((meta.get(str(i)) or {}).get("t") or 0) == t)
        sampel += [(i, t) for i in rng.sample(calon, min(N_PER, len(calon)))]
    ids = [i for i, _ in sampel]
    gb = thumb(ids)
    print("thumbnail 420:", len(gb), "dari", len(ids), flush=True)
    utuh, kain, ok = {}, {}, []
    for i, t in sampel:
        if i in gb:
            u, k = potong_kain(gb[i])
            utuh[i] = u
            kain[i] = k if k is not None else u.resize((224, 224))
            ok.append((i, t))
    os.makedirs("uji2d", exist_ok=True)
    per_t = {t: [i for i, tt in ok if tt == t] for t in (11, 12, 2)}
    hasil = {"item": [{"id": i, "t": t, "n": (meta.get(str(i)) or {}).get("n", "")} for i, t in ok], "varian": {}}
    logit = {f"ids|{t}": np.array(per_t[t], dtype=np.int64) for t in per_t}
    FACET = {"jenis": None, "pola": KI.POLA, "tema": KI.TEMA}

    def catat(nama, t, fnm, labels, L):
        logit[f"{nama}|{t}|{fnm}"] = L.astype(np.float32)
        for i, p in zip(per_t[t], top3(L)):
            hasil["varian"].setdefault(nama, {}).setdefault(str(i), {})[fnm] = [labels[j][0] for j in p]

    def emb_lama(i, crop):
        if crop and i in e2:
            return e2[i]
        return E[pos[i]]

    varian = [("b32_150", "b32", "lama"), ("b32_k150", "b32", "lama_kain"), ("b32_utuh", "b32", "utuh"),
              ("b32_kain", "b32", "kain"), ("fc_kain", "fc", "kain"), ("l14_kain", "l14", "kain")]
    cache_model = {}
    for nama, mk, sumber in varian:
        try:
            if mk not in cache_model:
                t0 = time.time()
                cache_model[mk] = Model(MODEL[mk])
                print(f"model {mk} dimuat {time.time() - t0:.0f} dtk", flush=True)
            M = cache_model[mk]
            for t in (11, 12, 2):
                sub = per_t[t]
                if not sub:
                    continue
                if sumber == "lama":
                    X, kal = np.stack([emb_lama(i, False) for i in sub]), KI.KALIMAT_2D
                elif sumber == "lama_kain":
                    X, kal = np.stack([emb_lama(i, True) for i in sub]), KAL_KAIN
                elif sumber == "utuh":
                    X, kal = M.gambar([utuh[i] for i in sub]), KI.KALIMAT_2D
                else:
                    X, kal = M.gambar([kain[i] for i in sub]), KAL_KAIN
                logit[f"X|{nama}|{t}"] = X
                for fnm, labels in FACET.items():
                    labels = labels or KI.JENIS[KEL[t]]
                    T = mat_label(M, labels, NOUN[t], kal)
                    catat(nama, t, fnm, labels, 100.0 * (X @ T.T))
            print("varian selesai:", nama, flush=True)
        except Exception as ex:
            print("varian gagal:", nama, repr(ex), flush=True)

    # PROBE pengawasan lemah dari nama (embedding lama, seluruh korpus 2D sejenis kecuali sampel)
    uji = set(ids)
    for crop, nama in ((False, "probe_150"), (True, "probe_k150")):
        try:
            for t in (11, 12, 2):
                kel = KEL[t]
                tt = (11, 2) if t in (11, 2) else (12,)
                latih = [i for i in emb_ids if int((meta.get(str(i)) or {}).get("t") or 0) in tt and i not in uji]
                for fnm, labels in FACET.items():
                    labels = labels or KI.JENIS[kel]
                    Xs, ys = [], []
                    for i in latih:
                        nm = (meta.get(str(i)) or {}).get("n") or ""
                        j = label_nama(labels, kel, nm.lower(), KI.token(nm))
                        if j is not None:
                            Xs.append(emb_lama(i, crop))
                            ys.append(j)
                    ys = np.array(ys, dtype=np.int64)
                    cnt = np.bincount(ys, minlength=len(labels)) if len(ys) else np.zeros(len(labels), int)
                    if len(ys) < 200:
                        print(f"probe {nama} {t}/{fnm}: data latih kurang ({len(ys)})", flush=True)
                        continue
                    W = latih_probe(np.stack(Xs).astype(np.float32), ys, len(labels))
                    L = pakai_probe(W, np.stack([emb_lama(i, crop) for i in per_t[t]]).astype(np.float32))
                    L[:, cnt < 15] = -1e4      # label tanpa contoh cukup tidak bisa diprediksi probe
                    catat(nama, t, fnm, labels, L)
                    logit[f"cnt|{nama}|{t}|{fnm}"] = cnt
                    print(f"probe {nama} {t}/{fnm}: latih {len(ys)}, label aktif {(cnt >= 15).sum()}/{len(labels)}", flush=True)
        except Exception as ex:
            print("probe gagal:", nama, repr(ex), flush=True)

    json.dump(hasil, open("uji2d/prediksi.json", "w", encoding="utf-8"), ensure_ascii=False)
    np.savez_compressed("uji2d/logit.npz", **logit)
    try:
        font = ImageFont.load_default(size=12)
    except TypeError:
        font = ImageFont.load_default()
    for t, nm in ((11, "baju"), (12, "celana"), (2, "kaos")):
        sub = per_t[t]
        kol, sel = 6, 220
        bar = (len(sub) + kol - 1) // kol
        kanvas = Image.new("RGB", (kol * sel, 24 + bar * (sel + 30)), (240, 240, 240))
        dr = ImageDraw.Draw(kanvas)
        dr.text((6, 5), f"Uji 2D {nm}: potongan pakaian 420 (besar) + thumbnail utuh (kecil kiri-atas). Nomor = urutan ids|{t}.",
                fill=(0, 0, 0), font=font)
        for k, i in enumerate(sub):
            x, y = (k % kol) * sel, 24 + (k // kol) * (sel + 30)
            kanvas.paste(kain[i].resize((sel - 20, sel - 20)), (x + 10, y))
            kanvas.paste(utuh[i].resize((80, 80)), (x + 10, y))
            dr.text((x + 6, y + sel - 16), f"#{k + 1} {(meta.get(str(i)) or {}).get('n', '')[:30]}", fill=(20, 20, 160), font=font)
        kanvas.save(f"uji2d/lembar_{nm}.png", optimize=True)
    print("selesai", flush=True)


if __name__ == "__main__":
    main()
