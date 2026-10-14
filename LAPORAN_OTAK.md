# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-14T12:51:15.389057+00:00 | putaran ke-47
- Outfit nyata terkumpul: **64224** | masuk bank (lolos saring): **7983**
  (ditolak karena item inti tidak bisa dibeli: 31783, tidak koheren: 2864)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4350, "gaya_masuk": 1285, "gaya_gemini": 0, "meta": {"diminta": 4800, "diperbarui": 4638, "hilang": 62, "sisa_antre": 1520}, "sepatu": {"cari": 30, "lihat": 1821, "baru": 310, "total": 5673}} | permintaan HTTP 5173, kena 429: 99, gagal 58

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.335 | Uji akhir |
| CLIP netral-slot | 0.500 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.786 | Pemilihan |
| Model MLP (dilatih) | 0.808 | Pemilihan |
| Model terpilih | 0.809 | Uji akhir |

- Dipakai: **mlp** | soal uji 55495 | outfit latih 44970, pemilihan 9646, uji 9558
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.712
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 43
- Durasi putaran: **64.0 menit** | META: {"diminta": 4800, "diperbarui": 4638, "hilang": 62, "sisa_antre": 1520}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.617** vs kemiripan gaya saja 0.438
- Masuk 5% teratas: model **0.726** vs 0.548 | 3159 soal | contoh latih 115596
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 47 | 2026-10-14T12:51 | 64224 | 130936 | 0.809 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.850 pada 8276 item berlabel wanita & 2458 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 2002 | 0.554 | 0.701 | 0.999 | v2 |
| FaceAcc | 2544 | 0.562 | 0.685 | 0.999 | v2 |
| Front | 2074 | 0.543 | 0.643 | 0.999 | v2 |
| Hair | 9322 | 0.688 | 0.805 | 1.000 | v2 |
| Hat | 6943 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5465 | 0.486 | 0.733 | 0.999 | v2 |
| LayerBawah | 3537 | 0.519 | 0.755 | 1.000 | v2 |
| Neck | 1776 | 0.583 | 0.708 | 0.999 | v2 |
| Pants | 4517 | 0.077 | 0.665 | 0.999 | v2 |
| Sepatu | 4661 | 0.614 | 0.708 | 1.000 | v2 |
| Shirt | 4502 | 0.282 | 0.723 | 1.000 | v2 |
| Shoulder | 928 | 0.593 | 0.696 | 1.000 | v2 |
| TShirt | 110 | 0.182 | 0.500 | 0.998 | v2 |
| Waist | 2236 | 0.593 | 0.687 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 17613 item | AUC {"asli": 0.59, "potongan": 0.618, "rata": 0.621} | label wanita/pria [676, 294] | dipakai: **rata**
- Pants: 17116 item | AUC {"asli": 0.666, "potongan": 0.673, "rata": 0.681} | label wanita/pria [1394, 251] | dipakai: **asli**
- TShirt: 3497 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [54, 17] | dipakai: **asli**

## Sepatu (bundle): 5673 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 1821, "baru": 310, "total": 5673}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
