# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-07T14:11:58.989006+00:00 | putaran ke-21
- Outfit nyata terkumpul: **32297** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 14954, tidak koheren: 1844)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4400, "gaya_masuk": 1437, "gaya_gemini": 0, "meta": {"diminta": 1471, "diperbarui": 1314, "hilang": 57, "sisa_antre": 1272}} | permintaan HTTP 4965, kena 429: 27, gagal 43

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.341 |
| CLIP netral-slot | 0.503 |
| CLIP PCA-32 (tanpa belajar) | 0.487 |
| Model linear (dilatih) | 0.767 |
| Model MLP (dilatih) | 0.781 |

- Dipakai: **mlp** | soal uji 28490 | outfit latih 27447, uji 4822
- AUC koherensi (outfit asli vs setengah-diacak): model 0.812, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **10** | outfit dasar dari server Roblox: 528 | item baru diminta pemain: 1
- Durasi putaran: **54.9 menit** | META: {"diminta": 1471, "diperbarui": 1314, "hilang": 57, "sisa_antre": 1272}

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 21 | 2026-10-07T14:11 | 32297 | 94944 | 0.781 | 10 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.844 pada 6176 item berlabel wanita & 1740 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
