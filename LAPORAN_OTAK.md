# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-13T15:13:45.800573+00:00 | putaran ke-44
- Outfit nyata terkumpul: **60253** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 29848, tidak koheren: 2867)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4275, "gaya_masuk": 1212, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4543, "hilang": 57, "sisa_antre": 1473}, "sepatu": {"cari": 29, "lihat": 2320, "baru": 32, "total": 4890}} | permintaan HTTP 5013, kena 429: 99, gagal 45

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.501 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.490 | Pemilihan |
| Model linear (dilatih) | 0.789 | Pemilihan |
| Model MLP (dilatih) | 0.808 | Pemilihan |
| Model terpilih | 0.810 | Uji akhir |

- Dipakai: **mlp** | soal uji 52076 | outfit latih 42184, pemilihan 9063, uji 8960
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.805, CLIP 0.711
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **66.6 menit** | META: {"diminta": 4700, "diperbarui": 4543, "hilang": 57, "sisa_antre": 1473}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.600** vs kemiripan gaya saja 0.444
- Masuk 5% teratas: model **0.712** vs 0.556 | 3081 soal | contoh latih 115855
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 33 | 2026-10-10T10:03 | 47092 | 114091 | 0.803 | 25 |
| 34 | 2026-10-10T13:30 | 48116 | 114932 | 0.803 | 25 |
| 35 | 2026-10-10T22:43 | 49352 | 116226 | 0.802 | 25 |
| 36 | 2026-10-11T02:37 | 50426 | 117219 | 0.8 | 25 |
| 37 | 2026-10-11T06:39 | 51714 | 118451 | 0.803 | 26 |
| 38 | 2026-10-11T13:46 | 53042 | 119578 | 0.806 | 26 |
| 39 | 2026-10-11T17:32 | 54490 | 120753 | 0.802 | 26 |
| 40 | 2026-10-11T23:00 | 55562 | 121756 | 0.803 | 26 |
| 41 | 2026-10-12T06:57 | 56598 | 122754 | 0.805 | 26 |
| 42 | 2026-10-12T16:20 | 57841 | 123952 | 0.805 | 26 |
| 43 | 2026-10-13T01:41 | 58986 | 125362 | 0.809 | 26 |
| 44 | 2026-10-13T15:13 | 60253 | 126460 | 0.81 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7869 item berlabel wanita & 2343 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1969 | 0.554 | 0.700 | 0.999 | v2 |
| FaceAcc | 2456 | 0.562 | 0.682 | 0.999 | v2 |
| Front | 2016 | 0.539 | 0.640 | 0.999 | v2 |
| Hair | 9036 | 0.690 | 0.805 | 1.000 | v2 |
| Hat | 6765 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5407 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3505 | 0.518 | 0.754 | 1.000 | v2 |
| Neck | 1723 | 0.579 | 0.706 | 0.999 | v2 |
| Pants | 4283 | 0.077 | 0.664 | 0.999 | v2 |
| Sepatu | 4094 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 4273 | 0.282 | 0.722 | 1.000 | v2 |
| Shoulder | 906 | 0.592 | 0.693 | 1.000 | v2 |
| TShirt | 101 | 0.188 | 0.515 | 0.998 | v2 |
| Waist | 2189 | 0.592 | 0.685 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 16795 item | AUC {"asli": 0.591, "potongan": 0.615, "rata": 0.618} | label wanita/pria [647, 276] | dipakai: **rata**
- Pants: 16345 item | AUC {"asli": 0.673, "potongan": 0.678, "rata": 0.686} | label wanita/pria [1333, 231] | dipakai: **asli**
- TShirt: 3345 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 15] | dipakai: **asli**

## Sepatu (bundle): 4890 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 2320, "baru": 32, "total": 4890}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
