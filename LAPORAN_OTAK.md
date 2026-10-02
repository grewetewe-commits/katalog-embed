# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-02T14:41:48.424506+00:00 | putaran ke-3
- Outfit nyata terkumpul: **1651** | masuk bank (lolos saring): **378**
  (ditolak karena item inti tidak bisa dibeli: 1249, tidak koheren: 24)
- Item dengan sidik jari visual: **29035**
- Panen putaran ini: {"kreator": 176, "outfit_baru": 388, "ditolak": 240, "kembar": 37, "tanpa_outfit": 104} | permintaan HTTP 1581, kena 429: 565, gagal 238

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.413 |
| CLIP netral-slot | 0.575 |
| CLIP PCA-32 (tanpa belajar) | 0.533 |
| Model linear (dilatih) | 0.627 |
| Model MLP (dilatih) | 0.626 |

- Dipakai: **linear** | soal uji 1616 | outfit latih 1412, uji 227
- AUC koherensi (outfit asli vs setengah-diacak): model 0.818, CLIP 0.800
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **0** | outfit dasar dari server Roblox: 291

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 3 | 2026-10-02T14:41 | 1651 | 29035 | 0.627 | 0 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.881 pada 2320 item berlabel wanita & 370 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
