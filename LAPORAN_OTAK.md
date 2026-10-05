# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-05T07:28:09.084162+00:00 | putaran ke-13
- Outfit nyata terkumpul: **19328** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 9750, tidak koheren: 1005)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 1966, "gaya_gemini": 0} | permintaan HTTP 6667, kena 429: 172, gagal 72

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.354 |
| CLIP netral-slot | 0.517 |
| CLIP PCA-32 (tanpa belajar) | 0.495 |
| Model linear (dilatih) | 0.744 |
| Model MLP (dilatih) | 0.764 |

- Dipakai: **mlp** | soal uji 17068 | outfit latih 16449, uji 2852
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.721
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 13 | 2026-10-05T07:28 | 19328 | 77559 | 0.764 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.856 pada 5126 item berlabel wanita & 1323 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
