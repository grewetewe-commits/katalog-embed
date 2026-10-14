# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-14T18:12:47.564414+00:00 | putaran ke-48
- Outfit nyata terkumpul: **65349** | masuk bank (lolos saring): **7978**
  (ditolak karena item inti tidak bisa dibeli: 32384, tidak koheren: 2996)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3790, "gaya_masuk": 1095, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4640, "hilang": 60, "sisa_antre": 2140}, "sepatu": {"cari": 30, "lihat": 1897, "baru": 107, "total": 5780}} | permintaan HTTP 4604, kena 429: 99, gagal 58

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.336 | Uji akhir |
| CLIP netral-slot | 0.498 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.486 | Pemilihan |
| Model linear (dilatih) | 0.788 | Pemilihan |
| Model MLP (dilatih) | 0.809 | Pemilihan |
| Model terpilih | 0.808 | Uji akhir |

- Dipakai: **mlp** | soal uji 56387 | outfit latih 45749, pemilihan 9832, uji 9713
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.805, CLIP 0.715
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **65.1 menit** | META: {"diminta": 4800, "diperbarui": 4640, "hilang": 60, "sisa_antre": 2140}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.606** vs kemiripan gaya saja 0.441
- Masuk 5% teratas: model **0.722** vs 0.560 | 3101 soal | contoh latih 115649
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 37 | 2026-10-11T06:39 | 51714 | 118451 | 0.803 | 26 |
| 38 | 2026-10-11T13:46 | 53042 | 119578 | 0.806 | 26 |
| 39 | 2026-10-11T17:32 | 54490 | 120753 | 0.802 | 26 |
| 40 | 2026-10-11T23:00 | 55562 | 121756 | 0.803 | 26 |
| 41 | 2026-10-12T06:57 | 56598 | 122754 | 0.805 | 26 |
| 42 | 2026-10-12T16:20 | 57841 | 123952 | 0.805 | 26 |
| 43 | 2026-10-13T01:41 | 58986 | 125362 | 0.809 | 26 |
| 44 | 2026-10-13T15:13 | 60253 | 126460 | 0.81 | 26 |
| 45 | 2026-10-13T23:47 | 61615 | 127986 | 0.808 | 26 |
| 46 | 2026-10-14T05:58 | 62911 | 129632 | 0.806 | 26 |
| 47 | 2026-10-14T12:51 | 64224 | 130936 | 0.809 | 26 |
| 48 | 2026-10-14T18:12 | 65349 | 132078 | 0.808 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 8326 item berlabel wanita & 2485 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2010 | 0.554 | 0.701 | 0.999 | v2 |
| FaceAcc | 2558 | 0.561 | 0.686 | 0.999 | v2 |
| Front | 2088 | 0.544 | 0.643 | 0.999 | v2 |
| Hair | 9380 | 0.689 | 0.805 | 1.000 | v2 |
| Hat | 6979 | 0.585 | 0.708 | 0.999 | v2 |
| LayerAtas | 5471 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3542 | 0.518 | 0.755 | 1.000 | v2 |
| Neck | 1792 | 0.583 | 0.708 | 0.999 | v2 |
| Pants | 4565 | 0.077 | 0.666 | 0.999 | v2 |
| Sepatu | 4727 | 0.613 | 0.708 | 1.000 | v2 |
| Shirt | 4547 | 0.283 | 0.723 | 1.000 | v2 |
| Shoulder | 935 | 0.590 | 0.694 | 1.000 | v2 |
| TShirt | 113 | 0.186 | 0.504 | 0.998 | v2 |
| Waist | 2239 | 0.592 | 0.687 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 17831 item | AUC {"asli": 0.589, "potongan": 0.618, "rata": 0.62} | label wanita/pria [683, 297] | dipakai: **rata**
- Pants: 17300 item | AUC {"asli": 0.665, "potongan": 0.673, "rata": 0.681} | label wanita/pria [1412, 255] | dipakai: **asli**
- TShirt: 3535 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [54, 17] | dipakai: **asli**

## Sepatu (bundle): 5780 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 1897, "baru": 107, "total": 5780}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
