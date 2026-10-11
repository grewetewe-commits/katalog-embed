# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-11T06:39:58.051187+00:00 | putaran ke-37
- Outfit nyata terkumpul: **51714** | masuk bank (lolos saring): **7980**
  (ditolak karena item inti tidak bisa dibeli: 25284, tidak koheren: 2370)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4160, "gaya_masuk": 1287, "gaya_gemini": 0, "meta": {"diminta": 4580, "diperbarui": 4429, "hilang": 51, "sisa_antre": 908}, "sepatu": {"cari": 30, "lihat": 2496, "baru": 24, "total": 4803}} | permintaan HTTP 4962, kena 429: 94, gagal 55

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.504 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.490 | Pemilihan |
| Model linear (dilatih) | 0.786 | Pemilihan |
| Model MLP (dilatih) | 0.804 | Pemilihan |
| Model terpilih | 0.803 | Uji akhir |

- Dipakai: **mlp** | soal uji 44933 | outfit latih 36194, pemilihan 7780, uji 7710
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 532 | item baru diminta pemain: 33
- Durasi putaran: **58.2 menit** | META: {"diminta": 4580, "diperbarui": 4429, "hilang": 51, "sisa_antre": 908}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.583** vs kemiripan gaya saja 0.427
- Masuk 5% teratas: model **0.697** vs 0.534 | 3202 soal | contoh latih 116353
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
| 36 | 2026-10-11T02:37 | 50426 | 117219 | 0.8 | 25 |
| 37 | 2026-10-11T06:39 | 51714 | 118451 | 0.803 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 7474 item berlabel wanita & 2157 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1906 | 0.556 | 0.701 | 0.999 | v2 |
| FaceAcc | 2329 | 0.561 | 0.680 | 0.999 | v2 |
| Front | 1919 | 0.535 | 0.637 | 0.999 | v2 |
| Hair | 8414 | 0.693 | 0.807 | 1.000 | v2 |
| Hat | 6385 | 0.583 | 0.708 | 0.999 | v2 |
| LayerAtas | 5264 | 0.483 | 0.730 | 0.999 | v2 |
| LayerBawah | 3429 | 0.518 | 0.752 | 1.000 | v2 |
| Neck | 1632 | 0.574 | 0.705 | 0.999 | v2 |
| Pants | 3869 | 0.077 | 0.662 | 0.999 | v2 |
| Sepatu | 3982 | 0.613 | 0.708 | 1.000 | v2 |
| Shirt | 3847 | 0.280 | 0.722 | 1.000 | v2 |
| Shoulder | 846 | 0.582 | 0.689 | 1.000 | v2 |
| TShirt | 98 | 0.194 | 0.520 | 0.998 | v2 |
| Waist | 2096 | 0.594 | 0.687 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 15059 item | AUC {"asli": 0.585, "potongan": 0.605, "rata": 0.609} | label wanita/pria [591, 245] | dipakai: **rata**
- Pants: 14681 item | AUC {"asli": 0.671, "potongan": 0.681, "rata": 0.688} | label wanita/pria [1213, 198] | dipakai: **asli**
- TShirt: 3047 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [52, 14] | dipakai: **asli**

## Sepatu (bundle): 4803 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2496, "baru": 24, "total": 4803}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
