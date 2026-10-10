# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-10T06:53:03.853809+00:00 | putaran ke-32
- Outfit nyata terkumpul: **45845** | masuk bank (lolos saring): **8000**
  (ditolak karena item inti tidak bisa dibeli: 21993, tidak koheren: 2158)
- Item dengan sidik jari visual: **40000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4450, "gaya_masuk": 1371, "gaya_gemini": 0, "meta": {"diminta": 4663, "diperbarui": 4591, "hilang": 72, "sisa_antre": 823}, "sepatu": {"cari": 30, "lihat": 2192, "baru": 417, "total": 4465}} | permintaan HTTP 5227, kena 429: 97, gagal 51

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.340 |
| CLIP netral-slot | 0.506 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.778 |
| Model MLP (dilatih) | 0.793 |

- Dipakai: **mlp** | soal uji 40000 | outfit latih 38984, uji 6845
- AUC koherensi (outfit asli vs setengah-diacak): model 0.808, CLIP 0.718
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 531 | item baru diminta pemain: 16
- Durasi putaran: **65.4 menit** | META: {"diminta": 4663, "diperbarui": 4591, "hilang": 72, "sisa_antre": 823}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.577** vs kemiripan gaya saja 0.414
- Masuk 5% teratas: model **0.690** vs 0.519 | 3272 soal | contoh latih 116492
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |
| 32 | 2026-10-10T06:53 | 45845 | 112870 | 0.793 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.852 pada 7244 item berlabel wanita & 2043 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1869 | 0.554 | 0.700 | 0.999 | v2 |
| FaceAcc | 2253 | 0.557 | 0.678 | 0.999 | v2 |
| Front | 1867 | 0.535 | 0.636 | 0.999 | v2 |
| Hair | 8000 | 0.695 | 0.806 | 1.000 | v2 |
| Hat | 6134 | 0.585 | 0.710 | 0.999 | v2 |
| LayerAtas | 5174 | 0.483 | 0.727 | 0.999 | v2 |
| LayerBawah | 3379 | 0.518 | 0.752 | 1.000 | v2 |
| Neck | 1572 | 0.576 | 0.707 | 0.999 | v2 |
| Pants | 3577 | 0.079 | 0.663 | 0.999 | v2 |
| Sepatu | 3712 | 0.603 | 0.707 | 1.000 | v2 |
| Shirt | 3539 | 0.279 | 0.723 | 1.000 | v2 |
| Shoulder | 805 | 0.584 | 0.687 | 1.000 | v2 |
| TShirt | 91 | 0.198 | 0.527 | 0.998 | v2 |
| Waist | 2028 | 0.597 | 0.685 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 13912 item | AUC {"asli": 0.59, "potongan": 0.605, "rata": 0.611} | label wanita/pria [561, 225] | dipakai: **rata**
- Pants: 13621 item | AUC {"asli": 0.673, "potongan": 0.686, "rata": 0.692} | label wanita/pria [1138, 182] | dipakai: **asli**
- TShirt: 2808 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [47, 13] | dipakai: **asli**

## Sepatu (bundle): 4465 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2192, "baru": 417, "total": 4465}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
