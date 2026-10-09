# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-09T00:19:07.364227+00:00 | putaran ke-27
- Outfit nyata terkumpul: **39702** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 18665, tidak koheren: 1935)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4271, "gaya_masuk": 1305, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4648, "hilang": 52, "sisa_antre": 1434}} | permintaan HTTP 4985, kena 429: 98, gagal 44

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.502 |
| CLIP PCA-32 (tanpa belajar) | 0.487 |
| Model linear (dilatih) | 0.773 |
| Model MLP (dilatih) | 0.790 |

- Dipakai: **mlp** | soal uji 34690 | outfit latih 33792, uji 5898
- AUC koherensi (outfit asli vs setengah-diacak): model 0.808, CLIP 0.719
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 529 | item baru diminta pemain: 9
- Durasi putaran: **59.8 menit** | META: {"diminta": 4800, "diperbarui": 4648, "hilang": 52, "sisa_antre": 1434}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.574** vs kemiripan gaya saja 0.404
- Masuk 5% teratas: model **0.698** vs 0.515 | 3199 soal | contoh latih 117076
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 27 | 2026-10-09T00:19 | 39702 | 102700 | 0.79 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6594 item berlabel wanita & 1927 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
