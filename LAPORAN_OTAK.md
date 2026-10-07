# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-07T06:48:25.610382+00:00 | putaran ke-20
- Outfit nyata terkumpul: **30855** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 14223, tidak koheren: 1772)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4149, "gaya_masuk": 1243, "gaya_gemini": 0, "meta": {"diminta": 1620, "diperbarui": 1524, "hilang": 96, "sisa_antre": 956}} | permintaan HTTP 4683, kena 429: 31, gagal 40

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.501 |
| CLIP PCA-32 (tanpa belajar) | 0.484 |
| Model linear (dilatih) | 0.763 |
| Model MLP (dilatih) | 0.779 |

- Dipakai: **mlp** | soal uji 27287 | outfit latih 26204, uji 4616
- AUC koherensi (outfit asli vs setengah-diacak): model 0.806, CLIP 0.712
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **5** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 1
- Durasi putaran: **53.8 menit** | META: {"diminta": 1620, "diperbarui": 1524, "hilang": 96, "sisa_antre": 956}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 20 | 2026-10-07T06:48 | 30855 | 93379 | 0.779 | 5 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.845 pada 6102 item berlabel wanita & 1711 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
