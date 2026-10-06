# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-06T02:20:07.303344+00:00 | putaran ke-15
- Outfit nyata terkumpul: **23373** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 11522, tidak koheren: 1221)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 1964, "gaya_gemini": 0} | permintaan HTTP 6776, kena 429: 259, gagal 90

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.348 |
| CLIP netral-slot | 0.508 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.754 |
| Model MLP (dilatih) | 0.769 |

- Dipakai: **mlp** | soal uji 20614 | outfit latih 19887, uji 3457
- AUC koherensi (outfit asli vs setengah-diacak): model 0.809, CLIP 0.724
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 15 | 2026-10-06T02:20 | 23373 | 83912 | 0.769 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.853 pada 5467 item berlabel wanita & 1467 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
