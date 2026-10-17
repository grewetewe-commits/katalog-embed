# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-17T16:41:44.635050+00:00 | putaran ke-60
- Outfit nyata terkumpul: **80263** | masuk bank (lolos saring): **7986**
  (ditolak karena item inti tidak bisa dibeli: 39706, tidak koheren: 3781)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4269, "gaya_masuk": 1208, "gaya_gemini": 0, "meta": {"diminta": 4700, "diperbarui": 4345, "hilang": 255, "sisa_antre": 13898}, "sepatu": {"cari": 29, "lihat": 1682, "baru": 22, "total": 6379}} | permintaan HTTP 5097, kena 429: 99, gagal 58

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.336 | Uji akhir |
| CLIP netral-slot | 0.499 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.794 | Pemilihan |
| Model MLP (dilatih) | 0.817 | Pemilihan |
| Model terpilih | 0.820 | Uji akhir |

- Dipakai: **mlp** | soal uji 69870 | outfit latih 56045, pemilihan 12068, uji 12069
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.806, CLIP 0.716
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 540 | item baru diminta pemain: 5700
- Durasi putaran: **71.6 menit** | META: {"diminta": 4700, "diperbarui": 4345, "hilang": 255, "sisa_antre": 13898}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.595** vs kemiripan gaya saja 0.406
- Masuk 5% teratas: model **0.695** vs 0.522 | 3245 soal | contoh latih 115464
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 60 | 2026-10-17T16:41 | 80263 | 149711 | 0.82 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.846 pada 9257 item berlabel wanita & 2790 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2284 | 0.558 | 0.709 | 0.999 | v2 |
| FaceAcc | 2902 | 0.565 | 0.690 | 0.999 | v2 |
| Front | 2361 | 0.544 | 0.644 | 0.999 | v2 |
| Hair | 10434 | 0.685 | 0.805 | 1.000 | v2 |
| Hat | 7746 | 0.585 | 0.710 | 0.999 | v2 |
| LayerAtas | 5890 | 0.489 | 0.736 | 0.999 | v2 |
| LayerBawah | 3756 | 0.516 | 0.753 | 1.000 | v2 |
| Neck | 2033 | 0.579 | 0.705 | 0.999 | v2 |
| Pants | 5278 | 0.074 | 0.662 | 0.999 | v2 |
| Sepatu | 5214 | 0.611 | 0.708 | 1.000 | v2 |
| Shirt | 5329 | 0.282 | 0.725 | 1.000 | v2 |
| Shoulder | 1100 | 0.588 | 0.697 | 1.000 | v2 |
| TShirt | 136 | 0.176 | 0.493 | 0.998 | v2 |
| Waist | 2505 | 0.588 | 0.689 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 21009 item | AUC {"asli": 0.598, "potongan": 0.624, "rata": 0.628} | label wanita/pria [828, 357] | dipakai: **rata**
- Pants: 20269 item | AUC {"asli": 0.663, "potongan": 0.667, "rata": 0.676} | label wanita/pria [1633, 301] | dipakai: **asli**
- TShirt: 4092 item | AUC {"asli": 0.601, "potongan": 0.429, "rata": 0.499} | label wanita/pria [60, 20] | dipakai: **asli**

## Sepatu (bundle): 6379 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 1682, "baru": 22, "total": 6379}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
