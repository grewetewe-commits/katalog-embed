# Laporan Kartu Item (MATA v2) — versi 1792190376

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **137574**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 12089 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7764 | 0.0 | 57% | 68% | 57% | 54% |
| aksen/tema | 7970 | 0.75 | 29% | 42% | 28% | 28% |
| atas2D/jenis | 5988 | 1.0 | 15% | 24% | 8% | 15% |
| atas2D/pola | 1107 | 1.0 | 50% | 63% | 47% | 50% |
| atas2D/subjek | 2205 | 0.5 | 33% | 43% | 31% | 32% |
| atas2D/tema | 4444 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5495 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2101 | 0.75 | 55% | 66% | 51% | 53% |
| atas3D/subjek | 2036 | 0.25 | 31% | 41% | 31% | 29% |
| atas3D/tema | 3432 | 0.75 | 30% | 40% | 27% | 30% |
| bawah2D/jenis | 4121 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2468 | 1.0 | 44% | 56% | 35% | 44% |
| bawah2D/subjek | 1774 | 0.75 | 15% | 22% | 12% | 14% |
| bawah2D/tema | 4165 | 0.5 | 25% | 31% | 21% | 23% |
| bawah3D/jenis | 3219 | 0.75 | 52% | 72% | 50% | 52% |
| bawah3D/pola | 2018 | 1.0 | 50% | 62% | 45% | 50% |
| bawah3D/subjek | 957 | 0.25 | 28% | 36% | 28% | 25% |
| bawah3D/tema | 2011 | 0.25 | 21% | 30% | 21% | 19% |
| kepala/jenis | 9983 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5550 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 7159 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5391 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2357 | 0.5 | 22% | 32% | 21% | 20% |
| wajah/jenis | 3797 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1610 | 0.0 | 47% | 54% | 47% | 45% |
| wajah/tema | 2180 | 1.0 | 22% | 35% | 15% | 22% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Bukti (rev 31): gender & tema dari bukti, bukan tebakan satu sumber

Outfit buatan manusia dipakai sebagai bukti pemakaian: **76759**.

### Gender (uji jujur: benih nama 20% item disembunyikan, ditebak dari pemakaian)

| ambang | benar | diputuskan | item uji |
|---|---|---|---|
| 0.1 | 1561 (95.4%) | 1637 | 2761 |
| 0.15 | 1432 (95.7%) | 1496 | 2761 |
| 0.25 | 1161 (97.2%) | 1194 | 2761 |

### Tema berbukti vs label emas (baju/celana 2D)

| tipe | n | diputuskan | tepat saat diputuskan | kartu lama tepat |
|---|---|---|---|---|
| 11 | 37 | 8 | 8 | 22 |
| 12 | 23 | 4 | 3 | 12 |

Item bertema berbukti: 16297 dari 137574 (sisanya tidak bertema khusus).

Sebaran: kawaii 2875, coquette 1584, formal 1513, halloween 1348, militer 1137, kerajaan 884, sporty 789, malaikat 638, gothic 615, punk 583, koboi 479, ksatria 470, natal 439, penyihir 262, iblis 252, musim_dingin 241, anime 208, antariksa 197, pantai 182, superhero 172, cyber 166, gaun_elegan 157, badut 148, peri 119, polisi 110

### Sambungan tema (PMI positif, dari outfit manusia)

- kawaii: coquette (0.22, 474)
- kerajaan: steampunk (0.36, 14), peri (0.31, 90), pantai (0.06, 29)
- formal: penyihir (0.37, 6), steampunk (0.26, 10)
- coquette: malaikat (0.31, 76), kawaii (0.22, 474), gaun_elegan (0.12, 11), peri (0.02, 48)
- militer: cyber (0.36, 8), koboi (0.02, 9)
- punk: gothic (0.76, 46), vampir (0.62, 6), iblis (0.48, 17), peri (0.34, 24)
- gothic: vampir (0.82, 6), iblis (0.79, 19), punk (0.76, 46)
- malaikat: peri (1.05, 37), iblis (0.62, 15), coquette (0.31, 76)
- peri: horor (1.50, 5), malaikat (1.05, 37), iblis (1.03, 19), punk (0.34, 24), kerajaan (0.31, 90)
- musim_dingin: natal (0.52, 9)
- iblis: vampir (1.54, 6), peri (1.03, 19), gothic (0.79, 19), malaikat (0.62, 15), punk (0.48, 17)
- natal: musim_dingin (0.52, 9)
- pantai: kerajaan (0.06, 29)
- koboi: militer (0.02, 9)
- cyber: militer (0.36, 8)
- gaun_elegan: coquette (0.12, 11)
- vampir: iblis (1.54, 6), gothic (0.82, 6), punk (0.62, 6)

## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)

Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,
celana tema 35%, pola 39-40%, kaos fungsi belum ada.

| tipe | facet | n | benar | akurasi | tanpa kartu |
|---|---|---|---|---|---|
| baju 2D | jenis | 57 | 28 | 49% | 0 |
| baju 2D | tema | 37 | 22 | 59% | 0 |
| baju 2D | pola | 54 | 15 | 28% | 0 |
| baju 2D | fungsi | 39 | 38 | 97% | 21 |
| celana 2D | jenis | 43 | 24 | 56% | 0 |
| celana 2D | tema | 23 | 12 | 52% | 0 |
| celana 2D | pola | 48 | 20 | 42% | 0 |
| celana 2D | fungsi | 39 | 38 | 97% | 20 |
| kaos klasik | fungsi | 55 | 48 | 87% | 0 |

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween] | gender=netral(0, 254 bukti) | temaBukti=halloween(3 poin)
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi] | gender=cowok(6, 5 bukti) | temaBukti=koboi(5 poin)
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut] | gender=cowok(2, 2 bukti) | temaBukti=bajak_laut(4 poin)
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(45)/mata(17) | [gambar:steampunk] | gender=cowok(6, 10 bukti)
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(53) | tema=maid(66)/punk(4) | subjek=salib(6)/rantai(6) | pola=bulu(23) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:maid] | fungsi=pakaian | gender=cewek(76, 41 bukti) | temaBukti=maid(3 poin) | DIUKUR: leher 21%
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=rompi(33) | tema=formal(70)/gothic(4) | subjek=kelelawar(10)/salib(8) | pola=bulu(27) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:formal] | fungsi=pakaian | gender=cowok(6, 105 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 5%
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat] | gender=cewek(4, 61 bukti) | temaBukti=malaikat(4 poin)
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(51)/bulan(35) | [gambar:steampunk] | gender=cowok(4, 4 bukti)
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(75) | tema=kawaii(68)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(96) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(44, 42 bukti) | temaBukti=kawaii(3 poin) | DIUKUR: leher 24%, bahu terbuka
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal] | gender=cewek(18, 29 bukti)
- `382538059` Green Jersey (atas): jenis=jersey(92) | tema=sporty(96)/y2k(1) | subjek=katak(24)/bintang(9) | pola=bunga(25) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | fungsi=pakaian | gender=cewek(1, 254 bukti) | temaBukti=sporty(5 poin) | DIUKUR: leher 9%
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(39)/formal(25) | subjek=salib(23)/kelelawar(12) | pola=kulit(55) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | gender=cowok(1, 254 bukti) | MESH 3D: 2.8x1.9x0.8 stud, lengan panjang
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette] | gender=cewek(31, 51 bukti) | temaBukti=coquette(4 poin)
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(78) | tema=y2k(31)/punk(28) | subjek=bulan(6)/rantai(6) | pola=denim(87) | panjang=panjang fit=lebar | [gambar:gothic] | fungsi=pakaian | gender=cowok(68, 144 bukti) | DIUKUR: -
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(53) | tema=gothic(46)/punk(28) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(87) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber] | gender=netral(0, 1 bukti)
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii] | gender=cewek(28, 3 bukti)
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan] | gender=cowok(6, 32 bukti) | temaBukti=kerajaan(6 poin)
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(26)/tulisan(10) | [gambar:streetwear] | gender=cewek(4, 254 bukti)
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii] | gender=cewek(36, 1 bukti) | temaBukti=kawaii(3 poin)
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween] | gender=cewek(21, 3 bukti) | temaBukti=halloween(7 poin)
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=kaos(22) | tema=halloween(77)/kawaii(11) | subjek=labu(45)/beruang(19) | pola=pelangi(48) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=jeans(26) | tema=halloween(74)/kawaii(5) | subjek=labu(48)/beruang(18) | pola=kotak(26) | panjang=pendek fit=lebar | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=jaket(62) | tema=antariksa(67)/cyber(22) | subjek=wajah_anime(13)/tulisan(9) | pola=denim(29) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=cewek(6, 4 bukti)
- `1239904` Akatsuki — nama: anime | jenis=kaos(75) | tema=anime(73)/horor(4) | subjek=api(18)/buah(14) | pola=bulu(40) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:horor] | fungsi=grafis | gender=cowok(1, 3 bukti)
- `1260428` Guitar Hero 2 Logo — nama: superhero | jenis=kaos(90) | tema=superhero(74)/punk(9) | subjek=logo(28)/musik(26) | pola=kotak(26) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=cowok(1, 254 bukti)
- `1397335` Me with snow wolf shirt. — nama: musim_dingin | jenis=hoodie(51) | tema=musim_dingin(74)/streetwear(7) | subjek=kartun(9)/hiu(7) | pola=polos(27) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1431511` ninja shirt — nama: ninja | jenis=kaos(70) | tema=ninja(70)/biasa(6) | subjek=logo(25)/tulisan(9) | pola=garis(21) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(1, 72 bukti)
- `1475939` Noob shirt — nama: novelty | jenis=kaos(50) | tema=novelty(85)/cyber(2) | subjek=logo(8)/hati(7) | pola=pelangi(55) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(1, 43 bukti)
- `1515399` My cute kitty! :) — nama: kawaii | jenis=kaos(73) | tema=kawaii(54)/superhero(14) | subjek=kucing(76)/anjing(6) | pola=polkadot(77) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=netral(0, 2 bukti) | temaBukti=kawaii(4 poin)
- `1521989` shadow military lvl 1 — nama: militer | jenis=rompi(42) | tema=militer(62)/cyber(6) | subjek=logo(13)/katak(11) | pola=polos(28) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:pantai] | fungsi=grafis | gender=cowok(6, 2 bukti)
- `1558188` Random Anime Character I made — nama: anime | jenis=jas(33) | tema=anime(59)/superhero(11) | subjek=wajah_anime(39)/naga(8) | pola=polos(53) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:vampir] | fungsi=grafis | gender=cewek(4, 20 bukti)
- `1591061` Cute Wolf — nama: kawaii | jenis=kaos(71) | tema=kawaii(74)/punk(10) | subjek=anjing(69)/wajah_anime(5) | pola=grafis(71) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan] | fungsi=badan | gender=cewek(2, 9 bukti)
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(53) | tema=sporty(83)/y2k(12) | subjek=tulisan(37)/petir(13) | pola=polkadot(83) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1621982` Yellow Dragon of the Western Winds — nama: koboi | jenis=kemeja(55) | tema=koboi(55)/kerajaan(10) | subjek=naga(92)/dinosaurus(2) | pola=grafis(70) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | fungsi=grafis | gender=cewek(1, 15 bukti)
- `1636113` Ninja Drone Of Shadows Version 2 — nama: ninja | jenis=jas(45) | tema=ninja(62)/gothic(12) | subjek=laba_laba(87)/ular(1) | pola=renda(51) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(2, 24 bukti)
- `1639327` Cyber Suit35 — nama: cyber | jenis=kostum_penuh(38) | tema=cyber(53)/sporty(23) | subjek=logo(32)/bendera(10) | pola=garis(38) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(2, 3 bukti)
- `1639359` Cyber Suit31 — nama: cyber | jenis=jas(53) | tema=cyber(78)/ninja(3) | subjek=pita(24)/rantai(15) | pola=catur(43) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:pantai] | fungsi=aksesori | gender=cewek(9, 21 bukti)
- `1639368` Cyber Suit29 — nama: cyber | jenis=rompi(39) | tema=cyber(69)/kawaii(7) | subjek=bulan(7)/bunga(6) | pola=catur(93) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:peri] | fungsi=grafis | gender=cewek(3, 2 bukti)
- `1639414` Cyber Suit22 — nama: cyber | jenis=kaos(35) | tema=cyber(86)/streetwear(2) | subjek=bendera(16)/logo(15) | pola=catur(43) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:musim_dingin] | fungsi=aksesori | gender=cewek(2, 1 bukti)
- `1639419` Cyber Suit21 — nama: cyber | jenis=kaos(49) | tema=cyber(89)/malaikat(4) | subjek=petir(23)/hiu(12) | pola=pelangi(49) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:punk] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1639424` Cyber Suit20 — nama: cyber | jenis=kaos(55) | tema=cyber(60)/antariksa(16) | subjek=bulan(14)/petir(11) | pola=bunga(61) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(6, 23 bukti)
- `1639431` Cyber ###### — nama: cyber | jenis=jas(38) | tema=cyber(78)/penyihir(8) | subjek=bintang(15)/bulan(14) | pola=kilau(60) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(1, 2 bukti)
- `1639438` Cyber Suit18 — nama: cyber | jenis=jubah(57) | tema=cyber(60)/kawaii(5) | subjek=bulan(29)/hiu(17) | pola=garis(43) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:pantai] | fungsi=pakaian | gender=cewek(2, 1 bukti)
- `1639470` Cyber Suit14 — nama: cyber | jenis=kaos(22) | tema=cyber(55)/gothic(14) | subjek=bulan(27)/rantai(17) | pola=catur(51) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(4, 6 bukti)
- `1639518` Cyber ##### — nama: cyber | jenis=hoodie(41) | tema=cyber(93)/sporty(3) | subjek=hiu(18)/logo(17) | pola=kilau(30) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 6 bukti)
- `1648160` ninja — nama: ninja | jenis=jas(26) | tema=ninja(74)/badut(9) | subjek=logo(44)/tulisan(5) | pola=polkadot(37) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis | gender=netral(0, 4 bukti)
- `1726226` Cutsey_Cosplay_by_Halogrunt — nama: anime | jenis=kaos(37) | tema=anime(60)/badut(13) | subjek=kucing(27)/katak(17) | pola=bulu(49) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:badut] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1753596` Cowboy NeckHat — nama: koboi | jenis=kostum_penuh(65) | tema=koboi(68)/halloween(12) | subjek=labu(77)/makanan(3) | pola=bulu(50) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | fungsi=aksesori | gender=netral(0, 2 bukti) | temaBukti=halloween(3 poin)
- `1756352` cute — nama: kawaii | jenis=hoodie(36) | tema=kawaii(50)/novelty(22) | subjek=api(27)/petir(11) | pola=pelangi(83) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cewek(2, 2 bukti)
- `1769022` I-Pod tux — nama: formal | jenis=hoodie(38) | tema=formal(56)/y2k(12) | subjek=bebek(40)/logo(8) | pola=polkadot(43) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(23, 1 bukti)
- `1769048` Luke Tux — nama: formal | jenis=hoodie(44) | tema=formal(87)/kawaii(4) | subjek=bebek(31)/logo(11) | pola=bulu(54) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(4, 4 bukti)
- `1769060` Metal Tux — nama: formal | jenis=seragam(21) | tema=formal(55)/natal(17) | subjek=bebek(17)/katak(13) | pola=bulu(69) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:natal] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1769091` Robin Tux — nama: formal | jenis=jubah(40) | tema=formal(53)/novelty(9) | subjek=bebek(44)/katak(8) | pola=bulu(36) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769097` ROBO TUX BEEP BOOP BOP! — nama: formal | jenis=jas(53) | tema=formal(68)/novelty(9) | subjek=hati(41)/logo(12) | pola=pelangi(87) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cowok(1, 1 bukti) | temaBukti=formal(3 poin)
- `1769130` Spy Tux — nama: formal | jenis=jaket(40) | tema=formal(55)/cyber(17) | subjek=katak(20)/bebek(11) | pola=garis(48) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769138` Super Tux!!! — nama: formal | jenis=jaket(25) | tema=formal(70)/novelty(12) | subjek=bebek(33)/logo(8) | pola=pelangi(43) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:superhero] | fungsi=grafis | gender=cewek(4, 5 bukti)
- `1770016` School Icon — nama: sekolah | jenis=kaos(53) | tema=sekolah(60)/sporty(28) | subjek=beruang(75)/logo(10) | pola=grafis(40) | lengan=pendek panjang=crop fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1771956` Disco Tux — nama: formal | jenis=jubah(26) | tema=formal(52)/kawaii(11) | subjek=bebek(10)/kartun(8) | pola=bulu(91) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic] | fungsi=grafis | gender=cowok(5, 1 bukti)
- `1771962` Ingured Tux — nama: formal | jenis=hoodie(38) | tema=formal(63)/kawaii(13) | subjek=bebek(31)/logo(9) | pola=bulu(58) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1771965` Jedi Tux — nama: formal | jenis=hoodie(36) | tema=formal(84)/kawaii(7) | subjek=bebek(26)/logo(12) | pola=bulu(35) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cowok(4, 6 bukti)
- `1773652` LOOK A WATER DRIP!(shirt) — nama: streetwear | jenis=kaos(97) | tema=streetwear(79)/kerajaan(5) | subjek=bebek(29)/katak(12) | pola=pelangi(81) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:novelty] | fungsi=grafis | gender=netral(0, 3 bukti)
- `1781595` some tux's — nama: formal | jenis=jaket(35) | tema=formal(53)/novelty(14) | subjek=bebek(46)/tulisan(5) | pola=garis(53) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=netral(0, 3 bukti)

## Contoh acak per kelompok

### aksen
- `11311636820` Black Luxury Diamond Pattern Purse (3.0) — jenis=tas(73) | tema=y2k(14)/gothic(13) | subjek=logo(15)/bintang(9) | [gambar:y2k] | gender=cewek(32, 1 bukti)
- `5410262465` Laid-back Earbuds — jenis=ekor(26) | tema=medis(20)/polisi(12) | subjek=petir(35)/tanpa(16) | [gambar:medis] | gender=cewek(4, 32 bukti)
- `7436683003` Big Blue Backpack — jenis=tas(100) | tema=streetwear(28)/y2k(12) | subjek=logo(55)/tulisan(8) | [gambar:streetwear] | gender=cowok(1, 1 bukti)
- `9617838611` Clarks Shoelace Wings — jenis=sayap(89) | tema=gothic(21)/punk(12) | subjek=petir(47)/kelelawar(13) | [gambar:gothic] | gender=cewek(20, 1 bukti)
- `3798231832` Party Unicorn Floatie — jenis=boneka(40) | tema=badut(69)/natal(9) | subjek=bebek(18)/ular(9) | [gambar:badut] | gender=cowok(16, 2 bukti)
- `4604288766` Demon Tail — jenis=ekor(75) | tema=iblis(39)/bajak_laut(13) | subjek=bulan(26)/logo(10) | [gambar:bajak_laut] | gender=cewek(16, 2 bukti) | temaBukti=iblis(3 poin)
- `12590283275` Bubbles 🧼 — jenis=kalung(46) | tema=kawaii(35)/badut(11) | subjek=mata(14)/rantai(12) | [gambar:kawaii] | gender=cewek(10, 2 bukti)
- `501761204` Lady of the Federation Necklace — jenis=kalung(46) | tema=penyihir(48)/kerajaan(18) | subjek=salib(24)/bulan(17) | [gambar:penyihir] | gender=cewek(64, 3 bukti)
- `12338957564` Green Hero Cape — jenis=jubah_belakang(71) | tema=superhero(40)/militer(11) | subjek=bendera(42)/bintang(11) | [gambar:militer] | temaBukti=superhero(3 poin)
- `10370246842` Guitar I - George Ezra — jenis=alat_musik(99) | tema=koboi(62)/halloween(12) | subjek=musik(100)/bintang(0) | [gambar:koboi] | gender=cowok(1, 8 bukti)
- `7137829899` Silver Bestie Card Necklace (3.0) — jenis=kalung(86) | tema=medis(18)/pantai(10) | subjek=rantai(59)/logo(12) | [gambar:medis] | gender=cowok(21, 1 bukti)
- `7335482400` Skelly Necklace — jenis=kalung(67) | tema=halloween(34)/punk(31) | subjek=tengkorak(71)/rantai(23) | [gambar:halloween] | gender=cewek(10, 2 bukti)
- `12707514631` 🐇 Bunny Tail 🐇 — jenis=ekor(41) | tema=steampunk(8)/kostum_hewan(7) | subjek=kelinci(36)/tanpa(9) | [gambar:steampunk] | gender=cewek(1, 1 bukti)
- `11773315272` gold chain — jenis=kalung(94) | tema=steampunk(84)/kerajaan(7) | subjek=rantai(89)/ular(8) | [gambar:steampunk]
- `4315489767` Demonic Greatsword — jenis=senjata(89) | tema=iblis(44)/vampir(31) | subjek=petir(28)/salib(23) | [gambar:vampir] | gender=cewek(3, 4 bukti)
- `12323746251` Iceland Flag Pin — jenis=syal(61) | tema=bajak_laut(23)/antariksa(12) | subjek=bendera(100)/logo(0) | [gambar:bajak_laut] | gender=cewek(45, 1 bukti)
- `5410704851` Cat Tail with Bell n' Bow — jenis=ekor(88) | tema=coquette(78)/peri(17) | subjek=pita(38)/kucing(19) | [gambar:coquette] | gender=cowok(1, 1 bukti) | temaBukti=coquette(3 poin)
- `6201622259` Flag of Scotland — jenis=jubah_belakang(23) | tema=bajak_laut(35)/sekolah(8) | subjek=bendera(99)/tanpa(0) | [gambar:bajak_laut] | gender=cewek(56, 1 bukti)
- `335079187` Heroic Golden Wings — jenis=sayap(97) | tema=kerajaan(59)/steampunk(13) | subjek=mahkota(44)/kupu_kupu(20) | [gambar:kerajaan] | gender=netral(0, 1 bukti)
- `7604751147` Cute Wandering Ghost — jenis=jubah_belakang(44) | tema=kawaii(60)/halloween(13) | subjek=hantu(100)/kartun(0) | [gambar:kawaii] | gender=cewek(13, 1 bukti) | temaBukti=halloween(4 poin)
- `8657807761` TapWater — jenis=jubah_belakang(34) | tema=punk(25)/superhero(12) | subjek=tanpa(12)/rantai(10) | [gambar:punk] | gender=cowok(30, 1 bukti)
- `5940844989` Mech Wings — jenis=sayap(42) | tema=antariksa(36)/medis(10) | subjek=pita(31)/hiu(14) | [gambar:antariksa] | gender=netral(0, 2 bukti)
- `8028454043` Rainbow Thunder Aura - Waist — jenis=senjata(34) | tema=peri(57)/malaikat(6) | subjek=petir(39)/bunga(7) | [gambar:peri] | gender=netral(0, 1 bukti)
- `5188273581` Left Frozen Shards of Etralice — jenis=sayap(60) | tema=malaikat(48)/peri(14) | subjek=naga(39)/petir(14) | [gambar:malaikat] | gender=netral(0, 1 bukti)
- `6711923625` Miau Heart Necklace Black — jenis=kalung(63) | tema=medis(34)/biasa(8) | subjek=hati(40)/rantai(23) | [gambar:medis] | gender=cewek(41, 2 bukti)

### atas
- `4872424922` [+] Gold — jenis=zirah(83) | tema=ksatria(44)/kerajaan(9) | subjek=mahkota(29)/naga(5) | pola=kulit(41) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kerajaan] | fungsi=pakaian | gender=netral(0, 1 bukti) | DIUKUR: leher 3%
- `70899749071733` Fire Skull Hoodie Grey — jenis=hoodie(67) | tema=musim_dingin(22)/halloween(16) | subjek=tengkorak(77)/api(18) | pola=bunga(22) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:musim_dingin]
- `9186615466` ✅ Green — jenis=zirah(65) | tema=militer(93)/ninja(1) | subjek=katak(36)/pita(13) | pola=loreng(90) | lengan=panjang panjang=panjang fit=pas depan=terbuka | [gambar:militer] | gender=cewek(21, 1 bukti) | temaBukti=militer(3 poin) | MESH 3D: 3.0x1.4x0.7 stud, lengan panjang
- `13936761436` 💅Short Nails - Purple — jenis=tanktop(17) | tema=kawaii(31)/peri(11) | subjek=kucing(13)/hantu(8) | pola=kilau(23) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | gender=cewek(32, 1 bukti) | MESH 3D: 3.5x1.9x0.4 stud
- `13947644006` 💅Short Nails - Dark Beige — jenis=tanktop(19) | tema=koboi(27)/malaikat(8) | subjek=kucing(10)/beruang(7) | pola=motif_hewan(48) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:koboi] | gender=cewek(33, 1 bukti) | MESH 3D: 3.5x1.9x0.4 stud
- `3396770531` Unicorn Rainbow Outfit — jenis=hoodie(31) | tema=kawaii(82)/badut(6) | subjek=makanan(13)/pita(10) | pola=pelangi(100) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(51, 1 bukti) | DIUKUR: leher 29%, bahu terbuka
- `5341870490` Scientist — jenis=jas(40) | tema=formal(59)/medis(16) | subjek=tanpa(6)/pita(6) | pola=denim(23) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:formal] | fungsi=pakaian | gender=netral(0, 1 bukti) | DIUKUR: leher 0%
- `13323738902` Ben 10 Accessory - Ben 10 Omnitrix — jenis=zirah(76) | tema=steampunk(46)/cyber(24) | subjek=mata(25)/salib(18) | pola=polos(23) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:steampunk] | gender=netral(0, 2 bukti) | MESH 3D: 0.5x0.5x0.3 stud
- `1635952` Teapot Drone Version 2 — jenis=jas(54) | tema=cyber(16)/gothic(13) | subjek=laba_laba(82)/bunga(3) | pola=bulu(23) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:peri] | fungsi=badan | gender=cowok(11, 2 bukti)
- `70755505800431` Sleeveless Compass Hoodie (cream) — jenis=hoodie(37) | tema=steampunk(27)/militer(17) | subjek=laba_laba(18)/salib(11) | pola=loreng(48) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:steampunk]
- `12731877003` Cute Pink Bunny Plushie Suit Rabbit Costume — jenis=kostum_penuh(58) | tema=kawaii(73)/kostum_hewan(12) | subjek=kelinci(97)/kartun(1) | pola=polkadot(25) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii] | gender=cewek(1, 1 bukti) | temaBukti=kawaii(3 poin) | MESH 3D: 3.6x8.0x1.7 stud
- `4056542533` Demon Slayer- Tanjiro Final Selection [Top] — jenis=hoodie(28) | tema=anime(22)/iblis(18) | subjek=hiu(11)/naga(9) | pola=kilau(29) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:antariksa] | gender=cewek(8, 1 bukti)
- `12131961441` Kitty Paw Oversized Hoodie Brown — jenis=hoodie(61) | tema=anime(12)/kostum_hewan(12) | subjek=kucing(37)/beruang(5) | pola=grafis(22) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:anime]
- `4971578793` ପ kawaii white bear hoodie ♡ — jenis=hoodie(47) | tema=kawaii(71)/coquette(8) | subjek=beruang(37)/bunga(5) | pola=bulu(33) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(64, 2 bukti) | temaBukti=kawaii(4 poin) | DIUKUR: leher 0%, crop
- `18499676766` White Ruffled Lace Parasol — jenis=zirah(26) | tema=peri(21)/steampunk(19) | subjek=petir(33)/rantai(13) | pola=renda(41) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:peri] | gender=cewek(1, 1 bukti) | MESH 3D: 7.7x5.9x7.0 stud
- `14918540152` white dress shirt for office suits — jenis=kemeja(21) | tema=formal(95)/malaikat(2) | subjek=hantu(27)/pita(10) | pola=polos(63) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:formal]
- `4915220823` Zoro (look at Description) — jenis=seragam(16) | tema=horor(13)/anime(10) | subjek=katak(25)/ular(14) | pola=garis(51) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:militer] | fungsi=pakaian | gender=cewek(38, 2 bukti) | DIUKUR: leher 58%
- `356233101` Yellow Diamond Sweater Vest - CProductions — jenis=sweater(28) | tema=kerajaan(41)/streetwear(10) | subjek=mahkota(53)/pita(5) | pola=kilau(39) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:kerajaan] | gender=netral(0, 1 bukti)
- `6418303226` Terno com luvas — jenis=jas(97) | tema=formal(99)/vampir(0) | subjek=logo(7)/pita(6) | pola=kotak(34) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:formal] | fungsi=pakaian | gender=netral(0, 1 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 0%
- `6403870162` Black Thick Simple Spagetti Strap Top — jenis=tanktop(57) | tema=biasa(46)/y2k(9) | subjek=kelelawar(6)/kucing(5) | pola=polos(48) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:gothic] | fungsi=pakaian | gender=cewek(51, 1 bukti) | DIUKUR: leher 29%, bahu terbuka, crop
- `4965672059` PRTI Police Top - Vest, S.Sleeves, Gloves, Tattoos — jenis=rompi(69) | tema=polisi(76)/militer(5) | subjek=tengkorak(8)/salib(7) | pola=loreng(25) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:polisi] | fungsi=pakaian | gender=cowok(1, 1 bukti) | temaBukti=polisi(3 poin) | DIUKUR: leher 1%
- `12731790212` Cottage Picnic Basket Orange Daisies White Brown — jenis=crop(36) | tema=maid(34)/novelty(12) | subjek=makanan(53)/buah(39) | pola=bunga(40) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:maid]
- `16125880503` Rolled Up Black Longsleeve — jenis=lengan_panjang(53) | tema=streetwear(18)/polisi(14) | subjek=logo(28)/tanpa(24) | pola=polos(46) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:streetwear] | gender=cowok(6, 1 bukti) | MESH 3D: 2.4x2.0x0.8 stud, lengan pendek
- `9239653059` Anime Arm Bandages — jenis=tanktop(30) | tema=steampunk(46)/anime(35) | subjek=rantai(37)/wajah_anime(35) | pola=garis(54) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:steampunk] | gender=cewek(23, 7 bukti) | MESH 3D: 3.1x1.1x0.6 stud
- `5918710825` i dont wanna die pls work god — jenis=zirah(52) | tema=ksatria(17)/militer(14) | subjek=api(11)/buah(9) | pola=kulit(46) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:vampir] | gender=netral(0, 1 bukti)

### bawah
- `6494648978` Preppy Set! — jenis=bawahan_gaun(38) | tema=kawaii(63)/coquette(9) | subjek=pita(10)/hati(9) | pola=bulu(37) | panjang=pendek fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(48, 1 bukti) | DIUKUR: menutup badan, kaus kaki/stoking
- `16536197442` ♡ siamese cat slippers — jenis=zirah_bawah(25) | tema=kawaii(73)/kostum_hewan(10) | subjek=kucing(94)/anjing(1) | pola=motif_hewan(66) | panjang=selutut fit=lebar | [gambar:kawaii] | gender=cewek(20, 1 bukti) | MESH 3D: 1.8x1.0x1.4 stud
- `5944956638` White pants — jenis=celana_kain(40) | tema=formal(14)/sekolah(9) | subjek=tanpa(5)/hantu(5) | pola=denim(32) | panjang=panjang fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=netral(0, 4 bukti) | DIUKUR: -
- `9353911507` Cute Blue Checkered Goth Pleated Skirt — jenis=rok_pendek(71) | tema=gothic(21)/kawaii(18) | subjek=musik(35)/bendera(8) | pola=kotak(64) | panjang=pendek fit=lebar | [gambar:punk] | gender=cewek(60, 2 bukti) | MESH 3D: 1.4x1.0x0.9 stud, rok/gaun, panjang pendek
- `5406846783` pastel pink dress w white dress — jenis=bawahan_gaun(44) | tema=kawaii(87)/coquette(2) | subjek=pita(8)/buah(6) | pola=polos(32) | panjang=selutut fit=lebar | [gambar:kawaii] | gender=cewek(100, 3 bukti) | temaBukti=kawaii(3 poin)
- `6518462187` ✭ AGEISPOLIS ✭  — jenis=jeans(41) | tema=gothic(23)/punk(11) | subjek=salib(9)/kelelawar(6) | pola=kulit(29) | panjang=panjang fit=lebar | [gambar:gothic] | fungsi=pakaian | gender=cewek(1, 1 bukti) | DIUKUR: -
- `12787796216` (1.0) Fire and Ice Aura - Legs — jenis=jeans(28) | tema=peri(14)/malaikat(13) | subjek=api(56)/petir(14) | pola=pelangi(92) | panjang=pendek fit=lebar | [gambar:peri] | gender=cowok(1, 1 bukti) | MESH 3D: 2.2x2.2x1.2 stud, celana
- `5256588484` Pride Month — jenis=celana_pendek(37) | tema=kawaii(57)/badut(16) | subjek=makanan(17)/bendera(5) | pola=pelangi(100) | panjang=panjang fit=ketat | [gambar:badut] | gender=cewek(2, 1 bukti)
- `4703301264` Celana SMA — jenis=jeans(47) | tema=anime(24)/sekolah(15) | subjek=hantu(6)/hiu(6) | pola=denim(77) | panjang=panjang fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=cowok(27, 2 bukti) | DIUKUR: -
- `6038126362` White socks wit tattoos — jenis=rok_pendek(33) | tema=coquette(15)/kawaii(14) | subjek=kartun(5)/hantu(5) | pola=polkadot(42) | panjang=panjang fit=lebar | [gambar:malaikat] | fungsi=pakaian | gender=cewek(35, 1 bukti) | DIUKUR: -
- `88172181649839` Flower Beach Sarong (Pink) — jenis=rok_panjang(36) | tema=pantai(47)/peri(18) | subjek=bunga(81)/pita(13) | pola=bunga(98) | panjang=pendek fit=lebar | [gambar:peri] | MESH 3D: 1.3x1.4x0.9 stud, rok/gaun, panjang pendek
- `15638002297` 🛍️Puff Sleeve Dress — jenis=bawahan_gaun(76) | tema=tradisional(55)/sekolah(12) | subjek=salib(26)/pita(14) | pola=kotak(22) | panjang=pendek fit=lebar | [gambar:tradisional] | gender=cewek(60, 2 bukti)
- `85513766572053` ♡ Strapless Pastel Floral White Elegant Dress (V1) — jenis=bawahan_gaun(87) | tema=gaun_elegan(81)/kawaii(18) | subjek=bunga(37)/kucing(22) | pola=renda(43) | panjang=selutut fit=ketat | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti) | temaBukti=gaun_elegan(3 poin)
- `15223988363` Christmas Santa Long Sleeve Dress — jenis=bawahan_gaun(48) | tema=natal(100)/musim_dingin(0) | subjek=pita(40)/buah(7) | pola=bulu(38) | panjang=pendek fit=lebar | [gambar:natal] | gender=cewek(60, 2 bukti) | temaBukti=natal(3 poin)
- `4743158436` funny pants (or not) — jenis=kostum_bawah(41) | tema=novelty(49)/natal(7) | subjek=buah(8)/makanan(7) | pola=bunga(42) | panjang=selutut fit=ketat | [gambar:badut] | gender=cewek(32, 1 bukti)
- `5114891270` Airlines Pilot Overcoat Pants [-] — jenis=celana_kain(42) | tema=formal(24)/biasa(9) | subjek=tanpa(6)/salib(4) | pola=denim(29) | panjang=panjang fit=lebar | [gambar:formal] | fungsi=pakaian | gender=cowok(1, 2 bukti) | DIUKUR: -
- `7014804184` Farmer Flamingo Albert Overalls Cleetus Meme Sussy — jenis=overall(90) | tema=novelty(49)/musim_dingin(9) | subjek=hiu(10)/naga(4) | pola=bunga(36) | panjang=panjang fit=lebar | [gambar:antariksa] | fungsi=pakaian | gender=netral(0, 1 bukti) | DIUKUR: menutup badan
- `74851159515064` Khaki Baggy Cargo Pants w/ Belt — jenis=kargo(89) | tema=koboi(34)/steampunk(14) | subjek=beruang(19)/rantai(11) | pola=loreng(36) | panjang=panjang fit=lebar | [gambar:koboi] | MESH 3D: 2.0x3.2x1.0 stud, celana, panjang panjang
- `95133166001749` Wide Daily Pants – Black — jenis=celana_kain(34) | tema=polisi(24)/formal(21) | subjek=salib(16)/tanpa(14) | pola=polos(45) | panjang=selutut fit=lebar | [gambar:polisi] | gender=cewek(19, 2 bukti)
- `1013737392` Medieval Brown Villager Attire [-] — jenis=rok_pendek(16) | tema=ksatria(38)/formal(9) | subjek=api(6)/salib(6) | pola=bulu(29) | panjang=panjang fit=lebar | [gambar:bajak_laut] | fungsi=pakaian | gender=cowok(12, 1 bukti) | DIUKUR: menutup badan
- `82679893809731` Red Leather Pencil Skirt Long Tight High Wasited — jenis=rok_panjang(46) | tema=gaun_elegan(44)/natal(20) | subjek=buah(18)/hati(11) | pola=kulit(64) | panjang=pendek fit=ketat | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti)
- `17586694803` All-White Skin-Tight Suit — jenis=zirah_bawah(46) | tema=formal(35)/superhero(14) | subjek=hantu(17)/ular(13) | pola=polos(28) | panjang=panjang fit=ketat | [gambar:superhero] | MESH 3D: 3.4x5.6x1.1 stud, rok/gaun, panjang panjang
- `6522425829` Red default outfit — jenis=bawahan_gaun(34) | tema=sporty(20)/kostum_hewan(18) | subjek=bendera(16)/logo(8) | pola=polos(22) | panjang=pendek fit=lebar | [gambar:iblis] | gender=cowok(9, 2 bukti)
- `6460065949` 🍁 autumn — jenis=rok_pendek(59) | tema=punk(25)/sekolah(17) | subjek=salib(7)/musik(6) | pola=kotak(91) | panjang=pendek fit=lebar | [gambar:maid] | fungsi=pakaian | gender=cewek(39, 1 bukti) | DIUKUR: menutup badan, kaus kaki/stoking
- `4390601195` Spider-Man — jenis=bawahan_gaun(44) | tema=superhero(99)/halloween(0) | subjek=laba_laba(98)/kelelawar(0) | pola=kilau(84) | panjang=panjang fit=ketat | [gambar:superhero] | fungsi=pakaian | gender=cowok(100, 3 bukti) | DIUKUR: menutup badan

### kepala
- `6096900447` Gothic Vampire Horns — jenis=anting(57) | tema=kerajaan(56)/vampir(18) | subjek=petir(37)/mahkota(32) | [gambar:kerajaan] | gender=cewek(1, 1 bukti)
- `12092086350` Distressed Knit Beanie — jenis=kupluk(93) | tema=gothic(15)/streetwear(13) | subjek=tanpa(23)/salib(14) | [gambar:gothic] | gender=cowok(21, 5 bukti)
- `3704315923` Martian Antennae — jenis=headphone(58) | tema=kawaii(11)/militer(10) | subjek=katak(41)/bulan(8) | [gambar:kawaii] | gender=cewek(31, 2 bukti)
- `12134492704` Cat Ears — jenis=telinga(49) | tema=gothic(17)/formal(16) | subjek=kucing(37)/kelelawar(18) | [gambar:gothic] | gender=cewek(19, 2 bukti)
- `12646375204` Animated Glitched Head — jenis=topeng_kepala(73) | tema=antariksa(17)/badut(15) | subjek=bendera(41)/uang(9) | [gambar:antariksa] | gender=netral(0, 1 bukti)
- `7442454031` Hair Bandana (White) — jenis=helm(36) | tema=militer(18)/medis(11) | subjek=hiu(25)/tanpa(16) | [gambar:militer] | gender=cowok(1, 1 bukti)
- `7032536765` Viking of Freedom — jenis=tanduk(24) | tema=iblis(22)/badut(20) | subjek=bendera(61)/bintang(6) | [gambar:iblis]
- `7061516662` Luobu Party Crown — jenis=mahkota(94) | tema=kerajaan(83)/penyihir(8) | subjek=mahkota(76)/buah(5) | [gambar:kerajaan] | gender=cewek(4, 10 bukti) | temaBukti=kerajaan(6 poin)
- `7962154591` Glamorous Head Bow Blue — jenis=pita_bando(79) | tema=coquette(56)/peri(31) | subjek=pita(91)/kupu_kupu(6) | [gambar:peri] | gender=cewek(26, 5 bukti) | temaBukti=coquette(4 poin)
- `114549646` ROBLOX Sailor Hat — jenis=topi_lain(40) | tema=bajak_laut(54)/sporty(8) | subjek=tanpa(27)/logo(8) | [gambar:bajak_laut] | gender=cowok(33, 1 bukti)
- `12636818966` Mixpat Tricorn Boonie Hat — jenis=topi_lain(39) | tema=militer(100)/polisi(0) | subjek=bendera(34)/tanpa(12) | [gambar:militer]
- `5004410945` Emoji Hearts — jenis=anting(33) | tema=peri(52)/malaikat(9) | subjek=hati(90)/bunga(3) | [gambar:peri] | gender=cewek(18, 1 bukti)
- `48894692` Evil Duck — jenis=topi_formal(22) | tema=iblis(44)/vampir(18) | subjek=bebek(98)/kelelawar(0) | [gambar:iblis] | gender=cowok(2, 13 bukti)
- `5343983739` Haunted Owl Mask White — jenis=topeng_kepala(59) | tema=antariksa(76)/malaikat(2) | subjek=hantu(31)/tengkorak(19) | [gambar:antariksa] | gender=cewek(29, 1 bukti)
- `10370321127` White Fedora - George Ezra — jenis=topi_formal(50) | tema=kawaii(41)/coquette(40) | subjek=bunga(26)/buah(20) | [gambar:kawaii] | gender=cowok(2, 2 bukti)
- `4440648072` Single Hanging Black Earring — jenis=anting(53) | tema=gothic(63)/punk(27) | subjek=salib(72)/rantai(25) | [gambar:gothic] | gender=cewek(8, 3 bukti)
- `12498239376` black headband — jenis=pita_bando(39) | tema=gothic(18)/novelty(9) | subjek=bulan(21)/musik(20) | [gambar:gothic] | gender=cewek(5, 1 bukti)
- `10227020701` Black Mecha Wing Headphones — jenis=headphone(40) | tema=cyber(36)/gothic(26) | subjek=petir(22)/kelelawar(14) | [gambar:gothic] | gender=cewek(21, 1 bukti)
- `73790802` Lion's hood — jenis=tudung(40) | tema=kerajaan(24)/kostum_hewan(20) | subjek=kelelawar(27)/mahkota(15) | [gambar:kerajaan] | gender=cowok(13, 2 bukti)
- `283749451` Stone Cold Viking — jenis=tanduk(34) | tema=ksatria(49)/iblis(15) | subjek=kelelawar(37)/tengkorak(21) | [gambar:ksatria]
- `5510853842` Gold Toon Antlers — jenis=tanduk(36) | tema=kerajaan(82)/kostum_hewan(6) | subjek=mahkota(74)/rantai(6) | [gambar:kerajaan] | gender=cowok(2, 1 bukti)
- `8673943243` Purple Kitsune Mask Front — jenis=topeng_kepala(47) | tema=coquette(26)/gothic(23) | subjek=kucing(89)/kelelawar(7) | [gambar:coquette]
- `6346982863` Moody's Unicorn Ears — jenis=telinga(39) | tema=vampir(61)/iblis(24) | subjek=buah(43)/bunga(25) | [gambar:vampir] | gender=netral(0, 1 bukti)
- `44113968` Kuddle E. Koala — jenis=kupluk(74) | tema=kostum_hewan(41)/musim_dingin(13) | subjek=beruang(86)/kartun(2) | [gambar:kostum_hewan] | gender=cewek(2, 2 bukti)
- `11365655137` Samurai — jenis=halo(42) | tema=ninja(41)/antariksa(16) | subjek=bulan(34)/bintang(20) | [gambar:antariksa]

### rambut
- `5918938570` Brown curly celebrity hair — tema=steampunk(42)/koboi(5) | [gambar:steampunk] | gender=cewek(19, 2 bukti)
- `14221695584` Aesthetic Low Ponytail ( Blonde ) — tema=coquette(51)/kawaii(19) | [gambar:coquette] | gender=cewek(44, 2 bukti)
- `13490038959` Cute Fluffy Pigtails(Brown) — tema=musim_dingin(19)/kawaii(19) | [gambar:koboi] | gender=cewek(65, 4 bukti)
- `417457909` Candy Apple Hair — tema=natal(47)/badut(18) | [gambar:natal] | gender=cewek(7, 2 bukti)
- `158066100` Master Fighter — tema=iblis(38)/vampir(20) | [gambar:iblis] | gender=cowok(45, 1 bukti)
- `11275959320` Aesthetic Braided Bun in Blonde — tema=coquette(27)/kawaii(25) | [gambar:coquette] | gender=cewek(27, 1 bukti)
- `13796838009` Preppy Braided Hair Half up Buns Cotton Candy — tema=kawaii(76)/peri(6) | [gambar:kawaii] | gender=cewek(12, 6 bukti)
- `9174354743` Top Knot - Black — tema=gaun_elegan(26)/formal(15) | [gambar:gaun_elegan] | gender=cowok(4, 56 bukti)
- `12553373151` Blonde Soft Wavy Hair — tema=gaun_elegan(19)/kawaii(13) | [gambar:gaun_elegan] | gender=cewek(34, 2 bukti)
- `6309005259` HollywoodLocks in Pink Ombre — tema=coquette(46)/kawaii(40) | [gambar:coquette] | gender=cewek(44, 3 bukti)
- `12669047808` Curly Mid Part in Black — tema=gothic(27)/gaun_elegan(15) | [gambar:gothic] | gender=cewek(27, 1 bukti)
- `12913278931` Long Cute Curly Preppy Pigtails (Black) — tema=kawaii(35)/gothic(20) | [gambar:gothic] | gender=cewek(70, 3 bukti)
- `13884716114` Brown Layered Bob with Bangs — tema=koboi(8)/punk(8) | [gambar:koboi] | gender=cewek(9, 2 bukti)
- `15083153301` Long Super Model Curly Hair (Dark Brown) — tema=gaun_elegan(27)/formal(12) | [gambar:gaun_elegan] | gender=cewek(28, 2 bukti)
- `10913007737` Country Girl Black Braids — tema=gothic(44)/coquette(7) | [gambar:gothic] | gender=cewek(76, 3 bukti)
- `11142009315` Pretty long black hair — tema=gothic(50)/gaun_elegan(18) | [gambar:gothic] | gender=cewek(46, 1 bukti)
- `7069883034` Long Blonde High Set Pigtails — tema=medis(25)/coquette(22) | [gambar:medis] | gender=cewek(81, 4 bukti)
- `14130402093` Black Kawaii Dolly Pigtails  — tema=kawaii(35)/gothic(34) | [gambar:gothic] | gender=cewek(73, 3 bukti)
- `15294791119` Half up Half Down Pigtails(White) — tema=malaikat(47)/kawaii(7) | [gambar:malaikat] | gender=cewek(67, 3 bukti)
- `13490062585` Messy Influencer Pigtails — tema=gothic(46)/vampir(21) | [gambar:gothic] | gender=cewek(70, 8 bukti)
- `12953488921` (꽃) Flower Messy Bun - Blonde — tema=steampunk(15)/gaun_elegan(13) | [gambar:steampunk] | gender=cewek(39, 5 bukti)
- `501965259` Neon Orange Charmer — tema=cyber(35)/iblis(18) | [gambar:iblis] | gender=cowok(1, 1 bukti)
- `14390235242` Black messy hair — tema=vampir(33)/gothic(18) | [gambar:vampir] | gender=cowok(1, 6 bukti)
- `12652869316` Wavy Full Messy Boy Hair (Black to White) — tema=formal(9)/punk(8) | [gambar:formal] | gender=cowok(70, 3 bukti)
- `15270438967` Y7KCC'S Cornrows (V13) — tema=streetwear(29)/koboi(17) | [gambar:streetwear] | gender=netral(0, 1 bukti)

### sepatu
- `77009173520496` Ultra Heavy Goth Boots — tema=gothic(53)/kostum_hewan(19) | [gambar:kostum_hewan]
- `82164021026282` Brown Boots 3.0 — tema=koboi(23)/militer(15) | [gambar:koboi]
- `92872222938014` 3.0 Moon Boots Pink Sneake… - Right Shoe Accessory — tema=musim_dingin(16)/punk(12) | [gambar:musim_dingin] | gender=cewek(28, 2 bukti) | MESH 3D: 0.8x0.8x1.2 stud, bot
- `90666182784433` Dark Green Ice Skates — tema=militer(50)/formal(8) | [gambar:militer]
- `85947654908671` White Sneakers with White Leg Warmers — tema=sekolah(18)/antariksa(15) | [gambar:sekolah]
- `76769799970265` boots — tema=polisi(24)/militer(14) | [gambar:polisi]
- `83466257538681` Pink Doll Platforms Y2K Shoes Layerable 1.0 — tema=coquette(41)/y2k(35) | [gambar:coquette]
- `85615922155735` Dark Blue Platform Sandals - Right Shoe Accessory — tema=steampunk(26)/kerajaan(20) | [gambar:steampunk] | gender=cewek(45, 1 bukti)
- `79160722360278` Red Bottoms Fancy Shoes (Black) — tema=formal(81)/sekolah(6) | [gambar:formal]
- `84960880217895` Green Fur Fuzzy Furry Boots Y2K — tema=y2k(38)/kostum_hewan(22) | [gambar:kostum_hewan]
- `74372540154745` Devil Slippers V2 Monochrome - Left Shoe Accessory — tema=iblis(36)/formal(22) | [gambar:formal] | gender=cewek(32, 2 bukti) | MESH 3D: 0.8x1.1x1.3 stud, bot
- `72501505129912` Red Shoes — tema=badut(22)/iblis(21) | [gambar:badut]
- `81091980249853` Cute Kawaii Pastel Decora A… - Left Shoe Accessory — tema=kawaii(90)/badut(3) | [gambar:kawaii] | gender=cewek(47, 1 bukti) | temaBukti=kawaii(4 poin) | MESH 3D: 0.8x1.0x1.1 stud, bot
- `78467184407736` Pink Gothic Spiderweb Combat Boots — tema=coquette(47)/gothic(35) | [gambar:coquette]
- `89642362496658` red and black monster fur claw slippers — tema=kostum_hewan(90)/gothic(3) | [gambar:kostum_hewan]
- `83274621535100` High Top Magenta — tema=sporty(19)/superhero(16) | [gambar:sporty]
- `89092864128189` red camo chunky sneakers — tema=iblis(42)/militer(35) | [gambar:iblis]
- `96688342344505` Purple Sneakers Boots — tema=punk(17)/cyber(11) | [gambar:punk]
- `92594088441288` Preppy Pink Charming Pink Clogs — tema=kawaii(44)/peri(18) | [gambar:kawaii]
- `73378130470627` Boots — tema=kostum_hewan(27)/gothic(26) | [gambar:kostum_hewan]
- `87000697844603` red emo buckled strap goth cross shoes — tema=gothic(20)/formal(18) | [gambar:formal]
- `82570927550367` platform sandals — tema=formal(29)/ninja(8) | [gambar:formal]
- `85007190479326` Summer Bow Espadrilles Sandals — tema=malaikat(22)/coquette(21) | [gambar:malaikat] | gender=cewek(14, 1 bukti)
- `94349563160263` Super Elevated Court Heels (It-Girl Doll) — tema=gaun_elegan(53)/coquette(23) | [gambar:gaun_elegan] | gender=cewek(60, 2 bukti)
- `87032500241730` Black Ballet Pumps — tema=gothic(31)/formal(14) | [gambar:gothic]

### wajah
- `5700137935` Medical Mask (Black) — jenis=masker(44) | tema=bajak_laut(14)/streetwear(10) | subjek=tanpa(22)/logo(6) | [gambar:bajak_laut] | gender=cowok(16, 4 bukti)
- `6719140978` Dark Cat Mask — jenis=masker(59) | tema=kostum_hewan(45)/maid(8) | subjek=kucing(73)/kelinci(4) | [gambar:kostum_hewan] | gender=cowok(17, 2 bukti)
- `13499990874` Cute Kitty Black Plushie Mask Hood — jenis=masker(63) | tema=kawaii(36)/kostum_hewan(23) | subjek=kucing(68)/kelelawar(13) | [gambar:kostum_hewan] | gender=cewek(3, 1 bukti) | temaBukti=kawaii(3 poin)
- `4820765156` Deal With It 1.5 — jenis=kacamata_hitam(56) | tema=cyber(17)/y2k(13) | subjek=petir(15)/salib(14) | [gambar:cyber] | gender=cewek(22, 1 bukti)
- `6343865955` Heart Flip-Up Sunglasses (Red) — jenis=kacamata_hitam(50) | tema=vampir(13)/peri(10) | subjek=hati(82)/buah(6) | [gambar:vampir]
- `13516726626` Silver Crystal Nymph Mask — jenis=masker(38) | tema=gothic(54)/peri(28) | subjek=rantai(17)/bulan(10) | [gambar:gothic] | gender=netral(0, 1 bukti)
- `15598027352` White Popular Messy Boy Hair — jenis=kumis_jenggot(70) | tema=malaikat(15)/natal(12) | subjek=logo(13)/bulan(12) | [gambar:malaikat] | gender=cowok(64, 3 bukti)
- `14124659781` Tactical Goggles — jenis=kacamata_hitam(91) | tema=militer(37)/cyber(25) | subjek=tanpa(24)/rantai(18) | [gambar:cyber] | gender=cewek(1, 3 bukti)
- `15599037917` Red Paint Splash - Dark Red — jenis=riasan(32) | tema=horor(61)/vampir(17) | subjek=salib(16)/logo(12) | [gambar:horor] | gender=cowok(2, 4 bukti)
- `12356081561` 💎 Diamond Forehead 💎 — jenis=tindik(52) | tema=iblis(32)/gaun_elegan(23) | subjek=bintang(23)/hati(16) | [gambar:iblis] | gender=cowok(9, 1 bukti)
- `16028539194` Heart Sunglasses — jenis=kacamata_hitam(67) | tema=pantai(14)/peri(11) | subjek=hati(89)/bulan(2) | [gambar:pantai]
- `15316113296` Mystery Face — jenis=riasan(45) | tema=maid(18)/antariksa(8) | subjek=logo(39)/tanpa(9) | [gambar:maid] | gender=cewek(32, 1 bukti)
- `13931691082` Cute Joyful  Blush Face Mask — jenis=riasan(38) | tema=kawaii(50)/coquette(10) | subjek=kartun(11)/tulisan(9) | [gambar:kawaii] | gender=netral(0, 1 bukti) | temaBukti=kawaii(3 poin)
- `11110615160` 🙃 Tiny Happy Face (3D) 🙃 — jenis=tindik(21) | tema=badut(12)/kostum_hewan(8) | subjek=logo(20)/kartun(11) | [gambar:badut] | gender=netral(0, 1 bukti)
- `14961177277` Bandages — jenis=tindik(47) | tema=malaikat(22)/antariksa(16) | subjek=rantai(60)/tanpa(10) | [gambar:malaikat] | gender=cowok(3, 1 bukti)
- `4708697945` Blue Void Gas Mask — jenis=masker(60) | tema=cyber(52)/steampunk(11) | subjek=laba_laba(17)/ular(10) | [gambar:cyber]
- `12702070524` easter spring baby pacifier bib y2k bloxburg bunny — jenis=riasan(39) | tema=coquette(35)/y2k(35) | subjek=kelinci(39)/kucing(21) | [gambar:coquette] | gender=cewek(65, 1 bukti)
- `14169306173` Simple Bangs in Black — jenis=riasan(36) | tema=biasa(36)/gothic(26) | subjek=logo(21)/wajah_anime(12) | [gambar:gothic] | gender=cewek(44, 1 bukti)
- `12114101218` Silver Bejeweled Y2K Star Shades — jenis=kacamata_hitam(81) | tema=y2k(35)/gothic(26) | subjek=bintang(36)/laba_laba(8) | [gambar:gothic] | gender=cowok(14, 7 bukti)
- `6565507468` Mouth Pride Flag: (Lesbian Flag) — jenis=riasan(39) | tema=tradisional(40)/pantai(22) | subjek=bendera(52)/pita(33) | [gambar:tradisional] | gender=cewek(19, 1 bukti)
- `14834743245` Anime - Black Swordmen Scar - Kagurabachi — jenis=kumis_jenggot(90) | tema=anime(35)/peri(14) | subjek=kelelawar(37)/wajah_anime(35) | [gambar:peri] | gender=cowok(32, 1 bukti)
- `15589798698` Antartica Shimmer Cheeks Head Light Skin Tone — jenis=riasan(56) | tema=kawaii(30)/coquette(14) | subjek=kartun(8)/bebek(8) | [gambar:kawaii] | gender=cewek(30, 3 bukti)
- `11113896935` Black Decorated Eyepatch — jenis=penutup_mata(59) | tema=bajak_laut(39)/medis(27) | subjek=salib(36)/musik(17) | [gambar:bajak_laut] | gender=cewek(2, 1 bukti)
- `10021533847` Brown Cyber Y2K Classy Iconic Glasses — jenis=kacamata_hitam(58) | tema=y2k(19)/cyber(19) | subjek=tulisan(8)/salib(7) | [gambar:steampunk]
- `13969567983` Claw Marks — jenis=kumis_jenggot(67) | tema=sporty(15)/horor(12) | subjek=petir(49)/logo(15) | [gambar:sporty] | gender=cowok(19, 1 bukti)

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 295, malaikat 192, gothic 173, coquette 156, formal 140, kostum_hewan 130, punk 108, steampunk 100, cyber 100, iblis 99, peri 97, militer 97
- atas: kawaii 812, formal 692, biasa 272, punk 242, sporty 240, gothic 238, militer 220, coquette 197, y2k 184, novelty 176, cyber 172, halloween 163
- bawah: formal 652, kawaii 614, y2k 429, biasa 358, gothic 330, punk 284, sekolah 262, coquette 245, musim_dingin 240, militer 193, maid 171, halloween 154
- kepala: coquette 234, kawaii 213, kerajaan 186, formal 167, malaikat 152, militer 142, gothic 125, peri 112, kostum_hewan 110, penyihir 99, iblis 99, antariksa 93
- rambut: kawaii 432, gothic 393, coquette 221, anime 183, gaun_elegan 170, steampunk 167, koboi 149, musim_dingin 145, punk 137, malaikat 118, iblis 92, y2k 83
- sepatu: kawaii 345, gothic 248, coquette 248, sporty 202, musim_dingin 191, y2k 158, kostum_hewan 150, pantai 129, militer 114, punk 110, gaun_elegan 99, formal 88
- wajah: kawaii 432, steampunk 236, gothic 183, militer 174, cyber 158, coquette 139, malaikat 92, anime 88, polisi 82, iblis 77, pantai 71, vampir 70
