# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-03T01:08:12.638282+00:00 | putaran ke-4
- Outfit nyata terkumpul: **2422** | masuk bank (lolos saring): **662**
  (ditolak karena item inti tidak bisa dibeli: 1706, tidak koheren: 54)
- Item dengan sidik jari visual: **39029**
- Panen putaran ini: {"kreator": 220, "outfit_baru": 611, "ditolak": 369, "kembar": 53, "tanpa_outfit": 108} | permintaan HTTP 2158, kena 429: 733, gagal 313

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.415 |
| CLIP netral-slot | 0.597 |
| CLIP PCA-32 (tanpa belajar) | 0.560 |
| Model linear (dilatih) | 0.640 |
| Model MLP (dilatih) | 0.655 |

- Dipakai: **mlp** | soal uji 2487 | outfit latih 2073, uji 341
- AUC koherensi (outfit asli vs setengah-diacak): model 0.832, CLIP 0.807
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **3** | outfit dasar dari server Roblox: 448

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 4 | 2026-10-03T01:08 | 2422 | 39029 | 0.655 | 3 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.877 pada 2914 item berlabel wanita & 598 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
