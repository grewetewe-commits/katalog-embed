# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-02T08:51:40.788305+00:00 | putaran ke-2
- Outfit nyata terkumpul: **972** | masuk bank (lolos saring): **163**
  (ditolak karena item inti tidak bisa dibeli: 789, tidak koheren: 20)
- Item dengan sidik jari visual: **19826**
- Panen putaran ini: {"kreator": 310, "outfit_baru": 777, "ditolak": 459, "kembar": 47, "tanpa_outfit": 175} | permintaan HTTP 2559, kena 429: 865, gagal 390

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.416 |
| CLIP netral-slot | 0.611 |
| CLIP PCA-32 (tanpa belajar) | 0.590 |
| Model linear (dilatih) | 0.589 |
| Model MLP (dilatih) | 0.636 |

- Dipakai: **mlp** | soal uji 786 | outfit latih 855, uji 110
- AUC koherensi (outfit asli vs setengah-diacak): model 0.831, CLIP 0.804
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.885 pada 1976 item berlabel wanita & 267 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
