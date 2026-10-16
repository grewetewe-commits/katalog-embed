#!/usr/bin/env python3
"""
PROBE 3D (sekali jalan, untuk verifikasi -- bukan bagian pipeline): memastikan format NYATA endpoint resmi
thumbnails.roblox.com/v1/assets-thumbnail-3d (Beta, docs: create.roblox.com/docs/cloud/reference/domains/thumbnails)
sebelum kode Kartu 3D dibangun di atasnya. Tidak menebak format: semua kunci & ukuran dicetak ke log.
Memakai ROBLOX_API_KEY (secret repo yang sudah ada) bila tersedia, tanpa itu dicoba anonim.
"""
import os, sys, json, time
import requests

ID_UJI = [int(x) for x in sys.argv[1:]] or [126884250250747, 72558563872966, 8565346973]
KEY = os.environ.get("ROBLOX_API_KEY") or ""
H = {"User-Agent": "KatalogPraktis-kartu/1.0 (GitHub Actions; github.com/grewetewe-commits/katalog-embed)"}


def get(url, params=None, kunci=False):
    h = dict(H)
    if kunci and KEY:
        h["x-api-key"] = KEY
    r = requests.get(url, params=params, headers=h, timeout=30)
    return r


for aid in ID_UJI:
    print("=" * 70, aid, flush=True)
    for kunci in (False, True):
        try:
            r = get("https://thumbnails.roblox.com/v1/assets-thumbnail-3d", {"assetId": aid}, kunci)
            print(f"[kunci={kunci}] HTTP {r.status_code} | {r.text[:400]}", flush=True)
            if r.status_code != 200:
                continue
            js = r.json()
            url = js.get("imageUrl")
            if not url:
                continue
            r2 = requests.get(url, headers=H, timeout=30)
            print(f"  imageUrl -> HTTP {r2.status_code}, {len(r2.content)} byte, tipe {r2.headers.get('content-type')}", flush=True)
            try:
                d = r2.json()
                print("  kunci JSON 3D:", list(d.keys()), flush=True)
                print("  isi ringkas:", json.dumps({k: (v if not isinstance(v, (list, dict)) or len(json.dumps(v)) < 300 else str(v)[:300])
                                                 for k, v in d.items()})[:1500], flush=True)
            except Exception as ex:
                print("  bukan JSON:", ex, r2.content[:200], flush=True)
            break
        except Exception as ex:
            print(f"[kunci={kunci}] gagal: {ex}", flush=True)
        time.sleep(1)
