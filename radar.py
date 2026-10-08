"""RADAR UGC GRATIS -- Katalog Praktis (Roblox)

Mencari item UGC GRATIS (collectible/limited, harga 0) yang hanya bisa diklaim di experience tertentu, MASIH ADA
stoknya dan SEDANG dijual, lalu mencatat experience tempat klaimnya (universe -> place utama, nama game, pemain aktif).
Hasil: radar.json di cabang `radar` repo ini. Server Roblox membacanya, MENGECEK ULANG stok secara live
(AvatarEditorService) sebelum menampilkan, lalu menyediakan tombol teleport ke game itu.

Aturan ketat (permintaan pemilik): hanya item yang benar-benar siap klaim (IsForSale, harga 0, stok > 0, lokasi jual
jelas 1-3 experience). Cara klaim di game lain TIDAK ditampilkan (tidak spoiler). Tanpa kunci API, tanpa biaya.
"""
import json
import re
import time

import requests

S = requests.Session()
S.headers["User-Agent"] = "KatalogPraktis-RadarUGC/1.0"
S.headers["Accept"] = "application/json"
LOG = []
MULAI = time.time()
BATAS_DETIK = 9 * 60          # workflow dibatasi 15 menit; sisakan waktu untuk push
MAKS_DETAIL = 200             # panggilan economy per putaran
MAKS_ITEM = 40                # item di radar.json
MAKS_PER_GAME = 4             # supaya radar tidak dikuasai satu game
# game yang klaimnya butuh KODE dari luar (medsos/Discord) tidak "siap klaim" untuk pemain biasa -> dilewati
POLA_KODE = re.compile(r"\bcodes?\b|\bkode\b|\bpromo\b", re.I)


def log(m):
    t = time.time() - MULAI
    baris = f"[{t:6.1f}s] {m}"
    print(baris, flush=True)
    LOG.append(baris)


def get(url, params=None, coba=4):
    jeda = 1.5
    for _ in range(coba):
        try:
            r = S.get(url, params=params, timeout=20)
        except Exception as e:  # jaringan
            log(f"  galat jaringan {url.split('?')[0]}: {e}")
            time.sleep(jeda)
            jeda *= 2
            continue
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                log(f"  bukan JSON: {url.split('?')[0]}")
                return None
        if r.status_code == 429:
            ra = r.headers.get("Retry-After", "")
            t = float(ra) if ra.replace(".", "", 1).isdigit() else jeda * 3
            log(f"  429 {url.split('?')[0]} -> tunggu {min(60.0, t):.0f}s")
            time.sleep(min(60.0, t))
            jeda *= 2
            continue
        if r.status_code >= 500:
            time.sleep(jeda)
            jeda *= 2
            continue
        log(f"  kode {r.status_code} {url.split('?')[0]} {r.text[:120]!r}")
        return None
    return None


def cari_kandidat():
    """Item collectible berharga 0 dari pencarian katalog publik (beberapa urutan & kata kunci)."""
    kandidat = {}
    kueri = [
        {"Category": "1", "SalesTypeFilter": "2", "MaxPrice": "0", "SortType": "3", "Limit": "120"},
        {"Category": "1", "SalesTypeFilter": "2", "MaxPrice": "0", "SortType": "0", "Limit": "120"},
        {"Category": "1", "Keyword": "free ugc", "SalesTypeFilter": "2", "MaxPrice": "0", "SortType": "3", "Limit": "120"},
        {"Category": "1", "Keyword": "free", "SalesTypeFilter": "2", "MaxPrice": "0", "SortType": "3", "Limit": "120"},
    ]
    contoh_dicatat = False
    for q in kueri:
        kursor = ""
        for _ in range(3):
            if time.time() - MULAI > BATAS_DETIK / 2:
                break
            p = dict(q)
            if kursor:
                p["Cursor"] = kursor
            js = get("https://catalog.roblox.com/v2/search/items/details", p) or {}
            data = js.get("data") or []
            if data and not contoh_dicatat:
                contoh_dicatat = True
                log("  contoh kolom katalog: " + ", ".join(sorted(data[0].keys())))
            for e in data:
                if e.get("itemType") != "Asset":
                    continue
                i = e.get("id")
                if not isinstance(i, int):
                    continue
                harga = e.get("price")
                if harga is None:
                    harga = e.get("lowestPrice")
                restr = e.get("itemRestrictions") or []
                if harga not in (0, None):
                    continue
                if "Collectible" not in restr and "Limited" not in restr and "LimitedUnique" not in restr:
                    continue
                # stok sudah 0 / hanya dijual di toko (bukan di game) -> tak perlu dicek detail
                if isinstance(e.get("unitsAvailableForConsumption"), int) and e.get("totalQuantity") and e["unitsAvailableForConsumption"] <= 0:
                    continue
                if e.get("saleLocationType") == "ShopOnly":
                    continue
                kandidat[i] = e
            kursor = js.get("nextPageCursor") or ""
            log(f"  kueri {q.get('Keyword', '-')}/sort {q['SortType']}: +{len(data)} baris, kandidat {len(kandidat)}")
            if not kursor:
                break
            time.sleep(1.5)
    return kandidat


def detail(kandidat):
    hasil = []
    n = 0
    for i, e in kandidat.items():
        if n >= MAKS_DETAIL or time.time() - MULAI > BATAS_DETIK:
            break
        n += 1
        d = get(f"https://economy.roblox.com/v2/assets/{i}/details")
        time.sleep(0.7)
        if not isinstance(d, dict):
            continue
        sl = d.get("SaleLocation") or {}
        uids = [u for u in (sl.get("UniverseIds") or []) if isinstance(u, int) and u > 0]
        sisa = d.get("Remaining")
        harga = d.get("PriceInRobux")
        cid = d.get("CollectiblesItemDetails") or {}
        if not d.get("IsForSale"):
            continue
        if harga != 0:
            continue
        if not isinstance(sisa, int) or sisa <= 0:
            continue
        if not uids or len(uids) > 3:
            continue
        kreator = (d.get("Creator") or {}).get("Name") or e.get("creatorName") or ""
        hasil.append({
            "id": i,
            "n": str(d.get("Name") or e.get("name") or "")[:60],
            "c": str(kreator)[:30],
            "t": d.get("AssetTypeId"),
            "s": sisa,
            "q": cid.get("TotalQuantity"),
            "uids": uids,
            "dibuat": d.get("Created") or "",
        })
    log(f"detail: {n} item dicek, {len(hasil)} lolos (gratis, dijual, stok ada, 1-3 experience)")
    return hasil


def game_info(uids):
    info = {}
    daftar = sorted(set(uids))
    for k in range(0, len(daftar), 50):
        js = get("https://games.roblox.com/v1/games", {"universeIds": ",".join(str(u) for u in daftar[k:k + 50])}) or {}
        for g in js.get("data") or []:
            if isinstance(g.get("id"), int) and isinstance(g.get("rootPlaceId"), int):
                info[g["id"]] = {"p": g["rootPlaceId"], "g": str(g.get("name") or "")[:50], "pl": int(g.get("playing") or 0)}
        time.sleep(1.0)
    log(f"game: {len(info)} dari {len(daftar)} universe terbaca")
    return info


def main():
    kandidat = cari_kandidat()
    log(f"kandidat katalog: {len(kandidat)}")
    item = detail(kandidat)
    gi = game_info([u for it in item for u in it["uids"]])
    keluar = []
    lewat_kode = 0
    for it in item:
        terbaik = None
        for u in it["uids"]:
            g = gi.get(u)
            if g and (terbaik is None or g["pl"] > terbaik[1]["pl"]):
                terbaik = (u, g)
        if not terbaik:
            continue
        u, g = terbaik
        if POLA_KODE.search(g["g"]):
            lewat_kode += 1
            continue
        keluar.append({"id": it["id"], "n": it["n"], "c": it["c"], "t": it["t"], "s": it["s"], "q": it["q"],
                       "u": u, "p": g["p"], "g": g["g"], "pl": g["pl"]})
    # game yang sedang ramai & stok masih banyak didahulukan
    keluar.sort(key=lambda x: (-(1 if x["pl"] > 0 else 0), -min(x["s"], 1000), -x["pl"], -x["id"]))
    per_game, rapi = {}, []
    for x in keluar:
        if per_game.get(x["u"], 0) >= MAKS_PER_GAME:
            continue
        per_game[x["u"]] = per_game.get(x["u"], 0) + 1
        rapi.append(x)
    log(f"dilewati: {lewat_kode} item di game ber-kode; {len(keluar) - len(rapi)} item kelebihan per game")
    keluar = rapi[:MAKS_ITEM]
    with open("radar.json", "w", encoding="utf-8") as f:
        json.dump({"v": 1, "w": int(time.time()), "n": len(keluar), "items": keluar}, f, ensure_ascii=False, separators=(",", ":"))
    log(f"SELESAI: {len(keluar)} item siap klaim ditulis ke radar.json")
    with open("LOG_RADAR.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # tetap tulis log & radar kosong supaya server tidak membaca data basi yang salah
        log(f"GAGAL: {e!r}")
        with open("radar.json", "w", encoding="utf-8") as f:
            json.dump({"v": 1, "w": int(time.time()), "n": 0, "items": [], "galat": str(e)[:200]}, f)
        with open("LOG_RADAR.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(LOG) + "\n")
