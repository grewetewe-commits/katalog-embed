# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-16T17:42:24.356161+00:00 | putaran ke-56
- Outfit nyata terkumpul: **75715** | masuk bank (lolos saring): **7985**
  (ditolak karena item inti tidak bisa dibeli: 37503, tidak koheren: 3611)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3950, "gaya_masuk": 1177, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4494, "hilang": 206, "sisa_antre": 9894}, "sepatu": {"cari": 30, "lihat": 1935, "baru": 52, "total": 6315}} | permintaan HTTP 4824, kena 429: 100, gagal 63

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.334 | Uji akhir |
| CLIP netral-slot | 0.497 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.793 | Pemilihan |
| Model MLP (dilatih) | 0.812 | Pemilihan |
| Model terpilih | 0.814 | Uji akhir |

- Dipakai: **mlp** | soal uji 65809 | outfit latih 52908, pemilihan 11374, uji 11359
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.803, CLIP 0.712
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 537 | item baru diminta pemain: 1061
- Durasi putaran: **66.7 menit** | META: {"diminta": 4800, "diperbarui": 4494, "hilang": 206, "sisa_antre": 9894}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.625** vs kemiripan gaya saja 0.447
- Masuk 5% teratas: model **0.725** vs 0.554 | 3108 soal | contoh latih 115688
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 55 | 2026-10-16T12:20 | 74501 | 140553 | 0.815 | 26 |
| 56 | 2026-10-16T17:42 | 75715 | 142074 | 0.814 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.848 pada 8854 item berlabel wanita & 2679 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2124 | 0.560 | 0.708 | 0.999 | v2 |
| FaceAcc | 2739 | 0.564 | 0.687 | 0.999 | v2 |
| Front | 2226 | 0.548 | 0.646 | 0.999 | v2 |
| Hair | 10049 | 0.688 | 0.805 | 1.000 | v2 |
| Hat | 7455 | 0.586 | 0.710 | 0.999 | v2 |
| LayerAtas | 5647 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3618 | 0.517 | 0.755 | 1.000 | v2 |
| Neck | 1917 | 0.583 | 0.709 | 0.999 | v2 |
| Pants | 5011 | 0.075 | 0.664 | 0.999 | v2 |
| Sepatu | 5148 | 0.610 | 0.707 | 1.000 | v2 |
| Shirt | 5030 | 0.284 | 0.723 | 1.000 | v2 |
| Shoulder | 1015 | 0.586 | 0.693 | 1.000 | v2 |
| TShirt | 132 | 0.159 | 0.485 | 0.998 | v2 |
| Waist | 2374 | 0.593 | 0.691 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 19809 item | AUC {"asli": 0.594, "potongan": 0.621, "rata": 0.624} | label wanita/pria [762, 338] | dipakai: **rata**
- Pants: 19140 item | AUC {"asli": 0.668, "potongan": 0.669, "rata": 0.679} | label wanita/pria [1535, 284] | dipakai: **asli**
- TShirt: 3915 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [57, 19] | dipakai: **asli**

## Sepatu (bundle): 6315 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 1935, "baru": 52, "total": 6315}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
