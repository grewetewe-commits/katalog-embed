# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-10T13:30:53.491435+00:00 | putaran ke-34
- Outfit nyata terkumpul: **48116** | masuk bank (lolos saring): **7980**
  (ditolak karena item inti tidak bisa dibeli: 23117, tidak koheren: 2356)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3420, "gaya_masuk": 1024, "gaya_gemini": 0, "meta": {"diminta": 1278, "diperbarui": 1114, "hilang": 64, "sisa_antre": 537}, "sepatu": {"cari": 30, "lihat": 2307, "baru": 3, "total": 4731}} | permintaan HTTP 4086, kena 429: 28, gagal 61

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.341 |
| CLIP netral-slot | 0.503 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.782 |
| Model MLP (dilatih) | 0.803 |

- Dipakai: **mlp** | soal uji 41949 | outfit latih 40906, uji 7192
- AUC koherensi (outfit asli vs setengah-diacak): model 0.810, CLIP 0.719
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 531 | item baru diminta pemain: 16
- Durasi putaran: **64.0 menit** | META: {"diminta": 1278, "diperbarui": 1114, "hilang": 64, "sisa_antre": 537}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.608** vs kemiripan gaya saja 0.448
- Masuk 5% teratas: model **0.719** vs 0.555 | 3206 soal | contoh latih 116343
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |
| 32 | 2026-10-10T06:53 | 45845 | 112870 | 0.793 | 25 |
| 33 | 2026-10-10T10:03 | 47092 | 114091 | 0.803 | 25 |
| 34 | 2026-10-10T13:30 | 48116 | 114932 | 0.803 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.851 pada 7333 item berlabel wanita & 2084 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1880 | 0.553 | 0.700 | 0.999 | v2 |
| FaceAcc | 2277 | 0.559 | 0.678 | 0.999 | v2 |
| Front | 1886 | 0.534 | 0.636 | 0.999 | v2 |
| Hair | 8159 | 0.694 | 0.806 | 1.000 | v2 |
| Hat | 6249 | 0.586 | 0.709 | 0.999 | v2 |
| LayerAtas | 5202 | 0.483 | 0.728 | 0.999 | v2 |
| LayerBawah | 3401 | 0.518 | 0.753 | 1.000 | v2 |
| Neck | 1596 | 0.579 | 0.707 | 0.999 | v2 |
| Pants | 3688 | 0.079 | 0.663 | 0.999 | v2 |
| Sepatu | 3909 | 0.615 | 0.708 | 1.000 | v2 |
| Shirt | 3668 | 0.281 | 0.724 | 1.000 | v2 |
| Shoulder | 826 | 0.584 | 0.689 | 1.000 | v2 |
| TShirt | 93 | 0.194 | 0.527 | 0.998 | v2 |
| Waist | 2056 | 0.594 | 0.688 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 14340 item | AUC {"asli": 0.586, "potongan": 0.604, "rata": 0.609} | label wanita/pria [573, 234] | dipakai: **rata**
- Pants: 13995 item | AUC {"asli": 0.674, "potongan": 0.683, "rata": 0.69} | label wanita/pria [1165, 189] | dipakai: **asli**
- TShirt: 2894 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [50, 14] | dipakai: **asli**

## Sepatu (bundle): 4731 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2307, "baru": 3, "total": 4731}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
