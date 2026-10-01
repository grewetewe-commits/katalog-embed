# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-01T22:54:50.155772+00:00 | putaran ke-1
- Outfit nyata terkumpul: **195** | masuk bank (lolos saring): **103**
  (ditolak karena item inti tidak bisa dibeli: 79, tidak koheren: 13)
- Item dengan sidik jari visual: **8082**
- Panen putaran ini: {"kreator": 123, "outfit_baru": 195, "ditolak": 161, "kembar": 18, "tanpa_outfit": 87} | permintaan HTTP 987, kena 429: 270, gagal 118

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.411 |
| CLIP netral-slot | 0.639 |
| CLIP PCA-32 (tanpa belajar) | 0.606 |
| Model linear (dilatih) | 0.822 |
| Model MLP (dilatih) | 0.789 |

- Dipakai: **linear** | soal uji 180 | outfit latih 169, uji 25
- AUC koherensi (outfit asli vs setengah-diacak): model 0.903, CLIP 0.814
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.844 pada 795 item berlabel wanita & 66 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
