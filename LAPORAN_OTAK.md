# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-03T07:27:20.413615+00:00 | putaran ke-5
- Outfit nyata terkumpul: **2846** | masuk bank (lolos saring): **978**
  (ditolak karena item inti tidak bisa dibeli: 1776, tidak koheren: 92)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 170, "outfit_baru": 423, "ditolak": 279, "kembar": 34, "tanpa_outfit": 95} | permintaan HTTP 1627, kena 429: 565, gagal 238

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.409 |
| CLIP netral-slot | 0.580 |
| CLIP PCA-32 (tanpa belajar) | 0.549 |
| Model linear (dilatih) | 0.645 |
| Model MLP (dilatih) | 0.658 |

- Dipakai: **mlp** | soal uji 2834 | outfit latih 2442, uji 390
- AUC koherensi (outfit asli vs setengah-diacak): model 0.854, CLIP 0.794
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **4** | outfit dasar dari server Roblox: 448

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 5 | 2026-10-03T07:27 | 2846 | 45533 | 0.658 | 4 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.875 pada 3424 item berlabel wanita & 656 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
