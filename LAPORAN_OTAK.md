# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-16T05:32:11.462832+00:00 | putaran ke-54
- Outfit nyata terkumpul: **73233** | masuk bank (lolos saring): **7985**
  (ditolak karena item inti tidak bisa dibeli: 36300, tidak koheren: 3400)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4374, "gaya_masuk": 1301, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4464, "hilang": 136, "sisa_antre": 7579}, "sepatu": {"cari": 29, "lihat": 1662, "baru": 20, "total": 6236}} | permintaan HTTP 5214, kena 429: 100, gagal 61

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.336 | Uji akhir |
| CLIP netral-slot | 0.496 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.794 | Pemilihan |
| Model MLP (dilatih) | 0.810 | Pemilihan |
| Model terpilih | 0.814 | Uji akhir |

- Dipakai: **mlp** | soal uji 63566 | outfit latih 51215, pemilihan 10979, uji 10970
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.718
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 535 | item baru diminta pemain: 43
- Durasi putaran: **65.3 menit** | META: {"diminta": 4700, "diperbarui": 4464, "hilang": 136, "sisa_antre": 7579}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.635** vs kemiripan gaya saja 0.488
- Masuk 5% teratas: model **0.740** vs 0.588 | 3183 soal | contoh latih 115760
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 43 | 2026-10-13T01:41 | 58986 | 125362 | 0.809 | 26 |
| 44 | 2026-10-13T15:13 | 60253 | 126460 | 0.81 | 26 |
| 45 | 2026-10-13T23:47 | 61615 | 127986 | 0.808 | 26 |
| 46 | 2026-10-14T05:58 | 62911 | 129632 | 0.806 | 26 |
| 47 | 2026-10-14T12:51 | 64224 | 130936 | 0.809 | 26 |
| 48 | 2026-10-14T18:12 | 65349 | 132078 | 0.808 | 26 |
| 49 | 2026-10-14T22:42 | 66597 | 133385 | 0.812 | 26 |
| 50 | 2026-10-15T05:39 | 67973 | 134788 | 0.813 | 26 |
| 51 | 2026-10-15T12:25 | 69199 | 135755 | 0.814 | 26 |
| 52 | 2026-10-15T18:02 | 70510 | 136971 | 0.81 | 26 |
| 53 | 2026-10-15T22:20 | 71893 | 138203 | 0.814 | 26 |
| 54 | 2026-10-16T05:32 | 73233 | 139463 | 0.814 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 8710 item berlabel wanita & 2628 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2079 | 0.560 | 0.706 | 0.999 | v2 |
| FaceAcc | 2691 | 0.563 | 0.688 | 0.999 | v2 |
| Front | 2177 | 0.548 | 0.649 | 0.999 | v2 |
| Hair | 9866 | 0.688 | 0.805 | 1.000 | v2 |
| Hat | 7308 | 0.586 | 0.709 | 0.999 | v2 |
| LayerAtas | 5581 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3586 | 0.518 | 0.755 | 1.000 | v2 |
| Neck | 1873 | 0.587 | 0.710 | 0.999 | v2 |
| Pants | 4903 | 0.076 | 0.667 | 0.999 | v2 |
| Sepatu | 5068 | 0.611 | 0.709 | 1.000 | v2 |
| Shirt | 4906 | 0.283 | 0.722 | 1.000 | v2 |
| Shoulder | 989 | 0.592 | 0.697 | 1.000 | v2 |
| TShirt | 124 | 0.169 | 0.500 | 0.998 | v2 |
| Waist | 2322 | 0.593 | 0.689 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 19332 item | AUC {"asli": 0.59, "potongan": 0.621, "rata": 0.623} | label wanita/pria [746, 324] | dipakai: **rata**
- Pants: 18713 item | AUC {"asli": 0.67, "potongan": 0.67, "rata": 0.68} | label wanita/pria [1504, 280] | dipakai: **asli**
- TShirt: 3823 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [57, 19] | dipakai: **asli**

## Sepatu (bundle): 6236 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 1662, "baru": 20, "total": 6236}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
