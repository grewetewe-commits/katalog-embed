# Laporan motif diukur (rev 33)

Label dari PIKSEL thumbnail (motif.py), dibandingkan dengan kata di NAMA item (bukan kebenaran mutlak: nama bisa
menyebut motif yang hanya kecil, atau bohong). Baris = kelas menurut nama, kolom = hasil ukur.

## 2D baju

| nama \ ukur | polos | blok | garis | kotak | taburan | ramai | grafis | lemah | - | n | cocok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| polos | 85 | 4 | 2 | 0 | 0 | 10 | 11 | 9 | 1 | 122 | 75% |
| garis | 25 | 4 | 43 | 4 | 2 | 24 | 11 | 8 | 0 | 121 | 38% |
| kotak | 41 | 13 | 4 | 2 | 8 | 35 | 7 | 10 | 0 | 120 | 2% |
| taburan | 16 | 2 | 0 | 0 | 21 | 56 | 14 | 6 | 0 | 115 | 19% |
| ramai | 24 | 3 | 0 | 0 | 12 | 64 | 14 | 5 | 0 | 122 | 65% |
| - | 38 | 5 | 4 | 2 | 5 | 55 | 69 | 20 | 0 | 198 |  |

- presisi `polos` (vs nama): 85/191 = 45%
- presisi `garis` (vs nama): 43/49 = 88%
- presisi `kotak` (vs nama): 2/6 = 33%
- presisi `taburan` (vs nama): 21/43 = 49%

## 2D celana

| nama \ ukur | polos | blok | garis | kotak | taburan | ramai | grafis | lemah | - | n | cocok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| polos | 58 | 19 | 0 | 2 | 2 | 29 | 0 | 13 | 1 | 124 | 52% |
| garis | 21 | 10 | 3 | 25 | 3 | 52 | 0 | 6 | 0 | 120 | 3% |
| kotak | 21 | 14 | 0 | 1 | 11 | 70 | 0 | 5 | 0 | 122 | 1% |
| taburan | 4 | 7 | 0 | 3 | 21 | 55 | 0 | 3 | 0 | 93 | 23% |
| ramai | 13 | 10 | 0 | 0 | 10 | 79 | 1 | 7 | 0 | 120 | 79% |
| - | 42 | 16 | 0 | 3 | 11 | 95 | 1 | 29 | 2 | 199 |  |

- presisi `polos` (vs nama): 58/117 = 50%
- presisi `garis` (vs nama): 3/3 = 100%
- presisi `kotak` (vs nama): 1/31 = 3%
- presisi `taburan` (vs nama): 21/47 = 45%

## 3D atas

| nama \ ukur | polos | blok | garis | kotak | taburan | ramai | grafis | lemah | - | n | cocok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| polos | 53 | 1 | 0 | 0 | 0 | 4 | 0 | 5 | 0 | 63 | 91% |
| garis | 32 | 4 | 0 | 0 | 2 | 19 | 1 | 3 | 0 | 61 | 0% |
| kotak | 27 | 1 | 0 | 1 | 10 | 19 | 0 | 2 | 0 | 60 | 2% |
| taburan | 6 | 0 | 0 | 0 | 15 | 11 | 0 | 0 | 20 | 52 | 29% |
| ramai | 24 | 2 | 0 | 0 | 12 | 22 | 2 | 0 | 1 | 63 | 54% |
| - | 36 | 2 | 0 | 0 | 2 | 18 | 3 | 4 | 1 | 66 |  |

- presisi `polos` (vs nama): 53/142 = 37%
- presisi `kotak` (vs nama): 1/1 = 100%
- presisi `taburan` (vs nama): 15/39 = 38%

## 3D bawah

| nama \ ukur | polos | blok | garis | kotak | taburan | ramai | grafis | lemah | - | n | cocok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| polos | 18 | 0 | 0 | 0 | 5 | 2 | 0 | 0 | 0 | 25 | 72% |
| garis | 10 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 16 | 0% |
| kotak | 27 | 2 | 1 | 1 | 9 | 19 | 0 | 4 | 0 | 63 | 2% |
| taburan | 1 | 1 | 0 | 0 | 18 | 5 | 0 | 0 | 0 | 25 | 72% |
| ramai | 18 | 1 | 0 | 0 | 9 | 16 | 2 | 5 | 0 | 51 | 54% |
| - | 29 | 4 | 0 | 0 | 9 | 13 | 1 | 9 | 0 | 65 |  |

- presisi `polos` (vs nama): 18/74 = 24%
- presisi `garis` (vs nama): 0/1 = 0%
- presisi `kotak` (vs nama): 1/1 = 100%
- presisi `taburan` (vs nama): 18/41 = 44%

## Label emas (dinilai mata)

| t | id | emas | ukur | wilayah |
|---|---|---|---|---|
| 11 | 131428808519634 | polos | blok | {'badan': 'blok', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 102620614467965 | bunga | ramai | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 140592934157389 | bunga | taburan | {'badan': 'taburan', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 18853286606 | tulisan | grafis | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 112383779040486 | garis | garis | {'badan': 'ramai', 'lenganL': 'garis', 'lenganR': 'garis'} |
| 11 | 12251127003 | grafis | grafis | {'badan': 'grafis', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 7902161752 | grafis | ramai X | {'badan': 'ramai'} |
| 11 | 134571956901672 | polos | polos | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 15006636423 | tulisan | grafis | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 135814612176227 | grafis | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 17152218636 | polos | polos | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 11943285508 | polos | lemah X | {'badan': 'lemah', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 6355262138 | polos | grafis X | {'badan': 'grafis', 'lenganL': 'lemah', 'lenganR': 'blok'} |
| 11 | 266394252 | polos | grafis X | {'badan': 'grafis', 'lenganL': 'lemah', 'lenganR': 'polos'} |
| 11 | 87650326274539 | polos | garis X | {'badan': 'garis', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 102497906320713 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 88107382628292 | tulisan | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 118300888078991 | grafis | polos X | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 9422776837 | polos | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 108634431372050 | polos | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'polos'} |
| 11 | 84662977057675 | polos | grafis X | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 6329241946 | garis | polos X | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 15043745378 | garis | garis | {'badan': 'garis', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 4959177259 | polos | polos | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 120672004317925 | tulisan | ramai X | {'badan': 'ramai', 'lenganL': 'lemah', 'lenganR': 'grafis'} |
| 11 | 14663131904 | grafis | polos X | {'badan': 'polos', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 129927595068672 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 74922696118418 | grafis | ramai X | {'badan': 'ramai', 'lenganR': 'lemah'} |
| 11 | 11154702948 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 10554943000 | grafis | grafis | {'badan': 'grafis', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 16114397838 | tulisan | ramai X | {'badan': 'ramai', 'lenganR': 'polos'} |
| 11 | 132896774016721 | grafis | ramai X | {'badan': 'ramai'} |
| 11 | 138195987165359 | tulisan | ramai X | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'ramai'} |
| 11 | 11233366673 | polos | blok | {'badan': 'blok', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 7584705601 | polos | grafis X | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 100461181770066 | polos | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'lemah'} |
| 11 | 113040431224906 | polos | polos | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 120433639811400 | grafis | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'lemah'} |
| 11 | 6864789360 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 18222833667 | garis | ramai X | {'badan': 'ramai'} |
| 11 | 10523448233 | polos | polos | {'badan': 'polos'} |
| 11 | 9525867465 | grafis | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'taburan'} |
| 11 | 11666573467 | polos | polos | {'badan': 'polos', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 72364046238793 | polos | grafis X | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 83200538257393 | kotak | polos X | {'badan': 'polos', 'lenganL': 'garis', 'lenganR': 'polos'} |
| 11 | 8733059577 | tulisan | ramai X | {'badan': 'ramai', 'lenganL': 'grafis', 'lenganR': 'polos'} |
| 11 | 118001467186665 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'blok'} |
| 11 | 84291603963538 | kotak | blok X | {'badan': 'blok', 'lenganL': 'taburan', 'lenganR': 'polos'} |
| 11 | 6143702745 | polos | polos | {'badan': 'polos', 'lenganL': 'lemah', 'lenganR': 'polos'} |
| 11 | 6473942024 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'blok', 'lenganR': 'polos'} |
| 11 | 77790987837771 | grafis | grafis | {'badan': 'ramai', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 11 | 7459996479 | polos | polos | {'badan': 'polos', 'lenganL': 'lemah', 'lenganR': 'polos'} |
| 11 | 85269518213785 | tulisan | ramai X | {'badan': 'ramai', 'lenganL': 'ramai', 'lenganR': 'ramai'} |
| 11 | 6400454693 | polos | grafis X | {'badan': 'grafis', 'lenganL': 'polos', 'lenganR': 'polos'} |
| 12 | 6412383226 | polos | polos | {'kaki': 'polos'} |
| 12 | 9765643560 | polos | polos | {'kaki': 'polos'} |
| 12 | 102697843287286 | grafis | ramai X | {'kaki': 'ramai'} |
| 12 | 133037400812964 | bunga | taburan | {'kaki': 'taburan'} |
| 12 | 8838650406 | grafis | ramai X | {'kaki': 'ramai'} |
| 12 | 12787336716 | polos | taburan X | {'kaki': 'taburan'} |
| 12 | 72449581501449 | polos | lemah X | {'kaki': 'lemah'} |
| 12 | 15876489908 | loreng | ramai | {'kaki': 'ramai'} |
| 12 | 74480228427266 | polos | polos | {'kaki': 'polos'} |
| 12 | 76560904237091 | denim | ramai X | {'kaki': 'ramai'} |
| 12 | 112931572454830 | denim | ramai X | {'kaki': 'ramai'} |
| 12 | 6354131610 | grafis | ramai X | {'kaki': 'ramai'} |
| 12 | 9581148637 | polos | polos | {'kaki': 'polos'} |
| 12 | 134349364704274 | denim | ramai X | {'kaki': 'ramai'} |
| 12 | 113187526373432 | grafis | ramai X | {'kaki': 'ramai'} |
| 12 | 115791573774105 | denim | ramai X | {'kaki': 'ramai'} |
| 12 | 6369440433 | denim | blok | {'kaki': 'blok'} |
| 12 | 98540796262697 | garis | ramai X | {'kaki': 'ramai'} |
| 12 | 110399493168289 | polos | ramai X | {'kaki': 'ramai'} |
| 12 | 72417705441468 | polos | polos | {'kaki': 'polos'} |
| 12 | 106062802480568 | polkadot | ramai X | {'kaki': 'ramai'} |
| 12 | 7013246407 | denim | ramai X | {'kaki': 'ramai'} |
| 12 | 124132113820522 | garis | ramai X | {'kaki': 'ramai'} |
| 12 | 101253385873611 | grafis | lemah X | {'kaki': 'lemah'} |
| 12 | 101441680900737 | loreng | ramai | {'kaki': 'ramai'} |
| 12 | 140064051564958 | polos | ramai X | {'kaki': 'ramai'} |
| 12 | 73178377741857 | polos | ramai X | {'kaki': 'ramai'} |
| 12 | 13495962985 | kulit | polos | {'kaki': 'polos'} |
| 12 | 15671548105 | motif_hewan | ramai | {'kaki': 'ramai'} |
| 12 | 13924577828 | denim | polos | {'kaki': 'polos'} |
| 12 | 132833761 | polos | polos | {'kaki': 'polos'} |
| 12 | 4445410180 | polos | blok | {'kaki': 'blok'} |
| 12 | 6320365265 | polos | blok | {'kaki': 'blok'} |
| 12 | 14263285175 | polos | lemah X | {'kaki': 'lemah'} |
| 12 | 139589769351705 | denim | taburan X | {'kaki': 'taburan'} |
| 12 | 15466785041 | polos | polos | {'kaki': 'polos'} |
| 12 | 5649424359 | garis | taburan X | {'kaki': 'taburan'} |
| 12 | 12758081223 | polos | blok | {'kaki': 'blok'} |
| 12 | 110993876103378 | polos | ramai X | {'kaki': 'ramai'} |
| 12 | 125419048024037 | kotak | kotak | {'kaki': 'kotak'} |
| 12 | 6927971309 | polos | blok | {'kaki': 'blok'} |
| 12 | 8068287334 | denim | blok | {'kaki': 'blok'} |
| 12 | 2574521581 | polos | ramai X | {'kaki': 'ramai'} |
| 12 | 12727573197 | grafis | ramai X | {'kaki': 'ramai'} |

**Emas: 45/98 cocok**

