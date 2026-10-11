# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-11T17:32:24.238242+00:00 | putaran ke-39
- Outfit nyata terkumpul: **54490** | masuk bank (lolos saring): **7980**
  (ditolak karena item inti tidak bisa dibeli: 26810, tidak koheren: 2525)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4713, "gaya_masuk": 1448, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4632, "hilang": 68, "sisa_antre": 4014}, "sepatu": {"cari": 29, "lihat": 2312, "baru": 7, "total": 4824}} | permintaan HTTP 5516, kena 429: 100, gagal 52

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.498 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.489 | Pemilihan |
| Model linear (dilatih) | 0.787 | Pemilihan |
| Model MLP (dilatih) | 0.805 | Pemilihan |
| Model terpilih | 0.802 | Uji akhir |

- Dipakai: **mlp** | soal uji 47376 | outfit latih 38119, pemilihan 8205, uji 8133
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.805, CLIP 0.710
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 533 | item baru diminta pemain: 34
- Durasi putaran: **60.2 menit** | META: {"diminta": 4800, "diperbarui": 4632, "hilang": 68, "sisa_antre": 4014}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.606** vs kemiripan gaya saja 0.433
- Masuk 5% teratas: model **0.707** vs 0.545 | 3203 soal | contoh latih 116117
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
| 38 | 2026-10-11T13:46 | 53042 | 119578 | 0.806 | 26 |
| 39 | 2026-10-11T17:32 | 54490 | 120753 | 0.802 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 7574 item berlabel wanita & 2211 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1919 | 0.555 | 0.701 | 0.999 | v2 |
| FaceAcc | 2365 | 0.561 | 0.680 | 0.999 | v2 |
| Front | 1950 | 0.535 | 0.637 | 0.999 | v2 |
| Hair | 8588 | 0.692 | 0.806 | 1.000 | v2 |
| Hat | 6503 | 0.583 | 0.708 | 0.999 | v2 |
| LayerAtas | 5305 | 0.484 | 0.731 | 0.999 | v2 |
| LayerBawah | 3449 | 0.519 | 0.752 | 1.000 | v2 |
| Neck | 1662 | 0.576 | 0.706 | 0.999 | v2 |
| Pants | 3985 | 0.077 | 0.662 | 0.999 | v2 |
| Sepatu | 4010 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 3964 | 0.280 | 0.720 | 1.000 | v2 |
| Shoulder | 865 | 0.586 | 0.688 | 1.000 | v2 |
| TShirt | 99 | 0.192 | 0.525 | 0.998 | v2 |
| Waist | 2118 | 0.592 | 0.685 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 15576 item | AUC {"asli": 0.586, "potongan": 0.607, "rata": 0.611} | label wanita/pria [606, 255] | dipakai: **rata**
- Pants: 15169 item | AUC {"asli": 0.67, "potongan": 0.678, "rata": 0.686} | label wanita/pria [1242, 207] | dipakai: **asli**
- TShirt: 3141 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 14] | dipakai: **asli**

## Sepatu (bundle): 4824 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 2312, "baru": 7, "total": 4824}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
