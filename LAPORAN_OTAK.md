# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-05T16:51:24.415320+00:00 | putaran ke-14
- Outfit nyata terkumpul: **21409** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 10649, tidak koheren: 1108)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2081, "gaya_gemini": 0} | permintaan HTTP 6801, kena 429: 262, gagal 94

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.348 |
| CLIP netral-slot | 0.509 |
| CLIP PCA-32 (tanpa belajar) | 0.491 |
| Model linear (dilatih) | 0.747 |
| Model MLP (dilatih) | 0.764 |

- Dipakai: **mlp** | soal uji 19021 | outfit latih 18205, uji 3176
- AUC koherensi (outfit asli vs setengah-diacak): model 0.808, CLIP 0.721
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 14 | 2026-10-05T16:51 | 21409 | 81095 | 0.764 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.853 pada 5304 item berlabel wanita & 1390 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
