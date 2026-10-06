# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-06T15:53:34.874074+00:00 | putaran ke-17
- Outfit nyata terkumpul: **27323** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 13224, tidak koheren: 1497)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 1959, "gaya_gemini": 0} | permintaan HTTP 6830, kena 429: 267, gagal 90

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.348 |
| CLIP netral-slot | 0.505 |
| CLIP PCA-32 (tanpa belajar) | 0.486 |
| Model linear (dilatih) | 0.757 |
| Model MLP (dilatih) | 0.774 |

- Dipakai: **mlp** | soal uji 23960 | outfit latih 23249, uji 4040
- AUC koherensi (outfit asli vs setengah-diacak): model 0.805, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 17 | 2026-10-06T15:53 | 27323 | 89193 | 0.774 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.848 pada 5782 item berlabel wanita & 1572 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
