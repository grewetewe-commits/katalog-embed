# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-03T18:36:16.850928+00:00 | putaran ke-7
- Outfit nyata terkumpul: **7082** | masuk bank (lolos saring): **2429**
  (ditolak karena item inti tidak bisa dibeli: 4396, tidak koheren: 257)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2040, "gaya_gemini": 0} | permintaan HTTP 6609, kena 429: 177, gagal 52

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.369 |
| CLIP netral-slot | 0.536 |
| CLIP PCA-32 (tanpa belajar) | 0.509 |
| Model linear (dilatih) | 0.713 |
| Model MLP (dilatih) | 0.724 |

- Dipakai: **mlp** | soal uji 6441 | outfit latih 6045, uji 1023
- AUC koherensi (outfit asli vs setengah-diacak): model 0.821, CLIP 0.744
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 7 | 2026-10-03T18:36 | 7082 | 55550 | 0.724 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.869 pada 3845 item berlabel wanita & 820 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
