# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-09T14:12:05.724848+00:00 | putaran ke-29
- Outfit nyata terkumpul: **41993** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 19855, tidak koheren: 2071)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4176, "gaya_masuk": 1283, "gaya_gemini": 0, "meta": {"diminta": 4719, "diperbarui": 4563, "hilang": 56, "sisa_antre": 979}} | permintaan HTTP 4924, kena 429: 96, gagal 60

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.341 |
| CLIP netral-slot | 0.503 |
| CLIP PCA-32 (tanpa belajar) | 0.485 |
| Model linear (dilatih) | 0.776 |
| Model MLP (dilatih) | 0.790 |

- Dipakai: **mlp** | soal uji 36903 | outfit latih 35694, uji 6285
- AUC koherensi (outfit asli vs setengah-diacak): model 0.803, CLIP 0.717
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 530 | item baru diminta pemain: 10
- Durasi putaran: **59.8 menit** | META: {"diminta": 4719, "diperbarui": 4563, "hilang": 56, "sisa_antre": 979}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.572** vs kemiripan gaya saja 0.408
- Masuk 5% teratas: model **0.700** vs 0.524 | 3175 soal | contoh latih 116906
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 29 | 2026-10-09T14:12 | 41993 | 105024 | 0.79 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6719 item berlabel wanita & 1971 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
