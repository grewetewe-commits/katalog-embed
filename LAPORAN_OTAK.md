# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-07T23:55:14.799290+00:00 | putaran ke-23
- Outfit nyata terkumpul: **35054** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 16217, tidak koheren: 1775)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4563, "gaya_masuk": 1380, "gaya_gemini": 0, "meta": {"diminta": 1721, "diperbarui": 1537, "hilang": 84, "sisa_antre": 1054}} | permintaan HTTP 5169, kena 429: 34, gagal 46

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.504 |
| CLIP PCA-32 (tanpa belajar) | 0.486 |
| Model linear (dilatih) | 0.768 |
| Model MLP (dilatih) | 0.787 |

- Dipakai: **mlp** | soal uji 30764 | outfit latih 29831, uji 5215
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.715
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 5
- Durasi putaran: **51.8 menit** | META: {"diminta": 1721, "diperbarui": 1537, "hilang": 84, "sisa_antre": 1054}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 23 | 2026-10-07T23:55 | 35054 | 97886 | 0.787 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.841 pada 6362 item berlabel wanita & 1820 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
