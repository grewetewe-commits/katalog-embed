# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-12T16:20:34.167950+00:00 | putaran ke-42
- Outfit nyata terkumpul: **57841** | masuk bank (lolos saring): **7982**
  (ditolak karena item inti tidak bisa dibeli: 28601, tidak koheren: 2666)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3900, "gaya_masuk": 1243, "gaya_gemini": 0, "meta": {"diminta": 3704, "diperbarui": 3546, "hilang": 58, "sisa_antre": 881}, "sepatu": {"cari": 30, "lihat": 2829, "baru": 15, "total": 4856}} | permintaan HTTP 4655, kena 429: 77, gagal 52

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.339 | Uji akhir |
| CLIP netral-slot | 0.498 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.488 | Pemilihan |
| Model linear (dilatih) | 0.786 | Pemilihan |
| Model MLP (dilatih) | 0.807 | Pemilihan |
| Model terpilih | 0.805 | Uji akhir |

- Dipakai: **mlp** | soal uji 50390 | outfit latih 40449, pemilihan 8695, uji 8658
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.804, CLIP 0.718
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 39
- Durasi putaran: **63.8 menit** | META: {"diminta": 3704, "diperbarui": 3546, "hilang": 58, "sisa_antre": 881}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.588** vs kemiripan gaya saja 0.425
- Masuk 5% teratas: model **0.697** vs 0.536 | 3173 soal | contoh latih 115920
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
| 31 | 2026-10-09T23:52 | 44474 | 111350 | 0.792 | 25 |
| 32 | 2026-10-10T06:53 | 45845 | 112870 | 0.793 | 25 |
| 33 | 2026-10-10T10:03 | 47092 | 114091 | 0.803 | 25 |
| 34 | 2026-10-10T13:30 | 48116 | 114932 | 0.803 | 25 |
| 35 | 2026-10-10T22:43 | 49352 | 116226 | 0.802 | 25 |
| 36 | 2026-10-11T02:37 | 50426 | 117219 | 0.8 | 25 |
| 37 | 2026-10-11T06:39 | 51714 | 118451 | 0.803 | 26 |
| 38 | 2026-10-11T13:46 | 53042 | 119578 | 0.806 | 26 |
| 39 | 2026-10-11T17:32 | 54490 | 120753 | 0.802 | 26 |
| 40 | 2026-10-11T23:00 | 55562 | 121756 | 0.803 | 26 |
| 41 | 2026-10-12T06:57 | 56598 | 122754 | 0.805 | 26 |
| 42 | 2026-10-12T16:20 | 57841 | 123952 | 0.805 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7732 item berlabel wanita & 2279 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1945 | 0.552 | 0.699 | 0.999 | v2 |
| FaceAcc | 2416 | 0.562 | 0.682 | 0.999 | v2 |
| Front | 1983 | 0.538 | 0.640 | 0.999 | v2 |
| Hair | 8855 | 0.691 | 0.805 | 1.000 | v2 |
| Hat | 6645 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5352 | 0.484 | 0.731 | 0.999 | v2 |
| LayerBawah | 3478 | 0.519 | 0.752 | 1.000 | v2 |
| Neck | 1697 | 0.578 | 0.705 | 0.999 | v2 |
| Pants | 4164 | 0.077 | 0.662 | 0.999 | v2 |
| Sepatu | 4042 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 4147 | 0.281 | 0.721 | 1.000 | v2 |
| Shoulder | 891 | 0.587 | 0.690 | 1.000 | v2 |
| TShirt | 100 | 0.190 | 0.520 | 0.998 | v2 |
| Waist | 2155 | 0.593 | 0.686 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 16277 item | AUC {"asli": 0.589, "potongan": 0.612, "rata": 0.616} | label wanita/pria [631, 267] | dipakai: **rata**
- Pants: 15833 item | AUC {"asli": 0.673, "potongan": 0.677, "rata": 0.686} | label wanita/pria [1296, 218] | dipakai: **asli**
- TShirt: 3268 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 15] | dipakai: **asli**

## Sepatu (bundle): 4856 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2829, "baru": 15, "total": 4856}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
