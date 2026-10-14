# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-14T05:58:15.312662+00:00 | putaran ke-46
- Outfit nyata terkumpul: **62911** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 31219, tidak koheren: 2975)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4342, "gaya_masuk": 1296, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4623, "hilang": 77, "sisa_antre": 3712}, "sepatu": {"cari": 30, "lihat": 2338, "baru": 390, "total": 5363}} | permintaan HTTP 5074, kena 429: 99, gagal 45

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.337 | Uji akhir |
| CLIP netral-slot | 0.498 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.487 | Pemilihan |
| Model linear (dilatih) | 0.787 | Pemilihan |
| Model MLP (dilatih) | 0.804 | Pemilihan |
| Model terpilih | 0.806 | Uji akhir |

- Dipakai: **mlp** | soal uji 54386 | outfit latih 44048, pemilihan 9454, uji 9360
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.801, CLIP 0.714
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **68.8 menit** | META: {"diminta": 4800, "diperbarui": 4623, "hilang": 77, "sisa_antre": 3712}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.586** vs kemiripan gaya saja 0.442
- Masuk 5% teratas: model **0.699** vs 0.543 | 3144 soal | contoh latih 115828
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 35 | 2026-10-10T22:43 | 49352 | 116226 | 0.802 | 25 |
| 36 | 2026-10-11T02:37 | 50426 | 117219 | 0.8 | 25 |
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

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 8142 item berlabel wanita & 2423 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1991 | 0.554 | 0.701 | 0.999 | v2 |
| FaceAcc | 2514 | 0.560 | 0.683 | 0.999 | v2 |
| Front | 2050 | 0.541 | 0.641 | 0.999 | v2 |
| Hair | 9222 | 0.689 | 0.804 | 1.000 | v2 |
| Hat | 6876 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5443 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3525 | 0.519 | 0.754 | 1.000 | v2 |
| Neck | 1759 | 0.582 | 0.709 | 0.999 | v2 |
| Pants | 4433 | 0.077 | 0.663 | 0.999 | v2 |
| Sepatu | 4423 | 0.616 | 0.711 | 1.000 | v2 |
| Shirt | 4417 | 0.282 | 0.723 | 1.000 | v2 |
| Shoulder | 922 | 0.594 | 0.694 | 1.000 | v2 |
| TShirt | 106 | 0.189 | 0.500 | 0.998 | v2 |
| Waist | 2219 | 0.593 | 0.686 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 17394 item | AUC {"asli": 0.586, "potongan": 0.618, "rata": 0.619} | label wanita/pria [661, 290] | dipakai: **rata**
- Pants: 16906 item | AUC {"asli": 0.671, "potongan": 0.678, "rata": 0.686} | label wanita/pria [1377, 245] | dipakai: **asli**
- TShirt: 3445 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [54, 16] | dipakai: **asli**

## Sepatu (bundle): 5363 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2338, "baru": 390, "total": 5363}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
