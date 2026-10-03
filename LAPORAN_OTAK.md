# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-03T22:58:45.190138+00:00 | putaran ke-8
- Outfit nyata terkumpul: **9217** | masuk bank (lolos saring): **3418**
  (ditolak karena item inti tidak bisa dibeli: 5407, tidak koheren: 392)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2136, "gaya_gemini": 0} | permintaan HTTP 6607, kena 429: 166, gagal 61

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.359 |
| CLIP netral-slot | 0.524 |
| CLIP PCA-32 (tanpa belajar) | 0.500 |
| Model linear (dilatih) | 0.726 |
| Model MLP (dilatih) | 0.745 |

- Dipakai: **mlp** | soal uji 8156 | outfit latih 7876, uji 1326
- AUC koherensi (outfit asli vs setengah-diacak): model 0.818, CLIP 0.721
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 8 | 2026-10-03T22:58 | 9217 | 59475 | 0.745 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.865 pada 4072 item berlabel wanita & 918 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
