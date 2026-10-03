# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-03T13:29:25.479052+00:00 | putaran ke-6
- Outfit nyata terkumpul: **4997** | masuk bank (lolos saring): **1607**
  (ditolak karena item inti tidak bisa dibeli: 3221, tidak koheren: 169)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2117, "gaya_gemini": 0} | permintaan HTTP 6600, kena 429: 161, gagal 52

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.378 |
| CLIP netral-slot | 0.542 |
| CLIP PCA-32 (tanpa belajar) | 0.519 |
| Model linear (dilatih) | 0.690 |
| Model MLP (dilatih) | 0.705 |

- Dipakai: **mlp** | soal uji 4769 | outfit latih 4260, uji 725
- AUC koherensi (outfit asli vs setengah-diacak): model 0.831, CLIP 0.762
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 482

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 6 | 2026-10-03T13:29 | 4997 | 50888 | 0.705 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.872 pada 3624 item berlabel wanita & 741 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
