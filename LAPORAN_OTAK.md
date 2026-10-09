# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-09T21:17:07.204859+00:00 | putaran ke-30
- Outfit nyata terkumpul: **43179** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 20524, tidak koheren: 2122)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3761, "gaya_masuk": 1186, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4640, "hilang": 60, "sisa_antre": 4062}, "sepatu": {"cari": 28, "lihat": 2313, "baru": 2232, "total": 2232}} | permintaan HTTP 5904, kena 429: 103, gagal 57

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.340 |
| CLIP netral-slot | 0.502 |
| CLIP PCA-32 (tanpa belajar) | 0.487 |
| Model linear (dilatih) | 0.778 |
| Model MLP (dilatih) | 0.794 |

- Dipakai: **mlp** | soal uji 37865 | outfit latih 36705, uji 6459
- AUC koherensi (outfit asli vs setengah-diacak): model 0.812, CLIP 0.716
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 530 | item baru diminta pemain: 11
- Durasi putaran: **78.1 menit** | META: {"diminta": 4800, "diperbarui": 4640, "hilang": 60, "sisa_antre": 4062}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.586** vs kemiripan gaya saja 0.412
- Masuk 5% teratas: model **0.705** vs 0.536 | 3187 soal | contoh latih 116818
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.843 pada 7026 item berlabel wanita & 1985 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 474 | 0.656 | 0.770 | 0.212 | v2 |
| FaceAcc | 1238 | 0.611 | 0.726 | 0.543 | v2 |
| Front | 774 | 0.549 | 0.664 | 0.381 | v2 |
| Hair | 5057 | 0.728 | 0.828 | 0.611 | v2 |
| Hat | 2890 | 0.628 | 0.755 | 0.371 | v2 |
| LayerAtas | 3068 | 0.489 | 0.742 | 0.602 | v2 |
| LayerBawah | 1998 | 0.515 | 0.759 | 0.588 | v2 |
| Neck | 809 | 0.625 | 0.735 | 0.451 | v2 |
| Pants | 3456 | 0.078 | 0.665 | 0.998 | v2 |
| Sepatu | 974 | 0.607 | 0.686 | 0.472 | v2 |
| Shirt | 3413 | 0.280 | 0.723 | 1.000 | v2 |
| Shoulder | 366 | 0.645 | 0.716 | 0.429 | v2 |
| TShirt | 87 | 0.207 | 0.540 | 0.997 | v2 |
| Waist | 747 | 0.664 | 0.730 | 0.370 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 13428 item | AUC {"asli": 0.59, "potongan": 0.603, "rata": 0.61} | label wanita/pria [544, 214] | dipakai: **asli**
- Pants: 13164 item | AUC {"asli": 0.681, "potongan": 0.688, "rata": 0.696} | label wanita/pria [1107, 175] | dipakai: **asli**
- TShirt: 2702 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [47, 13] | dipakai: **asli**

## Sepatu (bundle): 2232 bundle di meta/sepatu.json | putaran ini: {"cari": 28, "lihat": 2313, "baru": 2232, "total": 2232}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
