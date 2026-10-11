# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-11T13:46:41.930032+00:00 | putaran ke-38
- Outfit nyata terkumpul: **53042** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 26009, tidak koheren: 2395)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4552, "gaya_masuk": 1327, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4640, "hilang": 60, "sisa_antre": 2192}, "sepatu": {"cari": 30, "lihat": 2543, "baru": 14, "total": 4817}} | permintaan HTTP 5342, kena 429: 97, gagal 54

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.336 | Uji akhir |
| CLIP netral-slot | 0.500 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.489 | Pemilihan |
| Model linear (dilatih) | 0.785 | Pemilihan |
| Model MLP (dilatih) | 0.804 | Pemilihan |
| Model terpilih | 0.806 | Uji akhir |

- Dipakai: **mlp** | soal uji 46140 | outfit latih 37115, pemilihan 7978, uji 7917
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.808, CLIP 0.717
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 533 | item baru diminta pemain: 34
- Durasi putaran: **62.1 menit** | META: {"diminta": 4700, "diperbarui": 4640, "hilang": 60, "sisa_antre": 2192}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.593** vs kemiripan gaya saja 0.432
- Masuk 5% teratas: model **0.705** vs 0.547 | 3218 soal | contoh latih 116590
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

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7526 item berlabel wanita & 2191 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1914 | 0.556 | 0.701 | 0.999 | v2 |
| FaceAcc | 2345 | 0.562 | 0.680 | 0.999 | v2 |
| Front | 1936 | 0.536 | 0.637 | 0.999 | v2 |
| Hair | 8511 | 0.693 | 0.807 | 1.000 | v2 |
| Hat | 6438 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5288 | 0.484 | 0.731 | 0.999 | v2 |
| LayerBawah | 3442 | 0.518 | 0.752 | 1.000 | v2 |
| Neck | 1652 | 0.577 | 0.706 | 0.999 | v2 |
| Pants | 3923 | 0.077 | 0.664 | 0.999 | v2 |
| Sepatu | 3996 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 3903 | 0.280 | 0.723 | 1.000 | v2 |
| Shoulder | 858 | 0.586 | 0.690 | 1.000 | v2 |
| TShirt | 98 | 0.194 | 0.520 | 0.998 | v2 |
| Waist | 2110 | 0.592 | 0.686 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 15309 item | AUC {"asli": 0.582, "potongan": 0.603, "rata": 0.607} | label wanita/pria [599, 252] | dipakai: **rata**
- Pants: 14902 item | AUC {"asli": 0.671, "potongan": 0.68, "rata": 0.688} | label wanita/pria [1226, 204] | dipakai: **asli**
- TShirt: 3093 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [52, 14] | dipakai: **asli**

## Sepatu (bundle): 4817 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2543, "baru": 14, "total": 4817}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
