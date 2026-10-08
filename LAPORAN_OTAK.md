# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-08T14:17:32.446452+00:00 | putaran ke-25
- Outfit nyata terkumpul: **37144** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 17198, tidak koheren: 1884)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3450, "gaya_masuk": 1053, "gaya_gemini": 0, "meta": {"diminta": 3395, "diperbarui": 3227, "hilang": 68, "sisa_antre": 688}} | permintaan HTTP 4071, kena 429: 70, gagal 39

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.503 |
| CLIP PCA-32 (tanpa belajar) | 0.487 |
| Model linear (dilatih) | 0.772 |
| Model MLP (dilatih) | 0.787 |

- Dipakai: **mlp** | soal uji 32534 | outfit latih 31607, uji 5527
- AUC koherensi (outfit asli vs setengah-diacak): model 0.809, CLIP 0.712
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **21** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 6
- Durasi putaran: **53.6 menit** | META: {"diminta": 3395, "diperbarui": 3227, "hilang": 68, "sisa_antre": 688}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 25 | 2026-10-08T14:17 | 37144 | 100028 | 0.787 | 21 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.840 pada 6480 item berlabel wanita & 1879 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
