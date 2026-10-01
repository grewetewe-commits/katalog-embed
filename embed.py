#!/usr/bin/env python3
"""
Katalog Praktis -- "sidik jari visual" item avatar (dijalankan GitHub Actions, GRATIS di repo publik).

Langkah:
  1. Baca items.json (ID item per slot, hasil ekspor dari Studio).
  2. Unduh thumbnail tiap item dari API thumbnails.roblox.com (/v1/assets, terdokumentasi resmi).
  3. Hitung embedding gambar dengan CLIP (openai/clip-vit-base-patch32) -> vektor 512 angka per item.
  4. Zero-shot: tag gaya (gothic, kawaii, ...) dan atribut (sayap, tanduk, ...) dari kecocokan gambar-teks.
  5. Hilangkan "pengaruh jenis slot" (kurangi rata-rata tiap slot) lalu PCA ke 32 dimensi dan kuantisasi int8
     -> file kecil yang bisa diunduh server Roblox lewat HttpService dan dibaca sebagai matematika biasa.

Hasil (folder out/): embeddings.json, tags.json, info.json, tetangga_contoh.txt, raw.npz, gagal.json
Variabel lingkungan: BATAS (0 = semua item, N = uji N item acak), STUB=1 (uji tanpa jaringan/model, hanya untuk tes).

Skrip ini dapat dilanjutkan: item yang sudah ada di out/raw.npz tidak dihitung ulang.
"""
import hashlib
import io
import json
import math
import os
import random
import sys
import time
from datetime import datetime, timezone

import numpy as np
from PIL import Image

SUMBER = "items.json"
OUT = "out"
BATAS = int(os.environ.get("BATAS", "0") or 0)
STUB = os.environ.get("STUB") == "1"
BATCH_THUMB = 50
BATCH_MODEL = 32
DIM_AKHIR = 32
MODEL_ID = "openai/clip-vit-base-patch32"
HEADERS = {"User-Agent": "KatalogPraktis-embed/1.0 (GitHub Actions)"}
AMBANG_PLACEHOLDER = 4  # gambar yang byte-nya identik untuk >= N item berbeda dianggap placeholder (bukan gambar item)

# ---- tag zero-shot (deskripsi bahasa Inggris karena CLIP dilatih terutama dengan teks Inggris) ----
GAYA = {
    "gothic": "a gothic dark black lace style avatar item",
    "kawaii": "a cute kawaii pastel pink style avatar item",
    "royal": "a royal elegant gold and white noble style avatar item",
    "angel": "an angelic heavenly white halo and wings style avatar item",
    "demon": "a demonic dark red horns and tail style avatar item",
    "streetwear": "a streetwear hoodie and sneakers style avatar item",
    "punk": "a punk grunge chains and spikes style avatar item",
    "cyber": "a cyberpunk neon futuristic tech style avatar item",
    "fantasy": "a fantasy medieval armor or magical style avatar item",
    "military": "a military tactical camouflage style avatar item",
    "vintage": "a vintage retro old fashioned style avatar item",
    "sporty": "a sporty athletic style avatar item",
    "casual": "a plain casual everyday style avatar item",
    "y2k": "a y2k 2000s glittery pink style avatar item",
    "horror": "a horror scary bloody creepy style avatar item",
    "elegant": "a formal elegant suit or dress style avatar item",
}
ATRIBUT = {
    "sayap": ("an avatar item with wings", "an avatar item without wings"),
    "tanduk": ("an avatar item with horns", "an avatar item without horns"),
    "ekor": ("an avatar item with a tail", "an avatar item without a tail"),
    "halo": ("an avatar item with a halo", "an avatar item without a halo"),
    "jubah": ("an avatar item with a cape or cloak", "an avatar item without a cape"),
    "rantai": ("an avatar item with chains", "an avatar item without chains"),
    "kacamata": ("an avatar item with glasses", "an avatar item without glasses"),
    "telinga_hewan": ("an avatar item with animal ears", "an avatar item without animal ears"),
    "mahkota": ("an avatar item with a crown or tiara", "an avatar item without a crown"),
}


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------------------
# Daftar item
# ---------------------------------------------------------------------------
def muat_items():
    d = json.load(open(SUMBER, encoding="utf-8"))
    daftar = []
    for slot, ids in d["slot"].items():
        for i in ids:
            daftar.append((int(i), slot))
    daftar.sort(key=lambda x: (x[1], x[0]))
    return daftar


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------
def _get_json(url, params, coba=5):
    import requests
    for k in range(coba):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(60, 3 * (2 ** k)))
                continue
            log("  HTTP", r.status_code, "dari", url)
            return None
        except Exception as e:  # jaringan putus dsb
            time.sleep(2 ** k)
    return None


def _unduh_gambar(url):
    import requests
    for k in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200 and r.content:
                im = Image.open(io.BytesIO(r.content)).convert("RGBA")
                alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
                alas.alpha_composite(im)
                return alas.convert("RGB"), hashlib.md5(r.content).hexdigest()
        except Exception:
            pass
        time.sleep(1.5 * (k + 1))
    return None, None


def ambil_thumbnail(ids):
    """Mengembalikan {id: (PIL.Image, md5)} untuk id yang berhasil."""
    if STUB:
        hasil = {}
        for i in ids:
            rng = random.Random(i)
            warna = (rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
            hasil[i] = (Image.new("RGB", (150, 150), warna), hashlib.md5(str(i).encode()).hexdigest())
        return hasil
    hasil = {}
    sisa = list(ids)
    for putaran in range(4):
        if not sisa:
            break
        belum = []
        for a in range(0, len(sisa), BATCH_THUMB):
            potong = sisa[a:a + BATCH_THUMB]
            js = _get_json("https://thumbnails.roblox.com/v1/assets", {
                "assetIds": ",".join(str(x) for x in potong),
                "returnPolicy": "PlaceHolder",
                "size": "150x150",
                "format": "Png",
                "isCircular": "false",
            })
            time.sleep(0.6)
            if not js or "data" not in js:
                belum.extend(potong)
                continue
            dilihat = set()
            for e in js["data"]:
                tid = e.get("targetId")
                dilihat.add(tid)
                if e.get("state") == "Completed" and e.get("imageUrl"):
                    im, h = _unduh_gambar(e["imageUrl"])
                    if im is not None:
                        hasil[tid] = (im, h)
                    else:
                        belum.append(tid)
                elif e.get("state") in ("Pending", "TemporarilyUnavailable"):
                    belum.append(tid)
                # state lain (Error, Blocked, InReview): dilewati, dicatat sebagai gagal
            for x in potong:
                if x not in dilihat:
                    belum.append(x)
        sisa = belum
        if sisa and putaran < 3:
            log(f"  {len(sisa)} thumbnail belum siap, tunggu lalu coba lagi (putaran {putaran + 1})")
            time.sleep(8)
    return hasil


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class EmbedderStub:
    """Hanya untuk uji alur tanpa model: vektor acak deterministik per input."""
    dim = 512

    def gambar(self, daftar_pil):
        out = []
        for im in daftar_pil:
            rng = np.random.default_rng(int.from_bytes(hashlib.md5(im.tobytes()).digest()[:4], "little"))
            v = rng.normal(size=self.dim)
            out.append(v / np.linalg.norm(v))
        return np.array(out, dtype="float32")

    def teks(self, daftar_teks):
        out = []
        for t in daftar_teks:
            rng = np.random.default_rng(int.from_bytes(hashlib.md5(t.encode()).digest()[:4], "little"))
            v = rng.normal(size=self.dim)
            out.append(v / np.linalg.norm(v))
        return np.array(out, dtype="float32")


class EmbedderCLIP:
    def __init__(self):
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self.torch = torch
        self.model = CLIPModel.from_pretrained(MODEL_ID).eval()
        self.proc = CLIPProcessor.from_pretrained(MODEL_ID)

    @staticmethod
    def _tensor(x):
        # kompatibel lintas versi transformers: ada yang mengembalikan tensor, ada yang objek dengan field
        for nama in ("image_embeds", "text_embeds", "pooler_output"):
            v = getattr(x, nama, None)
            if v is not None:
                return v
        return x

    def _norm(self, f):
        f = f / f.norm(dim=-1, keepdim=True)
        return f.cpu().numpy().astype("float32")

    def gambar(self, daftar_pil):
        with self.torch.no_grad():
            inp = self.proc(images=daftar_pil, return_tensors="pt")
            f = self._tensor(self.model.get_image_features(**inp))
        return self._norm(f)

    def teks(self, daftar_teks):
        with self.torch.no_grad():
            inp = self.proc(text=daftar_teks, return_tensors="pt", padding=True)
            f = self._tensor(self.model.get_text_features(**inp))
        return self._norm(f)


def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


# ---------------------------------------------------------------------------
# Penyimpanan raw (dapat dilanjutkan)
# ---------------------------------------------------------------------------
def muat_raw():
    p = os.path.join(OUT, "raw.npz")
    if not os.path.exists(p):
        return {}, {}
    d = np.load(p, allow_pickle=False)
    ids = d["ids"].tolist()
    emb = d["emb"].astype("float32")
    slots = d["slot"].tolist()
    return {i: emb[k] for k, i in enumerate(ids)}, {i: slots[k] for k, i in enumerate(ids)}


def simpan_raw(emb_map, slot_map):
    ids = sorted(emb_map)
    np.savez_compressed(
        os.path.join(OUT, "raw.npz"),
        ids=np.array(ids, dtype="int64"),
        emb=np.array([emb_map[i] for i in ids], dtype="float16"),
        slot=np.array([slot_map[i] for i in ids]),
    )


# ---------------------------------------------------------------------------
# Pasca-proses
# ---------------------------------------------------------------------------
def pusatkan_per_slot(emb, slots):
    """Kurangi rata-rata tiap slot supaya jarak antar item mencerminkan GAYA/WARNA, bukan jenis slot."""
    emb = emb.copy()
    slots = np.array(slots)
    rata_global = emb.mean(axis=0)
    for s in sorted(set(slots.tolist())):
        idx = np.where(slots == s)[0]
        rata = emb[idx].mean(axis=0) if len(idx) >= 3 else rata_global
        emb[idx] = emb[idx] - rata
    n = np.linalg.norm(emb, axis=1, keepdims=True)
    n[n == 0] = 1
    return emb / n


def pca_kuantisasi(emb, dim):
    pusat = emb.mean(axis=0)
    x = emb - pusat
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    k = min(dim, vt.shape[0])
    z = x @ vt[:k].T
    maks = float(np.abs(z).max())
    skala = 127.0 / maks if maks > 0 else 1.0
    q = np.round(z * skala).astype(int)
    total = float((s ** 2).sum())
    var = float((s[:k] ** 2).sum() / total) if total > 0 else 0.0
    return q, skala, var, k


def tulis_hasil(emb_map, slot_map, gagal, tag_map):
    ids = sorted(emb_map)
    emb = np.array([emb_map[i] for i in ids], dtype="float32")
    slots = [slot_map[i] for i in ids]
    gaya_emb = pusatkan_per_slot(emb, slots)
    q, skala, var, k = pca_kuantisasi(gaya_emb, DIM_AKHIR)
    json.dump({
        "versi": 1,
        "model": MODEL_ID,
        "dim": k,
        "skala": round(skala, 6),
        "ragam_dijelaskan": round(var, 4),
        "catatan": "vec = PCA(32) dari embedding CLIP yang sudah dikurangi rata-rata per slot; kuantisasi int8 (nilai = float*skala)",
        "ids": ids,
        "slot": slots,
        "vec": q.tolist(),
    }, open(os.path.join(OUT, "embeddings.json"), "w"), separators=(",", ":"))
    json.dump({str(i): tag_map.get(i, {}) for i in ids}, open(os.path.join(OUT, "tags.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    json.dump(sorted(gagal), open(os.path.join(OUT, "gagal.json"), "w"))
    json.dump({
        "dibuat": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "jumlah_item": len(ids),
        "jumlah_gagal": len(gagal),
        "ragam_dijelaskan_pca": round(var, 4),
        "dim_akhir": k,
        "stub": STUB,
    }, open(os.path.join(OUT, "info.json"), "w"), indent=1)

    # contoh tetangga terdekat LINTAS slot pada ruang gaya (untuk dinilai mata: apakah masuk akal?)
    rng = random.Random(7)
    contoh = rng.sample(range(len(ids)), min(12, len(ids)))
    sim = gaya_emb @ gaya_emb.T
    baris = ["Tetangga terdekat pada ruang gaya (slot sumber sudah dinetralkan). Format: id[slot] -> id[slot](kemiripan)\n"]
    for a in contoh:
        urut = np.argsort(-sim[a])
        tetangga = [j for j in urut if j != a][:6]
        baris.append(f"{ids[a]}[{slots[a]}] -> " + "  ".join(f"{ids[j]}[{slots[j]}]({sim[a][j]:.2f})" for j in tetangga))
    open(os.path.join(OUT, "tetangga_contoh.txt"), "w", encoding="utf-8").write("\n".join(baris) + "\n")
    return var, k


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    semua = muat_items()
    log(f"items.json: {len(semua)} item")
    if BATAS > 0:
        acak = random.Random(1)
        acak.shuffle(semua)
        semua = semua[:BATAS]
        log(f"MODE UJI: hanya {len(semua)} item acak")
    slot_dari_id = {i: s for i, s in semua}

    emb_map, slot_map = muat_raw()
    gagal = set()
    p_gagal = os.path.join(OUT, "gagal.json")
    if os.path.exists(p_gagal):
        gagal = set(json.load(open(p_gagal)))
    sudah_tag = {}
    p_tag = os.path.join(OUT, "tags.json")
    if os.path.exists(p_tag):
        try:
            sudah_tag = {int(k): v for k, v in json.load(open(p_tag, encoding="utf-8")).items()}
        except Exception:
            sudah_tag = {}

    target = [i for i, _ in semua if i not in emb_map and i not in gagal]
    log(f"sudah ada {len(emb_map)} | gagal sebelumnya {len(gagal)} | akan dihitung {len(target)}")

    embedder = EmbedderStub() if STUB else EmbedderCLIP()
    emb_gaya = embedder.teks(list(GAYA.values()))
    nama_gaya = list(GAYA.keys())
    nama_atr = list(ATRIBUT.keys())
    emb_atr = np.stack([embedder.teks(list(ATRIBUT[n])) for n in nama_atr])  # A x 2 x D
    tag_map = dict(sudah_tag)

    hitung_md5 = {}
    md5_item = {}
    t0 = time.time()
    for a in range(0, len(target), BATCH_MODEL * 2):
        potong = target[a:a + BATCH_MODEL * 2]
        thumbs = ambil_thumbnail(potong)
        for i in potong:
            if i not in thumbs:
                gagal.add(i)
        sah = [(i, thumbs[i][0], thumbs[i][1]) for i in potong if i in thumbs]
        for i_, _, h in sah:
            hitung_md5[h] = hitung_md5.get(h, 0) + 1
            md5_item[i_] = h
        sah = [(i, im, h) for i, im, h in sah if hitung_md5[h] < AMBANG_PLACEHOLDER]
        for i in potong:
            if i in thumbs and i not in [x[0] for x in sah]:
                gagal.add(i)
        for b in range(0, len(sah), BATCH_MODEL):
            grup = sah[b:b + BATCH_MODEL]
            f = embedder.gambar([im for _, im, _ in grup])
            logit = 100.0 * f @ emb_gaya.T
            p = softmax(logit, axis=1)
            logit_a = 100.0 * np.einsum("nd,akd->nak", f, emb_atr)
            p_a = softmax(logit_a, axis=2)[:, :, 0]
            for k, (i, _, _) in enumerate(grup):
                emb_map[i] = f[k]
                slot_map[i] = slot_dari_id[i]
                urut = np.argsort(-p[k])[:3]
                tag_map[i] = {
                    "gaya": [[nama_gaya[j], int(round(float(p[k][j]) * 100))] for j in urut if p[k][j] >= 0.12],
                    "atribut": [nama_atr[j] for j in range(len(nama_atr)) if p_a[k][j] >= 0.75],
                }
        simpan_raw(emb_map, slot_map)
        json.dump(sorted(gagal), open(p_gagal, "w"))
        log(f"  {min(a + BATCH_MODEL * 2, len(target))}/{len(target)} diproses | berhasil total {len(emb_map)} | gagal {len(gagal)} | {time.time() - t0:.0f}s")

    # placeholder yang lolos di batch awal (baru ketahuan setelah muncul >= AMBANG kali): buang
    busuk = [i for i, h in md5_item.items() if hitung_md5.get(h, 0) >= AMBANG_PLACEHOLDER]
    for i in busuk:
        emb_map.pop(i, None)
        slot_map.pop(i, None)
        tag_map.pop(i, None)
        gagal.add(i)
    if busuk:
        log(f"  {len(busuk)} item dibuang karena gambarnya placeholder (identik untuk banyak item)")
        simpan_raw(emb_map, slot_map)

    if len(emb_map) < 3:
        log("Terlalu sedikit item berhasil untuk PCA. Periksa log di atas (thumbnail/jaringan).")
        sys.exit(1)
    var, k = tulis_hasil(emb_map, slot_map, gagal, tag_map)
    log(f"SELESAI: {len(emb_map)} item, dimensi akhir {k}, ragam dijelaskan PCA {var:.1%}")


if __name__ == "__main__":
    main()
