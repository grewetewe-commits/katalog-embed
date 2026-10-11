# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-11T02:37:44.381004+00:00 | putaran ke-36
- Outfit nyata terkumpul: **50426** | masuk bank (lolos saring): **7979**
  (ditolak karena item inti tidak bisa dibeli: 24504, tidak koheren: 2398)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3650, "gaya_masuk": 1074, "gaya_gemini": 0, "meta": {"diminta": 4784, "diperbarui": 4602, "hilang": 82, "sisa_antre": 579}, "sepatu": {"cari": 29, "lihat": 2401, "baru": 15, "total": 4779}} | permintaan HTTP 4378, kena 429: 97, gagal 45

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.340 | Uji akhir |
| CLIP netral-slot | 0.501 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.491 | Pemilihan |
| Model linear (dilatih) | 0.781 | Pemilihan |
| Model MLP (dilatih) | 0.803 | Pemilihan |
| Model terpilih | 0.800 | Uji akhir |

- Dipakai: **mlp** | soal uji 43769 | outfit latih 35309, pemilihan 7580, uji 7505
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.712
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 532 | item baru diminta pemain: 32
- Durasi putaran: **63.5 menit** | META: {"diminta": 4784, "diperbarui": 4602, "hilang": 82, "sisa_antre": 579}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.592** vs kemiripan gaya saja 0.435
- Masuk 5% teratas: model **0.699** vs 0.539 | 3246 soal | contoh latih 116529
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

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.851 pada 7426 item berlabel wanita & 2133 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1895 | 0.556 | 0.701 | 0.999 | v2 |
| FaceAcc | 2320 | 0.561 | 0.681 | 0.999 | v2 |
| Front | 1908 | 0.534 | 0.637 | 0.999 | v2 |
| Hair | 8342 | 0.693 | 0.807 | 1.000 | v2 |
| Hat | 6341 | 0.584 | 0.709 | 0.999 | v2 |
| LayerAtas | 5247 | 0.484 | 0.730 | 0.999 | v2 |
| LayerBawah | 3422 | 0.518 | 0.751 | 1.000 | v2 |
| Neck | 1617 | 0.576 | 0.706 | 0.999 | v2 |
| Pants | 3821 | 0.078 | 0.662 | 0.999 | v2 |
| Sepatu | 3957 | 0.614 | 0.708 | 1.000 | v2 |
| Shirt | 3794 | 0.281 | 0.722 | 1.000 | v2 |
| Shoulder | 840 | 0.583 | 0.689 | 1.000 | v2 |
| TShirt | 96 | 0.198 | 0.510 | 0.998 | v2 |
| Waist | 2087 | 0.595 | 0.687 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 14832 item | AUC {"asli": 0.581, "potongan": 0.602, "rata": 0.606} | label wanita/pria [585, 239] | dipakai: **rata**
- Pants: 14442 item | AUC {"asli": 0.678, "potongan": 0.686, "rata": 0.694} | label wanita/pria [1198, 195] | dipakai: **asli**
- TShirt: 2995 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [51, 14] | dipakai: **asli**

## Sepatu (bundle): 4779 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 2401, "baru": 15, "total": 4779}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
