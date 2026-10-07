# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-07T19:46:03.763398+00:00 | putaran ke-22
- Outfit nyata terkumpul: **33663** | masuk bank (lolos saring): **7909**
  (ditolak karena item inti tidak bisa dibeli: 15575, tidak koheren: 1689)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4569, "gaya_masuk": 1366, "gaya_gemini": 0, "meta": {"diminta": 1821, "diperbarui": 1629, "hilang": 92, "sisa_antre": 1183}} | permintaan HTTP 5223, kena 429: 39, gagal 49

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.344 |
| CLIP netral-slot | 0.507 |
| CLIP PCA-32 (tanpa belajar) | 0.487 |
| Model linear (dilatih) | 0.768 |
| Model MLP (dilatih) | 0.785 |

- Dipakai: **mlp** | soal uji 29592 | outfit latih 28620, uji 5014
- AUC koherensi (outfit asli vs setengah-diacak): model 0.813, CLIP 0.716
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **10** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 1
- Durasi putaran: **52.2 menit** | META: {"diminta": 1821, "diperbarui": 1629, "hilang": 92, "sisa_antre": 1183}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 22 | 2026-10-07T19:46 | 33663 | 96431 | 0.785 | 10 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.843 pada 6262 item berlabel wanita & 1777 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
