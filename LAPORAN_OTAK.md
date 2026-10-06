# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-06T23:33:36.470423+00:00 | putaran ke-19
- Outfit nyata terkumpul: **29612** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 13688, tidak koheren: 1700)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4021, "gaya_masuk": 1268, "gaya_gemini": 0, "meta": {"diminta": 1359, "diperbarui": 1199, "hilang": 60, "sisa_antre": 1179}} | permintaan HTTP 4526, kena 429: 22, gagal 35

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.345 |
| CLIP netral-slot | 0.504 |
| CLIP PCA-32 (tanpa belajar) | 0.485 |
| Model linear (dilatih) | 0.763 |
| Model MLP (dilatih) | 0.780 |

- Dipakai: **mlp** | soal uji 26115 | outfit latih 25159, uji 4418
- AUC koherensi (outfit asli vs setengah-diacak): model 0.814, CLIP 0.718
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 1
- Durasi putaran: **54.8 menit** | META: {"diminta": 1359, "diperbarui": 1199, "hilang": 60, "sisa_antre": 1179}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 19 | 2026-10-06T23:33 | 29612 | 92020 | 0.78 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.846 pada 6032 item berlabel wanita & 1674 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
