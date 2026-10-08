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
                saring + skor koherensi), meta/ (harga snapshot). Server Roblox mengunduh lewat CDN jsDelivr
                (cadangan raw.githubusercontent.com) dan tetap memvalidasi harga live item yang ditampilkan.

Jadwal waktu satu putaran (v6, target +-70 menit, dulu +-155 menit):
  menit 0  : META (utas sendiri, host katalog, laju adaptif AIMD) + MATA-1 (host thumbnail) + PANEN GAYA (host avatar)
             berjalan BERSAMAAN -- dulu META serial setelah panen dan 80% permintaannya terbuang kena HTTP 429.
  ~menit 50: KREATOR (hanya bila antrean META kosong) -> MATA-2 (item baru) -> BELAJAR -> EKSPOR.

Variabel lingkungan: STUB=1 (uji alur tanpa jaringan/model), MENIT_PANEN, MAKS_KREATOR, MAKS_ITEM_BARU,
                     MENIT_MATA, CACHE_DIR.
"""
import collections
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
MENIT_PANEN = float(os.environ.get("MENIT_PANEN", "75") or 75)  # batas akhir panen kreator (menit sejak mulai)
MENIT_MATA = float(os.environ.get("MENIT_MATA", "45") or 45)  # waktu MATA tambahan setelah panen
MENIT_CARI = float(os.environ.get("MENIT_CARI", "8") or 8)  # dihitung dari AWAL fase cari (dulu dari T0 -> fase mati)
# META (harga/status jual) jalan di utas sendiri SEJAK AWAL, paralel dengan panen (host catalog.roblox.com beda dari
# avatar.roblox.com). Dulu fase ini serial SETELAH panen: 65 menit untuk 46% item karena 267 dari 336 permintaan kena 429.
MENIT_META = float(os.environ.get("MENIT_META", "45") or 45)
TTL_META_JUAL = 5 * 86400     # item yang bisa dibeli: dicek ulang tiap 5 hari (server Roblox tetap cek live item yang tampil)
TTL_META_TIDAK = 14 * 86400   # item tidak dijual/dihapus jarang kembali dijual: cukup tiap 14 hari
MAKS_DIMINTA = 6000           # item tak dikenal yang diminta pemain di map (kunci "itembaru" di DataStore)
# PETA BADAN: bagian badan avatar pemain (kunci "badanbaru") -> bundle yang berisi bagian itu, lewat
# catalog.roblox.com/v1/assets/{id}/bundles (API ini tidak bisa dipanggil dari server Roblox). Server memakai peta ini
# untuk baris "Badan" di Detail: beli bundle badan bila dijual & salin avatar orang lain utuh.
MAKS_BADAN_PER_PUTARAN = 400
MAKS_PETA_BADAN = 30000
TTL_PETA_BADAN = 30 * 86400
TIPE_BADAN = {17, 27, 28, 29, 30, 31, 79}  # Head, Torso, RightArm, LeftArm, LeftLeg, RightLeg, DynamicHead
MAKS_KREATOR = int(os.environ.get("MAKS_KREATOR", "600") or 600)
MAKS_ITEM_BARU = int(os.environ.get("MAKS_ITEM_BARU", "25000") or 25000)
MAKS_OUTFIT_PER_KREATOR = 8
# v5 PANEN GAYA: avatar pemain sungguhan dari komunitas fashion (anggota grup toko baju / aesthetic / gaya), BUKAN
# hanya kreator UGC (yang sering memakai kostum pajangan barangnya sendiri -> hasil terasa jelek/aneh)
MENIT_GAYA = float(os.environ.get("MENIT_GAYA", "40") or 40)
MAKS_PEMAIN_GAYA = int(os.environ.get("MAKS_PEMAIN_GAYA", "6000") or 6000)
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MAKS_GEMINI = int(os.environ.get("MAKS_GEMINI", "700") or 700)
KATA_GRUP_GAYA = """aesthetic outfits|outfit ideas|clothing store|clothes store|fashion|streetwear|y2k clothing|baddie|preppy|
emo clothing|kawaii clothing|cottagecore|grunge clothing|soft girl|e-girl|e-boy|korean fashion|old money|techwear|
gothic clothing|vintage clothing|alt fashion|layered clothing|3d clothing|aesthetic clothes|cute outfits|drip|
fashion famous|royale high|dress to impress|outfit codes|ugc fashion|designer clothing|luxury clothing""".replace("\n", "").split("|")
PROMPT_BAGUS = ["a stylish fashionable roblox avatar wearing a cohesive trendy outfit",
                "a well dressed roblox character with matching clothes, hair and accessories",
                "an aesthetic roblox avatar with a coordinated color palette"]
PROMPT_JELEK = ["a messy roblox avatar wearing random mismatched items",
                "a roblox avatar in a silly joke costume",
                "a plain default roblox avatar with no style",
                "a cluttered roblox avatar covered in too many accessories"]
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
    # kosakata desainer tambahan (ditambah di AKHIR supaya indeks bit lama tetap sama)
    "workwear": "a rugged workwear uniform or utility style avatar item",
    "coquette": "a coquette soft feminine bows and ribbons style avatar item",
    "baddie": "a trendy baddie bold fashion style avatar item",
    "grunge": "a grunge emo dark distressed style avatar item",
    "fairy": "a fairycore whimsical nature fairy style avatar item",
    "cute_animal": "a cute animal ears or plush creature style avatar item",
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
    """Klien HTTP sopan & adaptif per host. Roblox membatasi IP datacenter (runner GitHub) cukup ketat, jadi:
    jeda per host yang membesar saat 429 (hormati Retry-After) dan mengecil saat lancar, percobaan ulang sedikit,
    statistik per host dicatat supaya batasnya kelihatan di log. Aman dipakai beberapa thread (kunci per host)."""
    def __init__(self):
        import requests
        import threading
        self.threading = threading
        self.s = requests.Session()
        self.s.headers.update(HEADERS)
        adapter = requests.adapters.HTTPAdapter(pool_connections=8, pool_maxsize=16)
        self.s.mount("https://", adapter)
        self.jeda = {}
        self.terakhir = {}
        self.kunci = {}
        self.kunci_global = threading.Lock()
        self.stat = {}
        self.csrf = None
        self.n = 0
        self.n429 = 0
        self.gagal = 0
        self.blok = {}

    def _host(self, url):
        # kunci jeda per ENDPOINT (host + 2 segmen path): kalau Roblox membatasi per endpoint, endpoint lain tidak
        # ikut menunggu; kalau per host, mundur adaptif tiap kunci tetap menjaga laju di bawah batas
        bag = url.split("/")
        return "/".join(bag[2:5])

    # jeda minimum per host: catalog.roblox.com membatasi IP datacenter jauh lebih ketat dari host lain
    JEDA_DASAR = {"catalog.roblox.com": 1.0}

    def _dasar(self, host):
        return self.JEDA_DASAR.get(host.split("/")[0], 0.4)

    def _st(self, host):
        with self.kunci_global:
            if host not in self.stat:
                self.stat[host] = {"n": 0, "ok": 0, "429": 0, "err": 0, "kode": {}}
                self.kunci[host] = self.threading.Lock()
                self.jeda.setdefault(host, self._dasar(host))
            return self.stat[host]

    def _tunggu(self, host):
        self._st(host)
        with self.kunci[host]:
            # cooldown bersama setelah 429: SEMUA utas berhenti menembak host ini sampai jendelanya lewat
            blok = self.blok.get(host, 0) - time.time()
            if blok > 0:
                time.sleep(blok)
            dt = time.time() - self.terakhir.get(host, 0)
            if dt < self.jeda[host]:
                time.sleep(self.jeda[host] - dt)
            self.terakhir[host] = time.time()

    def _kirim(self, metode, url, coba, **kw):
        host = self._host(url)
        st = self._st(host)
        for k in range(coba):
            self._tunggu(host)
            try:
                r = self.s.request(metode, url, timeout=20, **kw)
            except Exception:
                st["err"] += 1
                time.sleep(3)
                continue
            st["n"] += 1
            self.n += 1
            if r.status_code == 200:
                st["ok"] += 1
                # AIMD: turun pelan (aditif) saat lancar -- dulu x0,88 tiap sukses membuat jeda cepat kembali ke 0,4 dtk
                # lalu kena 429 lagi (gergaji): 267 dari 336 permintaan katalog terbuang
                self.jeda[host] = max(self._dasar(host), self.jeda[host] - 0.05)
                return r
            if r.status_code == 403 and r.headers.get("x-csrf-token") and metode == "POST":
                self.csrf = r.headers["x-csrf-token"]
                kw.setdefault("headers", {})["x-csrf-token"] = self.csrf
                continue
            if r.status_code == 429:
                st["429"] += 1
                self.n429 += 1
                self.jeda[host] = min(20.0, self.jeda[host] * 1.5 + 1.0)
                ra = r.headers.get("Retry-After", "")
                tunggu = float(ra) if ra.replace(".", "", 1).isdigit() else self.jeda[host] * 3
                self.blok[host] = time.time() + min(90.0, tunggu)
                continue
            st["kode"][str(r.status_code)] = st["kode"].get(str(r.status_code), 0) + 1
            if r.status_code >= 500:
                time.sleep(3)
                continue
            self.gagal += 1
            return None
        self.gagal += 1
        return None

    def get(self, url, params=None, coba=3):
        r = self._kirim("GET", url, coba, params=params)
        if r is None:
            return None
        try:
            return r.json()
        except Exception:
            return None

    def post_katalog(self, body, coba=4):
        h = {"Content-Type": "application/json"}
        if self.csrf:
            h["x-csrf-token"] = self.csrf
        r = self._kirim("POST", "https://catalog.roblox.com/v1/catalog/items/details", coba, data=json.dumps(body), headers=h)
        if r is None:
            return None
        try:
            return r.json()
        except Exception:
            return None

    def gambar(self, url):
        for k in range(3):
            try:
                r = self.s.get(url, timeout=20)
                if r.status_code == 200 and r.content:
                    return r.content
            except Exception:
                pass
            time.sleep(1.5 * (k + 1))
        return None

    def ringkas(self):
        return " | ".join(f"{h.replace('.roblox.com', '')}: ok {v['ok']}/{v['n']}, 429 {v['429']}, jeda {self.jeda.get(h, 0):.1f}s, kode {v['kode']}"
                          for h, v in sorted(self.stat.items()))


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
        if "groups/search" in url:
            return {"data": [{"id": 7000 + k, "memberCount": 5000} for k in range(3)]}
        if "/users" in url and "/groups/" in url:
            gid = int(url.split("/groups/")[1].split("/")[0])
            return {"data": [{"user": {"userId": gid * 10 + k}} for k in range(40)], "nextPageCursor": None}
        if "/groups/" in url:
            return {"owner": {"userId": 900 + int(url.rstrip("/").split("/")[-1]) % 50}}
        if "thumbnails" in url and "userIds" in (params or {}):
            ids = [int(x) for x in params["userIds"].split(",")]
            return {"data": [{"targetId": i, "state": "Completed", "imageUrl": f"stub://{10000 + i % 3000}"} for i in ids]}
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

    def ringkas(self):
        return f"stub n={self.n}"

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
def muat_state_v5(st):
    st.setdefault("pemain", {})
    return st


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


import threading as _threading
KUNCI_ST = _threading.RLock()  # st["meta"] ditulis utas meta, st disimpan utas utama -> wajib bergiliran


def simpan_state(st):
    os.makedirs(os.path.dirname(P_STATE), exist_ok=True)
    with KUNCI_ST:
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
    m = {"n": (e.get("name") or "")[:80], "p": int(price) if isinstance(price, (int, float)) else -1,
         "s": 1 if bisa else 0, "c": (e.get("creatorName") or "")[:40], "t": at, "w": int(time.time())}
    # bahan TREN: jumlah favorit + umur item (item baru yang cepat difavoritkan = sedang naik daun)
    fav = e.get("favoriteCount")
    if isinstance(fav, int) and fav >= 0:
        m["f"] = fav
    dibuat = e.get("itemCreatedUtc")
    if isinstance(dibuat, str) and len(dibuat) >= 10:
        try:
            m["d"] = int(datetime.strptime(dibuat[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() // 86400)
        except Exception:
            pass
    return m


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
def cari_kreator(http, st):
    """Cari item per kata kunci (catalog) -> item + meta + daftar kreator. Maks MENIT_CARI menit."""
    putaran = st["putaran"]
    rng = random.Random(putaran * 7919 + 13)
    kata = KATA_KUNCI[:]
    rng.shuffle(kata)
    mulai = (putaran * KATA_PER_PUTARAN) % len(kata)
    kata = (kata + kata)[mulai:mulai + KATA_PER_PUTARAN]
    kreator_user, kreator_grup = {}, {}
    n_item_cari = 0
    k_i = 0
    mulai_fase = time.time()
    for k_i, kw in enumerate(kata):
        if time.time() > mulai_fase + MENIT_CARI * 60:
            break
        for kategori in ("1", "3"):
            js = http.get("https://catalog.roblox.com/v2/search/items/details",
                          {"Keyword": kw, "Category": kategori, "Limit": "120", "SortType": "0"})
            for e in (js or {}).get("data", []) or []:
                if e.get("itemType") != "Asset":
                    continue
                i = e.get("id")
                if not isinstance(i, int):
                    continue
                if e.get("assetType") in ASET_KE_SLOT:
                    with KUNCI_ST:
                        st["meta"][str(i)] = meta_dari_katalog(e)
                    n_item_cari += 1
                cid = e.get("creatorTargetId")
                if not isinstance(cid, int) or cid == 1:
                    continue
                if e.get("creatorType") == "User":
                    kreator_user[cid] = kreator_user.get(cid, 0) + 1
                elif e.get("creatorType") == "Group":
                    kreator_grup[cid] = kreator_grup.get(cid, 0) + 1
        if k_i % 20 == 19:
            log(f"  cari {k_i + 1} kata | item {n_item_cari} | kreator user {len(kreator_user)} grup {len(kreator_grup)} | {http.ringkas()}")
    log(f"pencarian: {k_i + 1} kata kunci, {n_item_cari} item katalog, kreator user {len(kreator_user)}, grup {len(kreator_grup)}")
    # pemilik grup = desainer di balik toko grup (maks 3 menit)
    batas = time.time() + 3 * 60
    for gid, _ in sorted(kreator_grup.items(), key=lambda x: -x[1])[:150]:
        if time.time() > batas:
            break
        js = http.get(f"https://groups.roblox.com/v1/groups/{gid}", coba=2)
        uid = ((js or {}).get("owner") or {}).get("userId")
        if isinstance(uid, int):
            kreator_user[uid] = kreator_user.get(uid, 0) + kreator_grup[gid]
    antre = [u for u, _ in sorted(kreator_user.items(), key=lambda x: -x[1]) if hash_kreator(u) not in st["kreator"]]
    log(f"kreator baru untuk dibaca: {len(antre)} (sudah pernah: {len(st['kreator'])}) | {http.ringkas()}")
    return antre


def panen(http, st, antre):
    batas_waktu = T0 + MENIT_PANEN * 60
    n_kreator = n_outfit = n_tolak = n_mirip = n_kosong = 0
    t_log = time.time()
    for uid in antre[:MAKS_KREATOR]:
        if time.time() > batas_waktu:
            log("batas waktu panen tercapai, sisanya putaran berikutnya")
            break
        hasil_kreator = []
        js = http.get(f"https://avatar.roblox.com/v2/avatar/users/{uid}/outfits",
                      {"page": "1", "itemsPerPage": "50", "isEditable": "true"}, coba=2)
        daftar = [o for o in (js or {}).get("data", []) or [] if o.get("outfitType", "Avatar") == "Avatar"]
        if not daftar:
            n_kosong += 1
        sumber = [f"https://avatar.roblox.com/v1/outfits/{o['id']}/details" for o in daftar[:MAKS_OUTFIT_PER_KREATOR]]
        sumber.append(f"https://avatar.roblox.com/v1/users/{uid}/avatar")
        for url in sumber:
            if time.time() > batas_waktu:
                break
            d = http.get(url, coba=2)
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
                seed["K"] = hash_kreator(uid)[:6]  # untuk membagi uji per kreator (bukan identitas)
                st["outfit"][seed["H"]] = seed
                n_outfit += 1
        st["kreator"][hash_kreator(uid)] = int(time.time())
        n_kreator += 1
        if n_kreator % 10 == 0:
            simpan_state(st)
        if time.time() - t_log > 180:
            t_log = time.time()
            log(f"  kreator {n_kreator}: +{n_outfit} outfit (tolak {n_tolak}, kembar {n_mirip}, tanpa outfit {n_kosong}) | {http.ringkas()}")
    log(f"PANEN selesai: {n_kreator} kreator dibaca, +{n_outfit} outfit baru, total bank {len(st['outfit'])} | {http.ringkas()}")
    return {"kreator": n_kreator, "outfit_baru": n_outfit, "ditolak": n_tolak, "kembar": n_mirip, "tanpa_outfit": n_kosong}


# ---------------------------------------------------------------------------------------------
# 1b. PANEN GAYA (v5) + NILAI ESTETIKA
# ---------------------------------------------------------------------------------------------
class Penilai:
    """Menilai foto avatar 0-100. CLIP zero-shot selalu ada (gratis, offline). Bila secret GEMINI_API_KEY dipasang,
    foto yang lolos CLIP dinilai lagi oleh Gemini (gratis, kuota harian dibatasi MAKS_GEMINI) -> penilaian gaya
    jauh lebih manusiawi. Tanpa key: CLIP saja."""
    def __init__(self, embedder):
        self.e = embedder
        self.tb = embedder.teks(PROMPT_BAGUS).mean(axis=0)
        self.tj = embedder.teks(PROMPT_JELEK).mean(axis=0)
        self.riwayat = []
        self.n_gemini = 0
        self.model_gemini = None
        self.gemini_mati = not GEMINI_KEY
        self.t_gemini = 0.0

    def clip(self, ims):
        f = self.e.gambar(ims)
        raw = f @ self.tb - f @ self.tj
        return [float(x) for x in raw]

    def persen(self, raw):
        # persentil terhadap semua skor yang pernah dilihat putaran ini (skala relatif, stabil antar batch)
        self.riwayat.append(raw)
        r = sorted(self.riwayat[-5000:])
        import bisect
        return int(round(100 * bisect.bisect_left(r, raw) / max(1, len(r))))

    def _pilih_model(self, http):
        import requests
        try:
            r = requests.get("https://generativelanguage.googleapis.com/v1beta/models", params={"key": GEMINI_KEY, "pageSize": 200}, timeout=30)
            daftar = r.json().get("models", []) if r.status_code == 200 else []
        except Exception:
            daftar = []
        calon = [m["name"] for m in daftar if "generateContent" in (m.get("supportedGenerationMethods") or [])
                 and "flash" in m.get("name", "") and "image" not in m.get("name", "") and "tts" not in m.get("name", "")
                 and "live" not in m.get("name", "") and "exp" not in m.get("name", "")]
        def kunci(n):
            angka = re.findall(r"(\d+(?:\.\d+)?)", n)
            v = float(angka[0]) if angka else 0
            return (v, "lite" not in n, "preview" not in n)
        calon.sort(key=kunci, reverse=True)
        self.model_gemini = calon[0] if calon else None
        log(f"  Gemini: model dipilih {self.model_gemini} dari {len(calon)} calon")
        if not self.model_gemini:
            self.gemini_mati = True

    def gemini(self, http, png):
        if self.gemini_mati or self.n_gemini >= MAKS_GEMINI:
            return None
        if self.model_gemini is None:
            self._pilih_model(http)
            if self.gemini_mati:
                return None
        import requests, base64
        jeda = 6.5 - (time.time() - self.t_gemini)  # aman di bawah ~10 permintaan/menit kuota gratis
        if jeda > 0:
            time.sleep(jeda)
        self.t_gemini = time.time()
        prompt = ("You are a strict Roblox avatar fashion judge. Rate this avatar's OUTFIT from 1 to 10 for style: cohesion, "
                  "color harmony, trendiness and completeness (hair, top, bottom, shoes, tasteful accessories). Joke items, "
                  "mascot costumes, random mismatched pieces, clutter or a default look must score 1-4. Only genuinely stylish, "
                  "put-together outfits score 8-10. Reply ONLY with JSON: {\"skor\": <integer 1-10>, \"gaya\": \"<2-3 word style name>\"}")
        body = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(png).decode()}}]}],
                "generationConfig": {"temperature": 0.1, "maxOutputTokens": 60}}
        for k in range(2):
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/{self.model_gemini}:generateContent",
                                  params={"key": GEMINI_KEY}, json=body, timeout=60)
            except Exception:
                time.sleep(5)
                continue
            if r.status_code == 429:
                log("  Gemini: kuota habis/terbatas (429) -> sisa putaran memakai CLIP saja")
                self.gemini_mati = True
                return None
            if r.status_code in (400, 401, 403, 404):
                log(f"  Gemini: ditolak {r.status_code} -> CLIP saja. {r.text[:160]}")
                self.gemini_mati = True
                return None
            if r.status_code != 200:
                time.sleep(5)
                continue
            self.n_gemini += 1
            try:
                teks = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                m = re.search(r"\{.*\}", teks, re.S)
                d = json.loads(m.group(0)) if m else {}
                v = int(d.get("skor"))
                if 1 <= v <= 10:
                    return v, str(d.get("gaya", ""))[:30]
            except Exception:
                return None
        return None


def cari_pemain_gaya(http, st):
    """Grup komunitas fashion -> anggota terbaru (pemain aktif yang peduli gaya). Hanya hash yang disimpan."""
    rng = random.Random(st["putaran"] * 31 + 7)
    kata = KATA_GRUP_GAYA[:]
    rng.shuffle(kata)
    grup = {}
    batas = time.time() + 3 * 60
    for kw in kata:
        if time.time() > batas:
            break
        js = http.get("https://groups.roblox.com/v1/groups/search", {"keyword": kw, "prioritizeExactMatch": "false", "limit": "25"}, coba=2)
        for g in (js or {}).get("data", []) or []:
            if isinstance(g.get("id"), int) and (g.get("memberCount") or 0) >= 2000:
                grup[g["id"]] = g.get("memberCount") or 0
    log(f"GAYA: {len(grup)} grup komunitas fashion ditemukan | {http.ringkas()}")
    pemain = {}
    batas = time.time() + 5 * 60
    daftar_grup = list(grup)
    rng.shuffle(daftar_grup)
    for gid in daftar_grup:
        if time.time() > batas or len(pemain) >= MAKS_PEMAIN_GAYA * 2:
            break
        kursor = ""
        for _ in range(2):
            p = {"limit": "100", "sortOrder": "Desc"}
            if kursor:
                p["cursor"] = kursor
            js = http.get(f"https://groups.roblox.com/v1/groups/{gid}/users", p, coba=2)
            for u in (js or {}).get("data", []) or []:
                uid = ((u.get("user") or {}).get("userId"))
                if isinstance(uid, int) and hash_kreator(uid) not in st["pemain"]:
                    pemain[uid] = 1
            kursor = (js or {}).get("nextPageCursor") or ""
            if not kursor:
                break
    antre = list(pemain)
    rng.shuffle(antre)
    log(f"GAYA: {len(antre)} pemain baru untuk dibaca (sudah pernah: {len(st['pemain'])})")
    return antre[:MAKS_PEMAIN_GAYA]


def panen_gaya(http, st, antre, penilai):
    """Avatar pemain (v2, endpoint yang tidak kena batas ketat) -> seed. Fotonya dinilai (CLIP, lalu Gemini untuk yang
    menjanjikan). Hanya seed + nilai yang disimpan; userId TIDAK disimpan."""
    from PIL import Image
    batas = time.time() + MENIT_GAYA * 60
    n_baca = n_masuk = n_tolak = n_gemini = 0
    t_log = time.time()
    for a in range(0, len(antre), 50):
        if time.time() > batas:
            log("GAYA: batas waktu, sisanya putaran berikutnya")
            break
        potong = antre[a:a + 50]
        calon = {}
        for uid in potong:
            if time.time() > batas:
                break
            d = http.get(f"https://avatar.roblox.com/v2/avatar/users/{uid}/avatar", coba=2)
            st["pemain"][hash_kreator(uid)] = int(time.time())
            n_baca += 1
            seed = seed_dari_avatar(d)
            if not seed or seed["H"] in st["outfit"]:
                n_tolak += 1
                continue
            calon[uid] = seed
        if not calon:
            continue
        js = http.get("https://thumbnails.roblox.com/v1/users/avatar", {"userIds": ",".join(map(str, calon)), "size": "352x352",
                                                                      "format": "Png", "isCircular": "false"})
        foto = {}
        for e in (js or {}).get("data", []) or []:
            uid = e.get("targetId")
            if uid in calon and e.get("state") == "Completed" and e.get("imageUrl"):
                b = http.gambar(e["imageUrl"])
                if b:
                    foto[uid] = b
        ims, uids = [], []
        for uid, b in foto.items():
            try:
                im = Image.open(io.BytesIO(b)).convert("RGBA")
                alas = Image.new("RGBA", im.size, (235, 235, 235, 255))
                alas.alpha_composite(im)
                ims.append(alas.convert("RGB"))
                uids.append(uid)
            except Exception:
                pass
        if not ims:
            continue
        raw = penilai.clip(ims)
        for k, uid in enumerate(uids):
            seed = calon[uid]
            pc = penilai.persen(raw[k])
            nilai = pc
            if pc >= 55:  # hanya yang menjanjikan dikirim ke Gemini (hemat kuota)
                g = penilai.gemini(http, foto[uid])
                if g:
                    n_gemini += 1
                    nilai = int(round(0.7 * g[0] * 10 + 0.3 * pc))
                    seed["NG"] = g[0]
                    if g[1]:
                        seed["GY"] = g[1]
            if nilai < 45:
                n_tolak += 1
                continue
            seed["S"] = "gaya"
            seed["N"] = nilai
            seed["T"] = int(time.time())
            seed["K"] = "g" + hash_kreator(uid)[:5]
            st["outfit"][seed["H"]] = seed
            n_masuk += 1
        if time.time() - t_log > 180:
            t_log = time.time()
            log(f"  GAYA: dibaca {n_baca}, masuk {n_masuk} (nilai Gemini {n_gemini}), tolak {n_tolak} | {http.ringkas()}")
            simpan_state(st)
    log(f"GAYA selesai: dibaca {n_baca} pemain, +{n_masuk} outfit bergaya, dinilai Gemini {n_gemini}, ditolak {n_tolak}")
    return {"gaya_dibaca": n_baca, "gaya_masuk": n_masuk, "gaya_gemini": n_gemini}


# ---------------------------------------------------------------------------------------------
# 2. META untuk item di outfit yang belum punya meta (atau meta > 3 hari)
# ---------------------------------------------------------------------------------------------
def perlu_meta(st, ids, sekarang=None):
    """Item yang metanya belum ada / sudah lewat TTL berjenjang. Urut: belum ada dulu, lalu yang paling basi."""
    sekarang = sekarang or time.time()
    baru, basi = [], []
    for i in ids:
        m = st["meta"].get(str(i))
        if not m:
            baru.append(i)
            continue
        ttl = TTL_META_JUAL if m.get("s") == 1 else TTL_META_TIDAK
        umur = sekarang - m.get("w", 0)
        if umur > ttl:
            basi.append((umur, i))
    basi.sort(reverse=True)
    return baru, [i for _, i in basi]


class PekerjaMeta:
    """Utas META: antrean berprioritas (item yang diminta pemain & item outfit baru di depan), satu host, laju adaptif.
    Hasil ditulis ke st["meta"] di bawah KUNCI_ST. Antrean bisa ditambah utas utama selama panen berjalan."""
    def __init__(self, http, st, batas_waktu):
        self.http, self.st, self.batas = http, st, batas_waktu
        self.antre_depan, self.antre = [], []
        self.lihat = set()
        self.kunci = _threading.Lock()
        self.n_diminta = self.n_dapat = self.n_hilang = 0
        self.panen_selesai = False
        self.utas = _threading.Thread(target=self.jalan, daemon=True)

    def tambah(self, ids, depan=False):
        with self.kunci:
            for i in ids:
                if i not in self.lihat:
                    self.lihat.add(i)
                    (self.antre_depan if depan else self.antre).append(i)

    def _ambil(self, n):
        with self.kunci:
            out = self.antre_depan[:n]
            self.antre_depan = self.antre_depan[n:]
            if len(out) < n:
                k = n - len(out)
                out += self.antre[:k]
                self.antre = self.antre[k:]
            return out

    def sisa(self):
        with self.kunci:
            return len(self.antre_depan) + len(self.antre)

    def jalan(self):
        while time.time() < self.batas:
            potong = self._ambil(100)
            if not potong:
                if self.panen_selesai:
                    break
                time.sleep(2)
                continue
            self.n_diminta += len(potong)
            js = self.http.post_katalog({"items": [{"itemType": "Asset", "id": i} for i in potong]})
            if js is None:
                self.tambah_ulang(potong)  # gagal jaringan/429: JANGAN tandai apa pun, coba lagi nanti
                continue
            dapat = {}
            for e in js.get("data", []) or []:
                i = e.get("id")
                if isinstance(i, int):
                    dapat[i] = meta_dari_katalog(e)
            with KUNCI_ST:
                for i, m in dapat.items():
                    self.st["meta"][str(i)] = m
                for i in potong:
                    if i not in dapat:
                        # tidak ada di katalog (dihapus/disembunyikan) -> tandai tidak bisa dibeli (dicek ulang 14 hari lagi)
                        self.st["meta"][str(i)] = {"n": "", "p": -1, "s": 0, "c": "", "t": 0, "w": int(time.time())}
                        self.n_hilang += 1
            self.n_dapat += len(dapat)

    def tambah_ulang(self, ids):
        with self.kunci:
            self.antre = list(ids) + self.antre

    def ringkas(self):
        return {"diminta": self.n_diminta, "diperbarui": self.n_dapat, "hilang": self.n_hilang, "sisa_antre": self.sisa()}


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


def mata(http, st, embedder, emb, warna, batas, gagal_baru, label="MATA"):
    """Thumbnail -> CLIP untuk item yang belum punya embedding. Aman jalan di thread (tidak menulis st)."""
    from PIL import Image
    di_outfit = set()
    for s in list(st["outfit"].values()):
        di_outfit.update(ids_seed(s))
    universe = set(di_outfit)
    with KUNCI_ST:
        daftar_meta = list(st["meta"].items())
    for k, m in daftar_meta:
        if m.get("t") in ASET_KE_SLOT:
            universe.add(int(k))
    gagal_lama = st.get("gagal_thumb", {})
    target = [i for i in universe if i not in emb and str(i) not in gagal_lama and str(i) not in gagal_baru]
    target.sort(key=lambda i: (0 if i in di_outfit else 1, i))  # item yang ada di outfit dulu
    target = target[:MAKS_ITEM_BARU]
    log(f"{label}: universe {len(universe)} item, sudah ada {len(emb)}, akan dihitung {len(target)}")
    md5_hitung = {}
    t_log = time.time()
    for a in range(0, len(target), 50):
        if time.time() > batas:
            log(f"  {label}: batas waktu, sisanya putaran berikutnya")
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
                    gagal_baru[str(i)] = 1  # placeholder
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
                gagal_baru[str(i)] = 1
        for b0 in range(0, len(ims), 32):
            f = embedder.gambar(ims[b0:b0 + 32])
            for k, i in enumerate(ids_ok[b0:b0 + 32]):
                emb[i] = f[k]
        if time.time() - t_log > 240:
            t_log = time.time()
            log(f"  {label}: {a + len(potong)}/{len(target)} | total embedding {len(emb)}")
            simpan_emb(emb, warna)
    simpan_emb(emb, warna)


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
    # panjang rambut (khusus slot Hair): ikut menentukan kesan gender & gaya
    global P_RAMBUT_PANJANG
    P_RAMBUT_PANJANG = np.full(len(ids), 0.5, dtype="float32")
    idx = np.where(slots == "Hair")[0]
    if len(idx):
        tp = embedder.teks(["a long hairstyle for an avatar", "long flowing hair", "very long hair past the shoulders"]).mean(axis=0)
        ts = embedder.teks(["a short hairstyle for an avatar", "short cropped hair", "a buzz cut or short haircut"]).mean(axis=0)
        tp /= np.linalg.norm(tp)
        ts /= np.linalg.norm(ts)
        P_RAMBUT_PANJANG[idx] = 1 / (1 + np.exp(-(100 * X[idx] @ tp - 100 * X[idx] @ ts)))
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
    # bagi latih/uji PER KREATOR (outfit satu kreator sering berbagi item -> kalau tercampur, nilai uji bocor/terlalu
    # bagus). Outfit lama tanpa tanda kreator dibagi per hash outfit.
    kunci_bagi = {h: (st["outfit"][h].get("K") or h) for h, _ in outfits}
    def uji(h):
        return int(hashlib.md5(kunci_bagi[h].encode()).hexdigest()[:4], 16) % 100 < 15
    val = [o for o in outfits if uji(o[0])]
    trn = [o for o in outfits if not uji(o[0])]
    # outfit yang DIFAVORITKAN/DIBELI pemain sungguhan = sinyal paling berharga -> bobot 3x saat latih
    trn += [o for o in trn if st["outfit"][o[0]].get("S") == "sinyal"] * 2
    tolak = []
    for h, s in sorted(st.get("tolak", {}).items()):
        it = [idx_of[i] for i, sl in slot_item_seed(s) if i in idx_of and sl not in ("Alis",)]
        if len(it) >= 3:
            tolak.append(it)
    log(f"  contoh negatif dari jempol bawah pemain: {len(tolak)} outfit")
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
            if tolak:
                # outfit yang pemain tidak sukai: kemiripan antar itemnya didorong turun (di bawah 0,1)
                pilih = [tolak[int(r.integers(len(tolak)))] for _ in range(min(32, len(tolak)))]
                kn = []
                for it in pilih:
                    zt = model(Xt[it])
                    m = zt @ zt.T
                    n = len(it)
                    kn.append((m.sum() - m.diagonal().sum()) / (n * (n - 1)))
                loss = loss + 0.5 * torch.relu(torch.stack(kn) - 0.1).mean()
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
# 4b. BELAJAR DESAIN (desain v1, 9 Okt 2026): yang dipelajari adalah PROSES desainer, bukan outfitnya.
#   Dari outfit buatan pemain sungguhan, otak belajar: "kalau item utama (MC) seperti ini, bumbu (item lain)
#   seperti apa yang dipilih desainer?" -> bobot penilai per slot (vektor gaya, harmoni warna, set/kreator sama,
#   tren, popularitas di kalangan desainer, konteks item yang sudah dipasang), tabel harmoni warna (PMI), resep
#   (slot apa yang biasa dipakai bersama), dan jumlah aksesori. Server Roblox MENYUSUN outfit dari nol memakai
#   ini; bank outfit tidak lagi disalin. Uji jujur: outfit uji (kreator berbeda dari latih) -> peringkat item asli
#   di antara SEMUA item slotnya, dibandingkan cos vektor saja.
# ---------------------------------------------------------------------------------------------
DESAIN_VERSI = 1
DESAIN_SLOT = [1, 2, 13, 14, 6, 5, 7, 8, 9, 10, 11, 12]
DESAIN_FITUR = ["cos", "pmiWarna", "gayaSama", "bedaGender", "tren", "pop", "kreatorSama", "satC", "valC", "satCxM",
                "setSama", "cosKonteks", "pmiKonteks", "kreatorKonteks", "setKonteks", "adaKonteks"]
DESAIN_AKS = [5, 7, 8, 9, 10, 11, 12]
# sama persis dengan KATA_UMUM / KATA_WARNA / pecahKata di IndeksOutfitEngine (server)
KATA_UMUM_D = set("the and with for from new set full outfit style limited ugc free shirt shirts pants pant top tops "
                  "bottom bottoms tee tees jeans jean skirt shorts trousers classic layered version edition kaus kaos "
                  "celana baju atasan bawahan".split())
KATA_WARNA_D = set("black white pink blue red green purple yellow brown grey gray orange beige dark light cream navy "
                   "hitam putih merah biru hijau ungu kuning coklat cokelat abu cute aesthetic boy girl boys girls men "
                   "women mens womens".split())


def warna_desain(hx):
    """-> (bin 0-15, saturasi, value). 0-11 = rona (30 derajat), 12 hitam, 13 putih, 14 abu, 15 tanpa warna.
    Sama persis dengan binWarna di DesainerEngine (Color3.fromHex():ToHSV())."""
    import colorsys
    try:
        r, g, b = int(hx[0:2], 16) / 255, int(hx[2:4], 16) / 255, int(hx[4:6], 16) / 255
    except Exception:
        return 15, 0.0, 0.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if v < 0.18:
        return 12, s, v
    if s < 0.18:
        return (13 if v > 0.82 else 14), s, v
    return int(h * 12 + 0.5) % 12, s, v


def token_desain(nama):
    return {w for w in re.findall(r"[a-z0-9]+", (nama or "").lower()) if len(w) >= 3 and not w.isdigit() and w not in KATA_UMUM_D}


def logreg_irls(X, y, bobot_pos=6.0, l2=1.0, iterasi=30):
    Xb = np.hstack([X, np.ones((len(X), 1), dtype=np.float64)])
    w = np.zeros(Xb.shape[1])
    sw = np.where(y == 1, bobot_pos, 1.0)
    reg = np.ones(Xb.shape[1]) * l2
    reg[-1] = 0
    for _ in range(iterasi):
        z = np.clip(Xb @ w, -30, 30)
        p = 1 / (1 + np.exp(-z))
        g = Xb.T @ (sw * (p - y)) + reg * w
        H = (Xb * (sw * p * (1 - p))[:, None]).T @ Xb + np.diag(reg)
        step = np.linalg.solve(H, g)
        w -= step
        if np.abs(step).max() < 1e-7:
            break
    return w


def belajar_desain(st, hasil_latih, baris_of, tren, batas_detik=600, seed=3):
    """baris_of: {id: baris ekspor [slot, fem, hex, gb, ab, v1..v32]}. -> (desain dict untuk info.json, {id: pop*100})"""
    t0 = time.time()
    rng = np.random.default_rng(seed)
    ids = sorted(i for i, b in baris_of.items() if len(b) >= 5 + DIM)
    if len(ids) < 1000:
        return None, {}
    pos = {i: k for k, i in enumerate(ids)}
    n = len(ids)
    V = np.array([baris_of[i][5:5 + DIM] for i in ids], dtype=np.float32) / 127.0
    SL = np.array([baris_of[i][0] for i in ids])
    FEM = np.array([baris_of[i][1] for i in ids], dtype=np.float32)
    GB = np.array([baris_of[i][3] for i in ids], dtype=np.int64)
    BIN = np.zeros(n, dtype=np.int64)
    SAT = np.zeros(n, dtype=np.float32)
    VAL = np.zeros(n, dtype=np.float32)
    for k, i in enumerate(ids):
        BIN[k], SAT[k], VAL[k] = warna_desain(baris_of[i][2] or "")
    TR = np.array([(tren[i] / 100.0) if i in tren else 0.5 for i in ids], dtype=np.float32)
    meta = st["meta"]
    nama = [(meta.get(str(i)) or {}).get("n") or "" for i in ids]
    kre = [((meta.get(str(i)) or {}).get("c") or "").lower() for i in ids]
    peta_kre = {}
    CRE = np.array([peta_kre.setdefault(c, len(peta_kre)) if c else -1 for c in kre])
    TOK = [token_desain(x) for x in nama]
    df = collections.Counter()
    for t in TOK:
        df.update(t)
    KHAS = [{w for w in t if w not in KATA_WARNA_D and df[w] <= 150} for t in TOK]

    def satu_set(a, b):
        if a == b:
            return False
        if KHAS[a] & KHAS[b]:
            return True
        if kre[a] and kre[a] == kre[b] and (TOK[a] & TOK[b]) - KATA_WARNA_D:
            return True
        A, B = TOK[a] - KATA_WARNA_D, TOK[b] - KATA_WARNA_D
        s = A & B
        return any(len(w) >= 4 for w in s) and len(s) / max(1, len(A | B)) >= 0.5

    # outfit nyata (item yang punya baris), dibagi latih/uji PER KREATOR seperti latih()
    outfits = []
    for h, s in sorted(st["outfit"].items()):
        it = [pos[i] for i, sl in slot_item_seed(s) if i in pos and sl != "Alis"]
        if len(it) >= 3:
            outfits.append((h, it, int(hashlib.md5((s.get("K") or h).encode()).hexdigest()[:4], 16) % 100 < 15))
    trn = [o for o in outfits if not o[2]]
    val = [o for o in outfits if o[2]]
    # popularitas di kalangan desainer + harmoni warna (PMI 16x16) dari outfit latih
    FREQ = np.zeros(n, dtype=np.float32)
    cooc = np.ones((16, 16)) * 0.5
    marg = np.ones(16) * 0.5
    for _, it, _ in trn:
        for x in it:
            FREQ[x] += 1
        bs = [BIN[x] for x in it]
        for a in range(len(bs)):
            marg[bs[a]] += 1
            for b in range(len(bs)):
                if a != b:
                    cooc[bs[a], bs[b]] += 1
    PMI = np.log((cooc / cooc.sum()) / np.outer(marg / marg.sum(), marg / marg.sum()))
    LF = np.log1p(FREQ)
    pool = {s: np.where(SL == s)[0] for s in DESAIN_SLOT}
    peluang = {}
    for s in DESAIN_SLOT:
        w = FREQ[pool[s]] ** 0.75
        peluang[s] = (w / w.sum()) if len(pool[s]) and w.sum() > 0 else None

    def fitur(m, ctx, P):
        f = np.zeros((len(P), 16), dtype=np.float32)
        f[:, 0] = V[P] @ V[m]
        f[:, 1] = PMI[BIN[m], BIN[P]]
        f[:, 2] = (GB[P] & GB[m]) != 0
        f[:, 3] = np.abs(FEM[P] - FEM[m]) / 100
        f[:, 4] = TR[P]
        f[:, 5] = LF[P]
        f[:, 6] = (CRE[P] == CRE[m]) & (CRE[m] >= 0)
        f[:, 7] = SAT[P]
        f[:, 8] = VAL[P]
        f[:, 9] = SAT[P] * SAT[m]
        f[:, 10] = [satu_set(m, int(x)) for x in P]
        if ctx:
            c = V[ctx].mean(axis=0)
            f[:, 11] = V[P] @ c
            f[:, 12] = PMI[BIN[ctx][:, None], BIN[P][None, :]].mean(axis=0)
            f[:, 13] = np.max([(CRE[P] == CRE[x]) & (CRE[x] >= 0) for x in ctx], axis=0)
            f[:, 14] = np.max([[satu_set(x, int(p)) for p in P] for x in ctx], axis=0)
            f[:, 15] = 1
        return f

    X = {s: [] for s in DESAIN_SLOT}
    Y = {s: [] for s in DESAIN_SLOT}
    urut = rng.permutation(len(trn))[:22000]
    n_contoh = 0
    for oi in urut:
        if time.time() - t0 > batas_detik * 0.75:
            log(f"  DESAIN: batas waktu sampel ({n_contoh} contoh)")
            break
        it = trn[oi][1]
        isi = set(it)
        for ti, t in enumerate(it):
            ts = SL[t]
            if ts not in pool or len(pool[ts]) < 30:
                continue
            lain = [k for k in range(len(it)) if k != ti]
            mi = lain[rng.integers(len(lain))]
            m = it[mi]
            if SL[m] == ts:
                continue
            sisa = [it[k] for k in lain if k != mi]
            nc = rng.integers(0, len(sisa) + 1)
            ctx = [int(x) for x in rng.permutation(sisa)[:nc]] if sisa else []
            neg = list(pool[ts][rng.integers(len(pool[ts]), size=6)])
            if peluang[ts] is not None:
                neg += list(rng.choice(pool[ts], size=6, p=peluang[ts]))
            neg = [int(x) for x in neg if x not in isi]
            P = np.array([t] + neg)
            X[ts].append(fitur(m, ctx, P))
            Y[ts] += [1] + [0] * len(neg)
            n_contoh += 1
    bobot = {}
    for s in DESAIN_SLOT:
        if len(Y[s]) < 2000:
            continue
        w = logreg_irls(np.vstack(X[s]).astype(np.float64), np.array(Y[s], dtype=np.float64))
        if np.all(np.isfinite(w)):
            bobot[str(s)] = [round(float(x), 4) for x in w]
    if len(bobot) < 6:
        log(f"  DESAIN: bobot slot kurang ({len(bobot)}) -> tidak diekspor")
        return None, {}
    # uji jujur (outfit uji): peringkat item asli di antara SEMUA item slotnya; MC + 2 bumbu konteks
    r_cos, r_mod = [], []
    for _, it, _ in [val[k] for k in rng.permutation(len(val))[:600]]:
        if time.time() - t0 > batas_detik:
            break
        for ti, t in enumerate(it):
            ts = SL[t]
            if str(ts) not in bobot:
                continue
            lain = [k for k in range(len(it)) if k != ti]
            mi = lain[rng.integers(len(lain))]
            m = it[mi]
            if SL[m] == ts:
                continue
            sisa = [it[k] for k in lain if k != mi]
            ctx = [int(x) for x in rng.permutation(sisa)[:2]] if sisa else []
            P = pool[ts]
            ix = int(np.where(P == t)[0][0])
            sc = V[P] @ V[m]
            r_cos.append(float((sc > sc[ix]).mean()))
            w = np.array(bobot[str(ts)])
            sc = fitur(m, ctx, P) @ w[:-1]
            r_mod.append(float((sc > sc[ix]).mean()))
    rc, rm = np.array(r_cos), np.array(r_mod)
    metrik = {"n": int(len(rm)), "contoh_latih": n_contoh,
              "top1_cos": round(float((rc < 0.01).mean()), 4) if len(rc) else None,
              "top1_model": round(float((rm < 0.01).mean()), 4) if len(rm) else None,
              "top5_cos": round(float((rc < 0.05).mean()), 4) if len(rc) else None,
              "top5_model": round(float((rm < 0.05).mean()), 4) if len(rm) else None,
              "median_cos": round(float(np.median(rc)), 4) if len(rc) else None,
              "median_model": round(float(np.median(rm)), 4) if len(rm) else None}
    # resep: slot yang dipakai bersama, jumlah aksesori, pasangan atasan/bawahan 2D-3D
    ada = collections.Counter()
    bersama = collections.defaultdict(collections.Counter)
    n_aks = collections.Counter()
    pasang = collections.Counter()
    for _, it, _ in trn:
        sl = set(int(SL[x]) for x in it)
        for a in sl:
            ada[a] += 1
            for b in sl:
                if a != b:
                    bersama[a][b] += 1
        n_aks[min(6, sum(1 for x in it if SL[x] in DESAIN_AKS))] += 1
        atas = "3D" if 13 in sl else ("2D" if 1 in sl else "-")
        bawah = "3D" if 14 in sl else ("2D" if 2 in sl else "-")
        pasang[atas + bawah] += 1
    nt = max(1, len(trn))
    resep = {str(a): {str(b): round(bersama[a][b] / ada[a], 3) for b in DESAIN_SLOT if bersama[a][b]} for a in DESAIN_SLOT if ada[a] >= 50}
    desain = {
        "versi": DESAIN_VERSI, "fitur": DESAIN_FITUR, "w": bobot,
        "pmi": [[round(float(x), 3) for x in baris] for baris in PMI],
        "mu": [round(float(x), 4) for x in V.mean(axis=0)],
        "pAks": {str(s): round(ada[s] / nt, 3) for s in DESAIN_AKS},
        "nAks": [round(n_aks[k] / nt, 3) for k in range(7)],
        "resep": resep, "pasang": {k: round(v / nt, 3) for k, v in pasang.items()},
        "alpha": 1.3, "beta": 0.6, "lam": 1.2,
        "metrik": metrik, "outfit_latih": len(trn), "outfit_uji": len(val), "detik": round(time.time() - t0, 1),
    }
    pop = {ids[k]: int(round(float(LF[k]) * 100)) for k in range(n) if FREQ[k] > 0}
    log(f"  DESAIN v{DESAIN_VERSI}: {n_contoh} contoh, {len(bobot)} slot | uji top1% model {metrik['top1_model']} vs cos "
        f"{metrik['top1_cos']} | top5% {metrik['top5_model']} vs {metrik['top5_cos']} | {desain['detik']} dtk")
    return desain, pop


# ---------------------------------------------------------------------------------------------
# 5. EKSPOR
# ---------------------------------------------------------------------------------------------
def tulis_json(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


MAKS_ITEM_EKSPOR = 40000


def skor_tren(st):
    """0-100 per item: persentil gabungan popularitas (log favorit) + laju (favorit per hari sejak dibuat)."""
    hari_ini = int(time.time() // 86400)
    mentah = {}
    for k, m in st["meta"].items():
        f = m.get("f")
        if not isinstance(f, int):
            continue
        umur = max(7, hari_ini - m.get("d", hari_ini - 365))
        mentah[int(k)] = math.log10(f + 1) + 0.6 * math.log10(f / umur + 1)
    if not mentah:
        return {}
    urut = sorted(mentah.values())
    import bisect
    return {i: int(round(100 * bisect.bisect_left(urut, v) / len(urut))) for i, v in mentah.items()}


# v7 (7 Okt 2026, uji visual di Roblox): bank lama ternyata 72% berisi baju/rambut BAWAAN Roblox (Pal Hair, Dark Green
# Jeans, ...) karena N (estetika CLIP) dan Q (koherensi) justru tertinggi untuk outfit "noob" itu (Q>=75: 100% berisi item
# Roblox, Q<60: 35%). Akibatnya hanya ~1.700 dari 9.215 outfit modern yang terkumpul masuk bank. Sekarang: outfit dengan
# item inti bawaan Roblox dibuang, dan urutan memakai ciri "modern" (pakaian 3D layered, item baru, tren, aksesori cukup).
KATA_KAKI_TANGAN = {"shoe", "shoes", "boot", "boots", "slipper", "slippers", "sneaker", "sneakers", "heel", "heels", "sock",
                    "socks", "sandal", "sandals", "nail", "nails", "bracelet", "bracelets", "bangle", "bangles", "glove",
                    "gloves", "warmer", "warmers", "watch", "cuff", "cuffs", "ring", "rings"}
KATA_KOSTUM_BANK = {"costume", "cosplay", "pajama", "pajamas", "mascot", "ninja", "pixel", "minecraft", "elytra",
                    "creeper", "fursuit", "onesie", "inflatable", "uniform", "police", "sheriff", "prisoner", "noob"}


def info_modern(s, meta, tren):
    """-> (ada_item_inti_bawaan_roblox, jumlah_item_roblox, skor_modern). Murni dari meta (tanpa jaringan)."""
    n_rob = 0
    basic_inti = False
    n_lapis = n_kostum = 0
    ids = ids_seed(s)
    for i, sl in slot_item_seed(s):
        m = meta.get(str(i)) or {}
        nama = set(re.findall(r"[a-z]+", (m.get("n") or "").lower()))
        if m.get("c") == "Roblox":
            n_rob += 1
            if sl in ("Shirt", "Pants", "TShirt") or (sl == "Hair" and i < 10_000_000_000) or sl in ("LayerAtas", "LayerBawah") and i < 7_000_000_000:
                basic_inti = True
        if sl in ("LayerAtas", "LayerBawah") and not (nama & KATA_KAKI_TANGAN):
            n_lapis += 1
        if nama & KATA_KOSTUM_BANK and sl in ("Shirt", "Pants", "LayerAtas", "LayerBawah", "Hat"):
            n_kostum += 1
    acc = s.get("A", [])
    sm = 0.0
    if n_lapis:
        sm += 10
    baru = sorted(ids)[len(ids) // 2] if ids else 0
    if baru > 10_000_000_000:
        sm += 5
    tr = [tren.get(i) for i in ids if tren.get(i) is not None]
    if tr:
        sm += 0.15 * (sum(tr) / len(tr) - 50)
    if 3 <= len(acc) <= 7:
        sm += 4
    if not n_lapis and len(acc) <= 2:
        sm -= 8
    sm -= 15 * n_kostum
    return basic_inti, n_rob, sm


def ekspor(st, emb, warna, slot_of, zs, hasil_latih, statistik):
    versi = int(time.time())
    nama_gaya, p_gaya, nama_atr, p_atr, p_fem, ids_zs = zs
    pos_zs = {i: k for k, i in enumerate(ids_zs)}
    fz = idx_of = None
    if hasil_latih:
        fz, idx_of = hasil_latih["fz"], hasil_latih["idx_of"]
    # --- item: [slot, gender(0-100), hex, gayaBits, atrBits, v1..v32]
    tren = skor_tren(st)
    # RINGAN SELAMANYA: yang dikirim ke server dibatasi MAKS_ITEM_EKSPOR (prioritas: item di outfit bank, lalu item
    # yang bisa dibeli, lalu yang paling tren). Latihan tetap memakai SEMUA item.
    di_bank = set()
    for s0 in st["outfit"].values():
        bi0, nr0, _ = info_modern(s0, st["meta"], tren)
        if not bi0 and nr0 < 2:  # v7: item outfit yang bisa masuk bank didahulukan (dulu: semua outfit, termasuk "noob")
            di_bank.update(ids_seed(s0))
    diminta = set(int(k) for k in st.get("diminta", {}))
    def prioritas(i):
        m = st["meta"].get(str(i)) or {}
        return (0 if (i in di_bank or i in diminta) else 1, 0 if m.get("s") == 1 else 1, -tren.get(i, 0))
    ids_kirim = set(sorted(ids_zs, key=prioritas)[:MAKS_ITEM_EKSPOR])
    # desain v1: baris dihitung untuk SEMUA item (belajar memakai semua), yang dikirim tetap ids_kirim
    baris_of = {}
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
        if slot_of.get(i) == "Hair":
            pr = float(P_RAMBUT_PANJANG[k])
            if pr >= 0.65:
                a_bits |= 1 << 9   # rambut panjang
            elif pr <= 0.35:
                a_bits |= 1 << 10  # rambut pendek
        baris = [SLOT_KODE.get(slot_of.get(i, ""), 0), int(round(float(p_fem[k]) * 100)), warna.get(i, ""), g_bits, a_bits]
        if fz is not None and i in idx_of:
            baris += [int(round(float(x) * 127)) for x in fz[idx_of[i]]]
        baris_of[i] = baris
    # BELAJAR DESAIN (proses desainer) -- gagal = server Roblox memakai bobot bawaannya, ekspor lain tetap jalan
    desain, pop_of = None, {}
    if fz is not None:
        try:
            desain, pop_of = belajar_desain(st, hasil_latih, baris_of, tren)
        except Exception as ex:
            log("  DESAIN gagal (dilewati):", repr(ex)[:300])
            desain, pop_of = None, {}
    shard = [dict() for _ in range(SHARD_ITEM)]
    for i in ids_kirim:
        baris = baris_of.get(i)
        if baris is None:
            continue
        if len(baris) == 5 + DIM:
            baris = baris + [pop_of.get(i, 0)]  # desain v1: popularitas di kalangan desainer (log1p(frek) x100)
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
    n_tolak_beli = n_tolak_koh = n_tolak_basic = 0
    for s, kh, g, inti_ok, n_beli in nilai:
        if not inti_ok or n_beli < 3:
            n_tolak_beli += 1
            continue
        nama_item = " ".join((st["meta"].get(str(i)) or {}).get("n", "").lower() for i in ids_seed(s))
        if len(ids_seed(s)) < 4 or "invis" in nama_item or "headless" in nama_item:
            n_tolak_beli += 1  # bukan outfit jadi (terlalu sedikit item / item troll)
            continue
        bi, n_rob, sm = info_modern(s, st["meta"], tren)
        if bi or n_rob >= 2:
            n_tolak_basic += 1  # v7: outfit berisi baju/rambut bawaan Roblox = kesan "noob", bukan acuan gaya
            continue
        q = persentil(kh)
        if kh is not None and q < 10:
            n_tolak_koh += 1  # 10% paling tidak koheren menurut model: dibuang
            continue
        n_est = s.get("N")
        if n_est is not None and n_est < 30:  # v7: 45 -> 30 (N terbukti tidak mewakili selera; outfit modern sering 45-60)
            n_tolak_koh += 1  # dinilai jelek oleh mata estetika (CLIP/Gemini)
            continue
        e = {k: v for k, v in s.items() if k in ("Sh", "Pa", "Gt", "A", "F", "BCn", "SC", "R", "H", "S", "N", "GY")}
        e["Q"] = q
        e["G"] = g
        kandidat.append((e, sm))
    # v7: urutan = koherensi + ciri modern; N hanya bobot kecil. Keragaman: satu item maks 30 outfit di bank (dulu satu
    # penghangat lengan bisa muncul di ratusan outfit -> semua hasil terlihat sama)
    kandidat.sort(key=lambda x: -(0.45 * x[0]["Q"] + 0.15 * (x[0].get("N") if x[0].get("N") is not None else 50) + x[1]))
    pakai, terpilih, sisa = {}, [], []
    for e, _ in kandidat:
        ii = ids_seed(e)
        if any(pakai.get(i, 0) >= 30 for i in ii):
            sisa.append(e)
            continue
        for i in ii:
            pakai[i] = pakai.get(i, 0) + 1
        terpilih.append(e)
        if len(terpilih) >= MAKS_BANK:
            break
    if len(terpilih) < MAKS_BANK:
        terpilih += sisa[:MAKS_BANK - len(terpilih)]
    kandidat = terpilih
    log(f"BANK v7: {len(kandidat)} outfit | ditolak bawaan Roblox {n_tolak_basic}, tak bisa dibeli {n_tolak_beli}, tak koheren {n_tolak_koh}")
    bshard = [[] for _ in range(SHARD_BANK)]
    for e in kandidat:
        bshard[int(e["H"][:8], 16) % SHARD_BANK].append(e)
    for s in range(SHARD_BANK):
        tulis_json(f"bank/outfit_{s}.json", {"versi": versi, "seeds": bshard[s]})

    # --- meta harga snapshot untuk semua item di bank (server tetap validasi live, TTL)
    mshard = [dict() for _ in range(SHARD_ITEM)]
    ids_meta = set()
    for e in kandidat:
        ids_meta.update(ids_seed(e))
    # + semua item bervektor yang bisa dibeli: bahan KOMPOSISI otak di server (bukan cuma bank)
    for i in ids_kirim:
        m = st["meta"].get(str(i))
        if m and m.get("s") == 1 and m.get("p", -1) >= 0 and m.get("t", 0) in ASET_KE_SLOT:
            ids_meta.add(i)
    for i in sorted(ids_meta):
        if True:
            m = st["meta"].get(str(i))
            if m:
                mshard[i % SHARD_ITEM][str(i)] = [m.get("n", ""), m.get("p", -1), m.get("s", 0), m.get("c", ""), m.get("t", 0), m.get("w", 0), tren.get(i, -1)]
    for s in range(SHARD_ITEM):
        tulis_json(f"meta/harga_{s}.json", {"versi": versi, "d": mshard[s]})
    # --- peta bagian badan -> bundle (kandidat diurutkan: yang dijual dulu, lalu termurah)
    pbadan = st.get("badan") or {}
    bb = pbadan.get("b") or {}
    def urut_bundle(bid):
        v = bb.get(str(bid)) or ["", 0, 0]
        return (0 if v[1] else 1, v[2], bid)
    peta_a = {k: sorted(v, key=urut_bundle)[:6] for k, v in (pbadan.get("a") or {}).items() if v}
    tulis_json("meta/badan.json", {"versi": versi, "a": peta_a, "b": bb})

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
        "n_item": len(ids_kirim), "n_item_dipelajari": len(ids_zs), "n_outfit_panen": len(st["outfit"]), "n_bank": len(kandidat),
        "bank_tolak_tidak_bisa_dibeli": n_tolak_beli, "bank_tolak_tidak_koheren": n_tolak_koh,
        "shard_item": SHARD_ITEM, "shard_bank": SHARD_BANK, "shard_meta": SHARD_ITEM,
        "slot_kode": SLOT_KODE, "gaya": nama_gaya, "atribut": nama_atr, "panen": statistik,
        "n_sinyal_pemain": sum(1 for x in st["outfit"].values() if x.get("S") == "sinyal"),
        "n_tolak_pemain": len(st.get("tolak", {})),
        "n_dasar_lokal": sum(1 for x in st["outfit"].values() if x.get("S") == "lokal"),
        "n_diminta_pemain": len(st.get("diminta", {})),
        "badan": True, "n_peta_badan": len(peta_a), "n_bundle_badan": len(bb),
        "desain": desain,
        "durasi_menit": round((time.time() - T0) / 60, 1),
    }
    rw = st.setdefault("riwayat", [])
    rw.append({"putaran": st["putaran"], "waktu": info["dibuat"][:16], "outfit": len(st["outfit"]), "item": len(ids_zs),
               "fitb": round(float(hl.get("fitb_dipakai") or 0), 3), "sinyal": info["n_sinyal_pemain"]})
    st["riwayat"] = rw[-60:]
    info["riwayat"] = st["riwayat"][-12:]
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
        f"- Sinyal pemain (outfit difavoritkan/dibeli di map): **{info.get('n_sinyal_pemain', 0)}** | outfit dasar dari server Roblox: {info.get('n_dasar_lokal', 0)} | item baru diminta pemain: {info.get('n_diminta_pemain', 0)}",
        f"- Durasi putaran: **{info.get('durasi_menit', '-')} menit** | META: {json.dumps(info.get('panen', {}).get('meta', {}))}", "",
        "## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)", "",
    ] + ([
        f"- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: "
        f"model **{f((info.get('desain') or {}).get('metrik', {}).get('top1_model'))}** vs kemiripan gaya saja {f((info.get('desain') or {}).get('metrik', {}).get('top1_cos'))}",
        f"- Masuk 5% teratas: model **{f((info.get('desain') or {}).get('metrik', {}).get('top5_model'))}** vs {f((info.get('desain') or {}).get('metrik', {}).get('top5_cos'))} "
        f"| {(info.get('desain') or {}).get('metrik', {}).get('n', '-')} soal | contoh latih {(info.get('desain') or {}).get('metrik', {}).get('contoh_latih', '-')}",
        "- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, "
        "kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D", "",
    ] if info.get("desain") else ["- Belajar desain putaran ini GAGAL/dilewati: server memakai bobot bawaan (hasil lab).", ""]) + [
        "## Perkembangan otak (makin banyak data = makin pintar)", "",
        "| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |", "|---|---|---|---|---|---|",
    ] + [f"| {r['putaran']} | {r['waktu']} | {r['outfit']} | {r['item']} | {r['fitb']} | {r['sinyal']} |" for r in info.get("riwayat", [])] + [
        "",
        "## Gender visual (zero-shot CLIP) dicek dengan kata di nama item",
        f"- AUC = {f(info['auc_gender_vs_nama'])} pada {info['n_label_gender'][0]} item berlabel wanita & {info['n_label_gender'][1]} pria",
        "  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)", "",
        "_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._",
    ]
    open("LAPORAN_OTAK.md", "w", encoding="utf-8").write("\n".join(baris) + "\n")
    ring = os.environ.get("GITHUB_STEP_SUMMARY")
    if ring:
        open(ring, "a", encoding="utf-8").write("\n".join(baris) + "\n")


P_RAMBUT_PANJANG = None


def ambil_dari_roblox(st):
    """OPSIONAL (butuh secret ROBLOX_API_KEY, dibuat pemilik di Creator Dashboard; izin baca DataStore).
    Lewat Roblox Open Cloud (GET /cloud/v2/universes/{id}/data-stores/{store}/entries/{entry}):
      - KatalogOutfitDasar_v1 shard_0..15 : outfit dasar yang dipanen server Roblox (cepat, tanpa limit IP)
      - KatalogSinyalOtak_v1  pos_{0..7}_{0..3} (+ pos_0..7 lama) : outfit yang DIFAVORITKAN/DIBELI pemain (anonim)
      - KatalogSinyalOtak_v1  itembaru_{0..7} (+ itembaru lama)    : item pilihan pemain yang belum dikenal otak
    Tanpa secret: dilewati diam-diam (otak tetap belajar dari panen GitHub)."""
    kunci = os.environ.get("ROBLOX_API_KEY", "").strip()
    uni = os.environ.get("UNIVERSE_ID", "").strip()
    if STUB or not kunci or not uni:
        log("sumber Roblox (Open Cloud) dilewati: secret ROBLOX_API_KEY belum dipasang")
        return
    import requests
    from urllib.parse import quote
    def ambil(store, entri):
        url = f"https://apis.roblox.com/cloud/v2/universes/{uni}/data-stores/{quote(store)}/entries/{quote(entri)}"
        for k in range(3):
            try:
                r = requests.get(url, headers={"x-api-key": kunci}, timeout=30)
                if r.status_code == 200:
                    v = r.json().get("value")
                    if isinstance(v, str):
                        try:
                            v = json.loads(v)
                        except Exception:
                            return None
                    return v
                if r.status_code == 404:
                    return None
                if r.status_code in (401, 403):
                    log(f"  Open Cloud {r.status_code}: cek izin API key (data store read) & universe")
                    return None
            except Exception:
                pass
            time.sleep(3 * (k + 1))
        return None

    def masukkan(daftar, sumber):
        n = 0
        for s in daftar:
            if not isinstance(s, dict):
                continue
            acc = []
            for a in s.get("A") or []:
                if isinstance(a, list) and len(a) == 2 and all(isinstance(x, int) for x in a):
                    acc.append([a[0], a[1]])
            js = {"assets": []}
            for f, at in (("Sh", 11), ("Pa", 12), ("Gt", 2)):
                if isinstance(s.get(f), int):
                    js["assets"].append({"id": s[f], "assetType": {"id": at}})
            for i, t in acc:
                if t in ACC_KE_ASET:
                    js["assets"].append({"id": i, "assetType": {"id": ACC_KE_ASET[t]}})
            seed = seed_dari_avatar(js)
            if not seed:
                continue
            if sumber == "sinyal" and s.get("J") == "tidak":
                # jempol bawah pemain = contoh outfit yang TIDAK disukai -> dipakai sebagai negatif saat latih
                seed["S"] = "tolak"
                seed["T"] = int(time.time())
                st.setdefault("tolak", {})[seed["H"]] = seed
                st["outfit"].pop(seed["H"], None)
                continue
            if seed["H"] in st.get("tolak", {}):
                continue
            seed["S"] = sumber
            seed["K"] = sumber[:3] + seed["H"][:3]
            if sumber == "sinyal" or seed["H"] not in st["outfit"]:
                seed["T"] = int(time.time())
                st["outfit"][seed["H"]] = seed
                n += 1
        return n

    # semua kunci dibaca PARALEL (kunci "ember" per server sejak 7 Okt 2026: pos_{i}_{b}, itembaru_{b};
    # kunci lama tanpa ember tetap dibaca untuk data sebelum perubahan)
    from concurrent.futures import ThreadPoolExecutor
    daftar_kunci = [("KatalogOutfitDasar_v1", f"shard_{i}") for i in range(16)]
    daftar_kunci += [("KatalogSinyalOtak_v1", f"pos_{i}") for i in range(8)]
    daftar_kunci += [("KatalogSinyalOtak_v1", f"pos_{i}_{b}") for i in range(8) for b in range(4)]
    daftar_kunci += [("KatalogSinyalOtak_v1", "itembaru")] + [("KatalogSinyalOtak_v1", f"itembaru_{b}") for b in range(8)]
    daftar_kunci += [("KatalogSinyalOtak_v1", f"badanbaru_{b}") for b in range(8)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        nilai = dict(zip(daftar_kunci, ex.map(lambda sk: ambil(sk[0], sk[1]), daftar_kunci)))
    n_lokal = n_sinyal = 0
    for (store, entri), d in nilai.items():
        if store == "KatalogOutfitDasar_v1" and isinstance(d, dict) and isinstance(d.get("seeds"), dict):
            n_lokal += masukkan(list(d["seeds"].values()), "lokal")
        elif entri.startswith("pos_") and isinstance(d, dict) and isinstance(d.get("outfit"), list):
            n_sinyal += masukkan(d["outfit"], "sinyal")
    # item yang dipilih pemain di map tapi belum dikenal otak -> diprioritaskan META & MATA putaran ini
    n_diminta = 0
    dim = st.setdefault("diminta", {})
    for (store, entri), d in nilai.items():
        if not (entri.startswith("itembaru") and isinstance(d, dict) and isinstance(d.get("ids"), list)):
            continue
        for x in d["ids"]:
            if isinstance(x, int) and x > 0 and str(x) not in dim:
                dim[str(x)] = int(time.time())
                n_diminta += 1
    if len(dim) > MAKS_DIMINTA:
        for k, _ in sorted(dim.items(), key=lambda kv: kv[1])[:len(dim) - MAKS_DIMINTA]:
            dim.pop(k, None)
    # bagian badan avatar pemain yang bundlenya belum dikenal -> dipetakan putaran ini (peta_badan)
    bdim = st.setdefault("badan_diminta", {})
    for (store, entri), d in nilai.items():
        if entri.startswith("badanbaru") and isinstance(d, dict) and isinstance(d.get("ids"), list):
            for x in d["ids"]:
                if isinstance(x, int) and x > 0:
                    bdim.setdefault(str(x), int(time.time()))
    if len(bdim) > 5000:
        for k, _ in sorted(bdim.items(), key=lambda kv: kv[1])[:len(bdim) - 5000]:
            bdim.pop(k, None)
    log(f"sumber Roblox: +{n_lokal} outfit dasar server, {n_sinyal} outfit sinyal pemain, {n_diminta} item baru diminta pemain")


def peta_badan(http, st, batas, hasil):
    """Bagian badan -> bundle. Ditulis ke `hasil` (bukan st) supaya aman berjalan di utas sendiri; digabung ke st
    oleh utas utama sebelum ekspor."""
    lama = st.get("badan") or {}
    pa, pb, pt = dict(lama.get("a") or {}), dict(lama.get("b") or {}), dict(lama.get("t") or {})
    sekarang = int(time.time())
    dim = dict(st.get("badan_diminta") or {})
    antre = [k for k in dim if sekarang - int(pt.get(k, 0)) > TTL_PETA_BADAN]
    antre.sort(key=lambda k: -int(dim[k]))
    n_tanya = n_bundle = 0
    for k in antre[:MAKS_BADAN_PER_PUTARAN]:
        if time.time() > batas:
            break
        if sekarang - int(pt.get(k, 0)) <= TTL_PETA_BADAN:
            continue  # sudah ikut terpetakan dari bundle bagian badan lain
        try:
            aid = int(k)
        except Exception:
            continue
        js = http.get(f"https://catalog.roblox.com/v1/assets/{aid}/bundles")
        n_tanya += 1
        if not isinstance(js, dict) or not isinstance(js.get("data"), list):
            continue  # gagal jaringan: dicoba lagi putaran berikutnya
        pt[k] = sekarang
        pa.setdefault(k, [])
        for b in js["data"]:
            if not isinstance(b, dict) or b.get("bundleType") not in ("BodyParts", "DynamicHead"):
                continue
            try:
                bid = int(b["id"])
            except Exception:
                continue
            prod = b.get("product") or {}
            try:
                harga = int(prod.get("priceInRobux") or 0)
            except Exception:
                harga = 0
            pb[str(bid)] = [str(b.get("name") or "")[:60], 1 if prod.get("isForSale") else 0, harga]
            n_bundle += 1
            for it in b.get("items") or []:
                if not (isinstance(it, dict) and it.get("type") == "Asset" and it.get("assetType") in TIPE_BADAN):
                    continue
                try:
                    a = str(int(it["id"]))
                except Exception:
                    continue
                daftar = pa.setdefault(a, [])
                if bid not in daftar:
                    daftar.append(bid)
                pt[a] = sekarang
    if len(pt) > MAKS_PETA_BADAN:
        for k, _ in sorted(pt.items(), key=lambda kv: kv[1])[:len(pt) - MAKS_PETA_BADAN]:
            pt.pop(k, None)
            pa.pop(k, None)
    dipakai = set()
    for daftar in pa.values():
        dipakai.update(daftar)
    pb = {k: v for k, v in pb.items() if int(k) in dipakai}
    hasil["badan"] = {"a": pa, "b": pb, "t": pt}
    hasil["selesai"] = [k for k in dim if sekarang - int(pt.get(k, 0)) <= TTL_PETA_BADAN]
    log(f"PETA BADAN: {n_tanya} bagian badan ditanyakan, {n_bundle} bundle tercatat | peta {len(pa)} aset, {len(pb)} bundle")


def main():
    import threading
    st = muat_state()
    st["putaran"] = st.get("putaran", 0) + 1
    log(f"putaran {st['putaran']} | bank {len(st['outfit'])} outfit | meta {len(st['meta'])} | STUB={STUB}")
    http = HttpStub() if STUB else Http()
    embedder = EmbedderStub() if STUB else EmbedderCLIP()
    emb, warna = muat_emb()
    muat_state_v5(st)
    ambil_dari_roblox(st)
    # 0) PETA BADAN di utas sendiri (endpoint katalog /v1/assets, ringan: <= MAKS_BADAN_PER_PUTARAN permintaan)
    hasil_badan = {}
    utas_badan = threading.Thread(target=peta_badan, args=(http, st, T0 + 20 * 60, hasil_badan), daemon=True)
    utas_badan.start()
    # 1) META sejak menit 0, utas sendiri: item diminta pemain -> item outfit tanpa meta -> item paling basi
    meta = PekerjaMeta(http, st, T0 + MENIT_META * 60)
    semua_id = set()
    for s0 in st["outfit"].values():
        semua_id.update(ids_seed(s0))
    diminta = [int(k) for k in st.get("diminta", {}) if k not in st["meta"]]
    baru, basi = perlu_meta(st, semua_id)
    meta.tambah(diminta, depan=True)
    meta.tambah(baru, depan=True)
    meta.tambah(basi)
    log(f"META: {len(diminta)} item diminta pemain, {len(baru)} belum punya meta, {len(basi)} basi (TTL 5/14 hari) -> antre")
    meta.utas.start()
    # 2) MATA-1 paralel (host thumbnails): item lama yang belum punya sidik jari visual
    gagal_baru = {}
    mata1 = threading.Thread(target=mata, args=(http, st, embedder, emb, warna, T0 + (MENIT_GAYA + 10) * 60, gagal_baru, "MATA-1"), daemon=True)
    mata1.start()
    # 3) PANEN GAYA (host avatar): outfit pemain sungguhan dari komunitas fashion, dinilai CLIP (+ Gemini)
    stat_gaya = {}
    try:
        penilai = Penilai(embedder)
        n_outfit_awal = set(st["outfit"])
        stat_gaya = panen_gaya(http, st, cari_pemain_gaya(http, st), penilai)
        ids_baru = set()
        for h in set(st["outfit"]) - n_outfit_awal:
            ids_baru.update(ids_seed(st["outfit"][h]))
        b2, _ = perlu_meta(st, ids_baru)
        meta.tambah(b2, depan=True)
        log(f"META: +{len(b2)} item dari outfit gaya baru masuk antrean depan")
    except Exception as ex:
        log("GAYA gagal (dilewati):", repr(ex)[:200])
    simpan_state(st)
    # 4) KREATOR (opsional, sisa waktu): pencarian katalog memakai host yang sama dengan META -> hanya bila antrean
    #    META sudah kosong, supaya kuota katalog dipakai untuk harga dulu
    statistik = {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0}
    meta.panen_selesai = True
    meta.utas.join(timeout=max(0, T0 + MENIT_META * 60 - time.time()))
    if meta.sisa() == 0 and time.time() < T0 + (MENIT_META + 5) * 60:
        try:
            antre = cari_kreator(http, st)
            mata1.join(timeout=1)
            statistik = panen(http, st, antre[:150])
        except Exception as ex:
            log("KREATOR gagal (dilewati):", repr(ex)[:200])
    simpan_state(st)
    mata1.join(timeout=max(0, T0 + (MENIT_GAYA + 10) * 60 - time.time()))
    log(f"META selesai: {meta.ringkas()} | {http.ringkas()}")
    # 5) MATA-2: item baru (outfit gaya + item yang diminta pemain yang kini sudah punya meta)
    mata(http, st, embedder, emb, warna, time.time() + 15 * 60, gagal_baru, "MATA-2")
    st.setdefault("gagal_thumb", {}).update(gagal_baru)
    simpan_state(st)
    slot_of = slot_semua_item(st)
    ids_zs = sorted(i for i in emb if i in slot_of)
    if not ids_zs:
        log("tidak ada item berembedding -- berhenti")
        sys.exit(1)
    utas_badan.join(timeout=60)
    if "badan" in hasil_badan:
        with KUNCI_ST:
            st["badan"] = hasil_badan["badan"]
            for k in hasil_badan.get("selesai", []):
                st.get("badan_diminta", {}).pop(k, None)
    X = np.stack([emb[i] for i in ids_zs]).astype("float32")
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    nama_gaya, p_gaya, nama_atr, p_atr, p_fem = zero_shot(embedder, ids_zs, X, slot_of)
    hasil_latih = latih(st, emb, slot_of)
    statistik.update(stat_gaya)
    statistik["meta"] = meta.ringkas()
    info = ekspor(st, emb, warna, slot_of, (nama_gaya, p_gaya, nama_atr, p_atr, p_fem, ids_zs), hasil_latih, statistik)
    laporan(info, http)
    log(f"SELESAI {info['durasi_menit']} menit: bank {info['n_bank']} outfit, {info['n_item']} item, layak={info['layak']}, AUC gender {info['auc_gender_vs_nama']} | {http.ringkas()}")


if __name__ == "__main__":
    main()
