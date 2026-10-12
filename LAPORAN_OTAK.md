# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-12T06:57:13.888561+00:00 | putaran ke-41
- Outfit nyata terkumpul: **56598** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 27920, tidak koheren: 2582)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3400, "gaya_masuk": 1036, "gaya_gemini": 0, "meta": {"diminta": 4692, "diperbarui": 4538, "hilang": 54, "sisa_antre": 696}, "sepatu": {"cari": 29, "lihat": 2274, "baru": 2, "total": 4841}} | permintaan HTTP 4161, kena 429: 94, gagal 52

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.338 | Uji akhir |
| CLIP netral-slot | 0.500 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.494 | Pemilihan |
| Model linear (dilatih) | 0.790 | Pemilihan |
| Model MLP (dilatih) | 0.810 | Pemilihan |
| Model terpilih | 0.805 | Uji akhir |

- Dipakai: **mlp** | soal uji 49212 | outfit latih 39591, pemilihan 8520, uji 8451
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.808, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 38
- Durasi putaran: **65.2 menit** | META: {"diminta": 4692, "diperbarui": 4538, "hilang": 54, "sisa_antre": 696}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.590** vs kemiripan gaya saja 0.419
- Masuk 5% teratas: model **0.702** vs 0.543 | 3047 soal | contoh latih 115815
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
| 40 | 2026-10-11T23:00 | 55562 | 121756 | 0.803 | 26 |
| 41 | 2026-10-12T06:57 | 56598 | 122754 | 0.805 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7683 item berlabel wanita & 2259 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1932 | 0.553 | 0.700 | 0.999 | v2 |
| FaceAcc | 2399 | 0.561 | 0.680 | 0.999 | v2 |
| Front | 1966 | 0.537 | 0.639 | 0.999 | v2 |
| Hair | 8779 | 0.692 | 0.806 | 1.000 | v2 |
| Hat | 6602 | 0.583 | 0.708 | 0.999 | v2 |
| LayerAtas | 5342 | 0.484 | 0.731 | 0.999 | v2 |
| LayerBawah | 3468 | 0.519 | 0.752 | 1.000 | v2 |
| Neck | 1687 | 0.577 | 0.706 | 0.999 | v2 |
| Pants | 4112 | 0.077 | 0.662 | 0.999 | v2 |
| Sepatu | 4027 | 0.613 | 0.706 | 1.000 | v2 |
| Shirt | 4094 | 0.281 | 0.722 | 1.000 | v2 |
| Shoulder | 881 | 0.586 | 0.689 | 1.000 | v2 |
| TShirt | 99 | 0.192 | 0.525 | 0.998 | v2 |
| Waist | 2141 | 0.592 | 0.686 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 16023 item | AUC {"asli": 0.587, "potongan": 0.61, "rata": 0.613} | label wanita/pria [622, 263] | dipakai: **rata**
- Pants: 15599 item | AUC {"asli": 0.668, "potongan": 0.675, "rata": 0.683} | label wanita/pria [1280, 214] | dipakai: **asli**
- TShirt: 3214 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 15] | dipakai: **asli**

## Sepatu (bundle): 4841 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 2274, "baru": 2, "total": 4841}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
