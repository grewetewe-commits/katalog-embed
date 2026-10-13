# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-13T23:47:19.056936+00:00 | putaran ke-45
- Outfit nyata terkumpul: **61615** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 30616, tidak koheren: 2775)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4264, "gaya_masuk": 1336, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4553, "hilang": 47, "sisa_antre": 2769}, "sepatu": {"cari": 30, "lihat": 2465, "baru": 83, "total": 4973}} | permintaan HTTP 5044, kena 429: 100, gagal 55

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.340 | Uji akhir |
| CLIP netral-slot | 0.498 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.786 | Pemilihan |
| Model MLP (dilatih) | 0.806 | Pemilihan |
| Model terpilih | 0.808 | Uji akhir |

- Dipakai: **mlp** | soal uji 53215 | outfit latih 43140, pemilihan 9268, uji 9161
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.713
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **65.4 menit** | META: {"diminta": 4700, "diperbarui": 4553, "hilang": 47, "sisa_antre": 2769}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.597** vs kemiripan gaya saja 0.435
- Masuk 5% teratas: model **0.702** vs 0.540 | 3155 soal | contoh latih 115361
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 45 | 2026-10-13T23:47 | 61615 | 127986 | 0.808 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7941 item berlabel wanita & 2373 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1978 | 0.554 | 0.700 | 0.999 | v2 |
| FaceAcc | 2481 | 0.560 | 0.682 | 0.999 | v2 |
| Front | 2029 | 0.540 | 0.640 | 0.999 | v2 |
| Hair | 9128 | 0.690 | 0.804 | 1.000 | v2 |
| Hat | 6817 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5425 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3515 | 0.519 | 0.754 | 1.000 | v2 |
| Neck | 1733 | 0.580 | 0.707 | 0.999 | v2 |
| Pants | 4354 | 0.077 | 0.663 | 0.999 | v2 |
| Sepatu | 4163 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 4342 | 0.282 | 0.722 | 1.000 | v2 |
| Shoulder | 911 | 0.592 | 0.693 | 1.000 | v2 |
| TShirt | 101 | 0.188 | 0.515 | 0.998 | v2 |
| Waist | 2203 | 0.593 | 0.684 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 17110 item | AUC {"asli": 0.59, "potongan": 0.619, "rata": 0.621} | label wanita/pria [657, 283] | dipakai: **rata**
- Pants: 16638 item | AUC {"asli": 0.676, "potongan": 0.68, "rata": 0.688} | label wanita/pria [1356, 234] | dipakai: **asli**
- TShirt: 3404 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 15] | dipakai: **asli**

## Sepatu (bundle): 4973 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2465, "baru": 83, "total": 4973}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
