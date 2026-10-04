# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-04T07:39:26.003383+00:00 | putaran ke-9
- Outfit nyata terkumpul: **11216** | masuk bank (lolos saring): **4441**
  (ditolak karena item inti tidak bisa dibeli: 6293, tidak koheren: 482)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 1999, "gaya_gemini": 0} | permintaan HTTP 6594, kena 429: 165, gagal 55

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.359 |
| CLIP netral-slot | 0.522 |
| CLIP PCA-32 (tanpa belajar) | 0.505 |
| Model linear (dilatih) | 0.731 |
| Model MLP (dilatih) | 0.749 |

- Dipakai: **mlp** | soal uji 9829 | outfit latih 9594, uji 1602
- AUC koherensi (outfit asli vs setengah-diacak): model 0.809, CLIP 0.730
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 9 | 2026-10-04T07:39 | 11216 | 63178 | 0.749 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.863 pada 4327 item berlabel wanita & 997 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
