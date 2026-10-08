# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-08T06:55:18.090299+00:00 | putaran ke-24
- Outfit nyata terkumpul: **36091** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 16639, tidak koheren: 1812)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3250, "gaya_masuk": 1037, "gaya_gemini": 0, "meta": {"diminta": 1820, "diperbarui": 1643, "hilang": 77, "sisa_antre": 852}} | permintaan HTTP 3838, kena 429: 34, gagal 44

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.341 |
| CLIP netral-slot | 0.507 |
| CLIP PCA-32 (tanpa belajar) | 0.490 |
| Model linear (dilatih) | 0.768 |
| Model MLP (dilatih) | 0.788 |

- Dipakai: **mlp** | soal uji 31670 | outfit latih 30712, uji 5369
- AUC koherensi (outfit asli vs setengah-diacak): model 0.820, CLIP 0.720
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 5
- Durasi putaran: **56.7 menit** | META: {"diminta": 1820, "diperbarui": 1643, "hilang": 77, "sisa_antre": 852}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 24 | 2026-10-08T06:55 | 36091 | 99040 | 0.788 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6420 item berlabel wanita & 1854 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
