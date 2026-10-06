# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-06T08:33:08.229385+00:00 | putaran ke-16
- Outfit nyata terkumpul: **25364** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 12381, tidak koheren: 1337)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 1991, "gaya_gemini": 0} | permintaan HTTP 6811, kena 429: 245, gagal 97

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.351 |
| CLIP netral-slot | 0.509 |
| CLIP PCA-32 (tanpa belajar) | 0.488 |
| Model linear (dilatih) | 0.758 |
| Model MLP (dilatih) | 0.772 |

- Dipakai: **mlp** | soal uji 22226 | outfit latih 21585, uji 3745
- AUC koherensi (outfit asli vs setengah-diacak): model 0.809, CLIP 0.721
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 16 | 2026-10-06T08:33 | 25364 | 86595 | 0.772 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 5641 item berlabel wanita & 1521 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
