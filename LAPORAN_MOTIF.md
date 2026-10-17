# Laporan motif diukur (rev 33b)

Motif dibaca dari PIKSEL thumbnail resmi (motif.py: periodisitas/autokorelasi 2D, kisi, tepi, warna, sebaran).
Model: hutan keputusan per grup, dilatih dari item yang namanya menunjuk tepat satu motif; NAMA TIDAK masuk fitur.
Klaim hanya bila peluang >= 0.5; di bawahnya = tidak pasti (tidak dipakai generator).
Catatan: label nama sendiri bisa salah ("striped" padahal kotak), jadi presisi di bawah = batas bawah.

## baju (uji silang, 1082 item bernama-motif)

| ambang | garis | grafis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|---|
| 0.5 | 110/122 = 90% (recall 55%) | 59/84 = 70% (recall 37%) | 101/110 = 92% (recall 50%) | 126/148 = 85% (recall 61%) | 81/90 = 90% (recall 40%) | 32/32 = 100% (recall 28%) |
| 0.6 | 92/101 = 91% (recall 46%) | 35/49 = 71% (recall 22%) | 68/70 = 97% (recall 34%) | 110/126 = 87% (recall 53%) | 60/67 = 90% (recall 30%) | 20/20 = 100% (recall 17%) |

Sebaran pada 336 item ACAK (nama tanpa kata motif): ? 215, grafis 61, polos 29, ramai 20, kotak 6, garis 4, taburan 1

## celana (uji silang, 902 item bernama-motif)

| ambang | garis | grafis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|---|
| 0.5 | 43/49 = 88% (recall 30%) | 5/5 = 100% (recall 9%) | 75/82 = 91% (recall 37%) | 77/105 = 73% (recall 37%) | 72/88 = 82% (recall 36%) | 13/15 = 87% (recall 14%) |
| 0.6 | 38/43 = 88% (recall 27%) | 3/3 = 100% (recall 5%) | 57/59 = 97% (recall 28%) | 56/69 = 81% (recall 27%) | 53/56 = 95% (recall 26%) | 4/4 = 100% (recall 4%) |

Sebaran pada 326 item ACAK (nama tanpa kata motif): ? 259, polos 48, ramai 9, garis 6, kotak 4

## 3D (uji silang, 803 item bernama-motif)

| ambang | garis | grafis | kotak | polos | ramai | taburan |
|---|---|---|---|---|---|---|
| 0.5 | 33/35 = 94% (recall 28%) | 21/28 = 75% (recall 18%) | 63/83 = 76% (recall 30%) | 55/70 = 79% (recall 43%) | 35/48 = 73% (recall 22%) | 31/34 = 91% (recall 40%) |
| 0.6 | 26/26 = 100% (recall 22%) | 9/11 = 82% (recall 8%) | 28/32 = 88% (recall 14%) | 42/55 = 76% (recall 33%) | 17/22 = 77% (recall 11%) | 25/27 = 93% (recall 32%) |

Sebaran pada 269 item ACAK (nama tanpa kata motif): ? 203, polos 29, grafis 16, kotak 10, ramai 9, taburan 2

## Label emas (dinilai mata)

| t | id | emas | ukur |
|---|---|---|---|
| 11 | 131428808519634 | polos | tidak pasti (0.22) |
| 11 | 102620614467965 | bunga | ramai 0.63 |
| 11 | 140592934157389 | bunga | ramai 0.64 |
| 11 | 18853286606 | tulisan | grafis 0.6 |
| 11 | 112383779040486 | garis | garis 0.84 |
| 11 | 12251127003 | grafis | grafis 0.66 |
| 11 | 7902161752 | grafis | tidak pasti (0.42) |
| 11 | 134571956901672 | polos | tidak pasti (0.32) |
| 11 | 15006636423 | tulisan | grafis 0.69 |
| 11 | 135814612176227 | grafis | tidak pasti (0.42) |
| 11 | 17152218636 | polos | polos 0.54 |
| 11 | 11943285508 | polos | tidak pasti (0.33) |
| 11 | 6355262138 | polos | tidak pasti (0.29) |
| 11 | 266394252 | polos | grafis 0.53 X |
| 11 | 87650326274539 | polos | tidak pasti (0.4) |
| 11 | 102497906320713 | grafis | tidak pasti (0.45) |
| 11 | 88107382628292 | tulisan | ramai 0.59 |
| 11 | 118300888078991 | grafis | tidak pasti (0.34) |
| 11 | 9422776837 | polos | ramai 0.67 X |
| 11 | 108634431372050 | polos | tidak pasti (0.5) |
| 11 | 84662977057675 | polos | tidak pasti (0.31) |
| 11 | 6329241946 | garis | tidak pasti (0.48) |
| 11 | 15043745378 | garis | tidak pasti (0.38) |
| 11 | 4959177259 | polos | polos 0.97 |
| 11 | 120672004317925 | tulisan | tidak pasti (0.42) |
| 11 | 14663131904 | grafis | tidak pasti (0.24) |
| 11 | 129927595068672 | grafis | grafis 0.76 |
| 11 | 74922696118418 | grafis | grafis 0.52 |
| 11 | 11154702948 | grafis | grafis 0.65 |
| 11 | 10554943000 | grafis | grafis 0.57 |
| 11 | 16114397838 | tulisan | tidak pasti (0.42) |
| 11 | 132896774016721 | grafis | tidak pasti (0.36) |
| 11 | 138195987165359 | tulisan | tidak pasti (0.45) |
| 11 | 11233366673 | polos | tidak pasti (0.35) |
| 11 | 7584705601 | polos | tidak pasti (0.42) |
| 11 | 100461181770066 | polos | tidak pasti (0.34) |
| 11 | 113040431224906 | polos | tidak pasti (0.44) |
| 11 | 120433639811400 | grafis | tidak pasti (0.36) |
| 11 | 6864789360 | grafis | grafis 0.72 |
| 11 | 18222833667 | garis | tidak pasti (0.48) |
| 11 | 10523448233 | polos | tidak pasti (0.29) |
| 11 | 9525867465 | grafis | tidak pasti (0.5) |
| 11 | 11666573467 | polos | polos 0.89 |
| 11 | 72364046238793 | polos | tidak pasti (0.4) |
| 11 | 83200538257393 | kotak | kotak 0.54 |
| 11 | 8733059577 | tulisan | grafis 0.56 |
| 11 | 118001467186665 | grafis | tidak pasti (0.46) |
| 11 | 84291603963538 | kotak | tidak pasti (0.43) |
| 11 | 6143702745 | polos | polos 0.77 |
| 11 | 6473942024 | grafis | grafis 0.75 |
| 11 | 77790987837771 | grafis | grafis 0.72 |
| 11 | 7459996479 | polos | polos 0.96 |
| 11 | 85269518213785 | tulisan | tidak pasti (0.24) |
| 11 | 6400454693 | polos | tidak pasti (0.31) |
| 12 | 6412383226 | polos | tidak pasti (0.32) |
| 12 | 9765643560 | polos | tidak pasti (0.41) |
| 12 | 102697843287286 | grafis | tidak pasti (0.28) |
| 12 | 133037400812964 | bunga | tidak pasti (0.34) |
| 12 | 8838650406 | grafis | tidak pasti (0.33) |
| 12 | 12787336716 | polos | ramai 0.53 X |
| 12 | 72449581501449 | polos | tidak pasti (0.33) |
| 12 | 15876489908 | loreng | ramai 0.83 |
| 12 | 74480228427266 | polos | garis 0.55 X |
| 12 | 76560904237091 | denim | tidak pasti (0.41) |
| 12 | 112931572454830 | denim | tidak pasti (0.41) |
| 12 | 6354131610 | grafis | tidak pasti (0.43) |
| 12 | 9581148637 | polos | tidak pasti (0.38) |
| 12 | 134349364704274 | denim | tidak pasti (0.46) |
| 12 | 113187526373432 | grafis | tidak pasti (0.36) |
| 12 | 115791573774105 | denim | tidak pasti (0.28) |
| 12 | 6369440433 | denim | kotak 0.52 X |
| 12 | 98540796262697 | garis | tidak pasti (0.41) |
| 12 | 110399493168289 | polos | tidak pasti (0.28) |
| 12 | 72417705441468 | polos | garis 0.51 X |
| 12 | 106062802480568 | polkadot | taburan 0.65 |
| 12 | 7013246407 | denim | tidak pasti (0.38) |
| 12 | 124132113820522 | garis | tidak pasti (0.26) |
| 12 | 101253385873611 | grafis | tidak pasti (0.29) |
| 12 | 101441680900737 | loreng | tidak pasti (0.39) |
| 12 | 140064051564958 | polos | tidak pasti (0.29) |
| 12 | 73178377741857 | polos | tidak pasti (0.27) |
| 12 | 13495962985 | kulit | polos 0.52 |
| 12 | 15671548105 | motif_hewan | ramai 0.99 |
| 12 | 13924577828 | denim | tidak pasti (0.48) |
| 12 | 132833761 | polos | polos 0.61 |
| 12 | 4445410180 | polos | tidak pasti (0.44) |
| 12 | 6320365265 | polos | tidak pasti (0.46) |
| 12 | 14263285175 | polos | tidak pasti (0.34) |
| 12 | 139589769351705 | denim | tidak pasti (0.36) |
| 12 | 15466785041 | polos | polos 0.68 |
| 12 | 5649424359 | garis | tidak pasti (0.3) |
| 12 | 12758081223 | polos | polos 0.53 |
| 12 | 110993876103378 | polos | tidak pasti (0.32) |
| 12 | 125419048024037 | kotak | kotak 0.67 |
| 12 | 6927971309 | polos | polos 0.61 |
| 12 | 8068287334 | denim | tidak pasti (0.25) |
| 12 | 2574521581 | polos | tidak pasti (0.28) |
| 12 | 12727573197 | grafis | tidak pasti (0.2) |

**Emas: 30/36 cocok saat diklaim (62 tidak pasti)**

