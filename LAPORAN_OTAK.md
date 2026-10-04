# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-04T23:19:34.959126+00:00 | putaran ke-12
- Outfit nyata terkumpul: **17362** | masuk bank (lolos saring): **7457**
  (ditolak karena item inti tidak bisa dibeli: 9056, tidak koheren: 849)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2034, "gaya_gemini": 0} | permintaan HTTP 6638, kena 429: 160, gagal 56

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.350 |
| CLIP netral-slot | 0.516 |
| CLIP PCA-32 (tanpa belajar) | 0.495 |
| Model linear (dilatih) | 0.743 |
| Model MLP (dilatih) | 0.757 |

- Dipakai: **mlp** | soal uji 15200 | outfit latih 14811, uji 2526
- AUC koherensi (outfit asli vs setengah-diacak): model 0.816, CLIP 0.727
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 12 | 2026-10-04T23:19 | 17362 | 74457 | 0.757 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.858 pada 4935 item berlabel wanita & 1255 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
