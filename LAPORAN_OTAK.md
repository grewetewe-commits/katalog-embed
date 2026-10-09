# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-09T07:05:31.683821+00:00 | putaran ke-28
- Outfit nyata terkumpul: **40705** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 19066, tidak koheren: 2016)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3345, "gaya_masuk": 1003, "gaya_gemini": 0, "meta": {"diminta": 1745, "diperbarui": 1678, "hilang": 67, "sisa_antre": 737}} | permintaan HTTP 3942, kena 429: 38, gagal 42

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.505 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.776 |
| Model MLP (dilatih) | 0.794 |

- Dipakai: **mlp** | soal uji 35669 | outfit latih 34619, uji 6071
- AUC koherensi (outfit asli vs setengah-diacak): model 0.810, CLIP 0.719
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 529 | item baru diminta pemain: 9
- Durasi putaran: **61.0 menit** | META: {"diminta": 1745, "diperbarui": 1678, "hilang": 67, "sisa_antre": 737}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.562** vs kemiripan gaya saja 0.391
- Masuk 5% teratas: model **0.681** vs 0.502 | 3180 soal | contoh latih 117062
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 28 | 2026-10-09T07:05 | 40705 | 103737 | 0.794 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6657 item berlabel wanita & 1954 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
