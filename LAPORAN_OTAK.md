# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-10T10:03:10.619564+00:00 | putaran ke-33
- Outfit nyata terkumpul: **47092** | masuk bank (lolos saring): **7978**
  (ditolak karena item inti tidak bisa dibeli: 22664, tidak koheren: 2222)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 4200, "gaya_masuk": 1247, "gaya_gemini": 0, "meta": {"diminta": 4732, "diperbarui": 4573, "hilang": 59, "sisa_antre": 865}, "sepatu": {"cari": 30, "lihat": 2957, "baru": 263, "total": 4728}} | permintaan HTTP 5031, kena 429: 97, gagal 59

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi |
|---|---|
| Acak | 0.250 |
| CLIP mentah | 0.340 |
| CLIP netral-slot | 0.506 |
| CLIP PCA-32 (tanpa belajar) | 0.489 |
| Model linear (dilatih) | 0.783 |
| Model MLP (dilatih) | 0.803 |

- Dipakai: **mlp** | soal uji 41046 | outfit latih 40046, uji 7028
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.720
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **25** | outfit dasar dari server Roblox: 531 | item baru diminta pemain: 16
- Durasi putaran: **56.7 menit** | META: {"diminta": 4732, "diperbarui": 4573, "hilang": 59, "sisa_antre": 865}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.548** vs kemiripan gaya saja 0.394
- Masuk 5% teratas: model **0.678** vs 0.514 | 3196 soal | contoh latih 116586
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 30 | 2026-10-09T21:17 | 43179 | 108353 | 0.794 | 25 |
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |
| 32 | 2026-10-10T06:53 | 45845 | 112870 | 0.793 | 25 |
| 33 | 2026-10-10T10:03 | 47092 | 114091 | 0.803 | 25 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.852 pada 7297 item berlabel wanita & 2060 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1874 | 0.554 | 0.701 | 0.999 | v2 |
| FaceAcc | 2262 | 0.557 | 0.677 | 0.999 | v2 |
| Front | 1874 | 0.535 | 0.636 | 0.999 | v2 |
| Hair | 8079 | 0.694 | 0.806 | 1.000 | v2 |
| Hat | 6183 | 0.585 | 0.710 | 0.999 | v2 |
| LayerAtas | 5192 | 0.482 | 0.728 | 0.999 | v2 |
| LayerBawah | 3386 | 0.518 | 0.752 | 1.000 | v2 |
| Neck | 1586 | 0.579 | 0.708 | 0.999 | v2 |
| Pants | 3629 | 0.079 | 0.662 | 0.999 | v2 |
| Sepatu | 3905 | 0.615 | 0.708 | 1.000 | v2 |
| Shirt | 3595 | 0.280 | 0.723 | 1.000 | v2 |
| Shoulder | 814 | 0.581 | 0.686 | 1.000 | v2 |
| TShirt | 92 | 0.196 | 0.533 | 0.998 | v2 |
| Waist | 2039 | 0.596 | 0.687 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 14143 item | AUC {"asli": 0.591, "potongan": 0.608, "rata": 0.614} | label wanita/pria [569, 227] | dipakai: **rata**
- Pants: 13829 item | AUC {"asli": 0.673, "potongan": 0.686, "rata": 0.692} | label wanita/pria [1154, 183] | dipakai: **asli**
- TShirt: 2856 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [49, 13] | dipakai: **asli**

## Sepatu (bundle): 4728 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2957, "baru": 263, "total": 4728}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
