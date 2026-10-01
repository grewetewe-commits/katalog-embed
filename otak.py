#!/usr/bin/env python3
"""
OTAK Katalog Praktis -- model kecocokan outfit yang BELAJAR dari outfit buatan manusia.
Jalan di GitHub Actions (repo publik = gratis), terjadwal tiap hari, tanpa token/secret apa pun.

Alur satu putaran:
  1. PANEN    : cari item katalog per kata kunci (API publik catalog.roblox.com) -> kumpulkan kreatornya ->
                baca outfit tersimpan + avatar kreator (API publik avatar.roblox.com). Yang disimpan HANYA daftar
                ID item (tanpa userId/username). Kreator yang sudah dibaca dicatat sebagai hash.
  2. META     : nama, harga, status dijual, kreator item (dari hasil pencarian / catalog items details).
  3. MATA     : thumbnail item -> CLIP (openai/clip-vit-base-patch32) -> vektor 512. Plus warna dominan,
                skor feminin/maskulin, tag gaya & atribut (zero-shot).
  4. BELAJAR  : jaringan kecil dilatih supaya item yang MEMANG dipakai bersama dalam outfit nyata berdekatan,
                dibanding item lain di slot yang sama (contrastive, negatif satu slot).
                Diuji jujur dengan FITB (fill-in-the-blank) pada outfit yang TIDAK ikut dilatih.
  5. EKSPOR   : model/ (vektor gaya 32 angka per item + gender + warna + tag), bank/ (outfit dasar lolos
                saring + skor koherensi), meta/ (harga snapshot). Server Roblox mengunduh lewat
                raw.githubusercontent.com dan tetap memvalidasi harga live.

Variabel lingkungan: STUB=1 (uji alur tanpa jaringan/model), MENIT_PANEN, MAKS_KREATOR, MAKS_ITEM_BARU,
                     MENIT_MATA, CACHE_DIR.
"""
import gzip
import hashlib
import io
import json
import math
import os
import random
import re
import sys
import time
from datetime import datetime, timezone

import numpy as np

STUB = os.environ.get("STUB") == "1"
MENIT_PANEN = float(os.environ.get("MENIT_PANEN", "70") or 70)
MENIT_MATA = float(os.environ.get("MENIT_MATA", "100") or 100)
MAKS_KREATOR = int(os.environ.get("MAKS_KREATOR", "600") or 600)
MAKS_ITEM_BARU = int(os.environ.get("MAKS_ITEM_BARU", "25000") or 25000)
MAKS_OUTFIT_PER_KREATOR = 14
KATA_PER_PUTARAN = 160
CACHE_DIR = os.environ.get("CACHE_DIR", "cache")
P_STATE = "data/panen.json.gz"
P_EMB = os.path.join(CACHE_DIR, "emb.npz")
MODEL_ID = "openai/clip-vit-base-patch32"
DIM = 32
SHARD_ITEM = 8
SHARD_BANK = 4
MAKS_BANK = 8000
HEADERS = {"User-Agent": "KatalogPraktis-otak/2.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}
T0 = time.time()

# ---------------------------------------------------------------------------------------------
# Tipe aset Roblox (terverifikasi dari Enum.AssetType / Enum.AccessoryType di Studio)
# ---------------------------------------------------------------------------------------------
ASET_KE_ACC = {8: 1, 41: 2, 42: 3, 43: 4, 44: 5, 45: 6, 46: 7, 47: 8, 64: 9, 65: 10, 66: 11, 67: 12, 68: 13,
               69: 14, 70: 15, 71: 16, 72: 17, 76: 18, 77: 19}
ACC_KE_ASET = {v: k for k, v in ASET_KE_ACC.items()}
LAYERED = set(range(9, 18))
# kelas slot untuk belajar & ekspor (kode angka kecil dipakai server)
SLOT_KODE = {"Shirt": 1, "Pants": 2, "TShirt": 3, "Face": 4, "Hat": 5, "Hair": 6, "FaceAcc": 7, "Neck": 8,
             "Shoulder": 9, "Front": 10, "Back": 11, "Waist": 12, "LayerAtas": 13, "LayerBawah": 14, "Sepatu": 15,
             "Alis": 16}
ACC_KE_SLOT = {1: "Hat", 2: "Hair", 3: "FaceAcc", 4: "Neck", 5: "Shoulder", 6: "Front", 7: "Back", 8: "Waist",
               9: "LayerAtas", 10: "LayerAtas", 12: "LayerAtas", 13: "LayerAtas", 11: "LayerBawah", 14: "LayerBawah",
               17: "LayerBawah", 15: "Sepatu", 16: "Sepatu", 18: "Alis", 19: "Alis"}
ASET_KE_SLOT = {11: "Shirt", 12: "Pants", 2: "TShirt", 18: "Face"}
for _a, _c in ASET_KE_ACC.items():
    ASET_KE_SLOT[_a] = ACC_KE_SLOT[_c]
SLOT_NOUN = {"Shirt": "shirt", "Pants": "pants", "TShirt": "t-shirt", "Face": "face", "Hat": "hat",
             "Hair": "hairstyle", "FaceAcc": "face accessory", "Neck": "necklace", "Shoulder": "shoulder accessory",
             "Front": "outfit accessory", "Back": "back accessory", "Waist": "waist accessory",
             "LayerAtas": "top", "LayerBawah": "bottom", "Sepatu": "shoes", "Alis": "eyebrows"}
SLOT_GENDER = {"Hair": 3.0, "Shirt": 2.0, "Pants": 1.5, "LayerAtas": 2.0, "LayerBawah": 2.0, "TShirt": 1.0,
               "Hat": 0.7, "Face": 1.0, "FaceAcc": 0.5, "Neck": 0.5, "Sepatu": 0.7}

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
    "senjata": ("an avatar item with a sword, gun or weapon", "an avatar item without any weapon"),
    "kacamata": ("an avatar item with glasses", "an avatar item without glasses"),
    "telinga_hewan": ("an avatar item with animal ears", "an avatar item without animal ears"),
    "mahkota": ("an avatar item with a crown or tiara", "an avatar item without a crown"),
}
PROMPT_FEM = ["a feminine girl's avatar {s}", "a cute girly {s} for women", "a women's {s}", "a pretty female {s}"]
PROMPT_MASC = ["a masculine boy's avatar {s}", "a men's {s}", "a manly {s} for boys", "a cool male {s}"]
KATA_PRIA = {"pria", "cowok", "laki", "boy", "boys", "men", "male", "guy", "bro", "gentleman", "beard", "mustache"}
KATA_WANITA = {"wanita", "cewek", "cewe", "perempuan", "gadis", "girl", "girls", "women", "woman", "female", "lady",
               "ladies", "princess", "putri", "rok", "skirt", "dress", "gaun", "bralette", "bra", "korset", "corset",
               "bikini", "heels"}

# kata kunci pencarian (dari TemaList.Keywords di Studio + gaya umum) -- dirotasi tiap putaran
KATA_KUNCI = """butterfly top|crop hoodie|rhinestone zip|baby tee|star print|low rise jeans|denim skirt|flare pants|pleated mini|chunky sunglasses|star hair clips|cyber glasses|beaded necklace|cyberpunk trench coat|led leather jacket|neon mesh top|techwear joggers|neon visor|cyber headset|holy white armor|angelic silk robe|white flowing skirt|angel wings|glowing halo|seraphim wings|scp scientist coat|gas mask|steampunk corset vest|clockwork tailcoat|leather aviator jacket|top hat gears|brass goggles|plate armor knight|chainmail|royal doublet|knight helmet|broadsword back|superhero suit|hero cape|utility belt|police uniform|swat vest|aviator shades|pastel oversized hoodie|bunny sweater|lolita dress|frilly skirt|heart shorts|bunny ears|plushie backpack|heart sunglasses|hair bows|elven tunic|ranger cloak|elf ears|bow back|circlet|camo jacket|tactical vest|bomber jacket|cargo pants|combat boots|dog tags|military beret|pirate coat|poet shirt|tricorn hat|eyepatch|pirate boots|assassin cloak|ninja|dual daggers|mecha armor|robot helmet|denim overalls|plaid flannel|straw hat|pharaoh|egyptian dress|anubis|firefighter|blood splatter shirt|hockey mask|haori|school uniform|sailor uniform|pleated school skirt|katana back|spiky anime hair|kitsune mask|security guard shirt|spiked leather jacket|fishnet top|tartan pants|ripped black jeans|mohawk|studded collar|chains belt|oversized hoodie|puffer jacket|graphic tee|zip up hoodie|windbreaker|baggy sweatpants|stacked jeans|bucket hat|beanie|chunky sneakers|crossbody bag|silver chain|sci fi armor|holographic jacket|catsuit|chrome helmet|trench coat|detective vest|suspenders|fedora|astronaut|space helmet|jetpack|banana suit|samurai|hakama|lace cottage dress|corset top|mossy sweater|flower crown|fairy wings|butterfly clips|striped hoodie|band t-shirt|skull hoodie|skinny jeans|checkered skirt|studded belt|scene hair|arm warmers|fingerless gloves|leopard coat|leather pants|guitar back|messy hair|wizard robe|wizard hat|magic staff|lab coat|nurse uniform|scrubs|racing jumpsuit|racing helmet|track jacket|sports jersey|tennis skirt|gym shorts|headband|retro windbreaker|pastel hoodie|90s tee|light wash jeans|glitch mask|retro headphones|dragon armor|dragon wings|dragon horns|dragon tail|velvet robe|embroidered coat|royal gown|gold crown|royal cape|tiara|diamond necklace|linen blazer|cashmere sweater|cable knit|polo knit|tailored trousers|white linen pants|pearl necklace|loafers|luxury watch|demon lord coat|demon horns|devil tail|demon wings|seashell top|mermaid tail|trident|coral crown|shark fin|celestial robe|witch dress|moon print|goth lace cape|starry pants|witch hat|crystal necklace|choker|potion belt|crow shoulder|vintage coat|tweed jacket|high waisted trousers|long skirt|beret|newsboy cap|pocket watch|viking|fur pauldrons|horned helmet|battle axe|wooden shield|braided beard|wasteland|scrap armor|striped long sleeve|workwear jacket|denim shorts|skate pants|skateboard|backward cap|wallet chain|plain tee|crewneck|denim jacket|flannel|cardigan|straight jeans|khaki shorts|chino pants|sneakers|tote bag|baseball cap|cowboy hat|cowboy boots|bandana|poncho|puff sleeve dress|apron dress|gingham|floral overalls|tiered skirt|flower basket|braided hair|formal suit|blazer|dress shirt|tie|pencil skirt|briefcase|tv head|dreamcore|vhs|hawaiian shirt|bikini|board shorts|sarong|sun hat|flower lei|surfboard|oversized flannel|distressed sweater|striped sweater|skeleton tee|ripped jeans|cargo skirt|layered chains|ringmaster|jester|clown|chef coat|chef hat|knitted cardigan|oxford shirt|plaid tennis skirt|khaki trousers|pleated skirt|hair bow|glasses|pixel|8bit|arcade|tattered cloak|shadow robe|void|ragged cape|dark aura|basketball jersey|puffer vest|vintage tee|baggy jeans|track pants|gold chain|snapback|durag|iced out|retro sneakers|idol outfit|glitter top|sequin jacket|platform boots|lace corset|velvet coat|mesh top|goth skirt|strap pants|cross necklace|bat wings|goth hair|toga|laurel crown|greek dress|winter scarf|christmas sweater|fur coat|snow pants|santa hat|earmuffs|ski goggles|mittens|paint smock|artist beret|paint palette|safari vest|hiking backpack|binoculars|y2k|kawaii|emo|grunge|preppy|old money|cottagecore|coquette|fairycore|baddie|soft girl|e-girl|e-boy|streetwear|techwear|gyaru|harajuku|victorian|maid|butler|vampire|werewolf|zombie|cyborg|alien|angel|demon|goth|punk|rockstar|hip hop|skater|surfer|cowboy|knight|princess|prince|royal|ninja|samurai|pirate|wizard|witch|fairy|mermaid|elf|dragon|cat ears|fox ears|wolf tail|bow|ribbon|heart|star|moon|cross|skull|chains|lace|fur|denim|leather|plaid|stripes|polka dot|floral|camo|neon|pastel|black and white|all black|all white|red|pink|blue|green|purple|yellow|brown|beige|cream""".split("|")


def log(*a):
    print(f"[{(time.time() - T0) / 60:5.1f}m]", *a, flush=True)


def hash_kanonik(teks):
    """Sama persis dengan hashKanonik di OutfitDasarEngine (Luau) -> dedup lintas sistem."""
    h1, h2 = 5381, 52711
    for b in teks.encode("utf-8"):
        h1 = (h1 * 131 + b) % 4294967291
        h2 = (h2 * 137 + b) % 4294967279
    return "%08x%08x" % (h1, h2)


def hash_kreator(uid):
    return hashlib.sha1(("kp-otak-" + str(uid)).encode()).hexdigest()[:14]


# ---------------------------------------------------------------------------------------------
# HTTP sopan (jeda per host, mundur saat 429, CSRF untuk POST katalog)
# ---------------------------------------------------------------------------------------------
class Http:
    def __init__(self):
        import requests
        self.s = requests.Session()
        self.s.headers.update(HEADERS)
        self.jeda = {}
        self.terakhir = {}
        self.csrf = None
        self.n = 0
        self.n429 = 0
        self.gagal = 0

    def _tunggu(self, host):
        j = self.jeda.get(host, 0.35)
        dt = time.time() - self.terakhir.get(host, 0)
        if dt < j:
            time.sleep(j - dt)
        self.terakhir[host] = time.time()

    def _host(self, url):
        return url.split("/")[2]

    def get(self, url, params=None, coba=5):
        host = self._host(url)
        for k in range(coba):
            self._tunggu(host)
            try:
                r = self.s.get(url, params=params, timeout=30)
                self.n += 1
                if r.status_code == 200:
                    self.jeda[host] = max(0.35, self.jeda.get(host, 0.35) * 0.97)
                    return r.json()
                if r.status_code == 429 or r.status_code >= 500:
                    self.n429 += r.status_code == 429
                    self.jeda[host] = min(6.0, self.jeda.get(host, 0.35) * 1.6 + 0.3)
                    time.sleep(min(90, 4 * (2 ** k)))
                    continue
                self.gagal += 1
                return None
            except Exception:
                time.sleep(2 ** k)
        self.gagal += 1
        return None

    def post_katalog(self, body, coba=5):
        url = "https://catalog.roblox.com/v1/catalog/items/details"
        host = self._host(url)
        for k in range(coba):
            self._tunggu(host)
            try:
                h = {"Content-Type": "application/json"}
                if self.csrf:
                    h["x-csrf-token"] = self.csrf
                r = self.s.post(url, data=json.dumps(body), headers=h, timeout=30)
                self.n += 1
                if r.status_code == 403 and r.headers.get("x-csrf-token"):
                    self.csrf = r.headers["x-csrf-token"]
                    continue
                if r.status_code == 200:
                    return r.json()
                if r.status_code == 429 or r.status_code >= 500:
                    self.n429 += r.status_code == 429
                    self.jeda[host] = min(6.0, self.jeda.get(host, 0.35) * 1.6 + 0.3)
                    time.sleep(min(90, 4 * (2 ** k)))
                    continue
                self.gagal += 1
                return None
            except Exception:
                time.sleep(2 ** k)
        self.gagal += 1
        return None

    def gambar(self, url):
        for k in range(3):
            try:
                r = self.s.get(url, timeout=30)
                if r.status_code == 200 and r.content:
                    return r.content
            except Exception:
                pass
            time.sleep(1.5 * (k + 1))
        return None


class HttpStub:
    """Data palsu deterministik untuk uji alur lokal (STUB=1)."""
    def __init__(self):
        self.n = self.n429 = self.gagal = 0
        self.rng = random.Random(5)
        self.csrf = None

    def _item(self, i):
        r = random.Random(i)
        at = r.choice([11, 12, 41, 8, 42, 43, 44, 45, 46, 47, 65, 66, 67, 72, 18])
        return {"id": i, "itemType": "Asset", "assetType": at, "name": r.choice(["pink girl", "black boy", "lace", "cool", "star"]) + f" item {i}",
                "creatorType": r.choice(["User", "Group"]), "creatorTargetId": 1000 + i % 37, "creatorName": f"kreator{i % 37}",
                "price": r.choice([0, 25, 50, 75, 100, 300, None]), "priceStatus": r.choice([None, None, "Off Sale", "Free"]), "itemRestrictions": []}

    def get(self, url, params=None, coba=5):
        self.n += 1
        if "search/items" in url:
            base = abs(hash(params.get("Keyword", ""))) % 5000
            return {"data": [self._item(10000 + (base + k) % 3000) for k in range(30)]}
        if "/groups/" in url:
            return {"owner": {"userId": 900 + int(url.rstrip("/").split("/")[-1]) % 50}}
        if "/outfits?" in url or url.endswith("/outfits"):
            return {"data": [{"id": int(url.split("/users/")[1].split("/")[0]) * 100 + k, "outfitType": "Avatar"} for k in range(6)]}
        if "/outfits/" in url and url.endswith("/details") or "/avatar" in url:
            sid = int(re.findall(r"\d+", url)[-1])
            r = random.Random(sid)
            gaya = r.randint(0, 9)  # outfit "bergaya": item dipilih dari cluster gaya yang sama
            assets = []
            for at in [11, 12, 41, 8, 43, 46, 65]:
                if r.random() < 0.8:
                    pilihan = [10000 + k for k in range(3000) if random.Random(10000 + k).choice([11, 12, 41, 8, 42, 43, 44, 45, 46, 47, 65, 66, 67, 72, 18]) == at and (k % 10) == gaya]
                    if pilihan:
                        assets.append({"id": r.choice(pilihan), "assetType": {"id": at}})
            return {"assets": assets, "bodyColors": {"headColorId": 1, "torsoColorId": 194, "rightArmColorId": 1, "leftArmColorId": 1, "rightLegColorId": 1, "leftLegColorId": 1},
                    "scales": {"height": 1, "width": 1, "head": 1, "depth": 1, "proportion": 0, "bodyType": 0}, "playerAvatarType": "R15"}
        if "thumbnails" in url:
            ids = [int(x) for x in params["assetIds"].split(",")]
            return {"data": [{"targetId": i, "state": "Completed", "imageUrl": f"stub://{i}"} for i in ids]}
        return None

    def post_katalog(self, body, coba=5):
        self.n += 1
        return {"data": [self._item(x["id"]) for x in body["items"]]}

    def gambar(self, url):
        from PIL import Image
        i = int(url.split("//")[1])
        k = (i - 10000) % 10
        warna = ((k * 25) % 255, (k * 70) % 255, (k * 130) % 255)
        im = Image.new("RGBA", (64, 64), warna + (255,))
        im.putpixel((i % 64, (i // 64) % 64), (i % 255, 7, 9, 255))  # unik per item (bukan placeholder)
        b = io.BytesIO()
        im.save(b, "PNG")
        return b.getvalue()


# ---------------------------------------------------------------------------------------------
# State (repo: data/panen.json.gz) -- bisa dilanjutkan antar-putaran
# ---------------------------------------------------------------------------------------------
def muat_state():
    if os.path.exists(P_STATE):
        try:
            with gzip.open(P_STATE, "rt", encoding="utf-8") as f:
                st = json.load(f)
            st.setdefault("putaran", 0)
            return st
        except Exception as e:
            log("state rusak, mulai baru:", e)
    return {"versi": 2, "putaran": 0, "kreator": {}, "outfit": {}, "meta": {}, "gagal_thumb": {}}


def simpan_state(st):
    os.makedirs(os.path.dirname(P_STATE), exist_ok=True)
    with gzip.open(P_STATE + ".tmp", "wt", encoding="utf-8") as f:
        json.dump(st, f, separators=(",", ":"))
    os.replace(P_STATE + ".tmp", P_STATE)


def meta_dari_katalog(e):
    """Item katalog -> meta ringkas. s=1 hanya bila BENAR-BENAR bisa dibeli dengan harga tetap."""
    try:
        at = int(e.get("assetType") or 0)
    except Exception:
        at = 0
    price = e.get("price")
    status = e.get("priceStatus")
    restr = e.get("itemRestrictions") or []
    bisa = True
    if status in ("Off Sale", "No Resellers"):
        bisa = False
    if price is None and status != "Free":
        bisa = False
    if any(r in ("Limited", "LimitedUnique", "Collectible") for r in restr):
        # limited/koleksi: harga ikut pasar & stok bisa habis -> jangan dijanjikan
        if not (e.get("unitsAvailableForConsumption") or 0) > 0:
            bisa = False
    if status == "Free":
        price = 0
    return {"n": (e.get("name") or "")[:80], "p": int(price) if isinstance(price, (int, float)) else -1,
            "s": 1 if bisa else 0, "c": (e.get("creatorName") or "")[:40], "t": at, "w": int(time.time())}


def seed_dari_avatar(js):
    """JSON outfit/avatar (API publik) -> seed format OutfitDasarEngine. Return (seed, kreator_id_item) atau None."""
    if not js or not isinstance(js.get("assets"), list):
        return None
    sh = pa = gt = face = None
    acc = []
    lihat = set()
    for a in js["assets"]:
        try:
            i = int(a["id"])
            at = int(a["assetType"]["id"])
        except Exception:
            continue
        if at == 11 and not sh:
            sh = i
        elif at == 12 and not pa:
            pa = i
        elif at == 2 and not gt:
            gt = i
        elif at == 18 and not face:
            face = i
        elif at in ASET_KE_ACC and i not in lihat:
            lihat.add(i)
            acc.append([i, ASET_KE_ACC[at]])
    jumlah = (1 if sh else 0) + (1 if pa else 0) + (1 if gt else 0) + len(acc)
    if jumlah < 3 or len(acc) > 20:
        return None
    ada_pakaian = bool(sh or pa) or any(t in LAYERED for _, t in acc)
    if not ada_pakaian:
        return None
    if not any(t in (1, 2) for _, t in acc):
        return None  # kepala botak tanpa rambut/topi: biasanya avatar belum jadi
    kaku = sum(1 for _, t in acc if t in (1, 3, 4, 5, 6, 7, 8))
    if kaku > 12:
        return None  # terlalu penuh (aksesori tumpuk) -> sering jelek
    acc.sort(key=lambda x: (x[1], x[0]))
    bagian = [str(sh or 0), str(pa or 0), str(gt or 0)] + [f"{t}:{i}" for i, t in acc]
    seed = {"S": "gh", "Sh": sh, "Pa": pa, "Gt": gt, "A": acc, "H": hash_kanonik("|".join(bagian))}
    seed = {k: v for k, v in seed.items() if v is not None}
    if face:
        seed["F"] = face
    bc = js.get("bodyColors") or {}
    try:
        seed["BCn"] = [int(bc["headColorId"]), int(bc["torsoColorId"]), int(bc["leftArmColorId"]),
                       int(bc["rightArmColorId"]), int(bc["leftLegColorId"]), int(bc["rightLegColorId"])]
    except Exception:
        pass
    sc = js.get("scales") or js.get("scale") or {}
    try:
        v = [round(float(sc.get(k, d)), 2) for k, d in (("height", 1), ("width", 1), ("depth", 1), ("head", 1), ("proportion", 0), ("bodyType", 0))]
        dasar = [1, 1, 1, 1, 0, 0]
        if any(abs(a - b) > 0.011 for a, b in zip(v, dasar)):
            seed["SC"] = v
    except Exception:
        pass
    seed["R"] = "R6" if js.get("playerAvatarType") == "R6" else "R15"
    return seed


def ids_seed(s):
    out = [x for x in (s.get("Sh"), s.get("Pa"), s.get("Gt")) if x]
    out += [a[0] for a in s.get("A", [])]
    return out


def slot_item_seed(s):
    out = []
    if s.get("Sh"):
        out.append((s["Sh"], "Shirt"))
    if s.get("Pa"):
        out.append((s["Pa"], "Pants"))
    if s.get("Gt"):
        out.append((s["Gt"], "TShirt"))
    for i, t in s.get("A", []):
        out.append((i, ACC_KE_SLOT.get(t, "Hat")))
    return out


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / max(1, len(a | b))


# ---------------------------------------------------------------------------------------------
# 1. PANEN
# ---------------------------------------------------------------------------------------------
def panen(http, st):
    batas_waktu = T0 + MENIT_PANEN * 60
    putaran = st["putaran"]
    rng = random.Random(putaran * 7919 + 13)
    kata = KATA_KUNCI[:]
    rng.shuffle(kata)
    mulai = (putaran * KATA_PER_PUTARAN) % len(kata)
    kata = (kata + kata)[mulai:mulai + KATA_PER_PUTARAN]
    kreator_user, kreator_grup = {}, {}
    n_item_cari = 0
    for k_i, kw in enumerate(kata):
        if time.time() > T0 + MENIT_PANEN * 60 * 0.30:
            break  # maks 30% waktu panen untuk mencari kreator
        for kategori in ("1", "3"):
            js = http.get("https://catalog.roblox.com/v2/search/items/details",
                          {"Keyword": kw, "Category": kategori, "Limit": "120", "SortType": "0"})
            for e in (js or {}).get("data", []) or []:
                if e.get("itemType") != "Asset":
                    continue
                i = e.get("id")
                if not isinstance(i, int):
                    continue
                at = e.get("assetType")
                if at in ASET_KE_SLOT:
                    st["meta"][str(i)] = meta_dari_katalog(e)
                    n_item_cari += 1
                cid = e.get("creatorTargetId")
                if not isinstance(cid, int) or cid == 1:
                    continue
                if e.get("creatorType") == "User":
                    kreator_user[cid] = kreator_user.get(cid, 0) + 1
                elif e.get("creatorType") == "Group":
                    kreator_grup[cid] = kreator_grup.get(cid, 0) + 1
    log(f"pencarian: {k_i + 1} kata kunci, {n_item_cari} item katalog, kreator user {len(kreator_user)}, grup {len(kreator_grup)}")

    # pemilik grup = desainer di balik toko grup
    for gid, _ in sorted(kreator_grup.items(), key=lambda x: -x[1])[:250]:
        if time.time() > T0 + MENIT_PANEN * 60 * 0.40:
            break
        js = http.get(f"https://groups.roblox.com/v1/groups/{gid}")
        uid = ((js or {}).get("owner") or {}).get("userId")
        if isinstance(uid, int):
            kreator_user[uid] = kreator_user.get(uid, 0) + kreator_grup[gid]

    antre = [u for u, _ in sorted(kreator_user.items(), key=lambda x: -x[1]) if hash_kreator(u) not in st["kreator"]]
    log(f"kreator baru untuk dibaca: {len(antre)} (sudah pernah: {len(st['kreator'])})")
    n_kreator = n_outfit = n_tolak = n_mirip = 0
    for uid in antre[:MAKS_KREATOR]:
        if time.time() > batas_waktu:
            log("batas waktu panen tercapai, sisanya putaran berikutnya")
            break
        hasil_kreator = []
        js = http.get(f"https://avatar.roblox.com/v2/avatar/users/{uid}/outfits",
                      {"page": "1", "itemsPerPage": "50", "isEditable": "true"})
        daftar = [o for o in (js or {}).get("data", []) or [] if o.get("outfitType", "Avatar") == "Avatar"]
        sumber = [f"https://avatar.roblox.com/v1/outfits/{o['id']}/details" for o in daftar[:MAKS_OUTFIT_PER_KREATOR]]
        sumber.append(f"https://avatar.roblox.com/v1/users/{uid}/avatar")
        for url in sumber:
            d = http.get(url)
            seed = seed_dari_avatar(d)
            if not seed:
                n_tolak += 1
                continue
            ids = ids_seed(seed)
            if any(jaccard(ids, ids_seed(x)) >= 0.75 for x in hasil_kreator):
                n_mirip += 1  # varian warna/hampir kembar dari kreator yang sama: cukup satu
                continue
            hasil_kreator.append(seed)
        for seed in hasil_kreator:
            if seed["H"] not in st["outfit"]:
                seed["T"] = int(time.time())
                st["outfit"][seed["H"]] = seed
                n_outfit += 1
        st["kreator"][hash_kreator(uid)] = int(time.time())
        n_kreator += 1
        if n_kreator % 50 == 0:
            log(f"  kreator {n_kreator}: +{n_outfit} outfit (ditolak saring {n_tolak}, kembar {n_mirip}) | http {http.n}, 429 {http.n429}")
            simpan_state(st)
    log(f"PANEN selesai: {n_kreator} kreator dibaca, +{n_outfit} outfit baru, total bank {len(st['outfit'])}")
    return {"kreator": n_kreator, "outfit_baru": n_outfit, "ditolak": n_tolak, "kembar": n_mirip}


# ---------------------------------------------------------------------------------------------
# 2. META untuk item di outfit yang belum punya meta (atau meta > 3 hari)
# ---------------------------------------------------------------------------------------------
def lengkapi_meta(http, st):
    perlu = set()
    batas = time.time() - 3 * 86400
    for s in st["outfit"].values():
        for i in ids_seed(s):
            m = st["meta"].get(str(i))
            if not m or m.get("w", 0) < batas:
                perlu.add(i)
    perlu = sorted(perlu)
    log(f"meta perlu dilengkapi/diperbarui: {len(perlu)} item")
    n = 0
    for a in range(0, len(perlu), 100):
        if time.time() > T0 + (MENIT_PANEN + 25) * 60:
            log("  batas waktu meta, sisanya putaran berikutnya")
            break
        potong = perlu[a:a + 100]
        js = http.post_katalog({"items": [{"itemType": "Asset", "id": i} for i in potong]})
        dapat = set()
        if js is None:
            continue  # permintaan gagal: JANGAN tandai apa pun, coba lagi putaran berikutnya
        for e in js.get("data", []) or []:
            i = e.get("id")
            if isinstance(i, int):
                st["meta"][str(i)] = meta_dari_katalog(e)
                dapat.add(i)
                n += 1
        for i in potong:
            if i not in dapat and str(i) not in st["meta"]:
                # tidak ada di katalog (dihapus/disembunyikan) -> tandai tidak bisa dibeli
                st["meta"][str(i)] = {"n": "", "p": -1, "s": 0, "c": "", "t": 0, "w": int(time.time())}
    log(f"meta diperbarui: {n}")


# ---------------------------------------------------------------------------------------------
# 3. MATA (CLIP)
# ---------------------------------------------------------------------------------------------
class EmbedderStub:
    dim = 512

    def gambar(self, ims):
        out = []
        for im in ims:
            arr = np.asarray(im.resize((8, 8))).astype("float32").ravel()
            rng = np.random.default_rng(int(arr.sum()) % 100000)
            v = np.tile(arr, 3)[:512] / 255.0 + 0.05 * rng.normal(size=512)
            out.append(v / np.linalg.norm(v))
        return np.array(out, dtype="float32")

    def teks(self, t):
        out = []
        for s in t:
            rng = np.random.default_rng(int(hashlib.md5(s.encode()).hexdigest()[:6], 16))
            v = rng.normal(size=512)
            out.append(v / np.linalg.norm(v))
        return np.array(out, dtype="float32")


class EmbedderCLIP:
    def __init__(self):
        import torch
        from transformers import CLIPModel, CLIPProcessor
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        self.torch = torch
        self.model = CLIPModel.from_pretrained(MODEL_ID).eval()
        self.proc = CLIPProcessor.from_pretrained(MODEL_ID)

    @staticmethod
    def _t(x):
        for nama in ("image_embeds", "text_embeds", "pooler_output"):
            v = getattr(x, nama, None)
            if v is not None:
                return v
        return x

    def gambar(self, ims):
        with self.torch.no_grad():
            f = self._t(self.model.get_image_features(**self.proc(images=ims, return_tensors="pt")))
        f = f / f.norm(dim=-1, keepdim=True)
        return f.cpu().numpy().astype("float32")

    def teks(self, t):
        with self.torch.no_grad():
            f = self._t(self.model.get_text_features(**self.proc(text=t, return_tensors="pt", padding=True)))
        f = f / f.norm(dim=-1, keepdim=True)
        return f.cpu().numpy().astype("float32")


def muat_emb():
    emb, warna = {}, {}
    for p in (P_EMB, "out/raw.npz"):
        if os.path.exists(p):
            try:
                d = np.load(p, allow_pickle=False)
                ids = d["ids"].tolist()
                e = d["emb"].astype("float32")
                w = d["warna"].tolist() if "warna" in d.files else [""] * len(ids)
                for k, i in enumerate(ids):
                    if i not in emb:
                        emb[int(i)] = e[k]
                        if w[k]:
                            warna[int(i)] = str(w[k])
                log(f"embedding dimuat dari {p}: {len(ids)}")
            except Exception as ex:
                log("gagal muat", p, ex)
    return emb, warna


def simpan_emb(emb, warna):
    os.makedirs(CACHE_DIR, exist_ok=True)
    ids = sorted(emb)
    np.savez_compressed(P_EMB + ".tmp.npz", ids=np.array(ids, dtype="int64"),
                        emb=np.array([emb[i] for i in ids], dtype="float16"),
                        warna=np.array([warna.get(i, "") for i in ids]))
    os.replace(P_EMB + ".tmp.npz", P_EMB)


def warna_dominan(rgba):
    """Warna dominan piksel non-transparan (kuantisasi 4 bit per kanal, bin terbanyak, rata-rata bin)."""
    a = np.asarray(rgba.convert("RGBA").resize((64, 64))).reshape(-1, 4)
    a = a[a[:, 3] > 128][:, :3].astype("int32")
    if len(a) < 20:
        return ""
    q = (a // 32)
    kunci = q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]
    nilai, hitung = np.unique(kunci, return_counts=True)
    k = nilai[np.argmax(hitung)]
    m = a[kunci == k].mean(axis=0)
    return "%02x%02x%02x" % tuple(int(x) for x in m)


def mata(http, st, embedder):
    from PIL import Image
    emb, warna = muat_emb()
    universe = set()
    for s in st["outfit"].values():
        universe.update(ids_seed(s))
    for k, m in st["meta"].items():
        if m.get("t") in ASET_KE_SLOT:
            universe.add(int(k))
    gagal = st.setdefault("gagal_thumb", {})
    target = [i for i in universe if i not in emb and str(i) not in gagal]
    # prioritas: item yang ada di outfit dulu
    di_outfit = set()
    for s in st["outfit"].values():
        di_outfit.update(ids_seed(s))
    target.sort(key=lambda i: (0 if i in di_outfit else 1, i))
    target = target[:MAKS_ITEM_BARU]
    log(f"MATA: universe {len(universe)} item, sudah ada {len(emb)}, akan dihitung {len(target)}")
    batas = T0 + (MENIT_PANEN + 25 + MENIT_MATA) * 60
    md5_hitung = {}
    for a in range(0, len(target), 50):
        if time.time() > batas:
            log("  batas waktu MATA, sisanya putaran berikutnya")
            break
        potong = target[a:a + 50]
        js = http.get("https://thumbnails.roblox.com/v1/assets", {"assetIds": ",".join(map(str, potong)), "returnPolicy": "PlaceHolder",
                                                                  "size": "150x150", "format": "Png", "isCircular": "false"})
        ims, ids_ok = [], []
        for e in (js or {}).get("data", []) or []:
            i = e.get("targetId")
            if e.get("state") == "Completed" and e.get("imageUrl"):
                b = http.gambar(e["imageUrl"])
                if not b:
                    continue
                h = hashlib.md5(b).hexdigest()
                md5_hitung[h] = md5_hitung.get(h, 0) + 1
                if md5_hitung[h] >= 4:
                    gagal[str(i)] = 1  # placeholder
                    continue
                try:
                    im = Image.open(io.BytesIO(b)).convert("RGBA")
                except Exception:
                    continue
                warna[i] = warna_dominan(im)
                alas = Image.new("RGBA", im.size, (255, 255, 255, 255))
                alas.alpha_composite(im)
                ims.append(alas.convert("RGB"))
                ids_ok.append(i)
            elif e.get("state") in ("Blocked", "Error"):
                gagal[str(i)] = 1
        for b0 in range(0, len(ims), 32):
            f = embedder.gambar(ims[b0:b0 + 32])
            for k, i in enumerate(ids_ok[b0:b0 + 32]):
                emb[i] = f[k]
        if (a // 50) % 40 == 0:
            log(f"  {a + len(potong)}/{len(target)} | total embedding {len(emb)}")
            simpan_emb(emb, warna)
    simpan_emb(emb, warna)
    return emb, warna


# ---------------------------------------------------------------------------------------------
# 4. BELAJAR
# ---------------------------------------------------------------------------------------------
def slot_semua_item(st):
    slot = {}
    for s in st["outfit"].values():
        for i, sl in slot_item_seed(s):
            slot.setdefault(i, sl)
    for k, m in st["meta"].items():
        sl = ASET_KE_SLOT.get(m.get("t"))
        if sl:
            slot.setdefault(int(k), sl)
    return slot


def zero_shot(embedder, ids, X, slot_of):
    nama_gaya = list(GAYA)
    tg = embedder.teks([GAYA[n] for n in nama_gaya])
    p_gaya = np.exp(100 * (X @ tg.T - (X @ tg.T).max(axis=1, keepdims=True)))
    p_gaya /= p_gaya.sum(axis=1, keepdims=True)
    nama_atr = list(ATRIBUT)
    p_atr = np.zeros((len(ids), len(nama_atr)), dtype="float32")
    for j, n in enumerate(nama_atr):
        t = embedder.teks(list(ATRIBUT[n]))
        l = 100 * (X @ t.T)
        l -= l.max(axis=1, keepdims=True)
        e = np.exp(l)
        p_atr[:, j] = e[:, 0] / e.sum(axis=1)
    # gender per slot (prompt sesuai jenis item)
    p_fem = np.full(len(ids), 0.5, dtype="float32")
    slots = np.array([slot_of.get(i, "Hat") for i in ids])
    for sl in sorted(set(slots.tolist())):
        idx = np.where(slots == sl)[0]
        noun = SLOT_NOUN.get(sl, "item")
        tf = embedder.teks([p.format(s=noun) for p in PROMPT_FEM]).mean(axis=0)
        tm = embedder.teks([p.format(s=noun) for p in PROMPT_MASC]).mean(axis=0)
        tf /= np.linalg.norm(tf)
        tm /= np.linalg.norm(tm)
        lf = 100 * X[idx] @ tf
        lm = 100 * X[idx] @ tm
        p_fem[idx] = 1 / (1 + np.exp(-(lf - lm)))
    return nama_gaya, p_gaya, nama_atr, p_atr, p_fem


def gender_label_nama(nama):
    s = " " + re.sub(r"[^a-z]", " ", (nama or "").lower()) + " "
    pria = any(f" {w} " in s for w in KATA_PRIA)
    wanita = any(f" {w} " in s for w in KATA_WANITA)
    if pria and not wanita:
        return 0
    if wanita and not pria:
        return 1
    return None


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) < 20 or len(neg) < 20:
        return None
    semua = np.concatenate([pos, neg])
    r = semua.argsort().argsort().astype(float) + 1
    # rata-rata peringkat untuk nilai sama
    _, inv, cnt = np.unique(semua, return_inverse=True, return_counts=True)
    jumlah = np.bincount(inv, weights=r)
    r = (jumlah / cnt)[inv]
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def latih(st, emb, slot_of, rng_seed=1):
    import torch
    torch.manual_seed(rng_seed)
    rng = np.random.default_rng(rng_seed)
    ids_all = sorted(i for i in emb if i in slot_of)
    idx_of = {i: k for k, i in enumerate(ids_all)}
    X = np.stack([emb[i] for i in ids_all]).astype("float32")
    slots = np.array([slot_of[i] for i in ids_all])
    slot_list = sorted(set(slots.tolist()))
    slot_idx = {s: np.where(slots == s)[0] for s in slot_list}
    outfits = []
    for h, s in sorted(st["outfit"].items()):
        it = [(idx_of[i], sl) for i, sl in slot_item_seed(s) if i in idx_of and sl not in ("Alis",)]
        if len(it) >= 3:
            outfits.append((h, it))
    if len(outfits) < 60:
        log(f"BELAJAR dilewati: baru {len(outfits)} outfit berembedding (perlu >= 60)")
        return None
    val = [o for o in outfits if int(o[0][:4], 16) % 100 < 15]
    trn = [o for o in outfits if int(o[0][:4], 16) % 100 >= 15]
    log(f"BELAJAR: {len(ids_all)} item, outfit latih {len(trn)}, uji {len(val)}")
    # rata-rata per slot dari item latih (menetralkan "jenis slot", supaya yang dipelajari gaya)
    mu = {s: X[slot_idx[s]].mean(axis=0) for s in slot_list}
    Xc = X - np.stack([mu[s] for s in slots])
    Xc /= np.linalg.norm(Xc, axis=1, keepdims=True) + 1e-8
    Xt = torch.tensor(Xc)

    def fitb(fz, kumpulan, n_kand=4, seed=7):
        """Fill-in-the-blank: tebak item asli di antara n_kand kandidat satu slot. Acak = 1/n_kand."""
        r = np.random.default_rng(seed)
        benar = total = 0
        for _, it in kumpulan:
            for k, (j, sl) in enumerate(it):
                pool = slot_idx[sl]
                if len(pool) < 30:
                    continue
                konteks = [x for m, (x, _) in enumerate(it) if m != k]
                c = fz[konteks].mean(axis=0)
                c /= np.linalg.norm(c) + 1e-8
                isi = set(x for x, _ in it)
                kand = [j]
                while len(kand) < n_kand:
                    x = int(pool[r.integers(len(pool))])
                    if x not in isi and x not in kand:
                        kand.append(x)
                skor = fz[kand] @ c
                benar += int(np.argmax(skor) == 0)
                total += 1
        return benar / max(1, total), total

    def koherensi(fz, it):
        v = fz[[x for x, _ in it]]
        s = v @ v.T
        n = len(it)
        return float((s.sum() - np.trace(s)) / (n * (n - 1)))

    def auc_koherensi(fz, kumpulan, seed=11):
        r = np.random.default_rng(seed)
        pos, neg = [], []
        for _, it in kumpulan:
            pos.append(koherensi(fz, it))
            palsu = []
            for x, sl in it:
                pool = slot_idx[sl]
                palsu.append((int(pool[r.integers(len(pool))]) if r.random() < 0.5 else x, sl))
            neg.append(koherensi(fz, palsu))
        return auc(pos, neg)

    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    hasil = {"acak": 0.25}
    hasil["clip_mentah"], n_uji = fitb(Xn, val)
    hasil["clip_netral_slot"], _ = fitb(Xc, val)
    log(f"  FITB baseline: mentah {hasil['clip_mentah']:.3f} | netral-slot {hasil['clip_netral_slot']:.3f} | acak 0.25 | {n_uji} soal")

    class Kepala(torch.nn.Module):
        def __init__(self, dalam):
            super().__init__()
            if dalam:
                self.f = torch.nn.Sequential(torch.nn.Linear(512, 384), torch.nn.GELU(), torch.nn.Dropout(0.1), torch.nn.Linear(384, DIM))
            else:
                self.f = torch.nn.Linear(512, DIM, bias=False)
            self.log_suhu = torch.nn.Parameter(torch.tensor(math.log(1 / 0.07)))

        def forward(self, x):
            z = self.f(x)
            return z / (z.norm(dim=-1, keepdim=True) + 1e-8)

    def batch_contoh(n, r):
        kon, pos, neg = [], [], []
        for _ in range(n):
            _, it = trn[r.integers(len(trn))]
            k = r.integers(len(it))
            j, sl = it[k]
            konteks = [x for m, (x, _) in enumerate(it) if m != k]
            pool = slot_idx[sl]
            isi = set(x for x, _ in it)
            ng = []
            while len(ng) < 24:
                x = int(pool[r.integers(len(pool))])
                if x not in isi:
                    ng.append(x)
            kon.append(konteks)
            pos.append(j)
            neg.append(ng)
        return kon, pos, neg

    terbaik = None
    for dalam in (False, True):
        model = Kepala(dalam)
        opt = torch.optim.AdamW(model.parameters(), lr=2e-3 if not dalam else 1e-3, weight_decay=1e-4)
        r = np.random.default_rng(rng_seed + (5 if dalam else 0))
        langkah = 1500 if len(trn) < 2000 else 3000
        t_mulai = time.time()
        for step in range(langkah):
            kon, pos, neg = batch_contoh(128, r)
            model.train()
            semua_idx = sorted(set([x for k in kon for x in k] + pos + [x for n in neg for x in n]))
            peta = {x: m for m, x in enumerate(semua_idx)}
            Z = model(Xt[semua_idx])
            c = torch.stack([Z[[peta[x] for x in k]].mean(dim=0) for k in kon])
            c = c / (c.norm(dim=-1, keepdim=True) + 1e-8)
            zp = Z[[peta[x] for x in pos]]
            zn = Z[[[peta[x] for x in n] for n in neg]]
            suhu = model.log_suhu.exp().clamp(max=100)
            lp = (c * zp).sum(-1, keepdim=True)
            ln = torch.einsum("bd,bkd->bk", c, zn)
            logits = torch.cat([lp, ln], dim=1) * suhu
            loss = torch.nn.functional.cross_entropy(logits, torch.zeros(len(pos), dtype=torch.long))
            opt.zero_grad()
            loss.backward()
            opt.step()
            if time.time() - t_mulai > 9 * 60:
                log(f"  batas waktu latih ({step} langkah)")
                break
        model.eval()
        with torch.no_grad():
            fz = model(Xt).numpy()
        skor, _ = fitb(fz, val)
        nama = "mlp" if dalam else "linear"
        hasil["model_" + nama] = skor
        log(f"  model {nama}: FITB uji {skor:.3f} (loss akhir {loss.item():.3f})")
        if terbaik is None or skor > terbaik[0]:
            terbaik = (skor, nama, fz)
    # pembanding jujur: CLIP netral-slot dipadatkan PCA-32 (tanpa belajar). Dipakai bila model kalah.
    xc0 = Xc - Xc.mean(axis=0)
    _, _, vt = np.linalg.svd(xc0[rng.permutation(len(xc0))[:20000]], full_matrices=False)
    zp = xc0 @ vt[:DIM].T
    zp /= np.linalg.norm(zp, axis=1, keepdims=True) + 1e-8
    skor_pca, _ = fitb(zp, val)
    hasil["clip_pca32"] = skor_pca
    log(f"  pembanding CLIP PCA-32: FITB {skor_pca:.3f}")
    if skor_pca > terbaik[0]:
        terbaik = (skor_pca, "clip_pca32", zp.astype("float32"))
    skor, nama, fz = terbaik
    hasil["dipakai"] = nama
    hasil["fitb_dipakai"] = skor
    hasil["auc_koherensi_model"] = auc_koherensi(fz, val)
    hasil["auc_koherensi_clip"] = auc_koherensi(Xc, val)
    hasil["soal_uji"] = n_uji
    hasil["outfit_latih"] = len(trn)
    hasil["outfit_uji"] = len(val)
    # layak dipakai server bila jelas di atas acak (0,25) dengan cukup soal uji
    hasil["layak"] = bool(skor >= 0.38 and n_uji >= 150)
    log(f"  DIPAKAI {nama}: FITB {skor:.3f} -> layak={hasil['layak']} | AUC koherensi {hasil['auc_koherensi_model']}")
    return {"ids": ids_all, "fz": fz, "hasil": hasil, "koherensi": koherensi, "idx_of": idx_of, "outfits": outfits}


# ---------------------------------------------------------------------------------------------
# 5. EKSPOR
# ---------------------------------------------------------------------------------------------
def tulis_json(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def ekspor(st, emb, warna, slot_of, zs, hasil_latih, statistik):
    versi = int(time.time())
    nama_gaya, p_gaya, nama_atr, p_atr, p_fem, ids_zs = zs
    pos_zs = {i: k for k, i in enumerate(ids_zs)}
    fz = idx_of = None
    if hasil_latih:
        fz, idx_of = hasil_latih["fz"], hasil_latih["idx_of"]
    # --- item: [slot, gender(0-100), hex, gayaBits, atrBits, v1..v32]
    shard = [dict() for _ in range(SHARD_ITEM)]
    for i in ids_zs:
        k = pos_zs[i]
        g_bits = 0
        urut = np.argsort(-p_gaya[k])[:2]
        for j in urut:
            if p_gaya[k][j] >= 0.15:
                g_bits |= 1 << int(j)
        a_bits = 0
        for j in range(len(nama_atr)):
            if p_atr[k][j] >= 0.80:
                a_bits |= 1 << j
        baris = [SLOT_KODE.get(slot_of.get(i, ""), 0), int(round(float(p_fem[k]) * 100)), warna.get(i, ""), g_bits, a_bits]
        if fz is not None and i in idx_of:
            baris += [int(round(float(x) * 127)) for x in fz[idx_of[i]]]
        shard[i % SHARD_ITEM][str(i)] = baris
    for s in range(SHARD_ITEM):
        tulis_json(f"model/item_{s}.json", {"versi": versi, "d": shard[s]})

    # --- bank: outfit lolos saring + skor koherensi (Q 0-100, persentil di bank) + gender outfit (G 0-100)
    seeds = list(st["outfit"].values())
    nilai = []
    for s in seeds:
        it = [(idx_of[i], sl) for i, sl in slot_item_seed(s) if idx_of and i in idx_of]
        kh = hasil_latih["koherensi"](fz, it) if (fz is not None and len(it) >= 3) else None
        gw = gs = 0.0
        for i, sl in slot_item_seed(s):
            if i in pos_zs and sl in SLOT_GENDER:
                gw += SLOT_GENDER[sl]
                gs += SLOT_GENDER[sl] * float(p_fem[pos_zs[i]])
        g = int(round(100 * gs / gw)) if gw > 0 else 50
        # kelayakan beli: inti (baju/celana/rambut/layered) harus bisa dibeli
        inti_ok = True
        n_beli = 0
        for i, sl in slot_item_seed(s):
            m = st["meta"].get(str(i))
            ok = bool(m and m.get("s") == 1 and m.get("p", -1) >= 0)
            n_beli += ok
            if sl in ("Shirt", "Pants", "Hair", "LayerAtas", "LayerBawah") and not ok:
                inti_ok = False
        nilai.append((s, kh, g, inti_ok, n_beli))
    kh_list = sorted(x[1] for x in nilai if x[1] is not None)

    def persentil(v):
        if v is None or not kh_list:
            return 50
        import bisect
        return int(round(100 * bisect.bisect_left(kh_list, v) / len(kh_list)))
    kandidat = []
    n_tolak_beli = n_tolak_koh = 0
    for s, kh, g, inti_ok, n_beli in nilai:
        if not inti_ok or n_beli < 3:
            n_tolak_beli += 1
            continue
        q = persentil(kh)
        if kh is not None and q < 10:
            n_tolak_koh += 1  # 10% paling tidak koheren menurut model: dibuang
            continue
        e = {k: v for k, v in s.items() if k in ("Sh", "Pa", "Gt", "A", "F", "BCn", "SC", "R", "H", "S")}
        e["Q"] = q
        e["G"] = g
        kandidat.append(e)
    kandidat.sort(key=lambda e: -e["Q"])
    kandidat = kandidat[:MAKS_BANK]
    bshard = [[] for _ in range(SHARD_BANK)]
    for e in kandidat:
        bshard[int(e["H"][:8], 16) % SHARD_BANK].append(e)
    for s in range(SHARD_BANK):
        tulis_json(f"bank/outfit_{s}.json", {"versi": versi, "seeds": bshard[s]})

    # --- meta harga snapshot untuk semua item di bank (server tetap validasi live, TTL)
    mshard = [dict() for _ in range(SHARD_ITEM)]
    for e in kandidat:
        for i in ids_seed(e):
            m = st["meta"].get(str(i))
            if m:
                mshard[i % SHARD_ITEM][str(i)] = [m.get("n", ""), m.get("p", -1), m.get("s", 0), m.get("c", ""), m.get("t", 0), m.get("w", 0)]
    for s in range(SHARD_ITEM):
        tulis_json(f"meta/harga_{s}.json", {"versi": versi, "d": mshard[s]})

    # --- validasi gender visual memakai label kata di nama item (bukan klaim, angka)
    pos, neg = [], []
    for i in ids_zs:
        m = st["meta"].get(str(i))
        if not m:
            continue
        lab = gender_label_nama(m.get("n"))
        if lab is None:
            continue
        (pos if lab == 1 else neg).append(float(p_fem[pos_zs[i]]))
    auc_gender = auc(pos, neg)
    hl = hasil_latih["hasil"] if hasil_latih else {"layak": False}
    info = {
        "versi": versi, "dibuat": datetime.now(timezone.utc).isoformat(), "putaran": st["putaran"],
        "model": MODEL_ID, "dim": DIM if hasil_latih else 0, "layak": bool(hl.get("layak")),
        "metrik": hl, "auc_gender_vs_nama": auc_gender, "n_label_gender": [len(pos), len(neg)],
        "n_item": len(ids_zs), "n_outfit_panen": len(st["outfit"]), "n_bank": len(kandidat),
        "bank_tolak_tidak_bisa_dibeli": n_tolak_beli, "bank_tolak_tidak_koheren": n_tolak_koh,
        "shard_item": SHARD_ITEM, "shard_bank": SHARD_BANK, "shard_meta": SHARD_ITEM,
        "slot_kode": SLOT_KODE, "gaya": nama_gaya, "atribut": nama_atr, "panen": statistik,
    }
    tulis_json("model/info.json", info)
    return info


def laporan(info, http):
    m = info["metrik"]
    f = lambda v: "-" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
    baris = [
        "# Laporan OTAK Katalog Praktis", "",
        f"- Dibuat: {info['dibuat']} | putaran ke-{info['putaran']}",
        f"- Outfit nyata terkumpul: **{info['n_outfit_panen']}** | masuk bank (lolos saring): **{info['n_bank']}**",
        f"  (ditolak karena item inti tidak bisa dibeli: {info['bank_tolak_tidak_bisa_dibeli']}, tidak koheren: {info['bank_tolak_tidak_koheren']})",
        f"- Item dengan sidik jari visual: **{info['n_item']}**",
        f"- Panen putaran ini: {json.dumps(info['panen'])} | permintaan HTTP {http.n}, kena 429: {http.n429}, gagal {http.gagal}", "",
        "## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)", "",
        "| Metode | Akurasi |", "|---|---|",
        f"| Acak | 0.250 |", f"| CLIP mentah | {f(m.get('clip_mentah'))} |", f"| CLIP netral-slot | {f(m.get('clip_netral_slot'))} |",
        f"| CLIP PCA-32 (tanpa belajar) | {f(m.get('clip_pca32'))} |", f"| Model linear (dilatih) | {f(m.get('model_linear'))} |", f"| Model MLP (dilatih) | {f(m.get('model_mlp'))} |", "",
        f"- Dipakai: **{m.get('dipakai', '-')}** | soal uji {m.get('soal_uji', '-')} | outfit latih {m.get('outfit_latih', '-')}, uji {m.get('outfit_uji', '-')}",
        f"- AUC koherensi (outfit asli vs setengah-diacak): model {f(m.get('auc_koherensi_model'))}, CLIP {f(m.get('auc_koherensi_clip'))}",
        f"- **LAYAK DIPAKAI SERVER: {'YA' if info['layak'] else 'BELUM'}** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)", "",
        "## Gender visual (zero-shot CLIP) dicek dengan kata di nama item",
        f"- AUC = {f(info['auc_gender_vs_nama'])} pada {info['n_label_gender'][0]} item berlabel wanita & {info['n_label_gender'][1]} pria",
        "  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)", "",
        "_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._",
    ]
    open("LAPORAN_OTAK.md", "w", encoding="utf-8").write("\n".join(baris) + "\n")
    ring = os.environ.get("GITHUB_STEP_SUMMARY")
    if ring:
        open(ring, "a", encoding="utf-8").write("\n".join(baris) + "\n")


def main():
    st = muat_state()
    st["putaran"] = st.get("putaran", 0) + 1
    log(f"putaran {st['putaran']} | bank {len(st['outfit'])} outfit | meta {len(st['meta'])} | STUB={STUB}")
    http = HttpStub() if STUB else Http()
    statistik = panen(http, st)
    simpan_state(st)
    lengkapi_meta(http, st)
    simpan_state(st)
    embedder = EmbedderStub() if STUB else EmbedderCLIP()
    emb, warna = mata(http, st, embedder)
    simpan_state(st)
    slot_of = slot_semua_item(st)
    ids_zs = sorted(i for i in emb if i in slot_of)
    if not ids_zs:
        log("tidak ada item berembedding -- berhenti")
        sys.exit(1)
    X = np.stack([emb[i] for i in ids_zs]).astype("float32")
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    nama_gaya, p_gaya, nama_atr, p_atr, p_fem = zero_shot(embedder, ids_zs, X, slot_of)
    hasil_latih = latih(st, emb, slot_of)
    info = ekspor(st, emb, warna, slot_of, (nama_gaya, p_gaya, nama_atr, p_atr, p_fem, ids_zs), hasil_latih, statistik)
    laporan(info, http)
    log(f"SELESAI: bank {info['n_bank']} outfit, {info['n_item']} item, layak={info['layak']}, AUC gender {info['auc_gender_vs_nama']}")


if __name__ == "__main__":
    main()
