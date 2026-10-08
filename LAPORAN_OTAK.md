# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-08T20:48:43.218389+00:00 | putaran ke-26
- Outfit nyata terkumpul: **38397** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 17969, tidak koheren: 1906)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4257, "gaya_masuk": 1253, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4546, "hilang": 54, "sisa_antre": 1159}} | permintaan HTTP 4923, kena 429: 97, gagal 34

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.345 |
| CLIP netral-slot | 0.509 |
| CLIP PCA-32 (tanpa belajar) | 0.493 |
| Model linear (dilatih) | 0.777 |
| Model MLP (dilatih) | 0.792 |

- Dipakai: **mlp** | soal uji 33583 | outfit latih 32678, uji 5709
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.713
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 9
- Durasi putaran: **59.7 menit** | META: {"diminta": 4700, "diperbarui": 4546, "hilang": 54, "sisa_antre": 1159}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.583** vs kemiripan gaya saja 0.413
- Masuk 5% teratas: model **0.708** vs 0.524 | 3220 soal | contoh latih 116953
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 26 | 2026-10-08T20:48 | 38397 | 101318 | 0.792 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6530 item berlabel wanita & 1901 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
