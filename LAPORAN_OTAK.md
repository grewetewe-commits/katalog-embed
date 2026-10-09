# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-09T23:52:31.336125+00:00 | putaran ke-31
- Outfit nyata terkumpul: **44474** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 21233, tidak koheren: 2120)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4237, "gaya_masuk": 1294, "gaya_gemini": 0, "meta": {"diminta": 4556, "diperbarui": 4392, "hilang": 64, "sisa_antre": 953}, "sepatu": {"cari": 29, "lihat": 2472, "baru": 1816, "total": 4048}} | permintaan HTTP 5901, kena 429: 97, gagal 54

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.342 |
| CLIP netral-slot | 0.501 |
| CLIP PCA-32 (tanpa belajar) | 0.485 |
| Model linear (dilatih) | 0.775 |
| Model MLP (dilatih) | 0.792 |

- Dipakai: **mlp** | soal uji 38915 | outfit latih 37806, uji 6652
- AUC koherensi (outfit asli vs setengah-diacak): model 0.809, CLIP 0.715
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 531 | item baru diminta pemain: 16
- Durasi putaran: **76.5 menit** | META: {"diminta": 4556, "diperbarui": 4392, "hilang": 64, "sisa_antre": 953}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.577** vs kemiripan gaya saja 0.420
- Masuk 5% teratas: model **0.693** vs 0.523 | 3198 soal | contoh latih 116386
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.845 pada 7175 item berlabel wanita & 2014 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1858 | 0.553 | 0.700 | 0.999 | v2 |
| FaceAcc | 2232 | 0.558 | 0.678 | 0.999 | v2 |
| Front | 1848 | 0.533 | 0.634 | 0.999 | v2 |
| Hair | 7890 | 0.695 | 0.806 | 1.000 | v2 |
| Hat | 6070 | 0.585 | 0.709 | 0.999 | v2 |
| LayerAtas | 5153 | 0.483 | 0.728 | 0.999 | v2 |
| LayerBawah | 3368 | 0.517 | 0.752 | 1.000 | v2 |
| Neck | 1553 | 0.580 | 0.710 | 0.999 | v2 |
| Pants | 3516 | 0.079 | 0.663 | 0.998 | v2 |
| Sepatu | 3436 | 0.605 | 0.706 | 1.000 | v2 |
| Shirt | 3474 | 0.279 | 0.723 | 1.000 | v2 |
| Shoulder | 791 | 0.584 | 0.684 | 1.000 | v2 |
| TShirt | 87 | 0.207 | 0.540 | 0.997 | v2 |
| Waist | 2018 | 0.596 | 0.685 | 0.999 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 13683 item | AUC {"asli": 0.592, "potongan": 0.605, "rata": 0.612} | label wanita/pria [554, 220] | dipakai: **asli**
- Pants: 13413 item | AUC {"asli": 0.68, "potongan": 0.691, "rata": 0.698} | label wanita/pria [1122, 177] | dipakai: **asli**
- TShirt: 2750 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [47, 13] | dipakai: **asli**

## Sepatu (bundle): 4048 bundle di meta/sepatu.json | putaran ini: {"cari": 29, "lihat": 2472, "baru": 1816, "total": 4048}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
