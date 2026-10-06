# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-06T21:18:23.425222+00:00 | putaran ke-18
- Outfit nyata terkumpul: **28343** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 13054, tidak koheren: 1688)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3279, "gaya_masuk": 1020, "gaya_gemini": 0, "meta": {"diminta": 3282, "diperbarui": 3016, "hilang": 166, "sisa_antre": 850}} | permintaan HTTP 3847, kena 429: 62, gagal 45

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.345 |
| CLIP netral-slot | 0.505 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.758 |
| Model MLP (dilatih) | 0.777 |

- Dipakai: **mlp** | soal uji 24912 | outfit latih 24100, uji 4209
- AUC koherensi (outfit asli vs setengah-diacak): model 0.813, CLIP 0.713
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527 | item baru diminta pemain: 0
- Durasi putaran: **55.2 menit** | META: {"diminta": 3282, "diperbarui": 3016, "hilang": 166, "sisa_antre": 850}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 18 | 2026-10-06T21:18 | 28343 | 90441 | 0.777 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.847 pada 5965 item berlabel wanita & 1648 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
