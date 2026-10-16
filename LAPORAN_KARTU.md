# Laporan Kartu Item (MATA v2) — versi 1792185556

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **136051**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 11891 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7658 | 0.0 | 57% | 69% | 57% | 54% |
| aksen/tema | 7808 | 0.75 | 29% | 42% | 28% | 28% |
| atas2D/jenis | 5899 | 1.0 | 15% | 24% | 8% | 15% |
| atas2D/pola | 1083 | 0.75 | 49% | 62% | 47% | 49% |
| atas2D/subjek | 2187 | 0.5 | 33% | 43% | 31% | 32% |
| atas2D/tema | 4392 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5436 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2078 | 0.75 | 55% | 66% | 51% | 53% |
| atas3D/subjek | 2013 | 0.25 | 31% | 40% | 30% | 29% |
| atas3D/tema | 3389 | 0.75 | 30% | 40% | 27% | 30% |
| bawah2D/jenis | 4072 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2444 | 1.0 | 44% | 56% | 35% | 44% |
| bawah2D/subjek | 1758 | 0.75 | 15% | 22% | 12% | 14% |
| bawah2D/tema | 4117 | 0.5 | 25% | 31% | 21% | 23% |
| bawah3D/jenis | 3187 | 0.75 | 52% | 72% | 51% | 52% |
| bawah3D/pola | 1996 | 1.0 | 50% | 63% | 45% | 50% |
| bawah3D/subjek | 945 | 0.25 | 28% | 36% | 28% | 25% |
| bawah3D/tema | 1985 | 0.25 | 21% | 30% | 21% | 19% |
| kepala/jenis | 9911 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5519 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 7111 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5328 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2356 | 0.5 | 21% | 32% | 21% | 20% |
| wajah/jenis | 3759 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1592 | 0.25 | 47% | 55% | 47% | 45% |
| wajah/tema | 2157 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Bukti (rev 31): gender & tema dari bukti, bukan tebakan satu sumber

Outfit buatan manusia dipakai sebagai bukti pemakaian: **75715**.

### Gender (uji jujur: benih nama 20% item disembunyikan, ditebak dari pemakaian)

| ambang | benar | diputuskan | item uji |
|---|---|---|---|
| 0.1 | 1496 (95.3%) | 1570 | 2736 |
| 0.15 | 1392 (96.0%) | 1450 | 2736 |
| 0.25 | 1127 (97.6%) | 1155 | 2736 |

### Tema berbukti vs label emas (baju/celana 2D)

| tipe | n | diputuskan | tepat saat diputuskan | kartu lama tepat |
|---|---|---|---|---|
| 11 | 37 | 8 | 8 | 22 |
| 12 | 23 | 4 | 3 | 12 |

Item bertema berbukti: 16120 dari 136051 (sisanya tidak bertema khusus).

Sebaran: kawaii 2860, coquette 1580, formal 1493, halloween 1332, militer 1124, kerajaan 875, sporty 781, malaikat 628, gothic 610, punk 580, koboi 475, ksatria 453, natal 431, penyihir 261, iblis 250, musim_dingin 239, anime 207, antariksa 194, pantai 180, superhero 172, cyber 164, gaun_elegan 156, badut 145, peri 113, y2k 108

### Sambungan tema (PMI positif, dari outfit manusia)

- kawaii: coquette (0.22, 470)
- kerajaan: steampunk (0.36, 14), peri (0.30, 89), pantai (0.06, 29)
- formal: penyihir (0.38, 6), steampunk (0.26, 10)
- coquette: malaikat (0.32, 76), kawaii (0.22, 470), gaun_elegan (0.12, 11), peri (0.03, 48)
- militer: cyber (0.35, 8), koboi (0.03, 9)
- punk: gothic (0.74, 45), vampir (0.66, 6), iblis (0.47, 17), peri (0.34, 24)
- gothic: vampir (0.87, 6), iblis (0.75, 18), punk (0.74, 45)
- malaikat: peri (1.06, 37), iblis (0.56, 14), coquette (0.32, 76)
- peri: horor (1.50, 5), malaikat (1.06, 37), iblis (1.03, 19), punk (0.34, 24), kerajaan (0.30, 89)
- musim_dingin: natal (0.42, 8)
- iblis: vampir (1.58, 6), peri (1.03, 19), gothic (0.75, 18), malaikat (0.56, 14), punk (0.47, 17)
- natal: musim_dingin (0.42, 8)
- pantai: kerajaan (0.06, 29)
- koboi: militer (0.03, 9)
- cyber: militer (0.35, 8)
- gaun_elegan: coquette (0.12, 11)
- vampir: iblis (1.58, 6), gothic (0.87, 6), punk (0.66, 6)

## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)

Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,
celana tema 35%, pola 39-40%, kaos fungsi belum ada.

| tipe | facet | n | benar | akurasi | tanpa kartu |
|---|---|---|---|---|---|
| baju 2D | jenis | 57 | 27 | 47% | 0 |
| baju 2D | tema | 37 | 22 | 59% | 0 |
| baju 2D | pola | 54 | 15 | 28% | 0 |
| baju 2D | fungsi | 30 | 29 | 97% | 30 |
| celana 2D | jenis | 43 | 24 | 56% | 0 |
| celana 2D | tema | 23 | 12 | 52% | 0 |
| celana 2D | pola | 48 | 20 | 42% | 0 |
| celana 2D | fungsi | 20 | 19 | 95% | 39 |
| kaos klasik | fungsi | 55 | 48 | 87% | 0 |

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween] | gender=netral(0, 254 bukti) | temaBukti=halloween(3 poin)
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi] | gender=cowok(6, 5 bukti) | temaBukti=koboi(5 poin)
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut] | gender=cowok(2, 2 bukti) | temaBukti=bajak_laut(4 poin)
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(40)/mata(16) | [gambar:steampunk] | gender=cowok(6, 10 bukti)
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(54) | tema=maid(67)/punk(4) | subjek=salib(6)/rantai(6) | pola=bulu(29) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:maid] | fungsi=pakaian | gender=cewek(76, 41 bukti) | temaBukti=maid(3 poin) | DIUKUR: leher 21%
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=jas(31) | tema=formal(69)/gothic(4) | subjek=kelelawar(10)/salib(8) | pola=bulu(30) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:formal] | fungsi=pakaian | gender=cowok(6, 103 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 5%
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat] | gender=cewek(4, 61 bukti) | temaBukti=malaikat(4 poin)
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(50)/bulan(32) | [gambar:steampunk] | gender=cowok(4, 4 bukti)
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(74) | tema=kawaii(68)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(96) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(44, 42 bukti) | temaBukti=kawaii(3 poin) | DIUKUR: leher 24%, bahu terbuka
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal] | gender=cewek(17, 29 bukti)
- `382538059` Green Jersey (atas): jenis=jersey(92) | tema=sporty(95)/y2k(1) | subjek=katak(24)/bintang(9) | pola=bunga(26) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | fungsi=pakaian | gender=cewek(1, 254 bukti) | temaBukti=sporty(5 poin) | DIUKUR: leher 9%
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(39)/formal(25) | subjek=salib(23)/kelelawar(12) | pola=kulit(55) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | gender=cowok(1, 254 bukti) | MESH 3D: 2.8x1.9x0.8 stud, lengan panjang
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette] | gender=cewek(31, 51 bukti) | temaBukti=coquette(4 poin)
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(78) | tema=y2k(31)/punk(27) | subjek=bulan(6)/rantai(6) | pola=denim(87) | panjang=panjang fit=lebar | [gambar:gothic] | fungsi=pakaian | gender=cowok(68, 142 bukti) | DIUKUR: -
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(51) | tema=gothic(45)/punk(29) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(83) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber] | gender=netral(0, 1 bukti)
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii] | gender=cewek(25, 3 bukti)
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan] | gender=cowok(6, 32 bukti) | temaBukti=kerajaan(6 poin)
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(23)/tulisan(9) | [gambar:streetwear] | gender=cewek(4, 254 bukti)
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii] | gender=cewek(36, 1 bukti) | temaBukti=kawaii(3 poin)
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween] | gender=cewek(20, 3 bukti) | temaBukti=halloween(7 poin)
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=kaos(22) | tema=halloween(77)/kawaii(11) | subjek=labu(45)/beruang(19) | pola=pelangi(44) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=jeans(25) | tema=halloween(74)/kawaii(5) | subjek=labu(48)/beruang(18) | pola=kotak(27) | panjang=pendek fit=lebar | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=jaket(57) | tema=antariksa(66)/cyber(23) | subjek=wajah_anime(12)/tulisan(9) | pola=loreng(35) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=cewek(6, 4 bukti)
- `1239904` Akatsuki — nama: anime | jenis=kaos(73) | tema=anime(74)/y2k(4) | subjek=api(18)/buah(14) | pola=bulu(38) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:horor] | fungsi=grafis | gender=cowok(1, 3 bukti)
- `1260428` Guitar Hero 2 Logo — nama: superhero | jenis=kaos(91) | tema=superhero(73)/punk(9) | subjek=logo(28)/musik(26) | pola=kotak(22) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=cowok(1, 254 bukti)
- `1397335` Me with snow wolf shirt. — nama: musim_dingin | jenis=hoodie(50) | tema=musim_dingin(75)/streetwear(7) | subjek=kartun(9)/hiu(7) | pola=polos(34) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1431511` ninja shirt — nama: ninja | jenis=kaos(70) | tema=ninja(70)/biasa(7) | subjek=logo(25)/tulisan(9) | pola=garis(22) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(1, 72 bukti)
- `1475939` Noob shirt — nama: novelty | jenis=kaos(49) | tema=novelty(85)/cyber(2) | subjek=logo(8)/hati(7) | pola=pelangi(54) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(1, 43 bukti)
- `1515399` My cute kitty! :) — nama: kawaii | jenis=kaos(73) | tema=kawaii(54)/superhero(14) | subjek=kucing(76)/anjing(6) | pola=polkadot(80) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=netral(0, 2 bukti) | temaBukti=kawaii(4 poin)
- `1521989` shadow military lvl 1 — nama: militer | jenis=rompi(45) | tema=militer(62)/cyber(6) | subjek=logo(13)/katak(11) | pola=polos(32) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:pantai] | fungsi=grafis | gender=cowok(11, 1 bukti)
- `1558188` Random Anime Character I made — nama: anime | jenis=jas(27) | tema=anime(60)/superhero(11) | subjek=wajah_anime(39)/naga(8) | pola=polos(55) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:vampir] | fungsi=grafis | gender=cewek(4, 20 bukti)
- `1591061` Cute Wolf — nama: kawaii | jenis=kaos(73) | tema=kawaii(73)/punk(8) | subjek=anjing(69)/wajah_anime(5) | pola=grafis(66) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan] | fungsi=badan | gender=cewek(2, 9 bukti)
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(52) | tema=sporty(84)/y2k(11) | subjek=tulisan(37)/petir(13) | pola=polkadot(82) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1621982` Yellow Dragon of the Western Winds — nama: koboi | jenis=kemeja(54) | tema=koboi(55)/kerajaan(10) | subjek=naga(92)/dinosaurus(2) | pola=grafis(69) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | fungsi=grafis | gender=cewek(1, 15 bukti)
- `1636113` Ninja Drone Of Shadows Version 2 — nama: ninja | jenis=jas(47) | tema=ninja(62)/gothic(12) | subjek=laba_laba(87)/ular(1) | pola=renda(56) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(2, 24 bukti)
- `1639327` Cyber Suit35 — nama: cyber | jenis=jaket(36) | tema=cyber(54)/sporty(21) | subjek=logo(32)/bendera(10) | pola=garis(41) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(2, 3 bukti)
- `1639359` Cyber Suit31 — nama: cyber | jenis=jas(52) | tema=cyber(80)/ninja(3) | subjek=pita(24)/rantai(15) | pola=catur(41) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:pantai] | fungsi=aksesori | gender=cewek(9, 21 bukti)
- `1639368` Cyber Suit29 — nama: cyber | jenis=rompi(35) | tema=cyber(68)/kawaii(7) | subjek=bulan(7)/bunga(6) | pola=catur(93) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:peri] | fungsi=grafis | gender=cewek(2, 2 bukti)
- `1639414` Cyber Suit22 — nama: cyber | jenis=kaos(40) | tema=cyber(84)/militer(2) | subjek=bendera(16)/logo(15) | pola=catur(39) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:musim_dingin] | fungsi=aksesori | gender=cewek(2, 1 bukti)
- `1639419` Cyber Suit21 — nama: cyber | jenis=kaos(50) | tema=cyber(88)/malaikat(3) | subjek=petir(23)/hiu(12) | pola=pelangi(46) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:punk] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1639424` Cyber Suit20 — nama: cyber | jenis=kaos(56) | tema=cyber(60)/antariksa(15) | subjek=bulan(14)/petir(11) | pola=bunga(57) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(6, 22 bukti)
- `1639431` Cyber ###### — nama: cyber | jenis=jas(39) | tema=cyber(78)/penyihir(8) | subjek=bintang(15)/bulan(14) | pola=kilau(58) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(1, 2 bukti)
- `1639438` Cyber Suit18 — nama: cyber | jenis=jubah(54) | tema=cyber(59)/musim_dingin(5) | subjek=bulan(29)/hiu(17) | pola=garis(48) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:pantai] | fungsi=pakaian | gender=cewek(2, 1 bukti)
- `1639470` Cyber Suit14 — nama: cyber | jenis=kaos(21) | tema=cyber(56)/gothic(14) | subjek=bulan(27)/rantai(17) | pola=catur(50) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(4, 6 bukti)
- `1639518` Cyber ##### — nama: cyber | jenis=hoodie(39) | tema=cyber(93)/sporty(3) | subjek=hiu(18)/logo(17) | pola=kilau(25) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 6 bukti)
- `1648160` ninja — nama: ninja | jenis=jas(24) | tema=ninja(74)/badut(10) | subjek=logo(44)/tulisan(5) | pola=polkadot(39) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis | gender=netral(0, 4 bukti)
- `1726226` Cutsey_Cosplay_by_Halogrunt — nama: anime | jenis=kaos(37) | tema=anime(60)/badut(12) | subjek=kucing(27)/katak(17) | pola=bulu(56) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:badut] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1753596` Cowboy NeckHat — nama: koboi | jenis=kostum_penuh(64) | tema=koboi(68)/halloween(12) | subjek=labu(77)/makanan(3) | pola=bulu(73) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | fungsi=aksesori | gender=netral(0, 2 bukti) | temaBukti=halloween(3 poin)
- `1756352` cute — nama: kawaii | jenis=hoodie(34) | tema=kawaii(50)/novelty(22) | subjek=api(27)/petir(11) | pola=pelangi(79) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cewek(2, 2 bukti)
- `1769022` I-Pod tux — nama: formal | jenis=hoodie(37) | tema=formal(56)/y2k(12) | subjek=bebek(40)/logo(8) | pola=polkadot(45) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(23, 1 bukti)
- `1769048` Luke Tux — nama: formal | jenis=hoodie(48) | tema=formal(86)/kawaii(4) | subjek=bebek(31)/logo(11) | pola=bulu(55) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(4, 4 bukti)
- `1769060` Metal Tux — nama: formal | jenis=jaket(23) | tema=formal(54)/natal(20) | subjek=bebek(17)/katak(13) | pola=bulu(70) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:natal] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1769091` Robin Tux — nama: formal | jenis=jaket(34) | tema=formal(54)/novelty(9) | subjek=bebek(44)/katak(8) | pola=bulu(44) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769097` ROBO TUX BEEP BOOP BOP! — nama: formal | jenis=jas(49) | tema=formal(66)/novelty(8) | subjek=hati(41)/logo(12) | pola=pelangi(82) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cowok(1, 1 bukti) | temaBukti=formal(3 poin)
- `1769130` Spy Tux — nama: formal | jenis=jaket(43) | tema=formal(55)/cyber(15) | subjek=katak(20)/bebek(11) | pola=garis(51) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769138` Super Tux!!! — nama: formal | jenis=jaket(26) | tema=formal(71)/novelty(11) | subjek=bebek(33)/logo(8) | pola=pelangi(41) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:superhero] | fungsi=grafis | gender=cewek(4, 5 bukti)
- `1770016` School Icon — nama: sekolah | jenis=kaos(55) | tema=sekolah(61)/sporty(26) | subjek=beruang(75)/logo(10) | pola=grafis(42) | lengan=pendek panjang=crop fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1771956` Disco Tux — nama: formal | jenis=jubah(27) | tema=formal(52)/kawaii(12) | subjek=bebek(10)/kartun(8) | pola=bulu(92) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic] | fungsi=grafis | gender=cowok(5, 1 bukti)
- `1771962` Ingured Tux — nama: formal | jenis=hoodie(37) | tema=formal(64)/kawaii(12) | subjek=bebek(31)/logo(9) | pola=bulu(66) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1771965` Jedi Tux — nama: formal | jenis=hoodie(39) | tema=formal(82)/kawaii(7) | subjek=bebek(26)/logo(12) | pola=polkadot(36) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cowok(4, 6 bukti)
- `1773652` LOOK A WATER DRIP!(shirt) — nama: streetwear | jenis=kaos(97) | tema=streetwear(81)/kerajaan(5) | subjek=bebek(29)/katak(12) | pola=pelangi(77) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:novelty] | fungsi=grafis | gender=netral(0, 3 bukti)
- `1781595` some tux's — nama: formal | jenis=jubah(27) | tema=formal(53)/novelty(14) | subjek=bebek(46)/tulisan(5) | pola=garis(52) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=netral(0, 3 bukti)

## Contoh acak per kelompok

### aksen
- `11355947854` 444 Chain 3.0 — jenis=kalung(46) | tema=iblis(11)/malaikat(7) | subjek=rantai(37)/logo(15) | [gambar:iblis] | gender=cewek(32, 2 bukti)
- `5410704851` Cat Tail with Bell n' Bow — jenis=ekor(88) | tema=coquette(78)/peri(17) | subjek=pita(38)/kucing(19) | [gambar:coquette] | gender=cowok(1, 1 bukti) | temaBukti=coquette(3 poin)
- `7486038694` Right Sci-fi Samurai Shoulder Guard — jenis=jubah_belakang(57) | tema=ninja(36)/penyihir(16) | subjek=petir(19)/logo(11) | [gambar:penyihir] | gender=netral(0, 1 bukti)
- `9667387696` Star Necklace3.0 — jenis=sabuk(55) | tema=punk(66)/bajak_laut(13) | subjek=bintang(52)/rantai(26) | [gambar:punk] | gender=netral(0, 1 bukti)
- `3964190156` Sharkbite Bait Bucket — jenis=ekor(36) | tema=novelty(53)/bajak_laut(16) | subjek=bebek(44)/tulisan(12) | [gambar:novelty] | gender=netral(0, 1 bukti)
- `4623728953` Black Demon Trident — jenis=senjata(72) | tema=iblis(43)/penyihir(14) | subjek=petir(67)/logo(11) | [gambar:penyihir] | gender=cowok(3, 5 bukti)
- `12633009299` Emperor Cecil's Cloak from FGTeeV Book — jenis=jubah_belakang(67) | tema=iblis(20)/ksatria(19) | subjek=naga(18)/pita(11) | [gambar:iblis]
- `501761204` Lady of the Federation Necklace — jenis=kalung(46) | tema=penyihir(48)/kerajaan(18) | subjek=salib(24)/bulan(17) | [gambar:penyihir] | gender=cewek(64, 3 bukti)
- `12358124645` Y2K Glowing Airbrushed Hearts Confetti Pink — jenis=kalung(35) | tema=coquette(37)/y2k(35) | subjek=hati(97)/pita(1) | [gambar:coquette] | gender=cewek(35, 2 bukti)
- `10401224852` Nomad's Cape — jenis=jubah_belakang(73) | tema=kostum_hewan(28)/koboi(14) | subjek=kelelawar(33)/hiu(14) | [gambar:kostum_hewan] | gender=cowok(56, 1 bukti)
- `7168483270` Magical Girl Backpack 3.0 — jenis=tas(58) | tema=kawaii(41)/peri(35) | subjek=hantu(32)/kucing(20) | [gambar:kawaii] | gender=cewek(73, 3 bukti)
- `7374986976` Butterfly Necklace Gold 3.0 — jenis=kalung(76) | tema=malaikat(39)/kawaii(36) | subjek=kupu_kupu(63)/bintang(6) | [gambar:malaikat] | gender=cewek(22, 1 bukti)
- `12732837631` Paint Brush — jenis=senjata(35) | tema=kawaii(66)/coquette(12) | subjek=makanan(20)/hati(10) | [gambar:kawaii] | gender=cewek(23, 1 bukti)
- `11812586207` Blue and Green Rainbow Friends — jenis=boneka(60) | tema=kostum_hewan(41)/horor(27) | subjek=kartun(33)/katak(27) | [gambar:kostum_hewan] | gender=cowok(25, 1 bukti)
- `4319708501` Pink Heart Backpack — jenis=tas(58) | tema=coquette(86)/kawaii(4) | subjek=hati(74)/pita(4) | [gambar:coquette] | gender=cewek(7, 1 bukti)
- `12326831926` Black Ruffles White Striped (1.0) — jenis=sabuk(54) | tema=punk(43)/gothic(34) | subjek=rantai(79)/ular(10) | [gambar:punk] | gender=cowok(1, 1 bukti)
- `5451366099` Trench Shark Fin — jenis=ekor(52) | tema=formal(11)/polisi(11) | subjek=hiu(35)/bulan(14) | [gambar:formal] | gender=cowok(26, 1 bukti)
- `6201957204` Miau Luxury Purse 3.0 Black — jenis=tas(94) | tema=formal(24)/gaun_elegan(14) | subjek=tanpa(29)/logo(15) | [gambar:formal] | gender=cewek(36, 1 bukti)
- `335079187` Heroic Golden Wings — jenis=sayap(97) | tema=kerajaan(59)/steampunk(13) | subjek=mahkota(44)/kupu_kupu(20) | [gambar:kerajaan] | gender=cewek(1, 1 bukti)
- `7668322622` White Royal Parted Cape — jenis=jubah_belakang(49) | tema=kerajaan(35)/maid(13) | subjek=pita(61)/rantai(5) | [gambar:maid] | gender=cewek(32, 1 bukti)
- `8669170103` Cute Opossum Backpack - Kawaii Anime Pet Bag 3.0 — jenis=boneka(70) | tema=kostum_hewan(55)/kawaii(19) | subjek=wajah_anime(36)/beruang(24) | [gambar:kostum_hewan] | gender=cewek(37, 2 bukti)
- `5945286947` Rose — jenis=lain(55) | tema=coquette(17)/peri(13) | subjek=bunga(97)/hati(1) | [gambar:coquette] | gender=netral(0, 1 bukti)
- `8082688356` Golden Empire Quiver — jenis=senjata(55) | tema=ksatria(42)/penyihir(13) | subjek=api(30)/naga(19) | [gambar:ksatria] | gender=netral(0, 2 bukti)
- `5205483683` Fiery Fox Shoulder Pal — jenis=boneka(69) | tema=kostum_hewan(37)/iblis(27) | subjek=api(89)/kelinci(7) | [gambar:kostum_hewan] | gender=cowok(8, 3 bukti)
- `6736669721` Most Visits — jenis=sayap(92) | tema=malaikat(93)/kerajaan(3) | subjek=mahkota(37)/kartun(11) | [gambar:malaikat] | gender=netral(0, 1 bukti)

### atas
- `4889899981` Thai Logo — jenis=kaos(68) | tema=sporty(41)/medis(24) | subjek=bendera(64)/logo(35) | pola=polos(49) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:militer] | fungsi=grafis | gender=cewek(23, 6 bukti)
- `71568183652805` Y2k Hood Puffer Jacket Gray — jenis=jaket(98) | tema=y2k(35)/kostum_hewan(18) | subjek=beruang(22)/ular(15) | pola=bulu(81) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:kostum_hewan]
- `9186615466` ✅ Green — jenis=zirah(65) | tema=militer(93)/ninja(1) | subjek=katak(36)/pita(13) | pola=loreng(90) | lengan=panjang panjang=panjang fit=pas depan=terbuka | [gambar:militer] | gender=cewek(21, 1 bukti) | temaBukti=militer(3 poin) | MESH 3D: 3.0x1.4x0.7 stud, lengan panjang
- `13947644006` 💅Short Nails - Dark Beige — jenis=tanktop(19) | tema=koboi(27)/malaikat(8) | subjek=kucing(10)/beruang(7) | pola=motif_hewan(48) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:koboi] | gender=cewek(33, 1 bukti) | MESH 3D: 3.5x1.9x0.4 stud
- `13956862963` Purple Trench Coat — jenis=jaket(53) | tema=penyihir(27)/vampir(20) | subjek=hantu(21)/kelelawar(20) | pola=polos(57) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:penyihir] | MESH 3D: 2.9x3.0x0.8 stud, lengan panjang
- `3416308755` Plain White Short Sleeve — jenis=kaos(35) | tema=biasa(60)/malaikat(4) | subjek=logo(7)/tanpa(5) | pola=polos(88) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:biasa] | fungsi=pakaian | gender=cowok(2, 7 bukti) | DIUKUR: leher 4%
- `5356142944` Louis Vuitton Black and White — jenis=hoodie(34) | tema=ninja(28)/y2k(20) | subjek=uang(23)/bintang(9) | pola=kulit(49) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:punk] | gender=netral(0, 1 bukti)
- `13338509297` Black Leather Race Jacket — jenis=jaket(80) | tema=polisi(23)/superhero(19) | subjek=kelelawar(31)/salib(13) | pola=kulit(48) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | MESH 3D: 2.9x1.9x0.8 stud, lengan panjang
- `1635952` Teapot Drone Version 2 — jenis=jas(56) | tema=cyber(17)/gothic(13) | subjek=laba_laba(82)/bunga(3) | pola=bulu(21) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:peri] | fungsi=badan | gender=cowok(11, 2 bukti)
- `71359788198147` White Leather Bomber Jacket w/ Dress Shirt — jenis=jaket(54) | tema=militer(19)/streetwear(9) | subjek=rantai(23)/tanpa(14) | pola=kulit(49) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:militer] | MESH 3D: 3.0x1.8x0.9 stud, lengan panjang
- `12741562325` Bright Green Floral Overalls — jenis=kostum_penuh(74) | tema=badut(30)/peri(16) | subjek=bunga(65)/katak(18) | pola=bunga(96) | lengan=tanpa panjang=panjang fit=pas depan=terbuka | [gambar:badut] | MESH 3D: 1.6x4.3x0.8 stud, lengan tanpa
- `4086183193` [ 🌊 ] Shimmering Gold Body Jewelry — jenis=gaun(20) | tema=peri(30)/penyihir(11) | subjek=mahkota(26)/pita(23) | pola=renda(24) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | gender=cewek(42, 2 bukti)
- `12131984382` Kitty Paw Oversized Hoodie Pink — jenis=hoodie(65) | tema=kawaii(49)/cyber(12) | subjek=katak(43)/kucing(35) | pola=pelangi(79) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kawaii]
- `4985980531` 💥MU Gray Camo Jacket w/ White Tee💥 — jenis=jaket(48) | tema=militer(46)/formal(11) | subjek=salib(8)/tengkorak(8) | pola=loreng(70) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:formal] | fungsi=pakaian | gender=netral(0, 1 bukti) | temaBukti=militer(4 poin) | DIUKUR: leher 4%
- `18684984680` ♡  white and pink cutecore doll maid wrist cuffs — jenis=zirah(79) | tema=kawaii(35)/maid(24) | subjek=rantai(11)/buah(8) | pola=renda(26) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | gender=cewek(3, 1 bukti) | MESH 3D: 3.3x0.6x0.7 stud
- `14918697501` dress shirt — jenis=kemeja(25) | tema=formal(91)/sekolah(2) | subjek=logo(14)/hantu(12) | pola=polos(25) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:formal]
- `4932712826` navy — jenis=kemeja(55) | tema=sporty(38)/sekolah(16) | subjek=bendera(33)/logo(7) | pola=garis(99) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | gender=cewek(44, 1 bukti)
- `365102637` Argyle Sweater - Gray Edition — jenis=sweater(64) | tema=formal(24)/militer(13) | subjek=salib(9)/pita(8) | pola=kotak(36) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:formal] | fungsi=pakaian | gender=cewek(1, 1 bukti) | DIUKUR: leher 8%
- `6432006680` 🖤🤍cute emo off shoulder goth y2k grunge vamp — jenis=sweater(66) | tema=punk(32)/gothic(18) | subjek=pita(14)/rantai(11) | pola=garis(66) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:punk] | fungsi=pakaian | gender=cewek(41, 5 bukti) | DIUKUR: leher 25%, bahu terbuka, crop
- `6419866137` Attack on Titan Untucked Button Up — jenis=kemeja(40) | tema=formal(14)/musim_dingin(13) | subjek=rantai(9)/tanpa(8) | pola=bulu(27) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:militer] | fungsi=pakaian | gender=netral(0, 2 bukti) | DIUKUR: leher 2%
- `4980056672` South Korean Flag — jenis=kemeja(57) | tema=kawaii(19)/y2k(17) | subjek=bendera(51)/bulan(6) | pola=polos(54) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:sekolah] | fungsi=grafis | gender=cowok(42, 1 bukti)
- `12740768957` Lace Flower Cape - White — jenis=seragam(19) | tema=malaikat(16)/gothic(11) | subjek=bunga(35)/bulan(12) | pola=loreng(31) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:malaikat] | gender=cewek(35, 1 bukti) | MESH 3D: 4.9x4.7x2.5 stud, lengan panjang
- `16249772515` Star Hoodie — jenis=hoodie(97) | tema=streetwear(21)/sporty(17) | subjek=bintang(60)/hantu(11) | pola=loreng(41) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:streetwear]
- `9239653059` Anime Arm Bandages — jenis=tanktop(30) | tema=steampunk(46)/anime(35) | subjek=rantai(37)/wajah_anime(35) | pola=garis(54) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:steampunk] | gender=cewek(23, 7 bukti) | MESH 3D: 3.1x1.1x0.6 stud
- `5943461671` 🎅Red Santa Cute Preppy Y2K Christmas Ice Winter — jenis=tanktop(55) | tema=natal(53)/y2k(11) | subjek=hati(22)/buah(15) | pola=polos(47) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:natal] | fungsi=pakaian | gender=cewek(38, 1 bukti) | DIUKUR: leher 28%, bahu terbuka, crop

### bawah
- `6510575357` long white socks with black shorts — jenis=celana_pendek(64) | tema=sekolah(13)/coquette(11) | subjek=musik(9)/logo(5) | pola=polos(27) | panjang=selutut fit=lebar | [gambar:formal] | gender=cewek(23, 1 bukti)
- `16672528790` ♡ cookie muncher slippers — jenis=zirah_bawah(44) | tema=kostum_hewan(22)/steampunk(17) | subjek=beruang(36)/anjing(22) | pola=motif_hewan(79) | panjang=pendek fit=lebar | [gambar:kostum_hewan] | gender=cewek(17, 3 bukti) | MESH 3D: 1.6x1.1x1.6 stud
- `5957149174` White socks — jenis=bawahan_gaun(22) | tema=kawaii(14)/malaikat(11) | subjek=logo(10)/kartun(4) | pola=renda(46) | panjang=pendek fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=cewek(46, 1 bukti) | DIUKUR: kaus kaki/stoking
- `9353911507` Cute Blue Checkered Goth Pleated Skirt — jenis=rok_pendek(71) | tema=gothic(21)/kawaii(18) | subjek=musik(35)/bendera(8) | pola=kotak(64) | panjang=pendek fit=lebar | [gambar:punk] | gender=cewek(60, 2 bukti) | MESH 3D: 1.4x1.0x0.9 stud, rok/gaun, panjang pendek
- `5421181242` Formals- — jenis=celana_kain(39) | tema=formal(26)/biasa(18) | subjek=salib(5)/bintang(4) | pola=polos(71) | panjang=pendek fit=lebar | [gambar:formal] | gender=netral(0, 3 bukti)
- `6532841633` Cute shorts — jenis=celana_pendek(61) | tema=kawaii(47)/musim_dingin(9) | subjek=hiu(7)/hantu(6) | pola=denim(81) | panjang=pendek fit=lebar | [gambar:kawaii] | gender=cewek(2, 1 bukti) | temaBukti=kawaii(3 poin)
- `12788724664` Long Flowy Skirt - Baby Pink — jenis=rok_panjang(53) | tema=gaun_elegan(73)/coquette(21) | subjek=pita(42)/bunga(17) | pola=pelangi(29) | panjang=panjang fit=ketat | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti) | MESH 3D: 4.5x3.5x4.5 stud, rok/gaun, melebar ke bawah, panjang panjang
- `5273235402` Ripped Aesthetic Blue Jeans Emo Da Hood Y2K Belt — jenis=jeans(95) | tema=y2k(21)/punk(20) | subjek=hantu(8)/hiu(5) | pola=denim(98) | panjang=panjang fit=lebar | [gambar:biasa] | fungsi=pakaian | DIUKUR: -
- `4725793170` Pink Crop w/ Checker Belt — jenis=jeans(41) | tema=kawaii(46)/pantai(6) | subjek=hantu(5)/tulisan(4) | pola=catur(70) | panjang=panjang fit=lebar | [gambar:kawaii] | gender=cewek(32, 1 bukti)
- `6060378538` Dante Dark Version [ - ] — jenis=celana_kain(33) | tema=formal(22)/biasa(6) | subjek=kelelawar(5)/salib(5) | pola=kulit(37) | panjang=panjang fit=lebar | [gambar:vampir] | fungsi=pakaian | gender=cewek(11, 1 bukti) | DIUKUR: -
- `89130457321680` Royal Lace Ruffle Dress (Black White) — jenis=bawahan_gaun(80) | tema=maid(58)/kerajaan(35) | subjek=pita(29)/salib(10) | pola=renda(67) | panjang=pendek fit=lebar | [gambar:maid] | gender=cewek(60, 2 bukti)
- `15726169059` ♡ fluffy platform slippers (brown) — jenis=zirah_bawah(17) | tema=musim_dingin(44)/medis(7) | subjek=bebek(14)/hati(11) | pola=bulu(63) | panjang=selutut fit=lebar | [gambar:musim_dingin] | gender=cewek(22, 8 bukti) | temaBukti=musim_dingin(4 poin) | MESH 3D: 1.6x0.5x1.2 stud
- `86272365822277` White Elf hunter leather pants — jenis=kargo(47) | tema=militer(47)/ksatria(46) | subjek=naga(26)/ular(15) | pola=loreng(61) | panjang=pendek fit=lebar | [gambar:militer] | temaBukti=militer(3 poin)
- `15226415079` Cozy Winter Slippers - Brown — jenis=kargo(21) | tema=musim_dingin(95)/natal(1) | subjek=makanan(22)/beruang(15) | pola=bulu(91) | panjang=selutut fit=lebar | [gambar:musim_dingin] | gender=cewek(35, 1 bukti) | temaBukti=musim_dingin(4 poin) | MESH 3D: 1.5x0.5x1.1 stud
- `4762130536` pink softie skirt — jenis=rok_pendek(78) | tema=kawaii(81)/coquette(9) | subjek=bunga(10)/buah(10) | pola=garis(20) | panjang=pendek fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(70, 3 bukti) | DIUKUR: kaus kaki/stoking
- `5128013219` rainbow — jenis=legging(26) | tema=kawaii(68)/pantai(4) | subjek=hantu(8)/bendera(5) | pola=pelangi(99) | panjang=panjang fit=ketat | [gambar:kawaii] | gender=cewek(53, 2 bukti)
- `7034600998` angel  — jenis=bawahan_gaun(73) | tema=malaikat(54)/biasa(5) | subjek=laba_laba(6)/hantu(5) | pola=renda(26) | panjang=pendek fit=lebar | [gambar:formal] | fungsi=pakaian | gender=cewek(32, 1 bukti) | DIUKUR: menutup badan
- `75936305295884` green trendy shorts — jenis=celana_pendek(83) | tema=sporty(70)/pantai(12) | subjek=katak(20)/logo(10) | pola=tulisan(49) | panjang=pendek fit=lebar | [gambar:sporty] | gender=cewek(31, 1 bukti) | MESH 3D: 1.2x1.1x0.8 stud, celana, panjang pendek
- `96024847073208` ✨Pop Star Puff Sleeve Mini Dress-Black Leopard — jenis=bawahan_gaun(65) | tema=maid(60)/vampir(13) | subjek=bintang(35)/salib(8) | pola=motif_hewan(36) | panjang=pendek fit=lebar | [gambar:maid] | gender=cewek(60, 2 bukti)
- `1022938771` jeans — jenis=jeans(97) | tema=biasa(27)/kawaii(15) | subjek=tanpa(6)/hiu(6) | pola=denim(98) | panjang=panjang fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(9, 1 bukti) | DIUKUR: -
- `83611801532805` ♡. cozy cute light brown winter uggs slippers — jenis=zirah_bawah(35) | tema=medis(25)/kawaii(20) | subjek=hati(13)/mahkota(12) | pola=garis(18) | panjang=pendek fit=lebar | [gambar:medis] | gender=cewek(32, 1 bukti) | MESH 3D: 1.6x0.6x1.2 stud
- `17650103786` Cat Suit — jenis=jeans(34) | tema=kostum_hewan(40)/formal(35) | subjek=kucing(95)/labu(1) | pola=motif_hewan(68) | panjang=selutut fit=ketat | [gambar:kostum_hewan] | MESH 3D: 3.6x7.5x7.8 stud, celana
- `6537715059` 333 — jenis=jeans(36) | tema=formal(17)/biasa(11) | subjek=kelelawar(7)/tanpa(5) | pola=denim(77) | panjang=selutut fit=lebar | [gambar:formal] | gender=netral(0, 1 bukti)
- `6472210678` Y2K — jenis=celana_pendek(44) | tema=y2k(47)/streetwear(8) | subjek=buah(5)/kelelawar(5) | pola=denim(63) | panjang=pendek fit=ketat | [gambar:formal] | fungsi=pakaian | gender=cewek(37, 1 bukti) | DIUKUR: kaus kaki/stoking
- `4455908400` Macacão Azul — jenis=bawahan_gaun(23) | tema=kostum_hewan(15)/pantai(12) | subjek=hiu(15)/logo(6) | pola=bulu(39) | panjang=pendek fit=lebar | [gambar:musim_dingin] | fungsi=pakaian | gender=cewek(25, 1 bukti) | DIUKUR: menutup badan, kaus kaki/stoking

### kepala
- `6098124104` Pink Flower Crown — jenis=pita_bando(60) | tema=coquette(49)/kerajaan(35) | subjek=bunga(75)/mahkota(18) | [gambar:coquette] | gender=cewek(23, 1 bukti)
- `12103231132` AO Crazy Ball Head — jenis=topeng_kepala(50) | tema=novelty(13)/badut(7) | subjek=mata(23)/bebek(16) | [gambar:novelty] | gender=cewek(2, 45 bukti)
- `3706578589` Sushi Chef Hat — jenis=topi_lain(38) | tema=ninja(13)/sekolah(8) | subjek=musik(13)/tanpa(9) | [gambar:ninja]
- `12146169621` Void Head — jenis=topeng_kepala(38) | tema=polisi(26)/militer(18) | subjek=tanpa(35)/salib(6) | [gambar:polisi] | gender=netral(0, 1 bukti)
- `12659496899` 🌺 Flower Headphones 🌺 — jenis=headphone(67) | tema=peri(66)/natal(20) | subjek=bunga(99)/buah(1) | [gambar:peri] | gender=cewek(1, 1 bukti)
- `7483694265` Mr.Moon with its Bunny Hat — jenis=topi_lain(40) | tema=peri(59)/kawaii(28) | subjek=kelinci(36)/bebek(23) | [gambar:peri] | gender=cewek(5, 39 bukti)
- `7046021759` Yellow Axolotl Head — jenis=topeng_kepala(39) | tema=kawaii(26)/malaikat(21) | subjek=bebek(34)/mahkota(10) | [gambar:kawaii] | gender=cowok(1, 1 bukti)
- `7061587066` Upside-down China bowl — jenis=kupluk(30) | tema=tradisional(27)/natal(23) | subjek=bunga(16)/bendera(11) | [gambar:tradisional] | gender=cowok(3, 1 bukti)
- `7969727356` Black Tactical Gamer Headphone — jenis=headphone(91) | tema=militer(41)/polisi(30) | subjek=tanpa(15)/musik(11) | [gambar:polisi] | gender=cowok(1, 4 bukti)
- `114549646` ROBLOX Sailor Hat — jenis=topi_lain(40) | tema=bajak_laut(54)/sporty(8) | subjek=tanpa(27)/logo(8) | [gambar:bajak_laut] | gender=cowok(32, 1 bukti)
- `12651685566` Classic Skybox Top Hat — jenis=topi_formal(40) | tema=kawaii(40)/malaikat(33) | subjek=bunga(16)/bulan(14) | [gambar:kawaii] | gender=cowok(1, 1 bukti)
- `5028697470` White Haunted Rabbit Mask — jenis=telinga(53) | tema=kostum_hewan(84)/biasa(1) | subjek=kelinci(98)/hantu(1) | [gambar:kostum_hewan] | gender=netral(0, 1 bukti)
- `48894692` Evil Duck — jenis=topi_formal(22) | tema=iblis(44)/vampir(18) | subjek=bebek(98)/kelelawar(0) | [gambar:iblis] | gender=cowok(2, 13 bukti)
- `5354938243` Cardio Cans — jenis=headphone(91) | tema=coquette(32)/pantai(9) | subjek=hati(16)/musik(12) | [gambar:coquette] | gender=netral(0, 254 bukti)
- `10386280277` GENK Beanie — jenis=kupluk(99) | tema=musim_dingin(74)/streetwear(11) | subjek=tanpa(11)/logo(10) | [gambar:musim_dingin] | gender=cowok(27, 1 bukti)
- `4459330146` Cartoony Santa — jenis=halo(26) | tema=natal(91)/novelty(1) | subjek=buah(29)/makanan(16) | [gambar:natal] | gender=netral(0, 3 bukti) | temaBukti=natal(3 poin)
- `12518279793` Hairclips — jenis=anting(33) | tema=kostum_hewan(19)/biasa(7) | subjek=rantai(35)/bulan(17) | [gambar:kostum_hewan] | gender=cewek(1, 1 bukti)
- `10235265261` Tall Fluffy Fox Ears — jenis=telinga(49) | tema=musim_dingin(36)/antariksa(25) | subjek=kelelawar(18)/hiu(16) | [gambar:antariksa]
- `73790802` Lion's hood — jenis=tudung(40) | tema=kerajaan(24)/kostum_hewan(20) | subjek=kelelawar(27)/mahkota(15) | [gambar:kerajaan] | gender=cowok(13, 2 bukti)
- `283749451` Stone Cold Viking — jenis=tanduk(34) | tema=ksatria(49)/iblis(15) | subjek=kelelawar(37)/tengkorak(21) | [gambar:ksatria]
- `5535028025` Butterfly Earrings — jenis=anting(89) | tema=kerajaan(48)/malaikat(10) | subjek=kupu_kupu(36)/rantai(17) | [gambar:kerajaan] | gender=cewek(18, 5 bukti)
- `8714814268` Purple Fish Cake Hair Clip — jenis=headphone(23) | tema=penyihir(19)/ninja(11) | subjek=makanan(36)/bulan(11) | [gambar:penyihir] | gender=cowok(5, 2 bukti)
- `6351186573` Silver Star Hair Clip — jenis=mahkota(61) | tema=steampunk(22)/punk(22) | subjek=bintang(42)/rantai(37) | [gambar:steampunk] | gender=cewek(1, 2 bukti)
- `44113968` Kuddle E. Koala — jenis=kupluk(74) | tema=kostum_hewan(41)/musim_dingin(13) | subjek=beruang(86)/kartun(2) | [gambar:kostum_hewan] | gender=netral(0, 2 bukti)
- `11380606348` Black Overgrown — jenis=mahkota(35) | tema=gothic(55)/tradisional(7) | subjek=laba_laba(21)/buah(10) | [gambar:gothic] | gender=cewek(17, 1 bukti)

### rambut
- `5920341268` Brown Side Sweep Hair — tema=steampunk(19)/koboi(11) | [gambar:steampunk] | gender=cowok(6, 4 bukti)
- `14230035540` Blonde Soft Flowy Headband Hair — tema=coquette(8)/kawaii(7) | [gambar:coquette] | gender=cewek(24, 1 bukti)
- `13514386292` Black Flowy Long Straight Hime Cut w/ Bangs — tema=gothic(69)/horor(6) | [gambar:gothic] | gender=cewek(50, 1 bukti)
- `417457909` Candy Apple Hair — tema=natal(47)/badut(18) | [gambar:natal] | gender=netral(0, 2 bukti)
- `158066100` Master Fighter — tema=iblis(38)/vampir(20) | [gambar:iblis] | gender=cowok(45, 1 bukti)
- `11307205484` Miraculous Blue Soft Layers — tema=kawaii(78)/musim_dingin(3) | [gambar:kawaii] | gender=cewek(26, 1 bukti)
- `13811982287` Fluffy Messy Hair (Blonde) — tema=musim_dingin(37)/kawaii(11) | [gambar:kawaii] | gender=cewek(9, 1 bukti)
- `9237609885` Brown Short Hair with Bow Pigtails — tema=coquette(52)/sekolah(11) | [gambar:coquette] | gender=cewek(60, 2 bukti) | temaBukti=coquette(3 poin)
- `12581448928` Layered Messy Mullet in Black — tema=ksatria(15)/gothic(14) | [gambar:ksatria] | gender=cowok(29, 6 bukti)
- `6311254370` Red Messy Dreads — tema=iblis(32)/horor(30) | [gambar:iblis] | gender=netral(0, 2 bukti)
- `12725985163` Low Pigtails with Ribbons(Silver) — tema=coquette(52)/kawaii(46) | [gambar:kawaii] | gender=cewek(85, 3 bukti)
- `12932396064` Long Tied Messy Side Part Hair (Black) — tema=iblis(18)/vampir(13) | [gambar:iblis] | gender=netral(0, 2 bukti)
- `13895376541` Cute Half up Half Down Pigtails(White) — tema=kawaii(42)/malaikat(34) | [gambar:malaikat] | gender=cewek(61, 3 bukti)
- `15101593554` Cute Pastel Pink Aesthetic Curled Pigtails — tema=kawaii(94)/coquette(5) | [gambar:kawaii] | gender=cewek(71, 3 bukti) | temaBukti=kawaii(3 poin)
- `10948141979` Country Girl Pink Braids — tema=kawaii(79)/coquette(18) | [gambar:kawaii] | gender=cewek(78, 3 bukti)
- `11236763300` Kawaii Low Buns in Blonde — tema=kawaii(49)/coquette(6) | [gambar:kawaii] | gender=cewek(8, 1 bukti) | temaBukti=kawaii(3 poin)
- `7097937736` Black Mullet Undercut Hair Attachment — tema=gothic(16)/halloween(11) | [gambar:gothic] | gender=netral(0, 1 bukti)
- `14148281805` Y2K Wavy Hair Pink — tema=kawaii(47)/y2k(35) | [gambar:kawaii] | gender=cewek(31, 1 bukti)
- `15314246627` Scene queen XD in  epic rainbow — tema=kerajaan(18)/punk(18) | [gambar:badut] | gender=cewek(2, 1 bukti)
- `13515090062` Messy Lush Grunge Low Bun Brown — tema=punk(36)/medis(7) | [gambar:medis] | gender=cewek(31, 1 bukti)
- `12967513033` Siren TwinTails in Brown — tema=coquette(35)/gothic(8) | [gambar:coquette] | gender=cewek(8, 1 bukti)
- `501965259` Neon Orange Charmer — tema=cyber(35)/iblis(18) | [gambar:iblis] | gender=cowok(1, 1 bukti)
- `14427207224` Beachy Waves Pink — tema=kawaii(62)/coquette(23) | [gambar:kawaii] | gender=cewek(35, 1 bukti)
- `12670825546` Preppy — tema=vampir(41)/gothic(39) | [gambar:vampir]
- `15294026484` Messy Fluffy Spiky Anime Hair in Black — tema=anime(18)/musim_dingin(18) | [gambar:gothic] | gender=cowok(16, 1 bukti)

### sepatu
- `77030580782532` LED Tracks - Right Shoe Accessory — tema=antariksa(27)/cyber(26) | [gambar:antariksa] | gender=netral(0, 1 bukti) | MESH 3D: 0.5x0.5x1.0 stud
- `82177998186139` Chunky Sneakers Pink White — tema=kawaii(62)/coquette(15) | [gambar:kawaii]
- `92919996273622` Black Heart Chain Fur Platform Boots — tema=punk(61)/gothic(34) | [gambar:punk]
- `90707742241051` Sports running shoes — tema=sporty(31)/iblis(27) | [gambar:sporty]
- `85970668508162` ꒰ Japanese platform frilled socks mary janes Pink — tema=kawaii(60)/coquette(31) | [gambar:kawaii]
- `76771439328614` Doll Platform Shoes - Right Shoe Accessory — tema=musim_dingin(22)/maid(21) | [gambar:musim_dingin] | gender=cewek(24, 7 bukti) | MESH 3D: 0.9x1.5x1.3 stud, bot
- `83468433488916` red star doll mary janes — tema=natal(23)/iblis(22) | [gambar:natal]
- `85641749194583` Glossy Black Red S… - Acessório de calçado direito — tema=gaun_elegan(57)/gothic(12) | [gambar:gaun_elegan] | gender=cewek(32, 3 bukti) | MESH 3D: 0.3x0.7x0.8 stud, bot
- `79170183943893` Pink High Lace Heels Doll Platform Heel Boots Bow — tema=coquette(75)/kawaii(19) | [gambar:coquette] | temaBukti=coquette(3 poin)
- `84968589712044` Big Blobfish Slipper Feet — tema=kawaii(48)/coquette(7) | [gambar:kawaii]
- `74378617083258` Slippers w/ Socks — tema=militer(22)/polisi(10) | [gambar:militer]
- `72504219265850` Chunky Platform Boots w/ Grey Leg Warmers Socks — tema=maid(13)/musim_dingin(11) | [gambar:maid]
- `81102519822773` Fluffy White Slippers — tema=musim_dingin(41)/tradisional(11) | [gambar:tradisional]
- `78473503422766` Dark Red Boots Shoes 3.0 — tema=iblis(25)/vampir(9) | [gambar:iblis]
- `89667946608219` Baby Blue Classic Clogs — tema=musim_dingin(22)/y2k(15) | [gambar:musim_dingin]
- `83283198600178` Charm Clogs with Socks (Brown) — tema=antariksa(22)/kawaii(14) | [gambar:antariksa]
- `89100802272452` White Thigh High Boots — tema=militer(17)/polisi(10) | [gambar:militer]
- `96725270890789` summer chunky shoes / yellow — tema=pantai(35)/malaikat(34) | [gambar:malaikat]
- `92618352005127` Gloss Black Shoes — tema=formal(43)/gothic(17) | [gambar:formal]
- `73393923863667` Brown Leather Clogs — tema=pantai(31)/tradisional(16) | [gambar:pantai]
- `87006571792120` Blue Sneakers — tema=medis(23)/badut(19) | [gambar:medis]
- `82603218059943` Blue Fire Fur Snuggle Platform Boots — tema=musim_dingin(61)/pantai(8) | [gambar:musim_dingin]
- `85042398716921` Lamborghini Shoes — tema=vampir(13)/kostum_hewan(10) | [gambar:vampir]
- `94351852014659` cute pink doll platform y2k shoes + leg warmers — tema=kawaii(50)/coquette(25) | [gambar:kawaii]
- `87061440633882` Trendy Cosy Fall Grey Slippers with Socks — tema=streetwear(16)/musim_dingin(15) | [gambar:streetwear]

### wajah
- `5703030397` Cute Kitty Bandage — jenis=riasan(63) | tema=kawaii(80)/coquette(17) | subjek=kucing(80)/kelinci(8) | [gambar:kawaii] | gender=cewek(16, 1 bukti) | temaBukti=kawaii(4 poin)
- `6742065469` Black Goth Mask — jenis=masker(51) | tema=gothic(51)/bajak_laut(31) | subjek=rantai(75)/bulan(3) | [gambar:bajak_laut] | gender=cewek(43, 1 bukti)
- `13514089177` Glasses — jenis=kacamata(95) | tema=superhero(13)/formal(12) | subjek=logo(12)/tanpa(9) | [gambar:superhero] | gender=cewek(30, 2 bukti)
- `4855031321` Silver Rectangle Shades — jenis=kacamata(48) | tema=cyber(19)/anime(12) | subjek=tanpa(20)/salib(11) | [gambar:cyber] | gender=cowok(8, 12 bukti)
- `6347861285` Heart Flip-Up Sunglasses (Purple) — jenis=kacamata_hitam(58) | tema=peri(45)/kawaii(10) | subjek=hati(51)/kupu_kupu(14) | [gambar:peri]
- `13521537091` Eyepatch — jenis=penutup_mata(51) | tema=maid(42)/medis(9) | subjek=hati(87)/pita(5) | [gambar:maid]
- `15685748398` Ski Mask — jenis=masker(54) | tema=malaikat(37)/bajak_laut(9) | subjek=hantu(58)/salib(9) | [gambar:malaikat] | gender=cewek(10, 1 bukti)
- `14131541549` Bloody Hand Print - White — jenis=riasan(32) | tema=horor(36)/maid(11) | subjek=tanpa(9)/tulisan(6) | [gambar:maid] | gender=cewek(1, 2 bukti)
- `15685781277` Purple Designer Ski Mask — jenis=masker(38) | tema=penyihir(26)/halloween(10) | subjek=laba_laba(18)/tulisan(12) | [gambar:penyihir] | gender=cowok(27, 1 bukti)
- `12359400692` Red Aviator Rimmed Glasses Frame - Cartoony — jenis=kacamata(97) | tema=medis(17)/natal(15) | subjek=bendera(15)/logo(10) | [gambar:medis]
- `16068784881` Goth Knife Earrings — jenis=tindik(80) | tema=gothic(75)/ksatria(11) | subjek=salib(56)/bulan(12) | [gambar:gothic] | gender=cewek(18, 1 bukti) | temaBukti=gothic(3 poin)
- `15362998709` Flushing Stare Mask (Black) — jenis=masker(62) | tema=gothic(34)/horor(13) | subjek=hantu(27)/tengkorak(20) | [gambar:gothic] | gender=cewek(59, 1 bukti)
- `13945476059` Red Flower Blindfold — jenis=riasan(47) | tema=peri(49)/horor(8) | subjek=bunga(97)/hati(0) | [gambar:peri] | gender=cewek(1, 1 bukti)
- `11113896935` Black Decorated Eyepatch — jenis=penutup_mata(59) | tema=bajak_laut(39)/medis(26) | subjek=salib(31)/musik(20) | [gambar:bajak_laut] | gender=cewek(2, 1 bukti)
- `14977261730` Sukuna — jenis=kacamata(38) | tema=iblis(22)/steampunk(15) | subjek=wajah_anime(18)/mata(16) | [gambar:iblis] | gender=netral(0, 1 bukti)
- `4708712941` Kunai — jenis=tindik(48) | tema=bajak_laut(26)/ninja(24) | subjek=salib(20)/petir(17) | [gambar:bajak_laut] | gender=cewek(31, 1 bukti)
- `12717171813` Faceless Head (Dark Grey) • Blank Dummy No Face — jenis=penutup_mata(32) | tema=militer(39)/polisi(12) | subjek=tanpa(31)/logo(8) | [gambar:militer] | gender=cewek(28, 1 bukti)
- `14182306688` Troll Face — jenis=riasan(50) | tema=novelty(38)/badut(36) | subjek=kartun(12)/rantai(11) | [gambar:badut] | gender=cowok(29, 1 bukti)
- `12122626960` Curly Bangs in Brown — jenis=kumis_jenggot(58) | tema=gothic(32)/steampunk(21) | subjek=pita(24)/bulan(19) | [gambar:gothic] | gender=cowok(26, 1 bukti)
- `6590377982` Heroic Hero Visor — jenis=kacamata_hitam(58) | tema=superhero(38)/pantai(19) | subjek=katak(24)/dinosaurus(13) | [gambar:pantai] | gender=cewek(1, 1 bukti)
- `14847602991` Halloween Spiked Shades — jenis=kacamata_hitam(43) | tema=halloween(36)/steampunk(20) | subjek=mahkota(26)/labu(14) | [gambar:steampunk] | gender=netral(0, 2 bukti)
- `15612516004` Cute Kawaii Squinting Cosplay Blushing Tone Mask — jenis=masker(50) | tema=kawaii(25)/anime(18) | subjek=kucing(20)/hantu(17) | [gambar:musim_dingin] | gender=cewek(64, 2 bukti)
- `11118703485` swordsman face with scar — jenis=masker(32) | tema=ninja(11)/koboi(8) | subjek=wajah_anime(23)/kartun(11) | [gambar:ninja] | gender=cewek(3, 1 bukti)
- `10075023045` Black Surgical Mask — jenis=masker(41) | tema=bajak_laut(25)/polisi(13) | subjek=bendera(14)/bulan(8) | [gambar:bajak_laut] | gender=cowok(11, 7 bukti)
- `13988612164` Tongue Piercing (Narrow Head) — jenis=tindik(42) | tema=vampir(11)/natal(10) | subjek=hiu(38)/bintang(10) | [gambar:vampir] | gender=cewek(20, 1 bukti)

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 296, malaikat 192, gothic 176, coquette 156, formal 138, kostum_hewan 131, punk 108, steampunk 101, iblis 100, cyber 98, peri 97, militer 97
- atas: kawaii 804, formal 691, biasa 271, sporty 247, punk 239, gothic 238, militer 218, coquette 197, y2k 188, novelty 172, cyber 164, halloween 162
- bawah: formal 654, kawaii 618, y2k 422, biasa 349, gothic 326, punk 286, sekolah 264, coquette 248, musim_dingin 240, militer 191, maid 175, halloween 159
- kepala: coquette 234, kawaii 214, kerajaan 183, formal 166, malaikat 151, militer 142, gothic 125, peri 112, kostum_hewan 110, iblis 99, penyihir 98, antariksa 93
- rambut: kawaii 427, gothic 389, coquette 228, anime 182, gaun_elegan 171, steampunk 170, koboi 150, musim_dingin 145, punk 138, malaikat 119, iblis 90, y2k 86
- sepatu: kawaii 344, coquette 248, gothic 247, sporty 202, musim_dingin 191, y2k 158, kostum_hewan 150, pantai 129, militer 115, punk 110, gaun_elegan 99, formal 88
- wajah: kawaii 436, steampunk 235, gothic 183, militer 170, cyber 161, coquette 138, malaikat 93, anime 88, polisi 82, iblis 77, vampir 70, pantai 69
