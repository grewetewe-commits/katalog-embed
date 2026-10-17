# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-17T05:27:43.544403+00:00 | putaran ke-58
- Outfit nyata terkumpul: **78035** | masuk bank (lolos saring): **7986**
  (ditolak karena item inti tidak bisa dibeli: 38640, tidak koheren: 3538)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4510, "gaya_masuk": 1240, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4335, "hilang": 265, "sisa_antre": 12824}, "sepatu": {"cari": 29, "lihat": 1852, "baru": 34, "total": 6356}} | permintaan HTTP 5359, kena 429: 100, gagal 58

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.338 | Uji akhir |
| CLIP netral-slot | 0.497 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.485 | Pemilihan |
| Model linear (dilatih) | 0.791 | Pemilihan |
| Model MLP (dilatih) | 0.815 | Pemilihan |
| Model terpilih | 0.817 | Uji akhir |

- Dipakai: **mlp** | soal uji 67931 | outfit latih 54488, pemilihan 11739, uji 11731
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.816, CLIP 0.717
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 538 | item baru diminta pemain: 3195
- Durasi putaran: **66.7 menit** | META: {"diminta": 4700, "diperbarui": 4335, "hilang": 265, "sisa_antre": 12824}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.648** vs kemiripan gaya saja 0.478
- Masuk 5% teratas: model **0.737** vs 0.581 | 3205 soal | contoh latih 115394
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 47 | 2026-10-14T12:51 | 64224 | 130936 | 0.809 | 26 |
| 48 | 2026-10-14T18:12 | 65349 | 132078 | 0.808 | 26 |
| 49 | 2026-10-14T22:42 | 66597 | 133385 | 0.812 | 26 |
| 50 | 2026-10-15T05:39 | 67973 | 134788 | 0.813 | 26 |
| 51 | 2026-10-15T12:25 | 69199 | 135755 | 0.814 | 26 |
| 52 | 2026-10-15T18:02 | 70510 | 136971 | 0.81 | 26 |
| 53 | 2026-10-15T22:20 | 71893 | 138203 | 0.814 | 26 |
| 54 | 2026-10-16T05:32 | 73233 | 139463 | 0.814 | 26 |
| 55 | 2026-10-16T12:20 | 74501 | 140553 | 0.815 | 26 |
| 56 | 2026-10-16T17:42 | 75715 | 142074 | 0.814 | 26 |
| 57 | 2026-10-16T22:15 | 76759 | 143777 | 0.815 | 26 |
| 58 | 2026-10-17T05:27 | 78035 | 145697 | 0.817 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.848 pada 9063 item berlabel wanita & 2740 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2209 | 0.560 | 0.708 | 0.999 | v2 |
| FaceAcc | 2811 | 0.564 | 0.688 | 0.999 | v2 |
| Front | 2284 | 0.547 | 0.645 | 0.999 | v2 |
| Hair | 10238 | 0.686 | 0.805 | 1.000 | v2 |
| Hat | 7573 | 0.585 | 0.710 | 0.999 | v2 |
| LayerAtas | 5797 | 0.487 | 0.735 | 0.999 | v2 |
| LayerBawah | 3699 | 0.516 | 0.753 | 1.000 | v2 |
| Neck | 1974 | 0.583 | 0.708 | 0.999 | v2 |
| Pants | 5121 | 0.075 | 0.664 | 0.999 | v2 |
| Sepatu | 5192 | 0.611 | 0.708 | 1.000 | v2 |
| Shirt | 5163 | 0.283 | 0.725 | 1.000 | v2 |
| Shoulder | 1054 | 0.587 | 0.695 | 1.000 | v2 |
| TShirt | 133 | 0.165 | 0.489 | 0.998 | v2 |
| Waist | 2432 | 0.589 | 0.690 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 20347 item | AUC {"asli": 0.593, "potongan": 0.624, "rata": 0.626} | label wanita/pria [794, 350] | dipakai: **rata**
- Pants: 19616 item | AUC {"asli": 0.667, "potongan": 0.669, "rata": 0.678} | label wanita/pria [1568, 295] | dipakai: **asli**
- TShirt: 3997 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [58, 19] | dipakai: **asli**

## Sepatu (bundle): 6356 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 1852, "baru": 34, "total": 6356}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
