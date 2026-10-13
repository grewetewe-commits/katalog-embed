# Laporan OTAK Katalog Praktis

- Dibuat: 2026-10-13T01:41:32.253584+00:00 | putaran ke-43
- Outfit nyata terkumpul: **58986** | masuk bank (lolos saring): **7982**
  (ditolak karena item inti tidak bisa dibeli: 29166, tidak koheren: 2685)
- Item dengan sidik jari visual: **60000**
- Panen putaran ini: {"kreator": 0, "outfit_baru": 0, "ditolak": 0, "kembar": 0, "tanpa_outfit": 0, "gaya_dibaca": 3243, "gaya_masuk": 973, "gaya_gemini": 0, "meta": {"diminta": 4342, "diperbarui": 4172, "hilang": 70, "sisa_antre": 662}, "sepatu": {"cari": 30, "lihat": 2330, "baru": 2, "total": 4858}} | permintaan HTTP 3974, kena 429: 89, gagal 56

## Model kecocokan (FITB: tebak item asli di antara 4 kandidat satu slot, pada outfit yang TIDAK dilatih)

| Metode | Akurasi | Data |
|---|---|---|
| Acak | 0.250 | Teoritis |
| CLIP mentah | 0.339 | Uji akhir |
| CLIP netral-slot | 0.499 | Uji akhir |
| CLIP PCA-32 (tanpa belajar) | 0.491 | Pemilihan |
| Model linear (dilatih) | 0.788 | Pemilihan |
| Model MLP (dilatih) | 0.807 | Pemilihan |
| Model terpilih | 0.809 | Uji akhir |

- Dipakai: **mlp** | soal uji 51179 | outfit latih 41288, pemilihan 8862, uji 8793
- Evaluasi v2: kreator latih, pemilihan, dan uji akhir terpisah; skor seri tidak dihitung benar. Rata-rata slot dan PCA memakai item latih saja.
- AUC koherensi (outfit asli vs setengah-diacak): model 0.811, CLIP 0.717
- **LAYAK DIPAKAI SERVER: YA** (syarat: FITB >= 0,38 dengan >= 150 soal; acak = 0,25)

- Sinyal pemain (outfit difavoritkan/dibeli di map): **26** | outfit dasar dari server Roblox: 534 | item baru diminta pemain: 41
- Durasi putaran: **64.8 menit** | META: {"diminta": 4342, "diperbarui": 4172, "hilang": 70, "sisa_antre": 662}

## Belajar PROSES desain (dipakai server Roblox untuk menyusun outfit dari nol di sekitar item pilihan pemain)

- Uji jujur di outfit yang TIDAK dipelajari: item asli pilihan desainer masuk **1% teratas** dari semua item slotnya: model **0.587** vs kemiripan gaya saja 0.404
- Masuk 5% teratas: model **0.698** vs 0.523 | 3083 soal | contoh latih 115726
- Yang dipelajari: bobot 16 fitur per slot (gaya visual, harmoni warna, set/kreator sama, tren, popularitas di kalangan desainer, kecocokan dengan bumbu yang sudah dipasang), tabel harmoni warna 16x16, resep slot, jumlah aksesori, pasangan 2D/3D

## Perkembangan otak (makin banyak data = makin pintar)

| Putaran | Waktu (UTC) | Outfit dipelajari | Item dikenal | FITB | Sinyal pemain |
|---|---|---|---|---|---|
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
| 43 | 2026-10-13T01:41 | 58986 | 125362 | 0.809 | 26 |

## Gender visual (zero-shot CLIP) dicek dengan kata di nama item
- AUC = 0.849 pada 7832 item berlabel wanita & 2318 pria
  (0,5 = acak; >= 0,80 baru dipakai keras oleh server)

## Mata warna v2 (rev 24): cocok dengan warna yang disebut nama item

| Slot | Item berlabel | v1 | v2 | Cakupan v2 | Dipakai |
|---|---|---|---|---|---|
| Back | 1961 | 0.553 | 0.700 | 0.999 | v2 |
| FaceAcc | 2443 | 0.562 | 0.682 | 0.999 | v2 |
| Front | 2003 | 0.539 | 0.641 | 0.999 | v2 |
| Hair | 8978 | 0.691 | 0.805 | 1.000 | v2 |
| Hat | 6722 | 0.584 | 0.708 | 0.999 | v2 |
| LayerAtas | 5394 | 0.485 | 0.733 | 0.999 | v2 |
| LayerBawah | 3498 | 0.519 | 0.754 | 1.000 | v2 |
| Neck | 1718 | 0.579 | 0.707 | 0.999 | v2 |
| Pants | 4235 | 0.078 | 0.663 | 0.999 | v2 |
| Sepatu | 4059 | 0.613 | 0.707 | 1.000 | v2 |
| Shirt | 4228 | 0.281 | 0.722 | 1.000 | v2 |
| Shoulder | 902 | 0.591 | 0.693 | 1.000 | v2 |
| TShirt | 100 | 0.190 | 0.520 | 0.998 | v2 |
| Waist | 2182 | 0.593 | 0.686 | 1.000 | v2 |

- v2 dipakai per slot hanya bila >= 30 item berlabel & unggul >= 3 poin. Cakupan = porsi item slot yang sudah diukur ulang.

## Gender baju 2D (CLIP pada potongan pakaian tanpa manekin)

- Shirt: 16550 item | AUC {"asli": 0.591, "potongan": 0.613, "rata": 0.616} | label wanita/pria [644, 269] | dipakai: **rata**
- Pants: 16123 item | AUC {"asli": 0.67, "potongan": 0.677, "rata": 0.684} | label wanita/pria [1320, 225] | dipakai: **asli**
- TShirt: 3311 item | AUC {"asli": null, "potongan": null, "rata": null} | label wanita/pria [53, 15] | dipakai: **asli**

## Sepatu (bundle): 4858 bundle di meta/sepatu.json | putaran ini: {"cari": 30, "lihat": 2330, "baru": 2, "total": 4858}

_Catatan jujur: angka ini mengukur apakah model menangkap pola outfit buatan manusia. Enak-tidaknya hasil di mata pemain tetap diuji lewat penilaian pemilik._
