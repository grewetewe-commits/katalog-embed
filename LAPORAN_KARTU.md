# Laporan Kartu Item (MATA v2) — versi 1792170073

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **134585**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 11738 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7570 | 0.0 | 57% | 69% | 57% | 54% |
| aksen/tema | 7707 | 0.75 | 29% | 42% | 28% | 28% |
| atas2D/jenis | 5812 | 1.0 | 15% | 24% | 8% | 15% |
| atas2D/pola | 1068 | 0.75 | 50% | 62% | 47% | 50% |
| atas2D/subjek | 2162 | 0.5 | 33% | 43% | 31% | 32% |
| atas2D/tema | 4340 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5382 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2060 | 0.5 | 55% | 66% | 51% | 53% |
| atas3D/subjek | 1999 | 0.25 | 31% | 41% | 30% | 29% |
| atas3D/tema | 3350 | 0.75 | 30% | 40% | 27% | 30% |
| bawah2D/jenis | 4022 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2414 | 1.0 | 44% | 56% | 36% | 44% |
| bawah2D/subjek | 1735 | 0.75 | 15% | 22% | 12% | 14% |
| bawah2D/tema | 4070 | 0.5 | 26% | 31% | 21% | 23% |
| bawah3D/jenis | 3167 | 0.75 | 52% | 72% | 51% | 52% |
| bawah3D/pola | 1985 | 1.0 | 50% | 63% | 45% | 50% |
| bawah3D/subjek | 936 | 0.25 | 27% | 36% | 27% | 24% |
| bawah3D/tema | 1969 | 0.25 | 21% | 30% | 20% | 19% |
| kepala/jenis | 9834 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5461 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 7048 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5271 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2332 | 0.5 | 22% | 32% | 21% | 20% |
| wajah/jenis | 3727 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1575 | 0.25 | 47% | 55% | 47% | 45% |
| wajah/tema | 2133 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Bukti (rev 31): gender & tema dari bukti, bukan tebakan satu sumber

Outfit buatan manusia dipakai sebagai bukti pemakaian: **74501**.

### Gender (uji jujur: benih nama 20% item disembunyikan, ditebak dari pemakaian)

| ambang | benar | diputuskan | item uji |
|---|---|---|---|
| 0.1 | 1490 (95.5%) | 1560 | 2711 |
| 0.15 | 1375 (95.8%) | 1435 | 2711 |
| 0.25 | 1091 (97.6%) | 1118 | 2711 |

### Tema berbukti vs label emas (baju/celana 2D)

| tipe | n | diputuskan | tepat saat diputuskan | kartu lama tepat |
|---|---|---|---|---|
| 11 | 37 | 8 | 8 | 23 |
| 12 | 23 | 4 | 3 | 12 |

Item bertema berbukti: 15955 dari 134585 (sisanya tidak bertema khusus).

Sebaran: kawaii 2827, coquette 1569, formal 1470, halloween 1310, militer 1120, kerajaan 861, sporty 784, malaikat 617, gothic 607, punk 571, koboi 471, ksatria 447, natal 428, penyihir 262, iblis 248, musim_dingin 238, anime 196, antariksa 194, pantai 176, superhero 172, cyber 163, gaun_elegan 155, badut 145, peri 112, y2k 108

### Sambungan tema (PMI positif, dari outfit manusia)

- kawaii: coquette (0.21, 462)
- kerajaan: steampunk (0.37, 14), peri (0.28, 86), pantai (0.08, 29)
- formal: penyihir (0.34, 6), steampunk (0.27, 10)
- coquette: malaikat (0.32, 76), kawaii (0.21, 462), gaun_elegan (0.04, 10), peri (0.03, 48)
- militer: cyber (0.35, 8), koboi (0.05, 9)
- punk: gothic (0.73, 44), vampir (0.65, 6), iblis (0.49, 17), peri (0.35, 24)
- gothic: vampir (0.87, 6), iblis (0.77, 18), punk (0.73, 44)
- malaikat: peri (1.03, 36), iblis (0.57, 14), coquette (0.32, 76)
- peri: horor (1.53, 5), malaikat (1.03, 36), iblis (0.94, 17), punk (0.35, 24), kerajaan (0.28, 86)
- musim_dingin: natal (0.44, 8)
- iblis: vampir (1.58, 6), peri (0.94, 17), gothic (0.77, 18), malaikat (0.57, 14), punk (0.49, 17)
- natal: musim_dingin (0.44, 8)
- pantai: kerajaan (0.08, 29)
- koboi: militer (0.05, 9)
- cyber: militer (0.35, 8)
- gaun_elegan: coquette (0.04, 10)
- vampir: iblis (1.58, 6), gothic (0.87, 6), punk (0.65, 6)

## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)

Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,
celana tema 35%, pola 39-40%, kaos fungsi belum ada.

| tipe | facet | n | benar | akurasi | tanpa kartu |
|---|---|---|---|---|---|
| baju 2D | jenis | 57 | 27 | 47% | 0 |
| baju 2D | tema | 37 | 23 | 62% | 0 |
| baju 2D | pola | 54 | 16 | 30% | 0 |
| baju 2D | fungsi | 25 | 25 | 100% | 35 |
| celana 2D | jenis | 43 | 24 | 56% | 0 |
| celana 2D | tema | 23 | 12 | 52% | 0 |
| celana 2D | pola | 48 | 20 | 42% | 0 |
| celana 2D | fungsi | 16 | 15 | 94% | 43 |
| kaos klasik | fungsi | 55 | 48 | 87% | 0 |

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween] | gender=netral(0, 254 bukti) | temaBukti=halloween(3 poin)
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi] | gender=cowok(6, 5 bukti) | temaBukti=koboi(5 poin)
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut] | gender=cowok(2, 2 bukti) | temaBukti=bajak_laut(4 poin)
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(40)/mata(16) | [gambar:steampunk] | gender=cowok(6, 10 bukti)
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(54) | tema=maid(67)/punk(4) | subjek=salib(6)/rantai(6) | pola=bulu(25) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:maid] | fungsi=pakaian | gender=cewek(76, 40 bukti) | temaBukti=maid(3 poin) | DIUKUR: leher 21%
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=jas(30) | tema=formal(69)/gothic(4) | subjek=kelelawar(10)/salib(8) | pola=polos(30) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:formal] | fungsi=pakaian | gender=cowok(7, 97 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 5%
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat] | gender=cewek(4, 61 bukti) | temaBukti=malaikat(4 poin)
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(50)/bulan(32) | [gambar:steampunk] | gender=cowok(4, 4 bukti)
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(73) | tema=kawaii(70)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(96) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(44, 41 bukti) | temaBukti=kawaii(3 poin) | DIUKUR: leher 24%, bahu terbuka
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal] | gender=cewek(17, 28 bukti)
- `382538059` Green Jersey (atas): jenis=jersey(92) | tema=sporty(96)/y2k(1) | subjek=katak(24)/bintang(9) | pola=bunga(31) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | fungsi=pakaian | gender=cewek(1, 254 bukti) | temaBukti=sporty(5 poin) | DIUKUR: leher 9%
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(39)/formal(25) | subjek=salib(23)/kelelawar(12) | pola=kulit(59) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | gender=cowok(1, 254 bukti) | MESH 3D: 2.8x1.9x0.8 stud, lengan panjang
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette] | gender=cewek(30, 51 bukti) | temaBukti=coquette(4 poin)
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(79) | tema=y2k(31)/punk(27) | subjek=bulan(6)/rantai(6) | pola=denim(87) | panjang=panjang fit=lebar | [gambar:gothic] | fungsi=pakaian | gender=cowok(68, 140 bukti) | DIUKUR: -
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(50) | tema=gothic(49)/punk(25) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(81) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber] | gender=netral(0, 1 bukti)
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii] | gender=cewek(25, 3 bukti)
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan] | gender=cowok(6, 31 bukti) | temaBukti=kerajaan(6 poin)
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(23)/tulisan(9) | [gambar:streetwear] | gender=cewek(4, 254 bukti)
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii] | gender=cewek(36, 1 bukti) | temaBukti=kawaii(3 poin)
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween] | gender=cewek(14, 3 bukti) | temaBukti=halloween(7 poin)
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=kaos(23) | tema=halloween(77)/kawaii(11) | subjek=labu(45)/beruang(19) | pola=pelangi(46) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=jeans(26) | tema=halloween(74)/kawaii(5) | subjek=labu(48)/beruang(18) | pola=kotak(27) | panjang=pendek fit=lebar | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=jaket(61) | tema=antariksa(67)/cyber(22) | subjek=wajah_anime(12)/tulisan(9) | pola=loreng(40) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=cewek(6, 4 bukti)
- `1239904` Akatsuki — nama: anime | jenis=kaos(65) | tema=anime(74)/horor(5) | subjek=api(18)/buah(14) | pola=bulu(42) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:horor] | fungsi=grafis | gender=cowok(1, 3 bukti)
- `1260428` Guitar Hero 2 Logo — nama: superhero | jenis=kaos(89) | tema=superhero(73)/punk(10) | subjek=logo(28)/musik(26) | pola=kotak(25) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=cowok(1, 254 bukti)
- `1397335` Me with snow wolf shirt. — nama: musim_dingin | jenis=hoodie(42) | tema=musim_dingin(76)/streetwear(7) | subjek=kartun(9)/hiu(7) | pola=polos(35) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1431511` ninja shirt — nama: ninja | jenis=kaos(69) | tema=ninja(70)/biasa(6) | subjek=logo(25)/tulisan(9) | pola=polos(18) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(1, 71 bukti)
- `1475939` Noob shirt — nama: novelty | jenis=kaos(50) | tema=novelty(85)/cyber(2) | subjek=logo(8)/hati(7) | pola=pelangi(50) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(1, 40 bukti)
- `1515399` My cute kitty! :) — nama: kawaii | jenis=kaos(74) | tema=kawaii(54)/superhero(14) | subjek=kucing(76)/anjing(6) | pola=polkadot(75) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=netral(0, 2 bukti) | temaBukti=kawaii(4 poin)
- `1521989` shadow military lvl 1 — nama: militer | jenis=rompi(47) | tema=militer(63)/cyber(6) | subjek=logo(13)/katak(11) | pola=polos(32) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:pantai] | fungsi=grafis | gender=cowok(11, 1 bukti)
- `1558188` Random Anime Character I made — nama: anime | jenis=jas(31) | tema=anime(60)/superhero(10) | subjek=wajah_anime(39)/naga(8) | pola=polos(58) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:vampir] | fungsi=grafis | gender=cewek(4, 20 bukti)
- `1591061` Cute Wolf — nama: kawaii | jenis=kaos(77) | tema=kawaii(74)/punk(8) | subjek=anjing(69)/wajah_anime(5) | pola=grafis(66) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan] | fungsi=badan | gender=cewek(2, 9 bukti)
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(51) | tema=sporty(84)/y2k(12) | subjek=tulisan(37)/petir(13) | pola=polkadot(80) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1621982` Yellow Dragon of the Western Winds — nama: koboi | jenis=kemeja(60) | tema=koboi(56)/kerajaan(9) | subjek=naga(92)/dinosaurus(2) | pola=grafis(68) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | fungsi=grafis | gender=cewek(1, 14 bukti)
- `1636113` Ninja Drone Of Shadows Version 2 — nama: ninja | jenis=jas(52) | tema=ninja(63)/gothic(10) | subjek=laba_laba(87)/ular(1) | pola=renda(57) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(2, 22 bukti)
- `1639327` Cyber Suit35 — nama: cyber | jenis=jaket(36) | tema=cyber(54)/sporty(21) | subjek=logo(32)/bendera(10) | pola=catur(31) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(2, 3 bukti)
- `1639359` Cyber Suit31 — nama: cyber | jenis=jas(54) | tema=cyber(85)/kerajaan(2) | subjek=pita(24)/rantai(15) | pola=catur(42) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:pantai] | fungsi=aksesori | gender=cewek(9, 21 bukti)
- `1639368` Cyber Suit29 — nama: cyber | jenis=rompi(29) | tema=cyber(69)/kawaii(7) | subjek=bulan(7)/bunga(6) | pola=catur(94) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:peri] | fungsi=grafis | gender=cewek(9, 2 bukti)
- `1639414` Cyber Suit22 — nama: cyber | jenis=kaos(39) | tema=cyber(82)/streetwear(3) | subjek=bendera(16)/logo(15) | pola=catur(37) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:musim_dingin] | fungsi=aksesori | gender=cewek(2, 1 bukti)
- `1639419` Cyber Suit21 — nama: cyber | jenis=kaos(46) | tema=cyber(88)/malaikat(3) | subjek=petir(23)/hiu(12) | pola=pelangi(49) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:punk] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1639424` Cyber Suit20 — nama: cyber | jenis=kaos(53) | tema=cyber(64)/antariksa(15) | subjek=bulan(14)/petir(11) | pola=bunga(59) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(6, 22 bukti)
- `1639431` Cyber ###### — nama: cyber | jenis=jas(43) | tema=cyber(78)/penyihir(8) | subjek=bintang(15)/bulan(14) | pola=kilau(55) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(1, 2 bukti)
- `1639438` Cyber Suit18 — nama: cyber | jenis=jubah(68) | tema=cyber(61)/musim_dingin(5) | subjek=bulan(29)/hiu(17) | pola=garis(33) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:pantai] | fungsi=pakaian | gender=cewek(2, 1 bukti)
- `1639470` Cyber Suit14 — nama: cyber | jenis=jaket(23) | tema=cyber(54)/gothic(15) | subjek=bulan(27)/rantai(17) | pola=catur(52) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(4, 6 bukti)
- `1639518` Cyber ##### — nama: cyber | jenis=hoodie(41) | tema=cyber(93)/sporty(3) | subjek=hiu(18)/logo(17) | pola=kilau(25) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 6 bukti)
- `1648160` ninja — nama: ninja | jenis=jas(24) | tema=ninja(74)/badut(9) | subjek=logo(44)/tulisan(5) | pola=polkadot(38) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis | gender=netral(0, 4 bukti)
- `1705783` Halloween Tails — nama: halloween | jenis=jubah(50) | tema=halloween(50)/kostum_hewan(13) | subjek=kucing(43)/hiu(13) | pola=pelangi(27) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=netral(0, 44 bukti)
- `1726226` Cutsey_Cosplay_by_Halogrunt — nama: anime | jenis=kaos(38) | tema=anime(60)/badut(12) | subjek=kucing(27)/katak(17) | pola=bulu(63) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:badut] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1753596` Cowboy NeckHat — nama: koboi | jenis=kostum_penuh(66) | tema=koboi(68)/halloween(11) | subjek=labu(77)/makanan(3) | pola=bulu(69) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | fungsi=aksesori | gender=netral(0, 2 bukti) | temaBukti=halloween(3 poin)
- `1756352` cute — nama: kawaii | jenis=hoodie(34) | tema=kawaii(51)/novelty(22) | subjek=api(27)/petir(11) | pola=pelangi(78) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cewek(2, 2 bukti)
- `1769022` I-Pod tux — nama: formal | jenis=kostum_penuh(41) | tema=formal(55)/y2k(12) | subjek=bebek(40)/logo(8) | pola=garis(51) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(23, 1 bukti)
- `1769048` Luke Tux — nama: formal | jenis=hoodie(43) | tema=formal(86)/kawaii(4) | subjek=bebek(31)/logo(11) | pola=bulu(54) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(4, 4 bukti)
- `1769060` Metal Tux — nama: formal | jenis=jaket(26) | tema=formal(55)/natal(19) | subjek=bebek(17)/katak(13) | pola=bulu(58) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:natal] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1769091` Robin Tux — nama: formal | jenis=jaket(44) | tema=formal(55)/novelty(9) | subjek=bebek(44)/katak(8) | pola=bulu(33) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769097` ROBO TUX BEEP BOOP BOP! — nama: formal | jenis=jas(49) | tema=formal(67)/novelty(9) | subjek=hati(41)/logo(12) | pola=pelangi(77) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cowok(1, 1 bukti) | temaBukti=formal(3 poin)
- `1769130` Spy Tux — nama: formal | jenis=jaket(46) | tema=formal(56)/cyber(13) | subjek=katak(20)/bebek(11) | pola=garis(67) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769138` Super Tux!!! — nama: formal | jenis=jaket(30) | tema=formal(70)/novelty(12) | subjek=bebek(33)/logo(8) | pola=garis(37) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:superhero] | fungsi=grafis | gender=netral(0, 4 bukti)
- `1770016` School Icon — nama: sekolah | jenis=kaos(58) | tema=sekolah(61)/sporty(26) | subjek=beruang(75)/logo(10) | pola=grafis(40) | lengan=pendek panjang=crop fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1771956` Disco Tux — nama: formal | jenis=jas(28) | tema=formal(54)/kawaii(11) | subjek=bebek(10)/kartun(8) | pola=bulu(89) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic] | fungsi=grafis | gender=cowok(5, 1 bukti)
- `1771962` Ingured Tux — nama: formal | jenis=hoodie(34) | tema=formal(65)/kawaii(12) | subjek=bebek(31)/logo(9) | pola=bulu(58) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1771965` Jedi Tux — nama: formal | jenis=hoodie(38) | tema=formal(83)/kawaii(8) | subjek=bebek(26)/logo(12) | pola=bulu(32) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cowok(4, 6 bukti)
- `1773652` LOOK A WATER DRIP!(shirt) — nama: streetwear | jenis=kaos(97) | tema=streetwear(82)/kerajaan(5) | subjek=bebek(29)/katak(12) | pola=pelangi(74) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:novelty] | fungsi=grafis | gender=netral(0, 3 bukti)

## Contoh acak per kelompok

### aksen
- `11463274684` Red Mecha Armor — jenis=sabuk(53) | tema=iblis(38)/cyber(26) | subjek=api(11)/mahkota(11) | [gambar:iblis]
- `5463681525` Void Lord Scythe — jenis=senjata(83) | tema=vampir(39)/gothic(24) | subjek=kelelawar(44)/bulan(14) | [gambar:vampir] | gender=netral(0, 1 bukti)
- `7541650023` Heart Chain Grunge Necklace — jenis=kalung(98) | tema=punk(60)/kawaii(16) | subjek=rantai(60)/hati(37) | [gambar:punk] | gender=cewek(1, 1 bukti) | temaBukti=punk(4 poin)
- `9926282163` Capybara Shoulder Pet! — jenis=boneka(64) | tema=halloween(57)/kostum_hewan(34) | subjek=labu(60)/kucing(22) | [gambar:halloween] | gender=netral(0, 1 bukti) | temaBukti=halloween(3 poin)
- `4146870364` Rey’s Staff — jenis=senjata(60) | tema=ninja(36)/militer(18) | subjek=petir(17)/musik(14) | [gambar:ninja] | gender=cowok(5, 4 bukti)
- `4645922861` Bait Box Backpack — jenis=tas(52) | tema=pantai(89)/bajak_laut(3) | subjek=dinosaurus(24)/hiu(14) | [gambar:pantai] | gender=cewek(5, 1 bukti)
- `12694304872` R6 black pleated skirt — jenis=jubah_belakang(58) | tema=gothic(34)/gaun_elegan(14) | subjek=kelelawar(26)/tanpa(23) | [gambar:gothic] | gender=cewek(60, 2 bukti)
- `501938437` Shoulder Raccoon — jenis=boneka(63) | tema=kostum_hewan(75)/iblis(4) | subjek=anjing(78)/kucing(5) | [gambar:kostum_hewan] | gender=netral(0, 2 bukti)
- `12423905971` White Collar — jenis=sayap(41) | tema=malaikat(20)/vampir(7) | subjek=hiu(40)/kelelawar(32) | [gambar:malaikat] | gender=netral(0, 1 bukti)
- `10585934218` Cute Pink Crossbody Bag — jenis=tas(41) | tema=kawaii(69)/peri(21) | subjek=kupu_kupu(20)/pita(16) | [gambar:kawaii] | gender=cewek(40, 2 bukti) | temaBukti=kawaii(4 poin)
- `7209180136` Forest Elf - Axe — jenis=senjata(50) | tema=badut(21)/bajak_laut(12) | subjek=api(12)/musik(10) | [gambar:badut] | gender=cowok(5, 3 bukti)
- `7437019814` Y2K Butterfly Belly Piercing (3.0) — jenis=lain(57) | tema=peri(47)/y2k(35) | subjek=kupu_kupu(97)/bunga(1) | [gambar:peri] | gender=cewek(23, 2 bukti)
- `12797730449` Rich Money Aura — jenis=lain(21) | tema=y2k(24)/militer(21) | subjek=uang(96)/rantai(1) | [gambar:y2k] | gender=cewek(28, 4 bukti)
- `11966968506` Ribboned Heart Belly Piercing 3.0 — jenis=kalung(64) | tema=coquette(82)/kawaii(11) | subjek=hati(74)/pita(21) | [gambar:coquette] | gender=cewek(48, 1 bukti)
- `4376960922` Police Utility Belt — jenis=sabuk(67) | tema=polisi(67)/militer(7) | subjek=petir(15)/salib(11) | [gambar:polisi] | gender=cewek(1, 1 bukti) | temaBukti=polisi(3 poin)
- `12374205379` Trendy Y2K Monogram Sidebag — jenis=tas(78) | tema=y2k(38)/kawaii(16) | subjek=bunga(12)/bintang(12) | [gambar:kawaii] | gender=cewek(4, 1 bukti)
- `5488241290` Laid-back Black Earbuds — jenis=headphone(22) | tema=medis(20)/badut(10) | subjek=petir(56)/musik(8) | [gambar:medis] | gender=cewek(15, 2 bukti)
- `6202755939` High Fashion Fuzzy & Fab Purse — jenis=tas(98) | tema=horor(20)/kawaii(10) | subjek=rantai(33)/laba_laba(16) | [gambar:horor] | gender=cewek(2, 1 bukti)
- `356210971` Sophisticated Crow — jenis=sayap(83) | tema=vampir(31)/formal(22) | subjek=kelelawar(57)/bebek(9) | [gambar:vampir]
- `7794407127` Black Devilish Backpack [1.0] — jenis=tas(95) | tema=vampir(37)/iblis(30) | subjek=kelelawar(90)/logo(4) | [gambar:vampir] | gender=cewek(5, 3 bukti)
- `8780765950` Simple Gold Chain — jenis=kalung(63) | tema=biasa(39)/steampunk(14) | subjek=rantai(56)/mahkota(15) | [gambar:steampunk] | gender=netral(0, 1 bukti)
- `5997220564` Elf Backpack — jenis=ekor(39) | tema=natal(66)/badut(15) | subjek=kartun(35)/buah(12) | [gambar:natal] | gender=cowok(1, 1 bukti)
- `8185200308` Y2K Golden Heart Belly Piercing — jenis=kalung(71) | tema=y2k(43)/kerajaan(12) | subjek=hati(96)/rantai(3) | [gambar:kerajaan] | gender=cewek(29, 3 bukti)
- `5234712206` PinkLeaf Shoulder Pal — jenis=headphone(38) | tema=punk(97)/bajak_laut(1) | subjek=tanpa(13)/wajah_anime(12) | [gambar:punk] | gender=netral(0, 1 bukti)
- `6773963835` Popular Chain in Silver 3.0 — jenis=kalung(96) | tema=gaun_elegan(29)/kawaii(13) | subjek=rantai(95)/bulan(2) | [gambar:gaun_elegan] | gender=cewek(8, 2 bukti)

### atas
- `4923732521` Blossom — jenis=sweater(23) | tema=coquette(40)/kawaii(30) | subjek=pita(23)/kelelawar(9) | pola=renda(40) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:coquette] | gender=cewek(7, 1 bukti)
- `71954314286609` 👑 White Gold Warrior Armor — jenis=zirah(98) | tema=ksatria(93)/kerajaan(4) | subjek=mahkota(20)/naga(19) | pola=polos(41) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:ksatria] | temaBukti=ksatria(5 poin)
- `9202781175` Lacey Cami Crop - Hot Pink — jenis=korset(37) | tema=coquette(98)/kawaii(1) | subjek=pita(46)/hati(25) | pola=pelangi(22) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:coquette] | gender=cewek(60, 2 bukti) | MESH 3D: 1.4x1.2x0.7 stud, lengan tanpa
- `13978257971` [Hand] Gray Leather Briefcase Left — jenis=zirah(87) | tema=formal(23)/polisi(13) | subjek=musik(38)/tanpa(10) | pola=kulit(70) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:formal] | gender=cewek(2, 1 bukti) | MESH 3D: 0.5x1.9x2.3 stud, lengan tanpa
- `14000502219` White Arm Cast — jenis=kostum_penuh(21) | tema=maid(66)/malaikat(4) | subjek=ular(22)/pita(13) | pola=garis(46) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:maid] | gender=cowok(11, 6 bukti) | MESH 3D: 0.8x1.2x0.7 stud, lengan tanpa
- `3503648793` BILLIE EILISH NECKLACES / CHAINS — jenis=kaos(70) | tema=y2k(23)/malaikat(21) | subjek=rantai(71)/salib(5) | pola=kilau(70) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:malaikat] | fungsi=aksesori | gender=cewek(56, 1 bukti)
- `5410566530` Black Void Shirt — jenis=kaos(42) | tema=biasa(22)/formal(15) | subjek=salib(7)/kelelawar(7) | pola=polos(71) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=pakaian | gender=cowok(1, 1 bukti) | DIUKUR: leher 0%
- `13374948346` Necromancer Skeleton Guard (Purple) — jenis=zirah(21) | tema=halloween(37)/gothic(23) | subjek=tengkorak(76)/kelelawar(9) | pola=polos(27) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:halloween]
- `1636113` Ninja Drone Of Shadows Version 2 — jenis=jas(52) | tema=ninja(63)/gothic(10) | subjek=laba_laba(87)/ular(1) | pola=renda(57) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(2, 22 bukti)
- `71637138543841` ✅Red Lightning 95 car — jenis=hoodie(98) | tema=natal(35)/streetwear(11) | subjek=petir(35)/kartun(24) | pola=grafis(29) | lengan=pendek panjang=panjang fit=longgar depan=tertutup | [gambar:natal] | gender=netral(0, 1 bukti) | MESH 3D: 2.2x2.0x0.8 stud, lengan pendek
- `12754225063` Man Rainbow Outline Avatar Aura — jenis=crop(32) | tema=cyber(21)/badut(19) | subjek=beruang(38)/logo(14) | pola=pelangi(100) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:cyber] | gender=cowok(63, 6 bukti) | MESH 3D: 4.1x4.3x1.4 stud, lengan pendek
- `4202186598` HALLOWEEN — jenis=jas(22) | tema=halloween(44)/horor(18) | subjek=petir(24)/bendera(14) | pola=bulu(29) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:iblis] | fungsi=aksesori | gender=cowok(9, 1 bukti)
- `12175563772` Off-Shoulder Brown Sweater — jenis=jaket(39) | tema=kostum_hewan(33)/novelty(19) | subjek=kelinci(71)/beruang(12) | pola=kulit(73) | lengan=panjang panjang=panjang fit=longgar depan=terbuka | [gambar:kostum_hewan]
- `5024371981` LULULEMON- white sports top — jenis=crop(33) | tema=kawaii(21)/biasa(12) | subjek=hantu(7)/tanpa(6) | pola=polos(44) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:malaikat] | fungsi=pakaian | gender=cewek(48, 3 bukti) | DIUKUR: leher 31%, bahu terbuka, crop
- `18768917458` Pool Ball Bracelet — jenis=rompi(30) | tema=steampunk(52)/badut(28) | subjek=mata(63)/buah(6) | pola=pelangi(51) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:steampunk] | gender=cewek(25, 1 bukti) | MESH 3D: 0.6x0.5x0.6 stud, lengan tanpa
- `14952169925` Red & Black Cropped Striped Knitted Sweater — jenis=sweater(81) | tema=musim_dingin(45)/natal(21) | subjek=pita(19)/hati(12) | pola=garis(68) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:musim_dingin] | MESH 3D: 3.9x2.1x1.1 stud, lengan panjang
- `4965130448` White — jenis=jubah(16) | tema=musim_dingin(12)/y2k(9) | subjek=naga(15)/rantai(9) | pola=garis(27) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:malaikat] | gender=cewek(2, 2 bukti)
- `382537702` Teal Shirt — jenis=kaos(44) | tema=sporty(13)/kawaii(12) | subjek=katak(24)/pita(6) | pola=garis(32) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(38, 254 bukti) | DIUKUR: leher 25%
- `6456895097` Green T-Shirt. (Neon Green Beautiful Hair) — jenis=kaos(66) | tema=cyber(55)/biasa(13) | subjek=katak(64)/dinosaurus(3) | pola=polos(90) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:militer] | gender=cowok(1, 1 bukti)
- `6443337676` black crop top — jenis=crop(68) | tema=biasa(18)/punk(6) | subjek=kelelawar(10)/salib(7) | pola=polos(57) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:gothic] | gender=cewek(12, 1 bukti)
- `5018401049` 🔴RED CAMO Supreme Shirt⚫ — jenis=kaos(36) | tema=militer(80)/streetwear(6) | subjek=logo(35)/hati(11) | pola=loreng(100) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:iblis] | fungsi=pakaian | gender=cowok(1, 1 bukti) | temaBukti=militer(4 poin) | DIUKUR: leher 1%
- `12750694651` Purple Floral Denim Overalls — jenis=kostum_penuh(81) | tema=kostum_hewan(26)/antariksa(12) | subjek=bunga(35)/kelelawar(20) | pola=kulit(25) | lengan=pendek panjang=panjang fit=pas depan=terbuka | [gambar:kostum_hewan] | MESH 3D: 1.6x4.3x0.8 stud, lengan pendek
- `16288956215` Swift Style Midnight Blue Cardigan — jenis=sweater(60) | tema=sekolah(18)/punk(14) | subjek=bulan(45)/bintang(31) | pola=denim(48) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:sekolah] | MESH 3D: 2.9x1.7x0.8 stud, lengan panjang
- `9239724660` White Fluffy Shawl — jenis=zirah(27) | tema=malaikat(59)/musim_dingin(36) | subjek=naga(22)/hantu(15) | pola=bulu(98) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:malaikat] | gender=cewek(24, 3 bukti) | temaBukti=musim_dingin(3 poin) | MESH 3D: 3.3x2.0x2.4 stud, lengan panjang
- `5981298318` christmas — jenis=sweater(73) | tema=natal(48)/gothic(15) | subjek=tengkorak(83)/hantu(3) | pola=kulit(27) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic] | fungsi=pakaian | gender=cewek(17, 1 bukti) | DIUKUR: leher 1%

### bawah
- `6532007814` Steampunk — jenis=celana_kain(61) | tema=steampunk(36)/formal(11) | subjek=salib(8)/tengkorak(7) | pola=bunga(51) | panjang=panjang fit=lebar | [gambar:vampir] | fungsi=pakaian | gender=cowok(60, 1 bukti) | DIUKUR: menutup badan
- `16741899934` Bow Skirt Blush — jenis=rok_pendek(52) | tema=coquette(74)/kawaii(17) | subjek=pita(40)/bunga(37) | pola=bunga(33) | panjang=pendek fit=lebar | [gambar:coquette] | gender=cewek(78, 3 bukti) | temaBukti=coquette(4 poin) | MESH 3D: 1.8x1.1x1.7 stud, rok/gaun, melebar ke bawah, panjang pendek
- `5977722458` [MJR-CMMDR] Black BDU Long-Rolled Sleeve Trousers — jenis=celana_kain(58) | tema=formal(22)/biasa(12) | subjek=salib(5)/tanpa(5) | pola=polos(38) | panjang=panjang fit=lebar | [gambar:formal] | gender=cowok(2, 1 bukti)
- `9353911507` Cute Blue Checkered Goth Pleated Skirt — jenis=rok_pendek(71) | tema=gothic(21)/kawaii(18) | subjek=musik(35)/bendera(8) | pola=kotak(64) | panjang=pendek fit=lebar | [gambar:punk] | gender=cewek(60, 2 bukti) | MESH 3D: 1.4x1.0x0.9 stud, rok/gaun, panjang pendek
- `5459047950` purple plaid pant emo boy slender da hood girl dh — jenis=rok_pendek(30) | tema=punk(49)/natal(10) | subjek=bendera(8)/salib(8) | pola=kotak(100) | panjang=panjang fit=lebar | [gambar:sekolah] | fungsi=pakaian | gender=cowok(54, 1 bukti) | temaBukti=punk(3 poin) | DIUKUR: -
- `6553090960` MARIACHI MARIACHIS MEXICAN PARTY — jenis=zirah_bawah(59) | tema=penyihir(19)/gothic(12) | subjek=mahkota(18)/tengkorak(9) | pola=bunga(46) | panjang=panjang fit=lebar | [gambar:kerajaan] | gender=cowok(2, 2 bukti)
- `12788750272` Long Flowy Skirt - White — jenis=rok_pendek(38) | tema=gaun_elegan(46)/sekolah(10) | subjek=petir(18)/rantai(13) | pola=garis(37) | panjang=selutut fit=lebar | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti)
- `5304033285` denim shorts — jenis=jeans(57) | tema=y2k(16)/kawaii(11) | subjek=hantu(6)/hiu(5) | pola=denim(96) | panjang=pendek fit=lebar | [gambar:biasa] | gender=cewek(2, 1 bukti)
- `4757574285` Noob Skin — jenis=bawahan_gaun(51) | tema=novelty(72)/biasa(9) | subjek=katak(19)/dinosaurus(7) | pola=denim(19) | panjang=panjang fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=cewek(32, 1 bukti) | DIUKUR: menutup badan
- `6084539058` ecoFLO | Female Business Bottoms — jenis=celana_kain(29) | tema=formal(44)/polisi(9) | subjek=kelelawar(7)/mahkota(5) | pola=denim(52) | panjang=panjang fit=lebar | [gambar:formal] | gender=cewek(86, 3 bukti) | temaBukti=formal(3 poin)
- `89685154258377` Baggy Printed Star Cargos (Faded Mixture) — jenis=kargo(46) | tema=militer(85)/polisi(6) | subjek=bintang(37)/tanpa(10) | pola=loreng(63) | panjang=pendek fit=lebar | [gambar:militer] | temaBukti=militer(3 poin)
- `15789001692` Y2K White jumpsuit by DIVERGE — jenis=bawahan_gaun(57) | tema=y2k(37)/biasa(10) | subjek=hantu(19)/hati(6) | pola=polos(25) | panjang=selutut fit=ketat | [gambar:biasa] | gender=cewek(35, 1 bukti)
- `86546333293927` 💗 Cute Ruffle Trim Pleated Skirt Set _ White — jenis=rok_pendek(45) | tema=kawaii(36)/maid(30) | subjek=hantu(9)/tanpa(7) | pola=renda(19) | panjang=panjang fit=lebar | [gambar:maid] | gender=cewek(60, 2 bukti) | MESH 3D: 2.0x3.8x1.2 stud, rok/gaun, melebar ke bawah, panjang panjang
- `15246895303` BB School Girl Pleated Skirt w Belt Plaid White — jenis=rok_pendek(72) | tema=sekolah(88)/maid(4) | subjek=pita(15)/anjing(10) | pola=kotak(100) | panjang=pendek fit=lebar | [gambar:sekolah] | gender=cewek(60, 2 bukti) | temaBukti=sekolah(3 poin)
- `4785400711` ◤YG◢ Supreme Yellow Gearworks Suit — jenis=celana_kain(97) | tema=formal(94)/vampir(2) | subjek=logo(36)/salib(8) | pola=garis(42) | panjang=panjang fit=ketat | [gambar:formal] | gender=netral(0, 1 bukti) | temaBukti=formal(4 poin)
- `5144353614` Pantalón Negro  — jenis=celana_kain(39) | tema=biasa(16)/formal(16) | subjek=salib(5)/logo(5) | pola=polos(58) | panjang=panjang fit=lebar | [gambar:formal] | fungsi=pakaian | gender=cowok(1, 1 bukti) | DIUKUR: -
- `7064773844` blue — jenis=rok_pendek(60) | tema=kawaii(24)/sekolah(18) | subjek=hantu(7)/hiu(5) | pola=kotak(33) | panjang=pendek fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(40, 1 bukti) | DIUKUR: kaus kaki/stoking
- `76226941122776` Asian Opera Blossom Butterfly Sleeve Dress-Blue — jenis=zirah_bawah(49) | tema=ksatria(58)/kerajaan(25) | subjek=kupu_kupu(37)/naga(23) | pola=pelangi(16) | panjang=pendek fit=lebar | [gambar:ksatria] | gender=cewek(60, 2 bukti)
- `96413323720979` 💜 Kawaii Ribbon Checkered Skirt_Soft Pastel Blue — jenis=rok_pendek(88) | tema=sekolah(31)/kawaii(30) | subjek=pita(53)/kupu_kupu(5) | pola=catur(51) | panjang=selutut fit=lebar | [gambar:sekolah] | gender=cewek(60, 2 bukti) | MESH 3D: 2.0x1.6x1.6 stud, rok/gaun, panjang sedang
- `1028003348` GREE PANTS/LIMTED ITEM JUST FOR 5 ROBUX MY NOW — jenis=bawahan_gaun(39) | tema=antariksa(24)/horor(15) | subjek=katak(53)/hantu(4) | pola=bunga(21) | panjang=panjang fit=lebar | [gambar:penyihir] | fungsi=pakaian | gender=cowok(2, 1 bukti) | DIUKUR: menutup badan
- `83797857745695` ✨Stunning Fairytale Royal Princess Ball Gown-Red — jenis=bawahan_gaun(75) | tema=gaun_elegan(75)/kerajaan(20) | subjek=bunga(23)/mahkota(17) | pola=renda(52) | panjang=panjang fit=lebar | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti) | temaBukti=gaun_elegan(3 poin) | MESH 3D: 4.1x5.2x3.4 stud, rok/gaun, melebar ke bawah, panjang panjang
- `17702214986` ♡ shark slippers — jenis=jeans(56) | tema=vampir(20)/kawaii(19) | subjek=hiu(95)/kucing(1) | pola=denim(34) | panjang=panjang fit=lebar | [gambar:vampir] | gender=cewek(11, 2 bukti) | MESH 3D: 1.9x0.8x1.8 stud, celana, panjang panjang
- `6555797786` Grey Suit w/ Black Vest [-] — jenis=celana_kain(49) | tema=formal(78)/gothic(3) | subjek=salib(17)/kelelawar(9) | pola=renda(30) | panjang=panjang fit=ketat | [gambar:formal] | fungsi=pakaian | gender=cowok(8, 23 bukti) | temaBukti=formal(3 poin) | DIUKUR: menutup badan
- `6497901280` Mushroom Suit Pants — jenis=celana_kain(51) | tema=formal(40)/natal(9) | subjek=buah(11)/api(7) | pola=kilau(27) | panjang=panjang fit=lebar | [gambar:vampir] | gender=netral(0, 1 bukti)
- `4494396123` Dream Style — jenis=celana_pendek(24) | tema=anime(14)/kawaii(8) | subjek=mahkota(8)/beruang(6) | pola=kilau(27) | panjang=panjang fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=cewek(26, 1 bukti) | DIUKUR: menutup badan

### kepala
- `6101223186` Low White Aesthetic Headband  — jenis=pita_bando(50) | tema=medis(29)/malaikat(16) | subjek=rantai(19)/petir(11) | [gambar:medis] | gender=cewek(5, 1 bukti)
- `12154587792` Cat Ears — jenis=telinga(68) | tema=kostum_hewan(29)/coquette(9) | subjek=kucing(42)/kelelawar(11) | [gambar:kostum_hewan]
- `3798243238` Party Fedora — jenis=topi_formal(42) | tema=kawaii(44)/peri(30) | subjek=bunga(23)/buah(15) | [gambar:kawaii] | gender=cewek(1, 3 bukti)
- `12192710945` fairy — jenis=pita_bando(61) | tema=peri(46)/kawaii(45) | subjek=bunga(78)/kupu_kupu(5) | [gambar:kawaii] | temaBukti=peri(3 poin)
- `12698411058` Ribbon Pearl Earmuffs Pink — jenis=headphone(49) | tema=coquette(88)/kawaii(5) | subjek=pita(59)/kelinci(24) | [gambar:coquette] | gender=cewek(8, 1 bukti) | temaBukti=coquette(3 poin)
- `7540908300` Halloween Confetti — jenis=topi_koboi(28) | tema=halloween(69)/koboi(6) | subjek=labu(24)/laba_laba(13) | [gambar:halloween] | gender=cewek(8, 2 bukti) | temaBukti=halloween(3 poin)
- `7084418627` Black Beret — jenis=helm(15) | tema=polisi(16)/militer(12) | subjek=tanpa(14)/bebek(9) | [gambar:polisi] | gender=cewek(24, 6 bukti)
- `7097473931` Calico Cat Ears — jenis=telinga(49) | tema=vampir(23)/penyihir(18) | subjek=kelelawar(43)/kucing(35) | [gambar:vampir] | gender=cewek(2, 1 bukti)
- `8033028375` Portable Headphones  — jenis=headphone(99) | tema=antariksa(12)/militer(9) | subjek=musik(21)/tanpa(15) | [gambar:antariksa] | gender=cowok(1, 1 bukti)
- `114549646` ROBLOX Sailor Hat — jenis=topi_lain(40) | tema=bajak_laut(54)/sporty(8) | subjek=tanpa(27)/logo(8) | [gambar:bajak_laut] | gender=cowok(33, 1 bukti)
- `12686701348` ♡ Ribbon Bow Black (Droopy Bunny) — jenis=pita_bando(83) | tema=formal(63)/coquette(35) | subjek=pita(55)/kelinci(20) | [gambar:formal] | gender=cewek(26, 2 bukti) | temaBukti=coquette(3 poin)
- `5033022878` Soft Aesthetic Hat — jenis=topi_lain(40) | tema=coquette(42)/kawaii(13) | subjek=pita(13)/rantai(11) | [gambar:coquette] | gender=cewek(4, 1 bukti)
- `48894692` Evil Duck — jenis=topi_formal(22) | tema=iblis(44)/vampir(18) | subjek=bebek(98)/kelelawar(0) | [gambar:iblis] | gender=cowok(2, 13 bukti)
- `5410441336` Red Devil Hood — jenis=tudung(52) | tema=iblis(98)/vampir(1) | subjek=hati(45)/buah(22) | [gambar:iblis] | gender=cowok(42, 2 bukti) | temaBukti=iblis(3 poin)
- `10491606843` Tactical Scarf Half Mask — jenis=topeng_kepala(46) | tema=militer(36)/gothic(22) | subjek=pita(15)/tanpa(13) | [gambar:gothic] | gender=netral(0, 1 bukti)
- `4506851489` Fluffy Pink Bunny Hood — jenis=telinga(36) | tema=coquette(39)/musim_dingin(35) | subjek=kelinci(98)/pita(1) | [gambar:coquette] | gender=netral(0, 1 bukti)
- `12564668416` Y2K Cyber Heartache Earrings in Gold — jenis=anting(100) | tema=kerajaan(30)/y2k(19) | subjek=rantai(70)/hati(19) | [gambar:kerajaan] | gender=cewek(20, 1 bukti)
- `10389849688` Gold Drops Earrings — jenis=anting(98) | tema=kerajaan(64)/steampunk(13) | subjek=mahkota(46)/rantai(13) | [gambar:kerajaan] | gender=netral(0, 1 bukti)
- `73790802` Lion's hood — jenis=tudung(40) | tema=kerajaan(24)/kostum_hewan(20) | subjek=kelelawar(27)/mahkota(15) | [gambar:kerajaan] | gender=cowok(13, 2 bukti)
- `293195662` Endless Summer Grizzly Bear — jenis=telinga(45) | tema=kostum_hewan(49)/pantai(35) | subjek=beruang(100)/anjing(0) | [gambar:kostum_hewan] | gender=netral(0, 1 bukti)
- `5596158808` Magic 8-Ball — jenis=topi_formal(39) | tema=penyihir(40)/formal(13) | subjek=mata(22)/bulan(14) | [gambar:formal] | gender=cewek(16, 1 bukti)
- `8746150710` GLXW Wrecking Ball Piercing Set — jenis=anting(54) | tema=bajak_laut(39)/punk(24) | subjek=rantai(91)/musik(1) | [gambar:bajak_laut] | gender=cowok(1, 1 bukti)
- `6377003812` Pink Mushroom Beanie — jenis=kupluk(50) | tema=kawaii(70)/coquette(26) | subjek=makanan(50)/hati(9) | [gambar:kawaii] | gender=netral(0, 1 bukti)
- `44113968` Kuddle E. Koala — jenis=kupluk(74) | tema=kostum_hewan(41)/musim_dingin(13) | subjek=beruang(86)/kartun(2) | [gambar:kostum_hewan] | gender=netral(0, 2 bukti)
- `11460189460` Stylish White Headphones — jenis=headphone(99) | tema=malaikat(25)/antariksa(19) | subjek=musik(33)/rantai(17) | [gambar:malaikat] | gender=cewek(3, 1 bukti)

### rambut
- `5944865210` Brown High Double Space Buns  — tema=antariksa(35)/coquette(24) | [gambar:coquette] | gender=cewek(30, 2 bukti)
- `14278944734` Salt Water Waves in Ginger — tema=gaun_elegan(54)/steampunk(9) | [gambar:gaun_elegan] | gender=cewek(2, 1 bukti)
- `13521025890` Wavy Half up Half Down Pigtails(Blonde) — tema=kawaii(36)/malaikat(12) | [gambar:kawaii] | gender=cewek(71, 3 bukti)
- `430062818` Stylish Purple Hair — tema=halloween(17)/kerajaan(10) | [gambar:halloween] | gender=cewek(1, 1 bukti)
- `158066100` Master Fighter — tema=iblis(38)/vampir(20) | [gambar:iblis] | gender=cowok(45, 1 bukti)
- `11387419700` Kawaii Bob W/ Pigtails (Black) — tema=kawaii(35)/gothic(20) | [gambar:gothic] | gender=cewek(68, 3 bukti)
- `13835789532` Y2K Grunge Messy Lush Layered Wolf Hair White — tema=malaikat(28)/y2k(18) | [gambar:malaikat] | gender=cewek(2, 1 bukti)
- `9243992729` Short and Sleek - Black — tema=polisi(10)/streetwear(8) | [gambar:polisi] | gender=cowok(2, 231 bukti)
- `12593539495` Fluffy Messy Cool Boy Hair (Blonde) — tema=musim_dingin(40)/kawaii(9) | [gambar:kawaii] | gender=cowok(56, 4 bukti)
- `6317687313` Icy Blue Spikey Cool Hair — tema=polisi(18)/musim_dingin(8) | [gambar:polisi] | gender=cowok(2, 2 bukti)
- `12752932444` Y2K Sea Breeze Waves in Ginger — tema=y2k(38)/pantai(5) | [gambar:pantai] | gender=cewek(34, 1 bukti)
- `12956583271` Black to White Fluffy Messy Swept Hair — tema=musim_dingin(36)/gothic(9) | [gambar:gothic] | gender=cowok(18, 2 bukti)
- `13935852359` Stylish Side Swept Hair(Sky Blue) — tema=malaikat(36)/musim_dingin(7) | [gambar:malaikat] | gender=cewek(13, 1 bukti)
- `15122388715` ♡ blue layered hair w/ fluffy kawaii kitty beanie — tema=kawaii(80)/musim_dingin(18) | [gambar:kawaii] | gender=cewek(72, 1 bukti) | temaBukti=kawaii(3 poin)
- `11103880280` Blonde Bowl Cut — tema=pantai(16)/natal(9) | [gambar:pantai] | gender=cewek(23, 3 bukti)
- `11307205484` Miraculous Blue Soft Layers — tema=kawaii(78)/musim_dingin(3) | [gambar:kawaii] | gender=cewek(26, 1 bukti)
- `7104823821` Blonde Anime Style Hair — tema=anime(36)/koboi(13) | [gambar:koboi] | gender=cowok(8, 3 bukti)
- `14172045454` Messy Loose Summer Updo Bun (Blonde) — tema=pantai(37)/coquette(25) | [gambar:coquette] | gender=cewek(40, 1 bukti)
- `15351788189` Long Wavy Blonde Hair — tema=coquette(36)/kawaii(17) | [gambar:coquette] | gender=cewek(28, 6 bukti)
- `13521040732` Wavy Half up Half Down Pigtails(White) — tema=malaikat(54)/kawaii(15) | [gambar:malaikat] | gender=cewek(66, 3 bukti)
- `13002817579` Stylish Messy Hair(Blue) — tema=gothic(12)/steampunk(8) | [gambar:gothic] | gender=netral(0, 1 bukti)
- `553722174` Crimson Shaggy 2.0 — tema=iblis(25)/natal(12) | [gambar:iblis] | gender=cowok(7, 23 bukti)
- `14475494224` Messy Black Anime Hair — tema=anime(36)/polisi(15) | [gambar:polisi] | gender=cowok(51, 1 bukti)
- `12732133485` Fairy Lush Wavy Hair Cotton Candy — tema=kawaii(45)/peri(39) | [gambar:kawaii] | gender=cewek(8, 1 bukti)
- `15315015618` Black Anime Hair — tema=anime(36)/polisi(10) | [gambar:polisi]

### sepatu
- `77087395546653` Wild West Cowboy Boots White & Brown Cow Pattern — tema=koboi(51)/ksatria(9) | [gambar:koboi] | temaBukti=koboi(3 poin)
- `82244985820819` Fluffy Green and Black Scene Boots — tema=militer(53)/punk(19) | [gambar:militer]
- `93199020305597` Red heels — tema=iblis(40)/gaun_elegan(20) | [gambar:iblis]
- `90877643953425` Lime Rosary Heels — tema=gaun_elegan(17)/pantai(14) | [gambar:gaun_elegan]
- `86064003297335` Shoes W/Leg Warmers Red — tema=iblis(27)/natal(15) | [gambar:iblis]
- `76851031351383` Summer Gold Chain Sandals Black — tema=pantai(35)/kerajaan(35) | [gambar:kerajaan]
- `83571387548502` reds & blue camo shoes — tema=militer(36)/pantai(12) | [gambar:pantai]
- `85770389427293` Demon Boots — tema=iblis(37)/bajak_laut(10) | [gambar:bajak_laut]
- `79237511704487` ✅Pastel Pink High Heels Long Boots✅ Straps — tema=coquette(51)/kawaii(46) | [gambar:coquette]
- `85104414549957` Slippers & White Leg Warmers — tema=sekolah(18)/maid(14) | [gambar:sekolah]
- `74432677856564` Brown cowBoy boots — tema=koboi(99)/tradisional(0) | [gambar:koboi] | temaBukti=koboi(3 poin)
- `72516124933474` Beige Ye Slides w Socks Slippers Shoes Warmers y2k — tema=y2k(37)/medis(7) | [gambar:medis]
- `81290497910733` Cute Cheetah Agejo Gyar… - Linker-Schuh-Accessoire — tema=coquette(56)/kawaii(36) | [gambar:coquette] | gender=cewek(21, 2 bukti)
- `78509196211327` Cute Bunny Plush Slippers — tema=kawaii(40)/natal(17) | [gambar:natal]
- `89840943045344` Chunky Sneakers - Hot Pink — tema=kawaii(24)/coquette(24) | [gambar:kawaii]
- `83386295932241` Red Skate Sneaker Shoes — tema=iblis(38)/sporty(14) | [gambar:iblis]
- `89321618980326` Black Slides Sandals 3.0 — tema=gothic(15)/bajak_laut(9) | [gambar:gothic]
- `97048130026742` White Heels Chris Baddy Chic Stiletto ItGirl — tema=gaun_elegan(71)/formal(10) | [gambar:gaun_elegan]
- `92858589665803` Chunky Platform Black Loafers — tema=formal(46)/sekolah(27) | [gambar:formal]
- `73413894748569` canvas shoe hightop red — tema=iblis(26)/musim_dingin(19) | [gambar:iblis]
- `87189188832031` Black Boots W/Red Hearts - Left Shoe Accessory — tema=badut(13)/ninja(12) | [gambar:badut] | gender=cewek(31, 1 bukti)
- `82728800244474` Snowman Slippers Christmas — tema=natal(37)/malaikat(11) | [gambar:malaikat]
- `85204755924756` Black Padded Chunky Sneakers — tema=streetwear(22)/cyber(14) | [gambar:streetwear]
- `94625059582539` Moto Boots / Black — tema=gothic(28)/koboi(21) | [gambar:gothic]
- `87217182706785` Hot Pink Ballet Flat Shoes — tema=coquette(86)/kawaii(2) | [gambar:coquette]

### wajah
- `5728744669` Void Mask — jenis=masker(41) | tema=polisi(20)/maid(15) | subjek=tanpa(25)/logo(11) | [gambar:polisi] | gender=cewek(4, 5 bukti)
- `6774584712` Fancy Stylish Glasses — jenis=kacamata_hitam(60) | tema=formal(20)/streetwear(9) | subjek=tanpa(16)/logo(14) | [gambar:formal] | gender=cewek(5, 2 bukti)
- `13521532357` Eyepatch — jenis=penutup_mata(51) | tema=medis(16)/maid(13) | subjek=hati(90)/pita(3) | [gambar:medis]
- `4875723549` Gold Aviator Sunglasses — jenis=kacamata_hitam(94) | tema=steampunk(52)/militer(7) | subjek=tanpa(10)/mahkota(9) | [gambar:steampunk] | gender=netral(0, 1 bukti)
- `6376603866` Dark Polar Cub Mask — jenis=masker(49) | tema=gothic(32)/kostum_hewan(26) | subjek=beruang(32)/kucing(24) | [gambar:gothic] | gender=cewek(2, 2 bukti)
- `13539391468` Comic Robot Mask — jenis=masker(63) | tema=superhero(38)/cyber(36) | subjek=mahkota(25)/logo(9) | [gambar:superhero] | gender=cowok(89, 1 bukti)
- `15716552257` PEARL HOOP EARRINGS — jenis=tindik(50) | tema=gaun_elegan(12)/tradisional(11) | subjek=rantai(43)/bulan(25) | [gambar:gaun_elegan] | gender=cewek(34, 1 bukti)
- `14155756461` 😊 Happy Eyes (3D) 😊 — jenis=riasan(61) | tema=gaun_elegan(14)/kawaii(14) | subjek=mata(41)/bulan(7) | [gambar:gaun_elegan] | gender=netral(0, 1 bukti)
- `15716571578` Y2K Crosses Face Blush Narrow Head — jenis=riasan(50) | tema=y2k(35)/kawaii(19) | subjek=hantu(36)/mahkota(9) | [gambar:kawaii]
- `12366985658` Mr White Glasses on Head — jenis=kacamata_hitam(49) | tema=antariksa(20)/militer(7) | subjek=mata(62)/tanpa(7) | [gambar:antariksa] | gender=cewek(45, 2 bukti)
- `16112282289` Pixel Heart 8BIT — jenis=riasan(55) | tema=maid(29)/y2k(10) | subjek=hati(97)/tulisan(1) | [gambar:maid]
- `15418130093` Chibi Lips Lower [Brown] — jenis=masker(29) | tema=koboi(17)/natal(10) | subjek=buah(18)/bintang(11) | [gambar:koboi] | gender=cewek(29, 1 bukti)
- `13968534742` Red Frame Glasses — jenis=kacamata(99) | tema=medis(25)/natal(16) | subjek=tulisan(15)/mata(11) | [gambar:medis] | gender=cewek(16, 1 bukti)
- `11129803190` Red Face Stitches — jenis=tindik(45) | tema=sporty(21)/punk(18) | subjek=rantai(19)/petir(17) | [gambar:sporty] | gender=cewek(7, 1 bukti)
- `15012036715` Fedora — jenis=kumis_jenggot(21) | tema=formal(72)/sekolah(7) | subjek=tanpa(23)/logo(21) | [gambar:formal]
- `4735388946` Bunny Fashion Mask — jenis=masker(42) | tema=kawaii(88)/coquette(6) | subjek=kelinci(36)/hati(35) | [gambar:kawaii] | gender=cewek(3, 1 bukti)
- `12726334656` Cyan 1.0 Nose Spike Piercing — jenis=tindik(48) | tema=kawaii(69)/steampunk(5) | subjek=bulan(15)/logo(14) | [gambar:kawaii] | gender=cewek(3, 1 bukti)
- `14204517194` Clown — jenis=masker(30) | tema=badut(79)/natal(3) | subjek=buah(29)/bendera(18) | [gambar:badut] | temaBukti=badut(3 poin)
- `12199494116` . — jenis=penutup_kain(36) | tema=polisi(15)/gothic(14) | subjek=tanpa(21)/tulisan(13) | [gambar:polisi] | gender=cowok(1, 1 bukti)
- `6657508329` Fashionista Bangs in Blonde — jenis=kumis_jenggot(43) | tema=coquette(65)/gaun_elegan(9) | subjek=pita(27)/kelinci(19) | [gambar:coquette] | gender=cewek(6, 1 bukti)
- `14885847693` Halloween — jenis=riasan(60) | tema=halloween(99)/vampir(0) | subjek=labu(99)/hantu(1) | [gambar:halloween] | gender=cowok(18, 2 bukti) | temaBukti=halloween(7 poin)
- `15685738112` Gold Skull Mask — jenis=masker(62) | tema=bajak_laut(75)/militer(10) | subjek=tengkorak(95)/logo(1) | [gambar:bajak_laut] | gender=cowok(21, 1 bukti)
- `11134059762` Scruffy Beard In Black — jenis=kumis_jenggot(56) | tema=gothic(17)/iblis(13) | subjek=kelelawar(76)/petir(4) | [gambar:gothic] | gender=cowok(81, 5 bukti)
- `10168554869` Luna Moth (Pink) — jenis=riasan(67) | tema=peri(89)/coquette(6) | subjek=kupu_kupu(95)/kelelawar(3) | [gambar:peri] | gender=cewek(42, 1 bukti)
- `14033067835` Blush — jenis=riasan(68) | tema=coquette(62)/kawaii(8) | subjek=petir(25)/pita(14) | [gambar:coquette] | gender=cewek(44, 1 bukti)

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 299, malaikat 194, gothic 179, coquette 152, formal 137, kostum_hewan 132, punk 105, steampunk 102, iblis 98, cyber 98, militer 98, peri 96
- atas: kawaii 804, formal 683, biasa 275, punk 254, sporty 248, gothic 241, militer 219, coquette 200, y2k 188, novelty 177, halloween 162, musim_dingin 161
- bawah: formal 646, kawaii 625, y2k 429, biasa 355, gothic 324, punk 293, sekolah 266, coquette 246, musim_dingin 238, militer 187, maid 179, halloween 158
- kepala: coquette 236, kawaii 213, kerajaan 179, formal 166, malaikat 149, militer 143, gothic 121, peri 112, kostum_hewan 110, iblis 100, penyihir 99, polisi 94
- rambut: kawaii 431, gothic 391, coquette 229, anime 179, steampunk 171, gaun_elegan 170, koboi 150, musim_dingin 144, punk 136, malaikat 120, iblis 92, y2k 85
- sepatu: kawaii 348, gothic 248, coquette 244, sporty 202, musim_dingin 191, y2k 156, kostum_hewan 147, pantai 130, militer 114, punk 111, gaun_elegan 98, formal 88
- wajah: kawaii 436, steampunk 236, gothic 183, militer 170, cyber 164, coquette 139, malaikat 92, anime 90, polisi 82, iblis 76, vampir 70, pantai 68
