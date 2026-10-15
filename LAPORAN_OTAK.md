# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-15T05:39:13.539389+00:00 | putaran ke-50
- Outfit nyata terkumpul: **67973** | masuk bank (lolos saring): **7982**
  (ditolak karena item inti tidak bisa dibeli: 33775, tidak koheren: 3124)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4400, "gaya_masuk": 1343, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4621, "hilang": 79, "sisa_antre": 3611}, "sepatu": {"cari": 30, "lihat": 1628, "baru": 41, "total": 6011}} | permintaan HTTP 5242, kena 429: 101, gagal 57

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.334 | Uji akhir |
| CLIP netral-slot | 0.499 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.490 | Pemilihan |
| Model linear (dilatih) | 0.791 | Pemilihan |
| Model MLP (dilatih) | 0.811 | Pemilihan |
| Model terpilih | 0.813 | Uji akhir |

- Dipakai: **mlp** | soal uji 58999 | outfit latih 47561, pemilihan 10194, uji 10158
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.803, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **65.9 menit** | META: {"diminta": 4800, "diperbarui": 4621, "hilang": 79, "sisa_antre": 3611}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.613** vs kemiripan gaya saja 0.459
- Masuk 5% teratas: model **0.718** vs 0.564 | 3140 soal | contoh latih 115448
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 49 | 2026-10-14T22:42 | 66597 | 133385 | 0.812 | 26 |
| 50 | 2026-10-15T05:39 | 67973 | 134788 | 0.813 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 8443 item berlabel wanita & 2528 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2024 | 0.555 | 0.702 | 0.999 | v2 |
| FaceAcc | 2595 | 0.561 | 0.686 | 0.999 | v2 |
| Front | 2126 | 0.546 | 0.645 | 0.999 | v2 |
| Hair | 9542 | 0.688 | 0.805 | 1.000 | v2 |
| Hat | 7084 | 0.585 | 0.708 | 0.999 | v2 |
| LayerAtas | 5513 | 0.486 | 0.732 | 0.999 | v2 |
| LayerBawah | 3554 | 0.519 | 0.755 | 1.000 | v2 |
| Neck | 1813 | 0.584 | 0.708 | 0.999 | v2 |
| Pants | 4679 | 0.077 | 0.667 | 0.999 | v2 |
| Sepatu | 4896 | 0.611 | 0.708 | 1.000 | v2 |
| Shirt | 4664 | 0.282 | 0.722 | 1.000 | v2 |
| Shoulder | 955 | 0.595 | 0.697 | 1.000 | v2 |
| TShirt | 116 | 0.181 | 0.517 | 0.998 | v2 |
| Waist | 2265 | 0.592 | 0.688 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 18388 item | AUC {"asli": 0.588, "potongan": 0.616, "rata": 0.618} | label wanita/pria [703, 305] | dipakai: **rata**
- Pants: 17819 item | AUC {"asli": 0.667, "potongan": 0.673, "rata": 0.681} | label wanita/pria [1444, 262] | dipakai: **asli**
- TShirt: 3631 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [54, 18] | dipakai: **asli**

## Sepatu (bundle): 6011 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 1628, "baru": 41, "total": 6011}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
