# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-17T11:48:57.643787+00:00 | putaran ke-59
- Outfit nyata terkumpul: **79035** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 39086, tidak koheren: 3637)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3290, "gaya_masuk": 965, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4375, "hilang": 225, "sisa_antre": 14711}, "sepatu": {"cari": 30, "lihat": 1774, "baru": 1, "total": 6357}} | permintaan HTTP 4137, kena 429: 98, gagal 66

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.497 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.490 | Pemilihan |
| Model linear (dilatih) | 0.795 | Pemilihan |
| Model MLP (dilatih) | 0.817 | Pemilihan |
| Model terpilih | 0.819 | Uji akhir |

- Dipakai: **mlp** | soal uji 68815 | outfit latih 55186, pemilihan 11882, uji 11888
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.807, CLIP 0.713
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 539 | item baru diminta pemain: 4495
- Durasi putaran: **70.8 menit** | META: {"diminta": 4700, "diperbarui": 4375, "hilang": 225, "sisa_antre": 14711}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.622** vs kemiripan gaya saja 0.454
- Masuk 5% teratas: model **0.726** vs 0.566 | 3125 soal | contoh latih 115167
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 59 | 2026-10-17T11:48 | 79035 | 147646 | 0.819 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.847 pada 9164 item berlabel wanita & 2773 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2258 | 0.558 | 0.709 | 0.999 | v2 |
| FaceAcc | 2856 | 0.564 | 0.689 | 0.999 | v2 |
| Front | 2325 | 0.543 | 0.644 | 0.999 | v2 |
| Hair | 10332 | 0.686 | 0.805 | 1.000 | v2 |
| Hat | 7664 | 0.585 | 0.710 | 0.999 | v2 |
| LayerAtas | 5854 | 0.488 | 0.736 | 0.999 | v2 |
| LayerBawah | 3741 | 0.516 | 0.753 | 1.000 | v2 |
| Neck | 2005 | 0.581 | 0.706 | 0.999 | v2 |
| Pants | 5200 | 0.074 | 0.664 | 0.999 | v2 |
| Sepatu | 5199 | 0.611 | 0.707 | 1.000 | v2 |
| Shirt | 5258 | 0.282 | 0.724 | 1.000 | v2 |
| Shoulder | 1078 | 0.589 | 0.698 | 1.000 | v2 |
| TShirt | 133 | 0.165 | 0.489 | 0.998 | v2 |
| Waist | 2473 | 0.589 | 0.690 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 20653 item | AUC {"asli": 0.597, "potongan": 0.624, "rata": 0.628} | label wanita/pria [809, 356] | dipakai: **rata**
- Pants: 19908 item | AUC {"asli": 0.664, "potongan": 0.666, "rata": 0.676} | label wanita/pria [1600, 297] | dipakai: **asli**
- TShirt: 4047 item | AUC {"asli": 0.594, "potongan": 0.425, "rata": 0.491} | label wanita/pria [59, 20] | dipakai: **asli**

## Sepatu (bundle): 6357 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 1774, "baru": 1, "total": 6357}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
