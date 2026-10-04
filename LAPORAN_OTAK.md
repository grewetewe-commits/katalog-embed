# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-04T14:08:20.240235+00:00 | putaran ke-10
- Outfit nyata terkumpul: **13317** | masuk bank (lolos saring): **5454**
  (ditolak karena item inti tidak bisa dibeli: 7234, tidak koheren: 629)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 6000, "gaya_masuk": 2101, "gaya_gemini": 0} | permintaan HTTP 6606, kena 429: 154, gagal 53

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.363 |
| CLIP netral-slot | 0.522 |
| CLIP PCA-32 (tanpa belajar) | 0.499 |
| Model linear (dilatih) | 0.737 |
| Model MLP (dilatih) | 0.761 |

- Dipakai: **mlp** | soal uji 11623 | outfit latih 11372, uji 1924
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.729
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 527

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 10 | 2026-10-04T14:08 | 13317 | 66866 | 0.761 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.861 pada 4539 item berlabel wanita & 1088 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
