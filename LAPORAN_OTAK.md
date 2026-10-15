# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-15T12:25:44.779991+00:00 | putaran ke-51
- Outfit nyata terkumpul: **69199** | masuk bank (lolos saring): **7982**
  (ditolak karena item inti tidak bisa dibeli: 34294, tidak koheren: 3151)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3991, "gaya_masuk": 1200, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4620, "hilang": 80, "sisa_antre": 8325}, "sepatu": {"cari": 29, "lihat": 1959, "baru": 82, "total": 6093}} | permintaan HTTP 4771, kena 429: 100, gagal 55

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.500 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.489 | Pemilihan |
| Model linear (dilatih) | 0.791 | Pemilihan |
| Model MLP (dilatih) | 0.811 | Pemilihan |
| Model terpilih | 0.814 | Uji akhir |

- Dipakai: **mlp** | soal uji 60002 | outfit latih 48434, pemilihan 10377, uji 10325
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.810, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **62.6 menit** | META: {"diminta": 4800, "diperbarui": 4620, "hilang": 80, "sisa_antre": 8325}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.605** vs kemiripan gaya saja 0.435
- Masuk 5% teratas: model **0.716** vs 0.552 | 3215 soal | contoh latih 115301
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 40 | 2026-10-11T23:00 | 55562 | 121756 | 0.803 | 26 |
| 41 | 2026-10-12T06:57 | 56598 | 122754 | 0.805 | 26 |
| 42 | 2026-10-12T16:20 | 57841 | 123952 | 0.805 | 26 |
| 43 | 2026-10-13T01:41 | 58986 | 125362 | 0.809 | 26 |
| 44 | 2026-10-13T15:13 | 60253 | 126460 | 0.81 | 26 |
| 45 | 2026-10-13T23:47 | 61615 | 127986 | 0.808 | 26 |
| 46 | 2026-10-14T05:58 | 62911 | 129632 | 0.806 | 26 |
| 47 | 2026-10-14T12:51 | 64224 | 130936 | 0.809 | 26 |
| 48 | 2026-10-14T18:12 | 65349 | 132078 | 0.808 | 26 |
| 49 | 2026-10-14T22:42 | 66597 | 133385 | 0.812 | 26 |
| 50 | 2026-10-15T05:39 | 67973 | 134788 | 0.813 | 26 |
| 51 | 2026-10-15T12:25 | 69199 | 135755 | 0.814 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 8541 item berlabel wanita & 2564 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2042 | 0.556 | 0.703 | 0.999 | v2 |
| FaceAcc | 2617 | 0.562 | 0.687 | 0.999 | v2 |
| Front | 2146 | 0.548 | 0.646 | 0.999 | v2 |
| Hair | 9651 | 0.687 | 0.805 | 1.000 | v2 |
| Hat | 7161 | 0.585 | 0.708 | 0.999 | v2 |
| LayerAtas | 5533 | 0.486 | 0.732 | 0.999 | v2 |
| LayerBawah | 3567 | 0.518 | 0.755 | 1.000 | v2 |
| Neck | 1835 | 0.584 | 0.708 | 0.999 | v2 |
| Pants | 4740 | 0.077 | 0.666 | 0.999 | v2 |
| Sepatu | 4954 | 0.612 | 0.709 | 1.000 | v2 |
| Shirt | 4751 | 0.281 | 0.722 | 1.000 | v2 |
| Shoulder | 966 | 0.591 | 0.698 | 1.000 | v2 |
| TShirt | 117 | 0.179 | 0.521 | 0.998 | v2 |
| Waist | 2278 | 0.593 | 0.688 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 18576 item | AUC {"asli": 0.588, "potongan": 0.617, "rata": 0.619} | label wanita/pria [721, 312] | dipakai: **rata**
- Pants: 17999 item | AUC {"asli": 0.67, "potongan": 0.675, "rata": 0.684} | label wanita/pria [1465, 266] | dipakai: **asli**
- TShirt: 3672 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [54, 18] | dipakai: **asli**

## Sepatu (bundle): 6093 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 1959, "baru": 82, "total": 6093}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
