#!/usr/bin/env python3
"""
KARTU ITEM (MATA v2) -- Katalog Praktis
=======================================
Map tidak punya mata: server Roblox hanya tahu nama item. Nama sering menyesatkan ("Duck Pumpkin" = kepala labu Halloween
yang kebetulan berwajah bebek). Modul ini MEMBACA GAMBAR item (thumbnail, sudah di-embed CLIP oleh otak.py) dan menulis
kartu terstruktur per item:

  jenis   : barang apa (kaos, hoodie, jaket, gaun, rok, jeans, topi koboi, kacamata, sayap, ...)   -- per kelompok slot
  bentuk  : potongan (lengan, panjang atasan, panjang bawahan, longgar/ketat, jaket terbuka/tertutup)
  tema    : tema visual (halloween, koboi, maid, gothic, kawaii, militer, ...)                      -- 2 teratas
  subjek  : gambar/benda utama di desain (labu, tengkorak, bebek, hati, bintang, ...)                -- 2 teratas
  pola    : permukaan (polos, garis, kotak, grafis, kamuflase, renda, denim, ...)

Cara baca: zero-shot CLIP (openai/clip-vit-base-patch32, model yang SAMA dengan otak.py, gratis, jalan di GitHub Actions).
Tiap label punya beberapa kalimat (ensemble); logit dikoreksi rata-rata per kelompok slot (bias kalimat CLIP), lalu softmax.
Untuk baju/celana 2D dipakai juga sidik jari POTONGAN PAKAIAN (tanpa manekin) dari otak.py bila ada.
Nama item hanya BUKTI TAMBAHAN (fusi lunak). Gambar tetap penentu tema & subjek; nama tokoh (anime) tetap dari nama.

Masukan : cache/emb.npz (otak.py), cache/emb2d.npz (opsional), data/panen.json.gz (nama & tipe aset), model/item_*.json
Keluaran: kartu/kartu_{0..7}.json  {"versi","skema","label":{...},"d":{id:[...]}}   (shard = id % 8, sama dengan model/)
          LAPORAN_KARTU.md         (cakupan, akurasi gambar vs nama, contoh, item uji)

Pakai : python kartu_item.py            -> tulis kartu + laporan
        python kartu_item.py --uji ID.. -> tambahkan item uji ke laporan
Tidak ada API berbayar. Tidak menulis model/, meta/, bank/ (milik otak.py).
"""
import os, sys, json, gzip, re, time, math, collections
import numpy as np

MODEL_ID = "openai/clip-vit-base-patch32"
CACHE_DIR = os.environ.get("CACHE_DIR", "cache")
P_EMB = os.path.join(CACHE_DIR, "emb.npz")
P_E2D = os.path.join(CACHE_DIR, "emb2d.npz")
P_STATE = "data/panen.json.gz"
SHARD = 8
SKEMA = 2             # 2: kolom ke-19 "fungsi" (kaos klasik: pakaian/lapisan kulit/aksesori lukis/gambar)
SUHU = 100.0          # suhu softmax CLIP (sama dengan otak.py)
BOBOT_NAMA = 0.35     # fusi lunak: bukti nama menambah massa peluang, gambar tetap dominan

# ---------------------------------------------------------------------------------------------
# Tipe aset Roblox -> kelompok slot kartu (AssetType terverifikasi, sama dengan otak.py)
# ---------------------------------------------------------------------------------------------
ASET_KE_KEL = {11: "atas", 2: "atas", 64: "atas", 65: "atas", 67: "atas", 68: "atas",       # Shirt, TShirt, layered atas
               12: "bawah", 66: "bawah", 69: "bawah", 72: "bawah",                          # Pants, layered bawah, DressSkirt
               8: "kepala", 42: "wajah", 41: "rambut",
               43: "aksen", 44: "aksen", 45: "aksen", 46: "aksen", 47: "aksen",          # Neck Shoulder Front Back Waist
               70: "sepatu", 71: "sepatu"}
KELOMPOK = ["atas", "bawah", "kepala", "wajah", "rambut", "aksen", "sepatu"]  # urutan = kode kolom 0 kartu
KEL_NOUN = {"atas": "top", "bawah": "bottom clothing", "kepala": "hat", "wajah": "face accessory", "rambut": "hairstyle",
            "aksen": "accessory", "sepatu": "shoe"}
ASET_2D = {11, 12, 2}

# ---------------------------------------------------------------------------------------------
# TAKSONOMI. Urutan label = indeks yang dibaca server: TAMBAH DI AKHIR saja, jangan sisipkan/hapus (naikkan SKEMA bila perlu).
# Tiap label: (kunci, [deskripsi untuk kalimat CLIP], [kata nama untuk fusi])
# ---------------------------------------------------------------------------------------------
TEMA = [
    ("biasa", ["plain simple everyday casual", "basic casual", "an ordinary normal outfit with no special theme"],
     ["basic", "plain", "simple", "casual", "polos"]),
    ("streetwear", ["trendy urban streetwear", "hypebeast streetwear"], ["streetwear", "hypebeast", "drip", "bape", "stussy"]),
    ("sporty", ["sporty athletic", "sports team jersey"], ["sport", "sporty", "athletic", "jersey", "soccer", "football", "basketball", "gym"]),
    ("formal", ["formal business suit and tie", "classy formal tuxedo"], ["suit", "tuxedo", "tux", "blazer", "formal", "business"]),
    ("gaun_elegan", ["elegant evening ball gown", "luxurious elegant gown"], ["gown", "gala", "ballgown", "elegant"]),
    ("sekolah", ["japanese school uniform", "school uniform with pleated skirt"], ["school", "schoolgirl", "schoolboy", "seifuku", "sekolah"]),
    ("militer", ["military camouflage soldier", "tactical army soldier"], ["military", "army", "camo", "camouflage", "soldier", "tactical", "militer"]),
    ("polisi", ["police officer uniform", "swat police"], ["police", "cop", "swat", "sheriff", "polisi"]),
    ("medis", ["doctor or nurse medical uniform", "hospital scrubs"], ["nurse", "doctor", "scrubs", "medic", "perawat", "dokter"]),
    ("koboi", ["western cowboy", "wild west cowboy rodeo"], ["cowboy", "cowgirl", "western", "rodeo", "ranch", "stetson", "koboi"]),
    ("bajak_laut", ["pirate captain", "pirate sailor with skull flag"], ["pirate", "pirates", "buccaneer", "corsair", "bajak"]),
    ("ksatria", ["medieval knight in armor", "medieval warrior armor"], ["knight", "armor", "armour", "medieval", "chainmail", "paladin", "ksatria"]),
    ("kerajaan", ["royal king or queen with gold crown", "regal royal noble"], ["royal", "crown", "king", "queen", "regal", "tiara", "mahkota"]),
    ("maid", ["maid outfit with white apron and frills", "french maid"], ["maid", "apron"]),
    ("gothic", ["gothic dark victorian black lace", "goth dark"], ["goth", "gothic", "victorian", "gotik"]),
    ("punk", ["punk emo grunge with chains and spikes", "emo grunge rocker"], ["punk", "emo", "grunge", "rocker", "scene", "spiked", "studded"]),
    ("kawaii", ["cute kawaii pastel", "adorable cute pastel"], ["kawaii", "cute", "cutie", "cutecore", "pastel", "lucu", "imut"]),
    ("coquette", ["coquette with pink bows and ribbons", "soft girly ballet coquette"], ["coquette", "bow", "bows", "ribbon", "ribbons", "balletcore"]),
    ("y2k", ["y2k 2000s glittery", "early 2000s y2k fashion"], ["y2k", "2000s", "mcbling", "rhinestone", "bratz"]),
    ("cyber", ["cyberpunk futuristic neon sci-fi", "futuristic sci-fi techwear"], ["cyber", "cyberpunk", "neon", "techwear", "futuristic", "scifi", "robot", "mecha"]),
    ("penyihir", ["wizard or witch magical", "magic sorcerer"], ["wizard", "witch", "sorcerer", "warlock", "magic", "penyihir"]),
    ("peri", ["fairy with flowers and wings", "whimsical fairycore"], ["fairy", "fairycore", "fae", "pixie", "peri"]),
    ("malaikat", ["angelic white angel with halo", "heavenly angel"], ["angel", "angelic", "halo", "seraph", "malaikat"]),
    ("iblis", ["demon devil with horns", "evil red demon"], ["demon", "demonic", "devil", "iblis", "setan"]),
    ("vampir", ["vampire dracula", "vampire with fangs and cape"], ["vampire", "dracula", "vampir"]),
    ("halloween", ["halloween pumpkin jack-o-lantern", "spooky halloween"], ["halloween", "pumpkin", "jack", "labu", "spooky"]),
    ("horor", ["scary horror bloody zombie", "creepy horror monster"], ["horror", "zombie", "bloody", "blood", "creepy", "scary", "horor", "seram"]),
    ("natal", ["christmas santa festive", "christmas holiday"], ["christmas", "xmas", "santa", "natal", "reindeer"]),
    ("pantai", ["summer beach tropical", "hawaiian beach"], ["beach", "summer", "tropical", "hawaiian", "pantai"]),
    ("musim_dingin", ["winter snow cozy", "warm winter"], ["winter", "snow", "cozy", "fluffy"]),
    ("anime", ["anime character cosplay", "anime cosplay outfit"], ["anime", "cosplay", "naruto", "gojo", "jjk", "akatsuki", "uchiha", "demon slayer"]),
    ("kostum_hewan", ["animal mascot costume", "furry animal onesie costume"], ["mascot", "onesie", "kigurumi", "fursuit", "costume"]),
    ("novelty", ["funny food or meme novelty", "silly joke costume"], ["meme", "funny", "joke", "noob", "troll", "food"]),
    ("tradisional", ["traditional asian kimono or hanfu", "traditional cultural clothing"], ["kimono", "yukata", "hanfu", "qipao", "cheongsam", "batik", "kebaya", "hanbok"]),
    ("ninja", ["ninja or samurai", "japanese samurai warrior"], ["ninja", "samurai", "shinobi", "ronin"]),
    ("badut", ["clown or circus jester", "colorful circus clown"], ["clown", "jester", "circus", "harlequin", "badut"]),
    ("superhero", ["superhero with cape", "comic book superhero"], ["superhero", "hero", "spiderman", "batman", "superman"]),
    ("antariksa", ["astronaut space suit", "outer space astronaut"], ["astronaut", "space", "galaxy", "alien"]),
    ("steampunk", ["steampunk victorian brass gears", "steampunk goggles and gears"], ["steampunk", "gears", "clockwork"]),
]
SUBJEK = [
    ("tanpa", ["plain with no picture or graphic", "solid with no print"], []),
    ("labu", ["a pumpkin", "a jack-o-lantern pumpkin"], ["pumpkin", "labu", "jack"]),
    ("tengkorak", ["a skull", "skulls and bones"], ["skull", "skulls", "skeleton", "tengkorak"]),
    ("kelelawar", ["a bat", "bat wings"], ["bat", "bats", "kelelawar"]),
    ("hantu", ["a ghost", "a cute ghost"], ["ghost", "ghosts", "hantu"]),
    ("laba_laba", ["a spider and spider web", "spider web"], ["spider", "spiderweb", "web"]),
    ("bebek", ["a duck", "a rubber duck"], ["duck", "ducky", "bebek"]),
    ("kucing", ["a cat", "a kitty cat"], ["cat", "kitty", "kitten", "neko", "kucing"]),
    ("anjing", ["a dog", "a puppy"], ["dog", "puppy", "doggy", "anjing"]),
    ("beruang", ["a teddy bear", "a bear"], ["bear", "teddy", "beruang"]),
    ("kelinci", ["a bunny rabbit", "bunny ears"], ["bunny", "rabbit", "kelinci"]),
    ("katak", ["a frog", "a green frog"], ["frog", "froggy", "katak", "kodok"]),
    ("dinosaurus", ["a dinosaur", "a dino"], ["dinosaur", "dino", "rex"]),
    ("hiu", ["a shark", "a shark fin"], ["shark", "hiu"]),
    ("naga", ["a dragon", "dragon scales"], ["dragon", "naga"]),
    ("hati", ["hearts", "a heart shape"], ["heart", "hearts", "hati"]),
    ("bintang", ["stars", "a star shape"], ["star", "stars", "bintang"]),
    ("bulan", ["a crescent moon", "moon and stars"], ["moon", "crescent", "bulan"]),
    ("bunga", ["flowers", "a rose flower"], ["flower", "flowers", "floral", "rose", "roses", "bunga"]),
    ("kupu_kupu", ["a butterfly", "butterflies"], ["butterfly", "butterflies", "kupu"]),
    ("buah", ["strawberries or cherries", "fruit"], ["strawberry", "cherry", "cherries", "fruit", "buah"]),
    ("makanan", ["food like burger, pizza or candy", "sweets and candy"], ["burger", "pizza", "candy", "donut", "cake", "food", "makanan"]),
    ("api", ["flames and fire", "burning flames"], ["flame", "flames", "fire", "api"]),
    ("petir", ["a lightning bolt", "electric lightning"], ["lightning", "bolt", "thunder", "petir"]),
    ("salib", ["a cross", "a gothic cross"], ["cross", "crucifix", "salib"]),
    ("uang", ["money and dollar bills", "dollar signs"], ["money", "dollar", "cash", "uang"]),
    ("tulisan", ["text and letters", "words written on it"], ["text", "quote", "letters", "words"]),
    ("logo", ["a brand logo", "a designer logo"], ["logo", "nike", "adidas", "gucci", "supreme", "brand"]),
    ("wajah_anime", ["an anime character face", "an anime girl or boy picture"], ["anime"]),
    ("kartun", ["a cartoon character", "a cartoon mascot"], ["cartoon", "spongebob", "mickey", "sonic"]),
    ("bendera", ["a national flag", "a flag"], ["flag", "bendera"]),
    ("musik", ["a guitar or music notes", "musical instruments"], ["guitar", "music", "band", "musik"]),
    ("pita", ["a bow or ribbon", "big ribbon bows"], ["bow", "bows", "ribbon", "pita"]),
    ("mahkota", ["a crown", "a golden crown"], ["crown", "tiara", "mahkota"]),
    ("ular", ["a snake", "snake scales"], ["snake", "serpent", "ular"]),
    ("mata", ["eyes", "an eyeball"], ["eye", "eyes", "eyeball"]),
    ("rantai", ["metal chains", "silver chains"], ["chain", "chains", "rantai"]),
]
POLA = [
    ("polos", ["plain solid color", "a single solid color", "plain black with no pattern", "plain white with no pattern"],
     ["plain", "solid", "basic", "polos"]),
    ("garis", ["striped", "stripes pattern"], ["stripe", "stripes", "striped"]),
    ("kotak", ["plaid tartan", "flannel plaid"], ["plaid", "tartan", "flannel"]),
    ("catur", ["checkered checkerboard", "checker pattern"], ["checkered", "checker", "checkerboard"]),
    ("polkadot", ["polka dots", "dotted pattern"], ["polka", "dots", "dotted"]),
    ("bunga", ["floral print", "flower pattern"], ["floral", "flower", "flowers"]),
    ("loreng", ["camouflage pattern", "army camo"], ["camo", "camouflage", "loreng"]),
    ("motif_hewan", ["leopard or zebra animal print", "cheetah print"], ["leopard", "cheetah", "zebra", "cow print"]),
    ("grafis", ["a big graphic print", "printed picture graphic"], ["graphic", "print", "printed"]),
    ("tulisan", ["text print", "letters printed"], ["text", "quote"]),
    ("pelangi", ["rainbow tie-dye", "multicolor rainbow"], ["rainbow", "tie dye", "tiedye", "pelangi"]),
    ("renda", ["lace", "frilly lace"], ["lace", "renda", "frilly"]),
    ("denim", ["blue denim", "jean denim fabric"], ["denim", "jeans", "jean"]),
    ("kulit", ["shiny leather material with stitching", "glossy leather texture"], ["leather", "kulit"]),
    ("kilau", ["sparkly sequins and glitter", "shiny glitter"], ["glitter", "sparkle", "sparkly", "sequin", "rhinestone"]),
    ("bulu", ["fluffy fur", "faux fur"], ["fur", "fluffy", "furry"]),
]
JENIS = {
    "atas": [
        ("kaos", ["a short sleeve t-shirt"], ["tee", "t-shirt", "tshirt", "shirt", "kaos"]),
        ("lengan_panjang", ["a long sleeve shirt"], ["long sleeve", "longsleeve"]),
        ("hoodie", ["a hoodie sweatshirt with hood"], ["hoodie", "hoody", "hooded"]),
        ("sweater", ["a knit sweater or cardigan"], ["sweater", "cardigan", "knit", "jumper", "pullover"]),
        ("jaket", ["a jacket or coat", "a zip-up jacket", "a leather biker jacket"],["jacket", "coat", "puffer", "bomber", "windbreaker", "jaket"]),
        ("jas", ["a blazer suit jacket"], ["suit", "blazer", "tuxedo", "jas"]),
        ("kemeja", ["a button-up collared shirt"], ["button", "collared", "dress shirt", "kemeja", "polo"]),
        ("crop", ["a crop top showing the belly"], ["crop", "cropped"]),
        ("tanktop", ["a tank top or camisole"], ["tank", "cami", "camisole", "singlet"]),
        ("korset", ["a corset bustier top"], ["corset", "bustier", "korset"]),
        ("gaun", ["a dress"], ["dress", "gown", "gaun", "frock"]),
        ("kostum_penuh", ["a full body costume or onesie"], ["onesie", "costume", "kigurumi", "jumpsuit", "bodysuit", "fursuit"]),
        ("zirah", ["armor chest plate"], ["armor", "armour", "chestplate"]),
        ("seragam", ["a uniform"], ["uniform", "seragam"]),
        ("jubah", ["a long robe or kimono"], ["robe", "kimono", "haori", "jubah", "cloak"]),
        ("jersey", ["a sports jersey"], ["jersey"]),
        ("rompi", ["a vest"], ["vest", "rompi"]),
    ],
    "bawah": [
        ("jeans", ["blue jeans denim pants"], ["jeans", "jean", "denim"]),
        ("kargo", ["cargo pants with pockets"], ["cargo"]),
        ("jogger", ["sweatpants or joggers"], ["sweatpants", "joggers", "jogger", "sweats", "trackpants"]),
        ("celana_kain", ["dress trousers slacks"], ["trousers", "slacks", "chinos", "suit pants"]),
        ("celana_pendek", ["shorts"], ["shorts", "short", "jorts"]),
        ("rok_pendek", ["a short mini skirt"], ["mini skirt", "miniskirt", "skirt", "rok"]),
        ("rok_panjang", ["a long maxi skirt"], ["long skirt", "maxi"]),
        ("bawahan_gaun", ["the lower part of a dress"], ["dress", "gown", "gaun"]),
        ("legging", ["leggings or tights"], ["leggings", "tights", "stockings"]),
        ("overall", ["overalls"], ["overall", "overalls", "dungarees"]),
        ("kostum_bawah", ["costume legs"], ["costume", "onesie"]),
        ("zirah_bawah", ["armor leg plates"], ["armor", "armour"]),
    ],
    "kepala": [
        ("topi_baseball", ["a baseball cap"], ["cap", "snapback", "baseball"]),
        ("kupluk", ["a knit beanie"], ["beanie", "kupluk"]),
        ("topi_koboi", ["a cowboy hat"], ["cowboy", "stetson"]),
        ("topi_formal", ["a top hat or fedora"], ["fedora", "tophat", "top hat", "bowler"]),
        ("mahkota", ["a crown or tiara"], ["crown", "tiara", "mahkota"]),
        ("helm", ["a helmet"], ["helmet", "helm"]),
        ("tudung", ["a hood"], ["hood", "tudung"]),
        ("pita_bando", ["a headband or hair bow"], ["headband", "bow", "bando"]),
        ("telinga", ["animal ears"], ["ears", "ear"]),
        ("topeng_kepala", ["a full head mask"], ["head", "mask"]),
        ("tanduk", ["horns"], ["horns", "horn", "tanduk"]),
        ("halo", ["a halo ring"], ["halo"]),
        ("topi_lain", ["a hat"], ["hat", "topi"]),
        # tambahan 16 Okt (lembar kontak: anting & headphone yang diunggah sebagai topi terbaca mahkota/telinga)
        ("anting", ["earrings"], ["earring", "earrings", "anting"]),
        ("headphone", ["headphones or earmuffs"], ["headphone", "headphones", "headset", "earmuffs", "earmuff"]),
    ],
    "wajah": [
        ("kacamata", ["eyeglasses"], ["glasses", "spectacles", "kacamata"]),
        ("kacamata_hitam", ["sunglasses"], ["sunglasses", "shades"]),
        ("masker", ["a face mask covering the mouth"], ["mask", "facemask", "masker"]),
        ("penutup_mata", ["an eyepatch"], ["eyepatch"]),
        ("riasan", ["makeup blush or face stickers"], ["blush", "makeup", "freckles", "sticker", "lashes"]),
        ("tindik", ["a face piercing"], ["piercing", "pierced", "tindik"]),
        ("kumis_jenggot", ["a beard or mustache"], ["beard", "mustache", "moustache", "stubble", "goatee"]),
        ("penutup_kain", ["a blindfold"], ["blindfold"]),
    ],
    "aksen": [
        ("sayap", ["wings"], ["wings", "wing", "sayap"]),
        ("ekor", ["a tail"], ["tail", "ekor"]),
        ("tas", ["a bag or backpack"], ["bag", "backpack", "purse", "tas"]),
        ("senjata", ["a weapon or sword"], ["sword", "katana", "gun", "axe", "scythe", "weapon"]),
        ("jubah_belakang", ["a cape"], ["cape", "cloak"]),
        ("syal", ["a scarf"], ["scarf", "syal"]),
        ("kalung", ["a necklace or chain"], ["necklace", "chain", "pendant", "choker", "kalung"]),
        ("sabuk", ["a belt"], ["belt", "sabuk"]),
        ("boneka", ["a plush toy or pet"], ["plush", "plushie", "pet", "boneka"]),
        ("alat_musik", ["a musical instrument"], ["guitar", "violin", "bass"]),
        ("lain", ["a decorative accessory"], []),
        ("headphone", ["headphones around the neck"], ["headphone", "headphones", "headset"]),
    ],
}
BENTUK = {
    "atas": {
        "lengan": [("tanpa", ["sleeveless"]), ("pendek", ["with short sleeves"]), ("panjang", ["with long sleeves"])],
        "panjang": [("crop", ["cropped above the belly button"]), ("normal", ["regular length"]), ("panjang", ["long to the knees"])],
        "fit": [("longgar", ["oversized and baggy"]), ("pas", ["fitted and tight"])],
        "depan": [("terbuka", ["worn open in front"]), ("tertutup", ["closed in front"])],
    },
    "bawah": {
        "panjang": [("pendek", ["short above the knee"]), ("selutut", ["knee length"]), ("panjang", ["full length down to the ankles"])],
        "fit": [("lebar", ["wide and baggy"]), ("ketat", ["skinny and tight"])],
    },
}
# FUNGSI item 2D (uji emas 16 Okt: 70% "kaos" TShirt klasik BUKAN gambar kaos -- shading perut/otot, kalung dilukis, dsb.)
FUNGSI = [("pakaian", ["a piece of clothing", "a shirt or pants garment"], []),
          ("badan", ["soft gray body shading, abs, belly button or collarbone shadows drawn on skin", "skin shading overlay"],
           ["shading", "shade", "abs", "belly", "navel", "collarbone", "ribcage", "blush", "skin", "body"]),
          ("aksesori", ["a necklace, chain or jewelry drawn on the body", "a painted belt or strap"],
           ["necklace", "chain", "pearls", "pendant", "kalung", "choker", "piercing"]),
          ("grafis", ["a picture, cartoon character, logo, flag or text printed", "a graphic sticker image"],
           ["logo", "flag", "sticker", "decal"])]
# 2D: kata nama untuk PROBE (pengawasan lemah). "shirt" ada di hampir semua nama aset Shirt -> bukan bukti kaos.
KATA_2D = {("atas", "kaos"): ["tee", "t-shirt", "tshirt", "kaos"]}
KAL_KAIN = ["a photo of {d} {n}", "{d} {n}, product photo on white background", "a {n}: {d}"]
MIN_PROBE = 200       # data latih minimal per facet; label dengan < 15 contoh tidak diberi suara oleh probe
KALIMAT = ["a 3d render of {d} roblox {n}", "a roblox avatar {n}, {d}", "{d} {n}"]
KALIMAT_2D = ["a blocky white roblox mannequin wearing a {n}: {d}", "a roblox classic clothing {n} on a blocky avatar, {d}",
              "{d} {n} worn by a blocky white mannequin"]


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def token(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def ada_kata(nama_l, tok, kata):
    for k in kata:
        if " " in k or "-" in k:
            if k in nama_l:
                return True
        elif k in tok:
            return True
    return False


# ---------------------------------------------------------------------------------------------
class Teks:
    """Encoder teks CLIP (hanya teks; gambar sudah di-embed otak.py)."""
    def __init__(self, stub=False):
        self.stub = stub
        self.cache = {}
        if not stub:
            import torch
            from transformers import CLIPModel, CLIPTokenizer
            self.torch = torch
            self.model = CLIPModel.from_pretrained(MODEL_ID).eval()
            self.tok = CLIPTokenizer.from_pretrained(MODEL_ID)

    def __call__(self, kal):
        hasil = []
        baru = [k for k in kal if k not in self.cache]
        if baru:
            if self.stub:
                import hashlib
                for k in baru:
                    r = np.random.default_rng(int(hashlib.md5(k.encode()).hexdigest()[:8], 16))
                    v = r.normal(size=512).astype("float32")
                    self.cache[k] = v / np.linalg.norm(v)
            else:
                with self.torch.no_grad():
                    for i in range(0, len(baru), 256):
                        b = baru[i:i + 256]
                        f = self.model.get_text_features(**self.tok(b, return_tensors="pt", padding=True))
                        f = f / f.norm(dim=-1, keepdim=True)
                        for k, v in zip(b, f.cpu().numpy().astype("float32")):
                            self.cache[k] = v
        for k in kal:
            hasil.append(self.cache[k])
        return np.stack(hasil)


def vektor_label(teks, labels, noun, kal_t=None):
    """rata-rata ensemble kalimat per label -> matriks (L, 512) ternormalisasi"""
    out = []
    for lab in labels:
        desk = lab[1]
        kal = [t.format(d=d, n=noun) for d in desk for t in (kal_t or KALIMAT)]
        v = teks(kal).mean(axis=0)
        out.append(v / np.linalg.norm(v))
    return np.stack(out)


def softmax_terkoreksi(X, T, alfa=1.0):
    """logit CLIP dikurangi alfa x rata-rata per label di kelompok ini (bias kalimat), lalu softmax.
    alfa 0 = CLIP mentah (label "umum" seperti kulit/hitam menang terus), 1 = tiap label disamaratakan (label langka
    terlalu sering). Alfa dipilih per facet dari data (lihat pilih_alfa)."""
    L = SUHU * (X @ T.T)
    if alfa:
        L = L - alfa * L.mean(axis=0, keepdims=True)
    L = L - L.max(axis=1, keepdims=True)
    P = np.exp(L)
    return P / P.sum(axis=1, keepdims=True)


ALFA_CALON = (0.0, 0.25, 0.5, 0.75, 1.0)
NETRAL = ("biasa", "tanpa", "polos", "lain", "topi_lain")


def pilih_alfa(X, T, labels, nama_l, toks):
    """kalibrasi berbasis data: alfa dengan kecocokan top-1 gambar-vs-nama tertinggi (label nama tunggal, bukan netral).
    -> (alfa, {alfa: (cocok1, cocok2, total)})"""
    baris, target = [], []
    for r in range(X.shape[0]):
        ln = label_nama(labels, nama_l[r], toks[r])
        if ln is not None and labels[ln][0] not in NETRAL:
            baris.append(r)
            target.append(ln)
    skor = {}
    if len(baris) < 30:
        return 0.5, skor
    Xs, tg = X[baris], np.array(target)
    for a in ALFA_CALON:
        L = SUHU * (X @ T.T)
        mu = L.mean(axis=0, keepdims=True)
        Ls = SUHU * (Xs @ T.T) - a * mu
        o = np.argsort(-Ls, axis=1)[:, :2]
        skor[a] = (int((o[:, 0] == tg).sum()), int((o == tg[:, None]).any(axis=1).sum()), len(baris))
    terbaik = max(ALFA_CALON, key=lambda a: (skor[a][0], -abs(a - 0.5)))
    return terbaik, skor


def fusi_nama(P, labels, nama_l, toks):
    """bukti nama: label yang kata kuncinya ada di nama mendapat massa BOBOT_NAMA (dibagi rata), lalu dinormalkan"""
    P = P.copy()
    for r in range(P.shape[0]):
        hit = [j for j, lab in enumerate(labels) if lab[2] and ada_kata(nama_l[r], toks[r], lab[2])]
        if hit:
            P[r] *= (1 - BOBOT_NAMA)
            for j in hit:
                P[r, j] += BOBOT_NAMA / len(hit)
    return P


def label_nama(labels, nama_l, tok):
    """label dari nama saja (untuk evaluasi): hanya bila tepat SATU label cocok"""
    hit = [j for j, lab in enumerate(labels) if lab[2] and ada_kata(nama_l, tok, lab[2])]
    return hit[0] if len(hit) == 1 else None


def top2(P):
    o = np.argsort(-P, axis=1)[:, :2]
    p = np.take_along_axis(P, o, axis=1)
    return o, p


def latih_probe(X, y, ncls, iters=400, lr=0.05, l2=1e-4):
    """regresi softmax seimbang kelas (Adam, numpy). Fitur gambar CLIP -> label dari NAMA item lain (pengawasan lemah).
    Uji emas 16 Okt (uji2d/): baju 2D jenis 26%->49%, celana 2D jenis 14%->53%, tema baju 41%->62% bila digabung zero-shot."""
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


def log_softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    return Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))


def gabung_probe(Pimg, XX, labels, kel, nama_l, toks):
    """P gambar (zero-shot) x P probe (dilatih dari nama item lain) -> P gabungan. Label tanpa cukup contoh: probe netral."""
    ys, rows = [], []
    for r in range(XX.shape[0]):
        hit = [j for j, lab in enumerate(labels) if kata_2d(kel, lab) and ada_kata(nama_l[r], toks[r], kata_2d(kel, lab))]
        if len(hit) == 1:
            ys.append(hit[0])
            rows.append(r)
    if len(ys) < MIN_PROBE:
        return Pimg, 0
    ys = np.array(ys, dtype=np.int64)
    cnt = np.bincount(ys, minlength=len(labels))
    W = latih_probe(XX[rows].astype(np.float32), ys, len(labels))
    Zp = np.hstack([XX.astype(np.float32) * 10.0, np.ones((XX.shape[0], 1), dtype=np.float32)]) @ W
    aktif = cnt >= 15
    if aktif.any():
        netral = Zp[:, aktif].mean(axis=1, keepdims=True)
        Zp[:, ~aktif] = netral
    # rata-rata log (bukan jumlah): urutan label sama, peluang tidak terlalu yakin (lembar kontak: "I love mm2" ninja 85)
    L = 0.5 * np.log(np.maximum(Pimg, 1e-9)) + 0.5 * log_softmax(Zp)
    L -= L.max(axis=1, keepdims=True)
    P = np.exp(L)
    return P / P.sum(axis=1, keepdims=True), len(ys)


def kata_2d(kel, lab):
    return KATA_2D.get((kel, lab[0]), lab[2])


# ---------------------------------------------------------------------------------------------
def muat():
    d = np.load(P_EMB, allow_pickle=False)
    ids = d["ids"].astype("int64")
    E = d["emb"].astype("float32")
    E /= np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-6)
    e2 = {}
    if os.path.exists(P_E2D):
        try:
            d2 = np.load(P_E2D, allow_pickle=False)
            em = d2["emb"].astype("float32")
            em /= np.maximum(np.linalg.norm(em, axis=1, keepdims=True), 1e-6)
            for k, i in enumerate(d2["ids"].tolist()):
                e2[int(i)] = em[k]
        except Exception as ex:
            log("emb2d gagal dimuat:", ex)
    with gzip.open(P_STATE, "rt", encoding="utf-8") as f:
        st = json.load(f)
    meta = st.get("meta", {})
    log(f"embedding {len(ids)} | potongan 2D {len(e2)} | meta {len(meta)}")
    return ids, E, e2, meta


def ids_ekspor():
    s = set()
    for k in range(SHARD):
        p = f"model/item_{k}.json"
        if os.path.exists(p):
            s.update(int(x) for x in json.load(open(p, encoding="utf-8")).get("d", {}))
    return s


def bangun(teks, ids, E, e2, meta, hanya=None):
    """-> dict id -> baris kartu, plus statistik evaluasi"""
    idx_of = {int(i): k for k, i in enumerate(ids.tolist())}
    kel_items = collections.defaultdict(list)
    for i in ids.tolist():
        if hanya is not None and i not in hanya:
            continue
        m = meta.get(str(i))
        if not m:
            continue
        kel = ASET_KE_KEL.get(int(m.get("t") or 0))
        if kel:
            kel_items[kel].append(i)
    kartu, evals, contoh = {}, {}, []
    # baju/celana/kaos KLASIK 2D tampil di manekin kotak; kalimat CLIP-nya harus menyebut manekin itu, kalau tidak siluet
    # manekin terbaca "zirah"/"kostum" (lembar kontak 16 Okt: 9 dari 36 baju 2D jadi zirah). 3D tampil sendiri.
    sub = []
    for kel, daftar in kel_items.items():
        if kel in ("atas", "bawah"):
            d2 = [i for i in daftar if int(meta[str(i)].get("t") or 0) in ASET_2D]
            d3 = [i for i in daftar if int(meta[str(i)].get("t") or 0) not in ASET_2D]
            sub += [(kel, "2D", d2, KALIMAT_2D), (kel, "3D", d3, KALIMAT)]
        else:
            sub.append((kel, "", daftar, KALIMAT))
    for kel, varian, daftar, kal_t in sub:
        if not daftar:
            continue
        noun = KEL_NOUN[kel]
        n = len(daftar)
        log(f"kelompok {kel}{varian}: {n} item")
        X = np.stack([E[idx_of[i]] for i in daftar])
        # potongan pakaian (tanpa manekin) untuk 2D: jenis/bentuk/pola lebih tepat; tema/subjek dari rata-rata keduanya
        Xk = X.copy()
        for r, i in enumerate(daftar):
            if i in e2 and int(meta[str(i)].get("t") or 0) in ASET_2D:
                Xk[r] = e2[i]
        Xt = Xk + X
        Xt /= np.maximum(np.linalg.norm(Xt, axis=1, keepdims=True), 1e-6)
        nama = [(meta[str(i)].get("n") or "") for i in daftar]
        nama_l = [s.lower() for s in nama]
        toks = [token(s) for s in nama]
        hasil = {}
        # TEMA & SUBJEK (semua kelompok kecuali rambut/sepatu untuk subjek)
        facets = [("tema", TEMA, Xt, noun)]
        if kel not in ("rambut", "sepatu"):
            facets.append(("subjek", SUBJEK, Xt, noun))
        if kel in ("atas", "bawah"):
            facets.append(("pola", POLA, Xk, noun))
        if kel in JENIS:
            facets.append(("jenis", JENIS[kel], Xk, noun))
        for nm, labels, XX, nn in facets:
            T = vektor_label(teks, labels, nn, kal_t)
            # evaluasi jujur: gambar saja vs label nama (hanya nama yang menunjuk tepat satu label), sekaligus kalibrasi
            alfa, skor = pilih_alfa(XX, T, labels, nama_l, toks)
            if skor:
                evals[f"{kel}{varian}/{nm}"] = {"alfa": alfa, "skor": skor}
            Pimg = softmax_terkoreksi(XX, T, alfa)
            Pg = Pimg
            if varian == "2D" and nm in ("tema", "pola", "jenis"):
                # rev 30: baju/celana 2D -- gambar 150 px manekin terlalu kabur untuk zero-shot saja; probe dari nama item lain
                Pg, nLatih = gabung_probe(Pimg, XX, labels, kel, nama_l, toks)
                log(f"  probe {kel}{varian}/{nm}: latih {nLatih}")
            Pf = fusi_nama(Pg, labels, nama_l, toks)
            hasil[nm] = (top2(Pf), None, Pimg)
        # FUNGSI kaos klasik (TShirt): gambar potongan (tanpa ikon kaos) zero-shot; uji emas 51/55 benar
        if varian == "2D" and kel == "atas":
            kaos = [r for r, i in enumerate(daftar) if int(meta[str(i)].get("t") or 0) == 2]
            if kaos:
                T = vektor_label(teks, FUNGSI, "t-shirt graphic", KAL_KAIN)
                Pk = softmax_terkoreksi(Xk[kaos], T, 0.5)
                fk = np.full(n, -1, dtype=np.int64)
                fk[kaos] = np.argmax(fusi_nama(Pk, FUNGSI, [nama_l[r] for r in kaos], [toks[r] for r in kaos]), axis=1)
                hasil["fungsi"] = fk
        for nm, sb in (BENTUK.get(kel) or {}).items():
            T = vektor_label(teks, [(a, b, []) for a, b in sb], noun, kal_t)
            hasil["b_" + nm] = (top2(softmax_terkoreksi(Xk, T, 0.5)), None, None)
        for r, i in enumerate(daftar):
            def tp(nm, k=2):
                if nm not in hasil:
                    return [-1, 0] * k
                (o, p), _, _ = hasil[nm]
                out = []
                for q in range(k):
                    out += [int(o[r, q]), int(round(100 * float(p[r, q])))]
                return out
            # baris: [kel, jenis, p, tema1, p, tema2, p, subjek1, p, subjek2, p, pola, p, b_lengan, b_panjang, b_fit, b_depan,
            #         imgTema]  (indeks 0-based di sini; -1 = tidak ada)
            b = [KELOMPOK.index(kel)] + tp("jenis", 1) + tp("tema") + tp("subjek") + tp("pola", 1)
            for nm in ("b_lengan", "b_panjang", "b_fit", "b_depan"):
                b.append(int(hasil[nm][0][0][r, 0]) if nm in hasil else -1)
            b.append(int(np.argmax(hasil["tema"][2][r])))  # tema menurut GAMBAR saja (transparansi)
            b.append(int(hasil["fungsi"][r]) if "fungsi" in hasil else -1)  # skema 2: fungsi (kaos klasik saja)
            kartu[i] = b
            if r < 3000:
                contoh.append((kel, i, nama[r], b))
    return kartu, evals, contoh


def label_baca(kel, b):
    """baris kartu -> teks yang bisa dibaca manusia (laporan)"""
    def nm(lst, j):
        return lst[j][0] if 0 <= j < len(lst) else "-"
    s = []
    if kel in JENIS and b[1] >= 0:
        s.append(f"jenis={nm(JENIS[kel], b[1])}({b[2]})")
    s.append(f"tema={nm(TEMA, b[3])}({b[4]})/{nm(TEMA, b[5])}({b[6]})")
    if b[7] >= 0:
        s.append(f"subjek={nm(SUBJEK, b[7])}({b[8]})/{nm(SUBJEK, b[9])}({b[10]})")
    if b[11] >= 0:
        s.append(f"pola={nm(POLA, b[11])}({b[12]})")
    bt = BENTUK.get(kel)
    if bt:
        bb = []
        for k, nmb in enumerate(("lengan", "panjang", "fit", "depan")):
            if nmb in bt and b[13 + k] >= 0:
                bb.append(f"{nmb}={bt[nmb][b[13 + k]][0]}")
        s.append(" ".join(bb))
    s.append(f"[gambar:{nm(TEMA, b[17])}]")
    if len(b) > 18 and b[18] >= 0:
        s.append(f"fungsi={nm(FUNGSI, b[18])}")
    return " | ".join(s)


def nilai_emas(kartu):
    """akurasi kartu AKHIR (setelah fusi nama) terhadap label emas manual uji2d/emas.json (gambar 420 dilihat mata).
    -> daftar baris tabel markdown; kosong bila berkas emas tidak ada."""
    try:
        sampel = json.load(open("uji2d/sampel.json", encoding="utf-8"))["sampel"]
        emas = json.load(open("uji2d/emas.json", encoding="utf-8"))
    except Exception:
        return []
    per_t = collections.defaultdict(list)
    for i, t in sampel:
        per_t[str(t)].append(int(i))
    kol = {"jenis": 1, "tema": 3, "pola": 11, "fungsi": 18}
    out = []
    for t, nmT in (("11", "baju 2D"), ("12", "celana 2D"), ("2", "kaos klasik")):
        for f, c in kol.items():
            gold = (emas.get(t) or {}).get(f)
            if not gold:
                continue
            kel = "bawah" if t == "12" else "atas"
            labels = {"jenis": JENIS[kel], "tema": TEMA, "pola": POLA, "fungsi": FUNGSI}[f]
            nama = [x[0] for x in labels]
            benar = n = tanpa = 0
            for i, g in zip(per_t[t], gold):
                if g is None:
                    continue
                b = kartu.get(i)
                if not b or len(b) <= c or b[c] < 0:
                    tanpa += 1
                    continue
                n += 1
                benar += int(nama[b[c]] == g)
            if n:
                out.append(f"| {nmT} | {f} | {n} | {benar} | {100 * benar / n:.0f}% | {tanpa} |")
    return out


def label_semua():
    return {"kelompok": KELOMPOK, "tema": [t[0] for t in TEMA], "subjek": [t[0] for t in SUBJEK], "pola": [t[0] for t in POLA],
            "jenis": {k: [t[0] for t in v] for k, v in JENIS.items()},
            "bentuk": {k: {a: [x[0] for x in b] for a, b in v.items()} for k, v in BENTUK.items()},
            "kolom": ["kelompok", "jenis", "jenisP", "tema1", "tema1P", "tema2", "tema2P", "subjek1", "subjek1P", "subjek2",
                      "subjek2P", "pola", "polaP", "lengan", "panjang", "fit", "depan", "temaGambar", "fungsi"],
            "fungsi": [t[0] for t in FUNGSI],
            "kelompokAset": {str(k): v for k, v in ASET_KE_KEL.items()}}


def tulis(kartu, versi, evals):
    """kartu/info.json (kecil: versi, label, kalibrasi) + kartu/kartu_{0..7}.json (baris per item, shard = id % 8)"""
    os.makedirs("kartu", exist_ok=True)
    sh = [dict() for _ in range(SHARD)]
    for i, b in kartu.items():
        sh[i % SHARD][str(i)] = b
    for s in range(SHARD):
        with open(f"kartu/kartu_{s}.json.tmp", "w", encoding="utf-8") as f:
            json.dump({"versi": versi, "skema": SKEMA, "d": sh[s]}, f, ensure_ascii=False, separators=(",", ":"))
        os.replace(f"kartu/kartu_{s}.json.tmp", f"kartu/kartu_{s}.json")
    info = {"versi": versi, "skema": SKEMA, "n": len(kartu), "shard": SHARD, "model": MODEL_ID, "label": label_semua(),
            "kalibrasi": {k: v["alfa"] for k, v in evals.items()}}
    with open("kartu/info.json.tmp", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, separators=(",", ":"))
    os.replace("kartu/info.json.tmp", "kartu/info.json")


def laporan(kartu, evals, contoh, meta, uji, versi):
    L = [f"# Laporan Kartu Item (MATA v2) — versi {versi}", "",
         "Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.", "",
         f"- Item berkartu: **{len(kartu)}**", "",
         "## Kalibrasi & akurasi gambar saja vs nama", "",
         "Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP",
         "yang dipilih otomatis (kecocokan top-1 tertinggi).", "",
         "| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |", "|---|---|---|---|---|---|---|"]
    for k in sorted(evals):
        a, sk = evals[k]["alfa"], evals[k]["skor"]
        c1, c2, t = sk[a]
        L.append(f"| {k} | {t} | {a} | {100 * c1 / t:.0f}% | {100 * c2 / t:.0f}% | {100 * sk[0.0][0] / t:.0f}% | {100 * sk[1.0][0] / t:.0f}% |")
    L += ["", "Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.", ""]
    em = nilai_emas(kartu)
    if em:
        L += ["## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)", "",
              "Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,",
              "celana tema 35%, pola 39-40%, kaos fungsi belum ada.", "",
              "| tipe | facet | n | benar | akurasi | tanpa kartu |", "|---|---|---|---|---|---|"] + em + [""]
    if uji:
        L += ["## Item uji", ""]
        for i in uji:
            m = meta.get(str(i)) or {}
            kel = ASET_KE_KEL.get(int(m.get("t") or 0), "?")
            b = kartu.get(i)
            L.append(f"- `{i}` {m.get('n', '?')} ({kel}): " + (label_baca(kel, b) if b else "**tidak ada kartu** (belum di-embed)"))
        L.append("")
    # nama vs gambar berbeda tema (contoh kasus "labu berwajah bebek")
    beda = []
    for kel, i, nm, b in contoh:
        tl = label_nama(TEMA, nm.lower(), token(nm))
        if tl is not None and b[17] != tl and TEMA[b[17]][0] != "biasa" and b[4] >= 50:
            beda.append((kel, i, nm, b, tl))
    L += ["## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)", ""]
    for kel, i, nm, b, tl in beda[:40]:
        L.append(f"- `{i}` {nm[:60]} — nama: {TEMA[tl][0]} | " + label_baca(kel, b))
    L += ["", "## Contoh acak per kelompok", ""]
    per = collections.defaultdict(list)
    for kel, i, nm, b in contoh:
        per[kel].append((i, nm, b))
    rng = np.random.default_rng(3)
    for kel in sorted(per):
        L.append(f"### {kel}")
        pil = rng.choice(len(per[kel]), size=min(25, len(per[kel])), replace=False)
        for q in pil:
            i, nm, b = per[kel][q]
            L.append(f"- `{i}` {nm[:60]} — " + label_baca(kel, b))
        L.append("")
    # sebaran tema per kelompok
    L += ["## Sebaran tema (fusi) per kelompok", ""]
    for kel in sorted(per):
        c = collections.Counter(TEMA[b[3]][0] for _, _, b in per[kel])
        L.append(f"- {kel}: " + ", ".join(f"{k} {v}" for k, v in c.most_common(12)))
    with open("LAPORAN_KARTU.md", "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    uji = []
    if "--uji" in sys.argv:
        uji = [int(x) for x in sys.argv[sys.argv.index("--uji") + 1:] if x.isdigit()]
    stub = "--stub" in sys.argv
    t0 = time.time()
    ids, E, e2, meta = muat()
    teks = Teks(stub=stub)
    kartu, evals, contoh = bangun(teks, ids, E, e2, meta)
    versi = int(time.time())
    tulis(kartu, versi, evals)
    laporan(kartu, evals, contoh, meta, uji, versi)
    log(f"selesai: {len(kartu)} kartu, {time.time() - t0:.0f} dtk")


if __name__ == "__main__":
    main()
