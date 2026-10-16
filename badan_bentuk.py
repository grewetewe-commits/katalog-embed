#!/usr/bin/env python3
"""
BADAN AVATAR (rev 32b) -- dua bukti per BAGIAN BADAN (Torso/lengan/kaki) untuk map, tanpa menebak dari nama bundle:

1. MANUSIA atau bukan: thumbnail RESMI bundle badan (thumbnails.roblox.com/v1/bundles/thumbnails) dibaca CLIP (gratis,
   model yang sama dengan kartu). Skor = peluang kalimat "badan manusia" (orang, anime, blok, kerangka, ksatria, zombi,
   robot humanoid) melawan "bukan" (katak, anjing, kucing, ikan, burung, serangga, boneka hewan, gumpalan, telur, makanan,
   kendaraan, ...). Ambang dipilih dari LABEL UJI (uji3d/badan_label.json, dicek mata): manusia yang tertolak <= 2%.
   Bagian badan mewarisi skor TERTINGGI dari bundle yang memuatnya (satu bundle manusia cukup membuktikan bagian itu wajar).
2. CARA DIPAKAI manusia: dari outfit manusia yang mencatat bagian badannya (BP), berapa persen memakai atasan/bawahan
   3D berlapis vs baju/celana klasik 2D. Badan yang hampir selalu dipakai dengan pakaian 3D = baju 2D tidak cocok di sana.

Keluaran: kartu/badan_bentuk.json {"versi","ambang","uji":{...},"d":{bagianId:[skorManusia 0-100 | -1, nAtas, pctLapisAtas,
nBawah, pctLapisBawah]}} + LAPORAN_BADAN.md. Map: KartuItemKit.BadanBentuk(id).
"""
import gzip, io, json, os, sys, time, collections
import numpy as np
import requests
from PIL import Image

MODEL_ID = "openai/clip-vit-base-patch32"
H = {"User-Agent": "KatalogPraktis-badan/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
P_STATE = "data/panen.json.gz"
P_LABEL = "uji3d/badan_label.json"
P_OUT = "kartu/badan_bentuk.json"
MAKS_TANYA = int(os.environ.get("MAKS_TANYA_BADAN", "600"))   # pemetaan bagian -> bundle per putaran (API publik)
TIPE_BADAN = {"Torso", "LeftArm", "RightArm", "LeftLeg", "RightLeg"}
MANUSIA = ["a 3D avatar of a human person", "a 3D cartoon human character", "a cute 3D anime girl avatar",
           "a 3D boy avatar", "a blocky 3D human figure", "a 3D human skeleton", "a 3D knight in armor",
           "a 3D zombie person", "a 3D humanoid robot", "a 3D chibi doll of a person"]
BUKAN = ["a 3D frog", "a 3D dog", "a 3D cat", "a 3D fish", "a 3D bird", "a 3D duck", "a 3D penguin", "a 3D insect",
         "a 3D bat with wings", "a 3D bear", "a 3D plush toy animal", "a 3D blob", "a 3D egg", "a 3D bean",
         "a 3D food item", "a 3D car", "a 3D cube", "a 3D slime", "a 3D worm", "a 3D snail", "a 3D rabbit",
         "a 3D monster creature", "a 3D stick figure"]
LAPIS_ATAS = {9, 10, 12, 13, 17}     # Enum.AccessoryType: TShirt, Shirt, Jacket, Sweater, DressSkirt
LAPIS_BAWAH = {11, 14, 17}           # Pants, Shorts, DressSkirt


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def thumb_bundle(ids):
    out = {}
    for a in range(0, len(ids), 50):
        p = ids[a:a + 50]
        for _ in range(3):
            try:
                r = requests.get("https://thumbnails.roblox.com/v1/bundles/thumbnails", headers=H, timeout=30,
                                 params={"bundleIds": ",".join(map(str, p)), "size": "420x420", "format": "Png",
                                         "isCircular": "false"})
                pending = False
                for e in r.json().get("data", []):
                    if e.get("state") == "Completed" and e.get("imageUrl"):
                        b = requests.get(e["imageUrl"], headers=H, timeout=30).content
                        im = Image.open(io.BytesIO(b)).convert("RGBA")
                        alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
                        alas.alpha_composite(im)
                        out[int(e["targetId"])] = alas.convert("RGB")
                    elif e.get("state") == "Pending":
                        pending = True
                if not pending:
                    break
            except Exception as ex:
                log("thumbnail bundle gagal:", ex)
            time.sleep(2)
        time.sleep(0.3)
    return out


def bundle_dari_bagian(aid):
    """bagian badan -> bundle badan yang memuatnya (API katalog publik yang sama dengan otak.py peta_badan)"""
    try:
        r = requests.get(f"https://catalog.roblox.com/v1/assets/{aid}/bundles", headers=H, timeout=20)
        js = r.json()
    except Exception:
        return None
    if not isinstance(js, dict) or not isinstance(js.get("data"), list):
        return None
    out = []
    for b in js["data"]:
        if isinstance(b, dict) and b.get("bundleType") in ("BodyParts", "DynamicHead"):
            try:
                out.append(int(b["id"]))
            except Exception:
                pass
    return out


class Clip:
    def __init__(self):
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self.torch = torch
        self.m = CLIPModel.from_pretrained(MODEL_ID).eval()
        self.p = CLIPProcessor.from_pretrained(MODEL_ID)

    def gambar(self, ims):
        out = []
        with self.torch.no_grad():
            for i in range(0, len(ims), 16):
                f = self.m.get_image_features(**self.p(images=ims[i:i + 16], return_tensors="pt"))
                out.append((f / f.norm(dim=-1, keepdim=True)).cpu().numpy())
        return np.concatenate(out) if out else np.zeros((0, 512), "float32")

    def teks(self, kal):
        with self.torch.no_grad():
            f = self.m.get_text_features(**self.p(text=kal, return_tensors="pt", padding=True))
        return (f / f.norm(dim=-1, keepdim=True)).cpu().numpy()


def skor_manusia(clip, ims):
    """peluang 'manusia' (0..1) per gambar: softmax atas semua kalimat (suhu CLIP 100), dijumlah sisi manusia"""
    T = clip.teks(MANUSIA + BUKAN)
    G = clip.gambar(ims)
    z = 100.0 * G @ T.T
    z -= z.max(axis=1, keepdims=True)
    e = np.exp(z)
    p = e / e.sum(axis=1, keepdims=True)
    return p[:, :len(MANUSIA)].sum(axis=1)


def pakai_lapis(st):
    """bagian badan -> [nAtas, pctLapisAtas, nBawah, pctLapisBawah] dari outfit manusia R15 yang mencatat BP"""
    atas = collections.defaultdict(lambda: [0, 0])
    bawah = collections.defaultdict(lambda: [0, 0])
    for o in (st.get("outfit") or {}).values():
        if not (isinstance(o, dict) and o.get("R") == "R15" and isinstance(o.get("BP"), dict)):
            continue
        tA = {a[1] for a in (o.get("A") or []) if isinstance(a, list) and len(a) > 1}
        la, lb = bool(tA & LAPIS_ATAS), bool(tA & LAPIS_BAWAH)
        bp = o["BP"]
        for k in ("Torso", "LeftArm", "RightArm"):
            v = bp.get(k)
            if isinstance(v, int) and v > 0:
                atas[v][0] += 1
                atas[v][1] += la
        for k in ("Torso", "LeftLeg", "RightLeg"):
            v = bp.get(k)
            if isinstance(v, int) and v > 0:
                bawah[v][0] += 1
                bawah[v][1] += lb
    return atas, bawah


def main():
    t0 = time.time()
    with gzip.open(P_STATE, "rt", encoding="utf-8") as f:
        st = json.load(f)
    lama = {}
    if os.path.exists(P_OUT):
        try:
            lama = json.load(open(P_OUT, encoding="utf-8"))
        except Exception:
            lama = {}
    peta = {k: list(v) for k, v in ((lama.get("peta") or {}).items())}      # bagian -> bundle (disimpan antar putaran)
    skorB = {k: v for k, v in ((lama.get("bundle") or {}).items())}         # bundle -> skor 0..100
    for k, v in ((st.get("badan") or {}).get("a") or {}).items():
        peta.setdefault(str(k), [int(x) for x in v])
    atas, bawah = pakai_lapis(st)
    bagian = sorted(set(atas) | set(bawah), key=lambda i: -(atas.get(i, [0])[0] + bawah.get(i, [0])[0]))
    n_tanya = 0
    for b in bagian:
        if str(b) in peta or n_tanya >= MAKS_TANYA:
            continue
        r = bundle_dari_bagian(b)
        n_tanya += 1
        if r is not None:
            peta[str(b)] = r
        time.sleep(0.15)
    label = (json.load(open(P_LABEL, encoding="utf-8")).get("d") or {}) if os.path.exists(P_LABEL) else {}
    perlu = sorted(({x for v in peta.values() for x in v} | {int(k) for k in label}) - {int(k) for k in skorB})
    log(f"bagian badan dipakai manusia: {len(bagian)}, dipetakan {len(peta)} (+{n_tanya} tanya), bundle perlu dibaca {len(perlu)}")
    if perlu:
        gb = thumb_bundle(perlu)
        ids = [i for i in perlu if i in gb]
        if ids:
            clip = Clip()
            s = skor_manusia(clip, [gb[i] for i in ids])
            for i, v in zip(ids, s):
                skorB[str(i)] = int(round(100 * float(v)))
    # ambang dari label uji: manusia yang tertolak <= 2%
    uji = {}
    m = sorted(skorB[k] for k, v in label.items() if v == "manusia" and k in skorB)
    b = sorted(skorB[k] for k, v in label.items() if v == "bukan" and k in skorB)
    ambang = None
    if len(m) >= 20 and len(b) >= 20:
        for a in range(0, 101):
            tolakM = sum(x < a for x in m) / len(m)
            if tolakM > 0.02:
                break
            ambang = a
        uji = {"manusia": len(m), "bukan": len(b), "ambang": ambang,
               "manusiaLolos": round(sum(x >= ambang for x in m) / len(m), 3),
               "bukanTertangkap": round(sum(x < ambang for x in b) / len(b), 3)}
    if ambang is None:
        ambang = (lama.get("ambang") if isinstance(lama.get("ambang"), int) else 30)
    d = {}
    for k in set(peta) | {str(i) for i in atas} | {str(i) for i in bawah}:
        sk = [skorB[str(x)] for x in peta.get(k, []) if str(x) in skorB]
        a = atas.get(int(k), [0, 0])
        bw = bawah.get(int(k), [0, 0])
        d[k] = [max(sk) if sk else -1, a[0], int(round(100 * a[1] / a[0])) if a[0] else -1,
                bw[0], int(round(100 * bw[1] / bw[0])) if bw[0] else -1]
    versi = int(time.time())
    os.makedirs("kartu", exist_ok=True)
    json.dump({"versi": versi, "ambang": ambang, "uji": uji, "d": d, "peta": peta, "bundle": skorB},
              open(P_OUT, "w", encoding="utf-8"), separators=(",", ":"))
    baris = [f"# Badan avatar — {len(d)} bagian badan, {len(skorB)} bundle dibaca", "",
             f"Ambang skor manusia: **{ambang}** (dipilih dari label uji, manusia tertolak <= 2%).", "",
             f"Uji label: {json.dumps(uji)}", "", "## Bundle label uji yang salah baca", ""]
    for k, v in sorted(label.items()):
        if k in skorB and ((v == "manusia") != (skorB[k] >= ambang)):
            baris.append(f"- {k} label {v}, skor {skorB[k]}")
    baris += ["", "## Bagian badan paling sering dipakai: persen atasan/bawahan 3D", "", "| bagian | skor manusia | n atas | % 3D atas | n bawah | % 3D bawah |", "|---|---|---|---|---|---|"]
    for k in sorted(d, key=lambda k: -(d[k][1] + d[k][3]))[:60]:
        v = d[k]
        baris.append(f"| {k} | {v[0]} | {v[1]} | {v[2]} | {v[3]} | {v[4]} |")
    open("LAPORAN_BADAN.md", "w", encoding="utf-8").write("\n".join(baris))
    log(f"selesai: {len(d)} bagian, ambang {ambang}, uji {uji}, {time.time() - t0:.0f} dtk")


if __name__ == "__main__":
    main()
