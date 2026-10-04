# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-04T18:42:16.734659+00:00 | putaran ke-11
- Outfit nyata terkumpul: **15328** | masuk bank (lolos saring): **6447**
  (ditolak karena item inti tidak bisa dibeli: 8153, tidak koheren: 728)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2011, "gaya_gemini": 0} | permintaan HTTP 6604, kena 429: 148, gagal 54

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.356 |
| CLIP netral-slot | 0.513 |
| CLIP PCA-32 (tanpa belajar) | 0.488 |
| Model linear (dilatih) | 0.743 |
| Model MLP (dilatih) | 0.761 |

- Dipakai: **mlp** | soal uji 13377 | outfit latih 13076, uji 2228
- AUC koherensi (outfit asli vs setengah-diacak): model 0.810, CLIP 0.722
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 11 | 2026-10-04T18:42 | 15328 | 70314 | 0.761 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.860 pada 4743 item berlabel wanita & 1178 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
