# Laporan motif diukur (rev 33b)

Motif dibaca dari PIKSEL thumbnail resmi (motif.py: periodisitas/autokorelasi 2D, kisi, tepi, warna, sebaran).
Model: hutan keputusan per grup, dilatih dari item yang namanya menunjuk tepat satu motif; NAMA TIDAK masuk fitur.
Klaim hanya bila peluang >= 0.5; di bawahnya = tidak pasti (tidak dipakai generator).
Catatan: label nama sendiri bisa salah ("striped" padahal kotak), jadi presisi di bawah = batas bawah.

## baju (uji silang, 919 item bernama-motif)

| ambang | garis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|
| 0.5 | 116/126 = 92% (recall 58%) | 108/119 = 91% (recall 54%) | 131/155 = 85% (recall 65%) | 100/115 = 87% (recall 50%) | 35/36 = 97% (recall 30%) |
| 0.6 | 105/113 = 93% (recall 52%) | 75/76 = 99% (recall 38%) | 109/123 = 89% (recall 54%) | 79/87 = 91% (recall 39%) | 28/28 = 100% (recall 24%) |

Sebaran pada 342 item ACAK (nama tanpa kata motif): ? 231, ramai 52, polos 49, garis 4, kotak 4, grafis 2

## celana (uji silang, 846 item bernama-motif)

| ambang | garis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|
| 0.5 | 43/51 = 84% (recall 30%) | 81/94 = 86% (recall 40%) | 105/140 = 75% (recall 50%) | 83/109 = 76% (recall 42%) | 16/18 = 89% (recall 17%) |
| 0.6 | 33/38 = 87% (recall 23%) | 60/67 = 90% (recall 30%) | 80/98 = 82% (recall 38%) | 56/64 = 88% (recall 28%) | 8/8 = 100% (recall 9%) |

Sebaran pada 337 item ACAK (nama tanpa kata motif): ? 238, polos 61, ramai 30, kotak 4, garis 4

## 3D (uji silang, 683 item bernama-motif)

| ambang | garis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|
| 0.5 | 30/33 = 91% (recall 26%) | 97/121 = 80% (recall 47%) | 65/84 = 77% (recall 52%) | 64/86 = 74% (recall 41%) | 32/39 = 82% (recall 41%) |
| 0.6 | 15/17 = 88% (recall 13%) | 61/72 = 85% (recall 29%) | 45/56 = 80% (recall 36%) | 41/54 = 76% (recall 26%) | 24/29 = 83% (recall 31%) |

Sebaran pada 266 item ACAK (nama tanpa kata motif): ? 167, ramai 36, polos 30, kotak 25, taburan 6, garis 2

## Label emas (dinilai mata)

| t | id | emas | ukur |
|---|---|---|---|
| 11 | 131428808519634 | polos | tidak pasti (0.28) |
| 11 | 102620614467965 | bunga | ramai 0.74 |
| 11 | 140592934157389 | bunga | ramai 0.59 |
| 11 | 18853286606 | tulisan | tidak pasti (0.36) |
| 11 | 112383779040486 | garis | garis 0.87 |
| 11 | 12251127003 | grafis | tidak pasti (0.49) |
| 11 | 7902161752 | grafis | tidak pasti (0.5) |
| 11 | 134571956901672 | polos | tidak pasti (0.48) |
| 11 | 15006636423 | tulisan | tidak pasti (0.3) |
| 11 | 135814612176227 | grafis | tidak pasti (0.44) |
| 11 | 17152218636 | polos | tidak pasti (0.33) |
| 11 | 11943285508 | polos | tidak pasti (0.43) |
| 11 | 6355262138 | polos | tidak pasti (0.32) |
| 11 | 266394252 | polos | tidak pasti (0.45) |
| 11 | 87650326274539 | polos | tidak pasti (0.49) |
| 11 | 102497906320713 | grafis | tidak pasti (0.37) |
| 11 | 88107382628292 | tulisan | ramai 0.59 |
| 11 | 118300888078991 | grafis | tidak pasti (0.44) |
| 11 | 9422776837 | polos | ramai 0.78 X |
| 11 | 108634431372050 | polos | tidak pasti (0.34) |
| 11 | 84662977057675 | polos | polos 0.58 |
| 11 | 6329241946 | garis | tidak pasti (0.47) |
| 11 | 15043745378 | garis | tidak pasti (0.3) |
| 11 | 4959177259 | polos | polos 0.98 |
| 11 | 120672004317925 | tulisan | tidak pasti (0.31) |
| 11 | 14663131904 | grafis | tidak pasti (0.35) |
| 11 | 129927595068672 | grafis | tidak pasti (0.35) |
| 11 | 74922696118418 | grafis | tidak pasti (0.38) |
| 11 | 11154702948 | grafis | tidak pasti (0.4) |
| 11 | 10554943000 | grafis | tidak pasti (0.47) |
| 11 | 16114397838 | tulisan | tidak pasti (0.36) |
| 11 | 132896774016721 | grafis | tidak pasti (0.4) |
| 11 | 138195987165359 | tulisan | tidak pasti (0.24) |
| 11 | 11233366673 | polos | tidak pasti (0.45) |
| 11 | 7584705601 | polos | tidak pasti (0.38) |
| 11 | 100461181770066 | polos | tidak pasti (0.34) |
| 11 | 113040431224906 | polos | tidak pasti (0.5) |
| 11 | 120433639811400 | grafis | ramai 0.54 |
| 11 | 6864789360 | grafis | tidak pasti (0.3) |
| 11 | 18222833667 | garis | ramai 0.63 X |
| 11 | 10523448233 | polos | tidak pasti (0.33) |
| 11 | 9525867465 | grafis | ramai 0.64 |
| 11 | 11666573467 | polos | polos 0.9 |
| 11 | 72364046238793 | polos | tidak pasti (0.28) |
| 11 | 83200538257393 | kotak | kotak 0.61 |
| 11 | 8733059577 | tulisan | tidak pasti (0.25) |
| 11 | 118001467186665 | grafis | tidak pasti (0.25) |
| 11 | 84291603963538 | kotak | tidak pasti (0.39) |
| 11 | 6143702745 | polos | polos 0.8 |
| 11 | 6473942024 | grafis | tidak pasti (0.36) |
| 11 | 77790987837771 | grafis | tidak pasti (0.36) |
| 11 | 7459996479 | polos | polos 0.97 |
| 11 | 85269518213785 | tulisan | tidak pasti (0.28) |
| 11 | 6400454693 | polos | polos 0.65 |
| 12 | 6412383226 | polos | tidak pasti (0.41) |
| 12 | 9765643560 | polos | tidak pasti (0.41) |
| 12 | 102697843287286 | grafis | tidak pasti (0.34) |
| 12 | 133037400812964 | bunga | tidak pasti (0.4) |
| 12 | 8838650406 | grafis | tidak pasti (0.46) |
| 12 | 12787336716 | polos | ramai 0.6 X |
| 12 | 72449581501449 | polos | tidak pasti (0.32) |
| 12 | 15876489908 | loreng | ramai 0.91 |
| 12 | 74480228427266 | polos | garis 0.59 X |
| 12 | 76560904237091 | denim | tidak pasti (0.37) |
| 12 | 112931572454830 | denim | tidak pasti (0.35) |
| 12 | 6354131610 | grafis | kotak 0.5 X |
| 12 | 9581148637 | polos | tidak pasti (0.4) |
| 12 | 134349364704274 | denim | tidak pasti (0.47) |
| 12 | 113187526373432 | grafis | tidak pasti (0.38) |
| 12 | 115791573774105 | denim | tidak pasti (0.37) |
| 12 | 6369440433 | denim | kotak 0.51 X |
| 12 | 98540796262697 | garis | tidak pasti (0.4) |
| 12 | 110399493168289 | polos | tidak pasti (0.38) |
| 12 | 72417705441468 | polos | tidak pasti (0.48) |
| 12 | 106062802480568 | polkadot | taburan 0.66 |
| 12 | 7013246407 | denim | tidak pasti (0.38) |
| 12 | 124132113820522 | garis | tidak pasti (0.26) |
| 12 | 101253385873611 | grafis | tidak pasti (0.34) |
| 12 | 101441680900737 | loreng | ramai 0.54 |
| 12 | 140064051564958 | polos | tidak pasti (0.39) |
| 12 | 73178377741857 | polos | tidak pasti (0.28) |
| 12 | 13495962985 | kulit | polos 0.53 |
| 12 | 15671548105 | motif_hewan | ramai 0.96 |
| 12 | 13924577828 | denim | polos 0.59 |
| 12 | 132833761 | polos | polos 0.58 |
| 12 | 4445410180 | polos | tidak pasti (0.49) |
| 12 | 6320365265 | polos | polos 0.62 |
| 12 | 14263285175 | polos | tidak pasti (0.35) |
| 12 | 139589769351705 | denim | tidak pasti (0.35) |
| 12 | 15466785041 | polos | polos 0.74 |
| 12 | 5649424359 | garis | tidak pasti (0.35) |
| 12 | 12758081223 | polos | polos 0.74 |
| 12 | 110993876103378 | polos | tidak pasti (0.41) |
| 12 | 125419048024037 | kotak | kotak 0.76 |
| 12 | 6927971309 | polos | polos 0.66 |
| 12 | 8068287334 | denim | polos 0.63 |
| 12 | 2574521581 | polos | tidak pasti (0.43) |
| 12 | 12727573197 | grafis | tidak pasti (0.24) |

**Emas: 26/32 cocok saat diklaim (66 tidak pasti)**

