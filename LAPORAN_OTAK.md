# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-10T22:43:01.649881+00:00 | putaran ke-35
- Outfit nyata terkumpul: **49352** | masuk bank (lolos saring): **7979**
  (ditolak karena item inti tidak bisa dibeli: 23990, tidak koheren: 2314)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4050, "gaya_masuk": 1235, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4658, "hilang": 42, "sisa_antre": 2614}, "sepatu": {"cari": 30, "lihat": 2800, "baru": 33, "total": 4764}} | permintaan HTTP 4869, kena 429: 98, gagal 50

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.340 |
| CLIP netral-slot | 0.502 |
| CLIP PCA-32 (tanpa belajar) | 0.486 |
| Model linear (dilatih) | 0.783 |
| Model MLP (dilatih) | 0.802 |

- Dipakai: **mlp** | soal uji 42894 | outfit latih 41979, uji 7354
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.715
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 532 | item baru diminta pemain: 32
- Durasi putaran: **63.3 menit** | META: {"diminta": 4800, "diperbarui": 4658, "hilang": 42, "sisa_antre": 2614}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.574** vs kemiripan gaya saja 0.410
- Masuk 5% teratas: model **0.690** vs 0.516 | 3191 soal | contoh latih 116538
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |
| 32 | 2026-10-10T06:53 | 45845 | 112870 | 0.793 | 25 |
| 33 | 2026-10-10T10:03 | 47092 | 114091 | 0.803 | 25 |
| 34 | 2026-10-10T13:30 | 48116 | 114932 | 0.803 | 25 |
| 35 | 2026-10-10T22:43 | 49352 | 116226 | 0.802 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.851 pada 7365 item berlabel wanita & 2096 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1880 | 0.553 | 0.700 | 0.999 | v2 |
| FaceAcc | 2295 | 0.559 | 0.679 | 0.999 | v2 |
| Front | 1891 | 0.535 | 0.636 | 0.999 | v2 |
| Hair | 8225 | 0.693 | 0.806 | 1.000 | v2 |
| Hat | 6274 | 0.586 | 0.709 | 0.999 | v2 |
| LayerAtas | 5210 | 0.483 | 0.728 | 0.999 | v2 |
| LayerBawah | 3408 | 0.518 | 0.752 | 1.000 | v2 |
| Neck | 1602 | 0.577 | 0.707 | 0.999 | v2 |
| Pants | 3729 | 0.078 | 0.663 | 0.999 | v2 |
| Sepatu | 3938 | 0.614 | 0.707 | 1.000 | v2 |
| Shirt | 3707 | 0.281 | 0.723 | 1.000 | v2 |
| Shoulder | 831 | 0.585 | 0.690 | 1.000 | v2 |
| TShirt | 94 | 0.191 | 0.521 | 0.998 | v2 |
| Waist | 2065 | 0.596 | 0.688 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 14612 item | AUC {"asli": 0.583, "potongan": 0.601, "rata": 0.606} | label wanita/pria [577, 235] | dipakai: **rata**
- Pants: 14253 item | AUC {"asli": 0.674, "potongan": 0.684, "rata": 0.691} | label wanita/pria [1177, 190] | dipakai: **asli**
- TShirt: 2945 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [51, 14] | dipakai: **asli**

## Sepatu (bundle): 4764 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2800, "baru": 33, "total": 4764}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
