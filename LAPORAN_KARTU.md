# Laporan Kartu Item (MATA v2) — versi 1792227671

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **139549**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 12300 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7889 | 0.0 | 57% | 68% | 57% | 54% |
| aksen/tema | 8180 | 0.75 | 29% | 42% | 28% | 29% |
| atas2D/jenis | 6097 | 1.0 | 15% | 24% | 8% | 15% |
| atas2D/pola | 1133 | 1.0 | 50% | 63% | 47% | 50% |
| atas2D/subjek | 2232 | 0.5 | 32% | 43% | 31% | 32% |
| atas2D/tema | 4514 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5605 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2130 | 0.75 | 55% | 67% | 51% | 53% |
| atas3D/subjek | 2061 | 0.25 | 31% | 41% | 31% | 29% |
| atas3D/tema | 3489 | 1.0 | 30% | 39% | 27% | 30% |
| bawah2D/jenis | 4171 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2486 | 1.0 | 43% | 56% | 35% | 43% |
| bawah2D/subjek | 1796 | 0.75 | 15% | 22% | 12% | 14% |
| bawah2D/tema | 4224 | 0.5 | 25% | 31% | 21% | 23% |
| bawah3D/jenis | 3242 | 0.75 | 52% | 72% | 50% | 52% |
| bawah3D/pola | 2033 | 1.0 | 49% | 62% | 45% | 49% |
| bawah3D/subjek | 967 | 0.25 | 28% | 37% | 28% | 25% |
| bawah3D/tema | 2030 | 0.25 | 21% | 30% | 21% | 19% |
| kepala/jenis | 10085 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5610 | 0.5 | 48% | 58% | 48% | 48% |
| kepala/tema | 7234 | 0.5 | 34% | 45% | 33% | 33% |
| rambut/tema | 5459 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2375 | 0.25 | 22% | 33% | 21% | 20% |
| wajah/jenis | 3848 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1632 | 0.0 | 47% | 54% | 47% | 45% |
| wajah/tema | 2206 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Bukti (rev 31): gender & tema dari bukti, bukan tebakan satu sumber

Outfit buatan manusia dipakai sebagai bukti pemakaian: **78035**.

### Gender (uji jujur: benih nama 20% item disembunyikan, ditebak dari pemakaian)

| ambang | benar | diputuskan | item uji |
|---|---|---|---|
| 0.1 | 1728 (95.7%) | 1805 | 2797 |
| 0.15 | 1620 (96.3%) | 1683 | 2797 |
| 0.25 | 1350 (97.9%) | 1379 | 2797 |

### Tema berbukti vs label emas (baju/celana 2D)

| tipe | n | diputuskan | tepat saat diputuskan | kartu lama tepat |
|---|---|---|---|---|
| 11 | 37 | 8 | 8 | 21 |
| 12 | 23 | 4 | 3 | 12 |

Item bertema berbukti: 16540 dari 139549 (sisanya tidak bertema khusus).

Sebaran: kawaii 2929, coquette 1593, formal 1529, halloween 1379, militer 1145, kerajaan 898, sporty 799, malaikat 651, gothic 616, punk 585, koboi 486, ksatria 479, natal 442, penyihir 264, musim_dingin 255, iblis 255, anime 217, antariksa 199, pantai 187, superhero 174, cyber 170, gaun_elegan 157, badut 154, polisi 123, peri 121

### Sambungan tema (PMI positif, dari outfit manusia)

- kawaii: coquette (0.22, 484)
- kerajaan: steampunk (0.36, 14), peri (0.30, 90), pantai (0.06, 30)
- formal: penyihir (0.35, 6), steampunk (0.26, 10)
- coquette: malaikat (0.30, 76), kawaii (0.22, 484), gaun_elegan (0.13, 11), peri (0.01, 48)
- militer: cyber (0.35, 8), koboi (0.04, 9)
- punk: gothic (0.76, 46), vampir (0.60, 6), iblis (0.48, 17), peri (0.34, 24)
- gothic: vampir (0.81, 6), iblis (0.80, 19), punk (0.76, 46)
- malaikat: peri (1.04, 37), iblis (0.62, 15), coquette (0.30, 76)
- peri: horor (1.50, 5), malaikat (1.04, 37), iblis (1.03, 19), punk (0.34, 24), kerajaan (0.30, 90)
- musim_dingin: natal (0.60, 10)
- iblis: vampir (1.53, 6), peri (1.03, 19), gothic (0.80, 19), malaikat (0.62, 15), punk (0.48, 17)
- natal: musim_dingin (0.60, 10)
- pantai: kerajaan (0.06, 30)
- koboi: militer (0.04, 9)
- cyber: militer (0.35, 8)
- gaun_elegan: coquette (0.13, 11)
- vampir: iblis (1.53, 6), gothic (0.81, 6), punk (0.60, 6)

## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)

Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,
celana tema 35%, pola 39-40%, kaos fungsi belum ada.

| tipe | facet | n | benar | akurasi | tanpa kartu |
|---|---|---|---|---|---|
| baju 2D | jenis | 57 | 28 | 49% | 0 |
| baju 2D | tema | 37 | 21 | 57% | 0 |
| baju 2D | pola | 54 | 15 | 28% | 0 |
| baju 2D | fungsi | 46 | 45 | 98% | 14 |
| celana 2D | jenis | 43 | 24 | 56% | 0 |
| celana 2D | tema | 23 | 12 | 52% | 0 |
| celana 2D | pola | 48 | 19 | 40% | 0 |
| celana 2D | fungsi | 49 | 48 | 98% | 10 |
| kaos klasik | fungsi | 55 | 48 | 87% | 0 |

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween] | gender=netral(0, 254 bukti) | temaBukti=halloween(3 poin)
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi] | gender=cowok(6, 5 bukti) | temaBukti=koboi(5 poin)
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut] | gender=cowok(2, 2 bukti) | temaBukti=bajak_laut(4 poin)
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(45)/mata(17) | [gambar:steampunk] | gender=cowok(6, 10 bukti)
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(54) | tema=maid(66)/punk(4) | subjek=salib(6)/rantai(6) | pola=bulu(23) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:maid] | fungsi=pakaian | gender=cewek(76, 41 bukti) | temaBukti=maid(3 poin) | DIUKUR: leher 21%
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=rompi(35) | tema=formal(70)/gothic(4) | subjek=kelelawar(10)/salib(8) | pola=polos(29) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:formal] | MOTIF DIUKUR: polos(57) | fungsi=pakaian | gender=cowok(6, 106 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 5%
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat] | gender=cewek(4, 62 bukti) | temaBukti=malaikat(4 poin)
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(51)/bulan(35) | [gambar:steampunk] | gender=cowok(4, 4 bukti)
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(66) | tema=kawaii(68)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(96) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=pakaian | gender=cewek(44, 42 bukti) | temaBukti=kawaii(3 poin) | DIUKUR: leher 24%, bahu terbuka
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal] | gender=cewek(19, 29 bukti)
- `382538059` Green Jersey (atas): jenis=jersey(92) | tema=sporty(96)/y2k(1) | subjek=katak(24)/bintang(9) | pola=bunga(27) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | fungsi=pakaian | gender=cewek(1, 254 bukti) | temaBukti=sporty(5 poin) | DIUKUR: leher 9%
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(45)/formal(19) | subjek=salib(23)/kelelawar(12) | pola=kulit(54) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | gender=cowok(1, 254 bukti) | DIUKUR: - | MESH 3D: 2.8x1.9x0.8 stud, lengan panjang
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette] | gender=cewek(31, 51 bukti) | temaBukti=coquette(4 poin)
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(77) | tema=y2k(31)/punk(28) | subjek=bulan(6)/rantai(6) | pola=denim(86) | panjang=panjang fit=lebar | [gambar:gothic] | MOTIF DIUKUR: polos(88) | fungsi=pakaian | gender=cowok(68, 146 bukti) | DIUKUR: -
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(50) | tema=gothic(44)/punk(31) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(89) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber] | gender=netral(0, 1 bukti)
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii] | gender=cewek(32, 3 bukti)
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan] | gender=cowok(5, 32 bukti) | temaBukti=kerajaan(6 poin)
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(26)/tulisan(10) | [gambar:streetwear] | gender=cewek(5, 254 bukti)
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii] | gender=cewek(36, 1 bukti) | temaBukti=kawaii(3 poin)
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween] | gender=cewek(21, 3 bukti) | temaBukti=halloween(7 poin)
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=kaos(24) | tema=halloween(77)/kawaii(10) | subjek=labu(45)/beruang(19) | pola=pelangi(38) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=jeans(26) | tema=halloween(73)/kawaii(6) | subjek=labu(48)/beruang(18) | pola=kotak(26) | panjang=pendek fit=lebar | [gambar:halloween] | gender=cowok(8, 1 bukti) | temaBukti=halloween(5 poin)

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=jaket(62) | tema=antariksa(67)/cyber(22) | subjek=wajah_anime(13)/tulisan(9) | pola=denim(41) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=cewek(6, 4 bukti)
- `1239904` Akatsuki — nama: anime | jenis=kaos(74) | tema=anime(75)/horor(4) | subjek=api(18)/buah(14) | pola=bulu(47) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:horor] | fungsi=grafis | gender=cowok(1, 4 bukti)
- `1260428` Guitar Hero 2 Logo — nama: superhero | jenis=kaos(93) | tema=superhero(75)/punk(7) | subjek=logo(28)/musik(26) | pola=kotak(29) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=netral(0, 254 bukti)
- `1397335` Me with snow wolf shirt. — nama: musim_dingin | jenis=hoodie(52) | tema=musim_dingin(75)/streetwear(7) | subjek=kartun(9)/hiu(7) | pola=polos(28) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1431511` ninja shirt — nama: ninja | jenis=kaos(71) | tema=ninja(70)/biasa(6) | subjek=logo(25)/tulisan(9) | pola=garis(27) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(1, 76 bukti)
- `1475939` Noob shirt — nama: novelty | jenis=kaos(51) | tema=novelty(85)/cyber(3) | subjek=logo(8)/hati(7) | pola=pelangi(52) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(1, 43 bukti)
- `1515399` My cute kitty! :) — nama: kawaii | jenis=kaos(67) | tema=kawaii(52)/superhero(15) | subjek=kucing(76)/anjing(6) | pola=polkadot(79) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=netral(0, 2 bukti) | temaBukti=kawaii(4 poin)
- `1521989` shadow military lvl 1 — nama: militer | jenis=rompi(27) | tema=militer(61)/cyber(6) | subjek=logo(13)/katak(11) | pola=garis(36) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:pantai] | fungsi=grafis | gender=cowok(5, 2 bukti)
- `1558188` Random Anime Character I made — nama: anime | jenis=jas(26) | tema=anime(58)/superhero(10) | subjek=wajah_anime(39)/naga(8) | pola=polos(55) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:vampir] | fungsi=grafis | gender=cewek(4, 20 bukti)
- `1591061` Cute Wolf — nama: kawaii | jenis=kaos(70) | tema=kawaii(73)/punk(9) | subjek=anjing(69)/wajah_anime(5) | pola=grafis(66) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan] | fungsi=badan | gender=cewek(2, 9 bukti)
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(54) | tema=sporty(83)/y2k(11) | subjek=tulisan(37)/petir(13) | pola=polkadot(83) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k] | fungsi=grafis | gender=cewek(17, 1 bukti)
- `1621982` Yellow Dragon of the Western Winds — nama: koboi | jenis=kemeja(56) | tema=koboi(55)/kerajaan(10) | subjek=naga(92)/dinosaurus(2) | pola=grafis(74) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | fungsi=grafis | gender=cewek(1, 15 bukti)
- `1636113` Ninja Drone Of Shadows Version 2 — nama: ninja | jenis=jas(47) | tema=ninja(63)/gothic(12) | subjek=laba_laba(87)/ular(1) | pola=renda(48) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(2, 25 bukti)
- `1639327` Cyber Suit35 — nama: cyber | jenis=kostum_penuh(39) | tema=cyber(53)/sporty(25) | subjek=logo(32)/bendera(10) | pola=garis(46) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(2, 3 bukti)
- `1639359` Cyber Suit31 — nama: cyber | jenis=jas(50) | tema=cyber(79)/ninja(3) | subjek=pita(24)/rantai(15) | pola=catur(44) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:pantai] | fungsi=aksesori | gender=cewek(9, 21 bukti)
- `1639368` Cyber Suit29 — nama: cyber | jenis=rompi(35) | tema=cyber(69)/kawaii(7) | subjek=bulan(7)/bunga(6) | pola=catur(94) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:peri] | fungsi=grafis | gender=cewek(3, 2 bukti)
- `1639414` Cyber Suit22 — nama: cyber | jenis=kaos(34) | tema=cyber(87)/militer(2) | subjek=bendera(16)/logo(15) | pola=catur(40) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:musim_dingin] | fungsi=aksesori | gender=cewek(2, 1 bukti)
- `1639419` Cyber Suit21 — nama: cyber | jenis=kaos(45) | tema=cyber(88)/malaikat(4) | subjek=petir(23)/hiu(12) | pola=pelangi(37) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:punk] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1639424` Cyber Suit20 — nama: cyber | jenis=kaos(56) | tema=cyber(61)/antariksa(16) | subjek=bulan(14)/petir(11) | pola=bunga(59) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan | gender=cewek(6, 23 bukti)
- `1639431` Cyber ###### — nama: cyber | jenis=jas(38) | tema=cyber(75)/penyihir(10) | subjek=bintang(15)/bulan(14) | pola=pelangi(40) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:steampunk] | fungsi=aksesori | gender=cowok(1, 2 bukti)
- `1639438` Cyber Suit18 — nama: cyber | jenis=jubah(59) | tema=cyber(60)/kawaii(4) | subjek=bulan(29)/hiu(17) | pola=garis(49) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:pantai] | fungsi=pakaian | gender=cewek(2, 1 bukti)
- `1639470` Cyber Suit14 — nama: cyber | jenis=kaos(22) | tema=cyber(56)/gothic(15) | subjek=bulan(27)/rantai(17) | pola=catur(53) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori | gender=cewek(4, 6 bukti)
- `1639518` Cyber ##### — nama: cyber | jenis=hoodie(40) | tema=cyber(93)/sporty(3) | subjek=hiu(18)/logo(17) | pola=kilau(29) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 6 bukti)
- `1648160` ninja — nama: ninja | jenis=jas(27) | tema=ninja(73)/badut(10) | subjek=logo(44)/tulisan(5) | pola=polkadot(38) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis | gender=netral(0, 4 bukti)
- `1726226` Cutsey_Cosplay_by_Halogrunt — nama: anime | jenis=kaos(32) | tema=anime(62)/badut(12) | subjek=kucing(27)/katak(17) | pola=bulu(65) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:badut] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1753596` Cowboy NeckHat — nama: koboi | jenis=kostum_penuh(69) | tema=koboi(68)/halloween(12) | subjek=labu(77)/makanan(3) | pola=bulu(63) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | fungsi=aksesori | gender=netral(0, 2 bukti) | temaBukti=halloween(3 poin)
- `1756352` cute — nama: kawaii | jenis=hoodie(33) | tema=kawaii(50)/novelty(20) | subjek=api(27)/petir(11) | pola=pelangi(86) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cewek(2, 2 bukti)
- `1769022` I-Pod tux — nama: formal | jenis=kostum_penuh(41) | tema=formal(54)/y2k(14) | subjek=bebek(40)/logo(8) | pola=polkadot(48) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(23, 1 bukti)
- `1769048` Luke Tux — nama: formal | jenis=hoodie(46) | tema=formal(86)/kawaii(4) | subjek=bebek(31)/logo(11) | pola=bulu(63) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(4, 4 bukti)
- `1769060` Metal Tux — nama: formal | jenis=seragam(23) | tema=formal(53)/natal(17) | subjek=bebek(17)/katak(13) | pola=bulu(74) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:natal] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1769091` Robin Tux — nama: formal | jenis=jubah(32) | tema=formal(53)/ninja(9) | subjek=bebek(44)/katak(8) | pola=bulu(40) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:ninja] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769097` ROBO TUX BEEP BOOP BOP! — nama: formal | jenis=jas(55) | tema=formal(68)/novelty(8) | subjek=hati(41)/logo(12) | pola=pelangi(88) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis | gender=cowok(1, 1 bukti) | temaBukti=formal(3 poin)
- `1769130` Spy Tux — nama: formal | jenis=kostum_penuh(48) | tema=formal(53)/cyber(18) | subjek=katak(20)/bebek(11) | pola=garis(53) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis | gender=netral(0, 2 bukti)
- `1769138` Super Tux!!! — nama: formal | jenis=jaket(20) | tema=formal(67)/novelty(13) | subjek=bebek(33)/logo(8) | pola=pelangi(54) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:superhero] | fungsi=grafis | gender=cewek(4, 5 bukti)
- `1770016` School Icon — nama: sekolah | jenis=kaos(45) | tema=sekolah(60)/sporty(27) | subjek=beruang(75)/logo(10) | pola=garis(49) | lengan=pendek panjang=crop fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis | gender=cewek(1, 2 bukti)
- `1771956` Disco Tux — nama: formal | jenis=jubah(26) | tema=formal(52)/kawaii(10) | subjek=bebek(10)/kartun(8) | pola=bulu(93) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic] | fungsi=grafis | gender=cowok(5, 1 bukti)
- `1771962` Ingured Tux — nama: formal | jenis=hoodie(35) | tema=formal(61)/kawaii(13) | subjek=bebek(31)/logo(9) | pola=bulu(66) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis | gender=cewek(1, 1 bukti)
- `1771965` Jedi Tux — nama: formal | jenis=hoodie(40) | tema=formal(84)/kawaii(6) | subjek=bebek(26)/logo(12) | pola=bulu(43) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cowok(4, 6 bukti)
- `1773652` LOOK A WATER DRIP!(shirt) — nama: streetwear | jenis=kaos(97) | tema=streetwear(78)/kerajaan(5) | subjek=bebek(29)/katak(12) | pola=pelangi(80) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:novelty] | fungsi=grafis | gender=netral(0, 3 bukti)
- `1781595` some tux's — nama: formal | jenis=jaket(36) | tema=formal(52)/novelty(14) | subjek=bebek(46)/tulisan(5) | pola=bulu(38) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis | gender=cewek(1, 4 bukti)

## Contoh acak per kelompok

### aksen
- `11257129685` Autumn Lotus Flower Top — jenis=lain(39) | tema=peri(39)/pantai(31) | subjek=bunga(77)/buah(9) | [gambar:peri] | gender=cewek(22, 1 bukti)
- `5359896996` Right BFF Necklace  — jenis=kalung(94) | tema=kerajaan(27)/medis(10) | subjek=hati(26)/bulan(22) | [gambar:kerajaan] | gender=cewek(53, 3 bukti)
- `7390560332` Portal Openers Katana White — jenis=senjata(63) | tema=ninja(28)/medis(10) | subjek=musik(56)/petir(14) | [gambar:ninja] | gender=netral(0, 1 bukti)
- `9529437541` Butterfly Wings - SUNMI  — jenis=sayap(95) | tema=peri(72)/malaikat(17) | subjek=kupu_kupu(97)/pita(1) | [gambar:peri] | gender=cewek(23, 1 bukti)
- `3612256037` Viridian Bow Tie — jenis=ekor(31) | tema=formal(52)/coquette(35) | subjek=pita(90)/bintang(2) | [gambar:formal] | gender=netral(0, 1 bukti) | temaBukti=coquette(3 poin)
- `4602807964` Black Bow Tie — jenis=ekor(46) | tema=formal(60)/coquette(35) | subjek=pita(93)/bintang(1) | [gambar:formal] | gender=netral(0, 2 bukti) | temaBukti=coquette(3 poin)
- `12558088733` Black Bag — jenis=tas(82) | tema=militer(37)/polisi(32) | subjek=tanpa(25)/mata(9) | [gambar:militer] | gender=cowok(36, 1 bukti)
- `493483053` Shoulder Bear — jenis=boneka(32) | tema=kostum_hewan(75)/halloween(5) | subjek=beruang(95)/kartun(1) | [gambar:kostum_hewan] | gender=netral(0, 1 bukti)
- `12323849611` Mexico Flag Pin — jenis=ekor(31) | tema=antariksa(22)/natal(11) | subjek=bendera(99)/tanpa(0) | [gambar:antariksa] | gender=netral(0, 1 bukti)
- `10228635263` Tactical Shemagh — jenis=jubah_belakang(46) | tema=gothic(43)/militer(35) | subjek=kelelawar(39)/hati(7) | [gambar:gothic] | gender=cowok(5, 5 bukti)
- `7133894887` Buff Noob Trading Card — jenis=sabuk(36) | tema=novelty(42)/medis(30) | subjek=kartun(55)/tulisan(5) | [gambar:medis] | gender=cowok(22, 2 bukti)
- `7292534907` Blue Jay — jenis=sayap(28) | tema=musim_dingin(22)/kostum_hewan(16) | subjek=kartun(29)/kelelawar(11) | [gambar:musim_dingin] | gender=cewek(1, 1 bukti)
- `12669266288` Y2K Diamond Heart Belt White (3.0) — jenis=kalung(59) | tema=y2k(37)/coquette(18) | subjek=hati(54)/rantai(28) | [gambar:coquette] | gender=cewek(24, 2 bukti)
- `11706594166` Oversized Tied Hoodie — jenis=syal(40) | tema=badut(34)/iblis(16) | subjek=ular(17)/hati(14) | [gambar:badut] | gender=cewek(25, 1 bukti)
- `4262731024` Ceremonial Saber — jenis=senjata(86) | tema=ninja(30)/bajak_laut(17) | subjek=petir(48)/bulan(9) | [gambar:ninja] | gender=cewek(1, 6 bukti)
- `12302260904` Shoulder 8bit Turtle Shell — jenis=sabuk(19) | tema=militer(88)/steampunk(7) | subjek=katak(29)/ular(17) | [gambar:militer]
- `5410392781` Vtg Skateboard — jenis=lain(32) | tema=natal(11)/streetwear(11) | subjek=buah(16)/tanpa(12) | [gambar:natal] | gender=netral(0, 1 bukti)
- `6187021292` Baby Blue Mini Purse — jenis=tas(81) | tema=kawaii(54)/medis(11) | subjek=hati(20)/hantu(11) | [gambar:kawaii] | gender=cewek(45, 1 bukti)
- `331486478` Golden VIP Necklace — jenis=kalung(86) | tema=steampunk(16)/kerajaan(11) | subjek=rantai(66)/logo(20) | [gambar:steampunk] | gender=cowok(1, 1 bukti)
- `7583352167` Vector Arrow — jenis=kalung(21) | tema=militer(27)/steampunk(26) | subjek=bintang(32)/salib(15) | [gambar:militer] | gender=cowok(1, 67 bukti)
- `8651322585` White Angelic Fluffy Wings — jenis=sayap(98) | tema=malaikat(80)/musim_dingin(18) | subjek=kupu_kupu(27)/kelelawar(26) | [gambar:malaikat] | gender=cewek(10, 3 bukti) | temaBukti=malaikat(3 poin)
- `5909776064` Russo’s Sword of Truth — jenis=senjata(93) | tema=cyber(28)/penyihir(11) | subjek=petir(43)/logo(17) | [gambar:cyber] | gender=cewek(2, 13 bukti)
- `7961033702` Thunder Aura — jenis=senjata(44) | tema=coquette(12)/gaun_elegan(10) | subjek=petir(43)/pita(12) | [gambar:coquette] | gender=cewek(18, 2 bukti)
- `5165283690` Pride Crossbody Bag — jenis=tas(43) | tema=medis(27)/y2k(19) | subjek=tulisan(18)/logo(16) | [gambar:medis] | gender=cewek(6, 1 bukti)
- `6682402260` Miau Butterfly Necklace Silver and Pink — jenis=kalung(52) | tema=kawaii(61)/coquette(21) | subjek=kupu_kupu(87)/pita(6) | [gambar:kawaii] | gender=cewek(26, 1 bukti)

### atas
- `4835561357` CHAIN AND HEART LOCKET — jenis=kemeja(35) | tema=y2k(38)/punk(13) | subjek=rantai(72)/hati(18) | pola=kilau(77) | lengan=tanpa panjang=crop fit=pas depan=terbuka | [gambar:punk] | fungsi=aksesori | gender=cewek(5, 1 bukti)
- `70796842182753` adidas Washed Out Anime Pyjama Top — jenis=hoodie(98) | tema=anime(36)/streetwear(13) | subjek=logo(26)/wajah_anime(18) | pola=polos(67) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:streetwear] | gender=cewek(90, 1 bukti) | DIUKUR: - | MESH 3D: 3.0x2.3x1.1 stud, lengan panjang
- `9185734724` Soft White Turtleneck — jenis=kaos(62) | tema=kawaii(23)/sporty(22) | subjek=tanpa(31)/logo(15) | pola=polos(45) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | gender=cewek(56, 1 bukti) | DIUKUR: - | MESH 3D: 1.9x1.6x0.8 stud, lengan pendek
- `13905962208` 1.0 Ghillie Suit - Green Jungle — jenis=zirah(57) | tema=militer(52)/formal(35) | subjek=katak(16)/dinosaurus(12) | pola=loreng(92) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:militer] | gender=cowok(9, 1 bukti) | temaBukti=militer(3 poin) | DIUKUR: - | MESH 3D: 4.3x5.5x2.0 stud, lengan panjang
- `13919157081` 💅 Pink Cat Glitter Nails — jenis=jubah(18) | tema=kawaii(43)/coquette(17) | subjek=kucing(37)/pita(9) | pola=kilau(38) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii] | gender=cewek(42, 6 bukti) | MESH 3D: 3.6x0.7x0.6 stud
- `3289030357` ‘Vsco’ Star Necklace~ 💫  — jenis=kaos(39) | tema=kawaii(54)/y2k(11) | subjek=bintang(44)/bulan(17) | pola=bunga(41) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:kawaii] | fungsi=aksesori | gender=cewek(32, 1 bukti)
- `5318969100` jean jacket — jenis=jaket(46) | tema=kawaii(20)/y2k(10) | subjek=hantu(8)/tanpa(7) | pola=denim(96) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=pakaian | gender=cewek(40, 1 bukti) | DIUKUR: leher 58%, crop
- `13241944711` Oversized Striped Y2K Sweater — jenis=sweater(52) | tema=y2k(36)/sporty(26) | subjek=ular(19)/katak(16) | pola=garis(88) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | MOTIF DIUKUR: garis(98) | DIUKUR: - | MESH 3D: 3.2x2.4x0.8 stud, lengan panjang
- `1635921` Teakettle Drone Version 2 — jenis=jas(51) | tema=halloween(27)/ninja(11) | subjek=laba_laba(69)/labu(17) | pola=grafis(22) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:halloween] | fungsi=badan | gender=netral(0, 1 bukti) | temaBukti=halloween(3 poin)
- `70633006259247` Pink Graphic Print Tee — jenis=kaos(91) | tema=badut(14)/bajak_laut(12) | subjek=logo(14)/tanpa(12) | pola=grafis(68) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:badut] | DIUKUR: - | MESH 3D: 1.8x1.8x0.8 stud, lengan pendek
- `12731768568` Cottage Picnic Basket White Light Brown — jenis=gaun(22) | tema=maid(58)/peri(31) | subjek=makanan(27)/bunga(24) | pola=bunga(89) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:maid]
- `3895326233` Galaxy Suit — jenis=jas(75) | tema=antariksa(81)/formal(18) | subjek=bulan(47)/bintang(19) | pola=kilau(98) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:antariksa] | fungsi=pakaian | gender=netral(0, 1 bukti) | temaBukti=formal(3 poin) | DIUKUR: leher 4%
- `12079062364` Cultist's Black Robe (1.0) — jenis=jubah(41) | tema=gothic(74)/gaun_elegan(9) | subjek=bunga(29)/salib(13) | pola=renda(60) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | MOTIF DIUKUR: polos(63) | gender=netral(0, 1 bukti) | DIUKUR: - | MESH 3D: 4.7x5.2x2.2 stud, lengan panjang
- `4937511721` Green Formal robes [+] — jenis=rompi(20) | tema=formal(36)/militer(31) | subjek=katak(15)/bendera(10) | pola=kotak(26) | lengan=pendek panjang=panjang fit=longgar depan=tertutup | [gambar:militer] | gender=cowok(15, 1 bukti)
- `18460518578` soft arm warmers black — jenis=tanktop(21) | tema=steampunk(32)/militer(10) | subjek=musik(52)/bulan(7) | pola=loreng(25) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:steampunk] | gender=cewek(3, 1 bukti) | MESH 3D: 3.0x1.2x0.5 stud
- `14915170144` Knitted Arm Warmers Pastel Light Purple — jenis=tanktop(32) | tema=kawaii(85)/maid(2) | subjek=ular(13)/bulan(10) | pola=pelangi(24) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii] | gender=cewek(21, 3 bukti) | temaBukti=kawaii(3 poin) | MESH 3D: 3.2x1.3x0.7 stud
- `4880136035` shine — jenis=crop(35) | tema=kawaii(17)/peri(14) | subjek=mahkota(14)/pita(7) | pola=polos(74) | lengan=pendek panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=pakaian | gender=cewek(41, 1 bukti) | DIUKUR: leher 24%, crop
- `314839559` Sparkle Time Pumpkin Torso Match — jenis=rompi(86) | tema=halloween(77)/sporty(3) | subjek=labu(77)/api(2) | pola=kilau(70) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:halloween] | fungsi=pakaian | gender=cewek(1, 1 bukti) | temaBukti=halloween(5 poin) | DIUKUR: leher 0%
- `6394193061` silver initial necklace: R — jenis=kemeja(59) | tema=y2k(31)/biasa(14) | subjek=logo(34)/tanpa(10) | pola=polkadot(14) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:sekolah] | fungsi=aksesori | gender=cewek(35, 1 bukti)
- `6380030062` white chanel tennis shirt — jenis=kaos(43) | tema=sporty(16)/kerajaan(13) | subjek=logo(8)/salib(7) | pola=polos(42) | lengan=pendek panjang=crop fit=pas depan=tertutup | [gambar:malaikat] | fungsi=pakaian | gender=cewek(40, 1 bukti) | DIUKUR: leher 5%, crop
- `4932712826` navy — jenis=kemeja(52) | tema=sporty(44)/sekolah(14) | subjek=bendera(33)/logo(7) | pola=garis(99) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:sporty] | MOTIF DIUKUR: garis(97) | fungsi=pakaian | gender=cewek(44, 1 bukti) | DIUKUR: leher 0%
- `12731447979` Lace Flower Cape - Black — jenis=hoodie(24) | tema=gothic(72)/pantai(4) | subjek=bunga(35)/bulan(16) | pola=loreng(42) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic] | MOTIF DIUKUR: polos(76) | gender=cewek(27, 1 bukti) | DIUKUR: - | MESH 3D: 4.9x4.7x2.5 stud, lengan panjang
- `16089902603` Cross Hoodie — jenis=hoodie(83) | tema=punk(29)/gothic(13) | subjek=salib(45)/bintang(26) | pola=polkadot(37) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:punk] | gender=cowok(2, 1 bukti) | DIUKUR: - | MESH 3D: 3.0x1.9x1.1 stud, lengan panjang
- `9239518791` Rainbow T-Shirt — jenis=kaos(63) | tema=kawaii(89)/pantai(3) | subjek=logo(31)/hati(14) | pola=pelangi(100) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | gender=netral(0, 1 bukti) | MESH 3D: 7.5x6.3x3.1 stud
- `5891866853` Black Rose Shirt — jenis=kaos(37) | tema=iblis(13)/formal(13) | subjek=bunga(36)/kelelawar(5) | pola=loreng(26) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:iblis] | gender=cewek(1, 1 bukti)

### bawah
- `6469871908` PINK PANTS — jenis=legging(25) | tema=kawaii(51)/biasa(16) | subjek=bunga(6)/kelinci(5) | pola=polos(47) | panjang=panjang fit=lebar | [gambar:kawaii] | MOTIF DIUKUR: polos(92) | fungsi=pakaian | gender=cowok(20, 1 bukti) | DIUKUR: -
- `16536197442` ♡ siamese cat slippers — jenis=zirah_bawah(25) | tema=kawaii(73)/kostum_hewan(10) | subjek=kucing(94)/anjing(1) | pola=motif_hewan(66) | panjang=selutut fit=lebar | [gambar:kawaii] | gender=cewek(20, 1 bukti) | MESH 3D: 1.8x1.0x1.4 stud
- `5923212440` Kestrel | Black Snap Pants with White AF1s — jenis=jogger(62) | tema=formal(12)/biasa(8) | subjek=tanpa(6)/salib(4) | pola=denim(52) | panjang=panjang fit=lebar | [gambar:formal] | MOTIF DIUKUR: polos(54) | fungsi=pakaian | gender=cowok(1, 1 bukti) | DIUKUR: -
- `9353911507` Cute Blue Checkered Goth Pleated Skirt — jenis=rok_pendek(71) | tema=gothic(21)/kawaii(18) | subjek=musik(35)/bendera(8) | pola=kotak(64) | panjang=pendek fit=lebar | [gambar:punk] | gender=cewek(60, 2 bukti) | MESH 3D: 1.4x1.0x0.9 stud, rok/gaun, panjang pendek
- `5374208354` Extra High-waisted White Skirt + Heels — jenis=rok_pendek(63) | tema=gaun_elegan(15)/malaikat(9) | subjek=hantu(6)/tanpa(6) | pola=denim(24) | panjang=pendek fit=lebar | [gambar:biasa] | fungsi=pakaian | gender=cewek(87, 3 bukti) | DIUKUR: -
- `6494648978` Preppy Set! — jenis=bawahan_gaun(39) | tema=kawaii(65)/coquette(9) | subjek=pita(10)/hati(9) | pola=bulu(37) | panjang=pendek fit=lebar | [gambar:kawaii] | MOTIF DIUKUR: polos(73) | fungsi=pakaian | gender=cewek(48, 1 bukti) | DIUKUR: menutup badan, kaus kaki/stoking
- `12787796216` (1.0) Fire and Ice Aura - Legs — jenis=jeans(28) | tema=peri(14)/malaikat(13) | subjek=api(56)/petir(14) | pola=pelangi(92) | panjang=pendek fit=lebar | [gambar:peri] | gender=cowok(1, 1 bukti) | MESH 3D: 2.2x2.2x1.2 stud, celana
- `5242175930` beige — jenis=kargo(68) | tema=biasa(19)/formal(12) | subjek=mahkota(7)/tanpa(6) | pola=polos(35) | panjang=panjang fit=lebar | [gambar:biasa] | MOTIF DIUKUR: polos(88) | fungsi=pakaian | gender=cowok(20, 1 bukti) | DIUKUR: -
- `4666031720` Snow Pants — jenis=celana_kain(45) | tema=musim_dingin(38)/formal(31) | subjek=kelelawar(12)/salib(9) | pola=denim(26) | panjang=panjang fit=lebar | [gambar:formal]
- `6010099006` Black Trench Pants — jenis=zirah_bawah(32) | tema=gothic(11)/ksatria(9) | subjek=kelelawar(6)/salib(4) | pola=loreng(49) | panjang=panjang fit=lebar | [gambar:gothic] | MOTIF DIUKUR: polos(67) | fungsi=pakaian | gender=cewek(5, 2 bukti) | DIUKUR: -
- `87677968961124` Blue Accordion Pleated Skirt [PBR] — jenis=rok_pendek(43) | tema=sekolah(30)/formal(15) | subjek=bendera(14)/tanpa(11) | pola=garis(50) | panjang=pendek fit=lebar | [gambar:sekolah] | gender=cewek(60, 2 bukti) | MESH 3D: 1.5x1.4x0.9 stud, rok/gaun, melebar ke bawah, panjang pendek
- `15638002297` 🛍️Puff Sleeve Dress — jenis=bawahan_gaun(76) | tema=tradisional(55)/sekolah(12) | subjek=salib(26)/pita(14) | pola=kotak(22) | panjang=pendek fit=lebar | [gambar:tradisional] | gender=cewek(60, 2 bukti)
- `85102288379004` L$ - Baggy Sport Sweatpants (White) — jenis=jogger(41) | tema=sporty(37)/maid(18) | subjek=rantai(14)/petir(13) | pola=garis(89) | panjang=panjang fit=lebar | [gambar:maid] | MESH 3D: 3.4x3.5x1.5 stud, celana, panjang panjang
- `15223988363` Christmas Santa Long Sleeve Dress — jenis=bawahan_gaun(48) | tema=natal(100)/musim_dingin(0) | subjek=pita(40)/buah(7) | pola=bulu(38) | panjang=pendek fit=lebar | [gambar:natal] | gender=cewek(60, 2 bukti) | temaBukti=natal(3 poin)
- `4703301264` Celana SMA — jenis=jeans(46) | tema=anime(22)/sekolah(17) | subjek=hantu(6)/hiu(6) | pola=denim(76) | panjang=panjang fit=lebar | [gambar:biasa] | MOTIF DIUKUR: polos(62) | fungsi=pakaian | gender=cowok(28, 2 bukti) | DIUKUR: -
- `5095150875` ramen — jenis=kostum_bawah(45) | tema=novelty(61)/kerajaan(18) | subjek=mahkota(50)/labu(7) | pola=motif_hewan(63) | panjang=panjang fit=lebar | [gambar:kerajaan] | MOTIF DIUKUR: ramai(67) | fungsi=pakaian | gender=netral(0, 1 bukti) | DIUKUR: menutup badan
- `6979254581` mary janes — jenis=rok_pendek(40) | tema=sekolah(20)/kawaii(7) | subjek=logo(11)/pita(5) | pola=garis(43) | panjang=panjang fit=lebar | [gambar:formal] | fungsi=pakaian | gender=cewek(3, 1 bukti) | DIUKUR: -
- `74837538182808` Gray Sweatpants & Sneakers — jenis=jogger(44) | tema=penyihir(15)/y2k(13) | subjek=rantai(24)/hantu(16) | pola=denim(33) | panjang=panjang fit=lebar | [gambar:penyihir] | gender=cewek(27, 1 bukti) | MESH 3D: 2.4x3.2x1.2 stud, celana, panjang panjang
- `94261287950141` Leggings White Baddie Skinny Sport Gym 2000s Y2K — jenis=legging(87) | tema=sporty(28)/y2k(18) | subjek=hati(8)/logo(8) | pola=polos(28) | panjang=panjang fit=ketat | [gambar:biasa] | MOTIF DIUKUR: polos(84) | gender=cewek(74, 11 bukti) | MESH 3D: 1.1x3.0x0.7 stud, celana, panjang panjang
- `1004054816` Secret Service — jenis=celana_kain(35) | tema=biasa(22)/formal(18) | subjek=salib(5)/bintang(5) | pola=polos(74) | panjang=pendek fit=lebar | [gambar:formal] | gender=cewek(14, 1 bukti)
- `82547670475077` Y2K Plaid Pajamas Pink — jenis=rok_pendek(43) | tema=y2k(36)/coquette(32) | subjek=beruang(28)/bunga(8) | pola=kotak(92) | panjang=panjang fit=lebar | [gambar:coquette] | gender=cewek(12, 5 bukti) | MESH 3D: 1.6x2.7x1.1 stud, celana, panjang panjang
- `17586694803` All-White Skin-Tight Suit — jenis=zirah_bawah(46) | tema=formal(35)/superhero(14) | subjek=hantu(17)/ular(13) | pola=polos(28) | panjang=panjang fit=ketat | [gambar:superhero] | MESH 3D: 3.4x5.6x1.1 stud, rok/gaun, panjang panjang
- `6501642465` pink cow — jenis=celana_pendek(34) | tema=kawaii(53)/pantai(19) | subjek=bunga(6)/kupu_kupu(6) | pola=denim(56) | panjang=pendek fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(43, 1 bukti) | DIUKUR: menutup badan, kaus kaki/stoking
- `6443309665` green — jenis=kargo(38) | tema=punk(51)/y2k(12) | subjek=katak(11)/musik(7) | pola=grafis(43) | panjang=panjang fit=lebar | [gambar:formal] | MOTIF DIUKUR: polos(69) | fungsi=pakaian | gender=cowok(2, 1 bukti) | DIUKUR: -
- `4318467995` Baby — jenis=kostum_bawah(75) | tema=kawaii(47)/kostum_hewan(13) | subjek=pita(11)/makanan(10) | pola=pelangi(61) | panjang=pendek fit=lebar | [gambar:kawaii] | fungsi=pakaian | gender=cewek(7, 1 bukti) | DIUKUR: menutup badan

### kepala
- `6070758616` Fluffy White Winter Hood — jenis=tudung(36) | tema=musim_dingin(47)/malaikat(10) | subjek=tengkorak(23)/beruang(12) | [gambar:musim_dingin] | gender=cewek(1, 1 bukti) | temaBukti=musim_dingin(3 poin)
- `11988484192` Valentines Pink love heart Bow — jenis=pita_bando(100) | tema=coquette(99)/gaun_elegan(0) | subjek=pita(81)/hati(18) | [gambar:coquette] | gender=cewek(16, 1 bukti) | temaBukti=coquette(5 poin)
- `3438342658` International Fedora - Argentina — jenis=topi_formal(61) | tema=koboi(35)/biasa(15) | subjek=bendera(74)/tanpa(4) | [gambar:koboi] | gender=netral(0, 221 bukti)
- `12072541792` white vintage headphones — jenis=headphone(99) | tema=steampunk(42)/antariksa(19) | subjek=rantai(52)/musik(12) | [gambar:steampunk] | gender=cowok(1, 1 bukti)
- `12596837133` Blueberry Dango Earrings — jenis=anting(67) | tema=kawaii(39)/penyihir(11) | subjek=makanan(26)/bulan(14) | [gambar:kawaii] | gender=cewek(44, 1 bukti)
- `7345242790` Slogan Cap - Miami, Florida — jenis=topi_baseball(74) | tema=sporty(30)/streetwear(25) | subjek=tulisan(49)/logo(13) | [gambar:sporty] | gender=cewek(27, 1 bukti)
- `6999094193` Big Head ShowCaster TV fnf — jenis=topi_formal(52) | tema=formal(85)/vampir(6) | subjek=kartun(41)/hantu(40) | [gambar:formal] | gender=cowok(4, 1 bukti)
- `7028832960` Tilted Gray Plaid Cap — jenis=topi_baseball(68) | tema=streetwear(20)/biasa(18) | subjek=tanpa(24)/salib(20) | [gambar:streetwear] | gender=cewek(32, 1 bukti)
- `7895645634` (Back Tilt) Samurai Hat — jenis=topi_lain(43) | tema=pantai(37)/ninja(37) | subjek=ular(27)/tanpa(10) | [gambar:pantai] | gender=cowok(17, 1 bukti)
- `112601040` Jade Summer Shade — jenis=kupluk(22) | tema=pantai(58)/militer(10) | subjek=ular(72)/katak(18) | [gambar:pantai] | gender=cewek(25, 1 bukti) | temaBukti=pantai(3 poin)
- `12593961624` X Shaped Simple Hair Clips — jenis=topi_baseball(23) | tema=biasa(36)/iblis(24) | subjek=salib(57)/logo(9) | [gambar:iblis] | gender=cewek(1, 1 bukti)
- `4995603056` Black Divot Bunny Ears — jenis=headphone(48) | tema=formal(34)/sporty(14) | subjek=kelinci(41)/kelelawar(12) | [gambar:formal] | gender=netral(0, 1 bukti)
- `48474313` Red Roblox Cap — jenis=topi_baseball(92) | tema=sporty(82)/streetwear(5) | subjek=logo(36)/tulisan(10) | [gambar:sporty] | gender=cewek(1, 254 bukti)
- `5314840741` Mini Hoop Diamond Earrings — jenis=anting(72) | tema=kerajaan(53)/steampunk(27) | subjek=rantai(27)/mahkota(24) | [gambar:kerajaan] | gender=cowok(29, 1 bukti)
- `10203753231` Sometimes, Forever Cap - Soccer Mommy — jenis=topi_baseball(82) | tema=sporty(89)/coquette(4) | subjek=tulisan(38)/logo(30) | [gambar:sporty] | gender=cewek(10, 2 bukti) | temaBukti=sporty(4 poin)
- `4391384843` International Fedora - Russia — jenis=topi_formal(38) | tema=antariksa(16)/badut(14) | subjek=bendera(93)/makanan(1) | [gambar:antariksa] | gender=netral(0, 118 bukti)
- `12459507563` Star Goggles — jenis=halo(75) | tema=penyihir(24)/malaikat(19) | subjek=bintang(77)/bulan(7) | [gambar:penyihir] | gender=cewek(3, 1 bukti)
- `10097155007` Red Racing Helmet — jenis=helm(53) | tema=badut(12)/natal(11) | subjek=buah(34)/mata(22) | [gambar:badut]
- `71499623` Dark Horns of Pwnage — jenis=tanduk(66) | tema=vampir(47)/gothic(36) | subjek=kelelawar(97)/naga(2) | [gambar:vampir] | gender=cewek(15, 19 bukti)
- `273377471` Neon Blue Animal Hoodie — jenis=telinga(75) | tema=kostum_hewan(41)/cyber(35) | subjek=kucing(43)/anjing(22) | [gambar:kostum_hewan] | gender=cowok(1, 4 bukti)
- `5460019377` Axolotl Gills — jenis=telinga(34) | tema=coquette(64)/kawaii(10) | subjek=kelinci(41)/hati(12) | [gambar:coquette] | gender=cewek(28, 11 bukti)
- `8626011621` Black Fuzzy Winter Headband — jenis=pita_bando(40) | tema=musim_dingin(35)/gothic(35) | subjek=tanpa(9)/bulan(7) | [gambar:gothic] | gender=cewek(12, 3 bukti)
- `6313180813` Valentines Heart Boppers Pink — jenis=pita_bando(63) | tema=coquette(86)/peri(8) | subjek=hati(53)/pita(34) | [gambar:coquette] | gender=cewek(20, 1 bukti)
- `42847646` Fancy Matching Sweater Cap — jenis=kupluk(53) | tema=tradisional(27)/musim_dingin(15) | subjek=tengkorak(18)/bunga(16) | [gambar:tradisional] | gender=netral(0, 1 bukti)
- `11308550547` Chemistry Teacher Face Mask — jenis=topeng_kepala(60) | tema=novelty(20)/koboi(7) | subjek=beruang(16)/bebek(12) | [gambar:novelty] | gender=netral(0, 3 bukti)

### rambut
- `5918510414` Blonde Anime Princess Ponytails — tema=coquette(38)/anime(35) | [gambar:coquette] | gender=cewek(71, 3 bukti)
- `14157122053` Wavy Half up Pigtails with Ribbons(Sky Blue) — tema=coquette(36)/kawaii(25) | [gambar:kawaii] | gender=cewek(75, 5 bukti)
- `13456148719` Blonde Hair — tema=coquette(38)/kawaii(18) | [gambar:coquette] | gender=cewek(30, 2 bukti)
- `417457909` Candy Apple Hair — tema=natal(47)/badut(18) | [gambar:natal] | gender=cewek(7, 2 bukti)
- `158066100` Master Fighter — tema=iblis(38)/vampir(20) | [gambar:iblis] | gender=cowok(45, 1 bukti)
- `11189196593` BB Hair - Spellbound - Blonde — tema=kawaii(30)/coquette(19) | [gambar:kawaii] | gender=netral(0, 1 bukti)
- `13743065265` Slicked Back Neon Green Hair Realistic Hairline — tema=cyber(45)/militer(19) | [gambar:militer] | gender=cewek(1, 1 bukti)
- `9122023757` Dark Blue Messy Hair (1.0) — tema=polisi(18)/gothic(10) | [gambar:polisi] | gender=cowok(14, 1 bukti)
- `12523698801` Black Wolf Hair — tema=gothic(31)/ninja(9) | [gambar:gothic] | gender=cewek(14, 2 bukti)
- `6294980031` Soft Long Blonde Bangs — tema=coquette(36)/kawaii(24) | [gambar:coquette] | gender=cewek(12, 1 bukti)
- `12635809632` Black Fantasy Royal Hair — tema=kerajaan(35)/punk(13) | [gambar:punk] | gender=cowok(1, 1 bukti)
- `12893233179` Royal Fairy Flowy Ponytail in Black — tema=gothic(38)/peri(19) | [gambar:gothic] | gender=cewek(6, 1 bukti)
- `13840632183` 💇 Messy Hair 💇 — tema=kawaii(91)/coquette(4) | [gambar:kawaii]
- `15033463245` Mash Hair — tema=gothic(17)/punk(14) | [gambar:gothic] | gender=netral(0, 1 bukti)
- `10793771018` Y2k Stylish Swoop HalfUp Ponytail (Blonde) — tema=y2k(37)/kawaii(13) | [gambar:kawaii] | gender=cewek(37, 1 bukti)
- `11007873671` Messy Curly Hair Blonde — tema=steampunk(33)/kerajaan(11) | [gambar:steampunk] | gender=cewek(14, 1 bukti)
- `7067610701` Brown Fluffy Messy Boy Hair — tema=musim_dingin(38)/pantai(4) | [gambar:pantai] | gender=cowok(64, 9 bukti)
- `14066449900` Bouncy Curls Hair(Black) — tema=gothic(23)/gaun_elegan(21) | [gambar:gothic] | gender=cewek(34, 1 bukti)
- `15266557256` Lelouch Hair — tema=punk(35)/gothic(10) | [gambar:punk] | gender=cewek(3, 1 bukti)
- `13458497312` Cool Anime Boy Light Brown Hair 2.0 — tema=anime(37)/militer(5) | [gambar:militer] | gender=cowok(62, 5 bukti)
- `12913836914` Fluffy Middle Part Wolf Cut (Black) — tema=musim_dingin(36)/gothic(17) | [gambar:gothic] | gender=cowok(66, 1 bukti)
- `501965259` Neon Orange Charmer — tema=cyber(35)/iblis(18) | [gambar:iblis] | gender=cowok(1, 1 bukti)
- `14331635554` Black Hair Rainbow — tema=cyber(54)/kerajaan(7) | [gambar:cyber] | gender=cowok(3, 2 bukti)
- `12600789698` Black to Red Fluffy Messy Cool Boy Hair — tema=iblis(39)/musim_dingin(35) | [gambar:iblis] | gender=cowok(68, 5 bukti)
- `15227860532` Straight Hair with Headphones(Dark Pink) — tema=kawaii(11)/steampunk(11) | [gambar:kawaii] | gender=cewek(24, 1 bukti)

### sepatu
- `76975737616155` LV Sneaker Trainer x Tyler The Creator ''Brown'' — tema=militer(23)/streetwear(21) | [gambar:militer]
- `82099575892293` Criss Cross Summer Strap Sandals — tema=pantai(61)/koboi(28) | [gambar:koboi]
- `92594210958064` Pink Glam Bow Slippers — tema=coquette(66)/kawaii(31) | [gambar:coquette] | temaBukti=coquette(3 poin)
- `90480394830189` White Spike High Socks - Right Shoe Accessory — tema=medis(29)/formal(12) | [gambar:medis] | gender=cewek(19, 1 bukti) | MESH 3D: 0.7x2.3x0.7 stud, bot
- `85879774916851` ☆ black ankle boots (it-girl) (red bottom) — tema=gothic(33)/vampir(8) | [gambar:gothic] | gender=cewek(60, 2 bukti)
- `76735528264420` ✅Y2K Star Pastel Pink Platform Shoes✅ — tema=coquette(37)/kawaii(33) | [gambar:coquette]
- `83386295932241` Red Skate Sneaker Shoes — tema=iblis(31)/sporty(17) | [gambar:iblis]
- `85483964778080` Zorzax - Left Boot — tema=polisi(27)/musim_dingin(15) | [gambar:polisi] | gender=cewek(1, 3 bukti) | MESH 3D: 0.2x0.6x0.6 stud
- `79105072619323` slides with socks - Right Shoe Accessory — tema=kawaii(82)/coquette(9) | [gambar:kawaii] | gender=cewek(19, 3 bukti) | MESH 3D: 0.3x0.6x0.8 stud
- `84887393233910` Star Panel Low-Top Sneakers (Blue) — tema=bajak_laut(57)/sporty(11) | [gambar:bajak_laut]
- `74367806345839` Fur Slides White Euina Fluffy Slippers Shoes — tema=musim_dingin(38)/sekolah(12) | [gambar:sekolah]
- `72501505129912` Red Shoes — tema=badut(20)/iblis(18) | [gambar:badut]
- `81064187124275` Red Chunky Spider Clogs 3.0 — tema=iblis(26)/sekolah(11) | [gambar:iblis]
- `78455436578591` ♾️ Black rose vine flower wrap around heels — tema=gothic(67)/gaun_elegan(12) | [gambar:gothic]
- `89452694917842` Pink Cute Alien Slippers - Left Shoe Accessory — tema=kostum_hewan(33)/kawaii(21) | [gambar:kostum_hewan] | gender=cewek(46, 1 bukti) | MESH 3D: 0.4x0.7x0.8 stud
- `83209667067717` Monster Shoes Black — tema=vampir(31)/gothic(29) | [gambar:vampir]
- `89041222388371` Y2k Cool Fur Boots (Red) - Left Shoe Accessory — tema=natal(41)/y2k(35) | [gambar:natal] | gender=cewek(32, 1 bukti) | MESH 3D: 0.8x1.7x1.1 stud, bot
- `96483588401493` Red Sneakers — tema=iblis(19)/natal(16) | [gambar:iblis]
- `92422416563822` ☆ fw2012 curved heeled platform boots (it girl) — tema=gothic(55)/coquette(21) | [gambar:gothic] | gender=cewek(60, 2 bukti)
- `73378130470627` Boots — tema=kostum_hewan(31)/gothic(19) | [gambar:kostum_hewan]
- `86920270171824` Black Streetwear Shoes — tema=streetwear(53)/polisi(17) | [gambar:streetwear] | temaBukti=streetwear(3 poin)
- `82542810482216` Rainbow Roller Skates — tema=badut(33)/y2k(28) | [gambar:badut]
- `84960880217895` Green Fur Fuzzy Furry Boots Y2K — tema=y2k(39)/kostum_hewan(23) | [gambar:kostum_hewan]
- `94154382737434` courtside - cork sandals[green] — tema=streetwear(20)/militer(19) | [gambar:streetwear]
- `86963839996937` Red Boots Shoes Stripes 3.0 — tema=musim_dingin(16)/punk(15) | [gambar:musim_dingin]

### wajah
- `5700133881` Medical Mask (White) — jenis=masker(73) | tema=maid(31)/malaikat(23) | subjek=tanpa(27)/hantu(10) | [gambar:maid] | gender=cowok(20, 5 bukti)
- `6714978691` Eyeliner — jenis=penutup_mata(29) | tema=vampir(14)/ksatria(13) | subjek=kelelawar(17)/logo(14) | [gambar:vampir] | gender=cewek(59, 1 bukti)
- `13490141518` Piercing Set Y2K — jenis=tindik(51) | tema=y2k(37)/horor(6) | subjek=hantu(11)/petir(9) | [gambar:horor] | gender=netral(0, 1 bukti)
- `4794152748` Red Badass Shades for Badass Individuals — jenis=kacamata_hitam(39) | tema=superhero(21)/natal(12) | subjek=bendera(22)/logo(21) | [gambar:superhero] | gender=cowok(44, 1 bukti)
- `6343864578` Heart Flip-Up Sunglasses (Black) — jenis=kacamata_hitam(61) | tema=formal(12)/bajak_laut(11) | subjek=hati(61)/pita(8) | [gambar:formal]
- `13505630514` Green Retro Glasses — jenis=kacamata_hitam(52) | tema=sporty(16)/superhero(13) | subjek=katak(57)/logo(10) | [gambar:sporty]
- `15589895609` Christmas Morning Cheeks Head Nougat Skin Tone — jenis=riasan(54) | tema=natal(36)/kawaii(15) | subjek=tulisan(12)/kartun(8) | [gambar:kawaii] | gender=cewek(13, 2 bukti)
- `14112059057` Ski Sunglasses — jenis=kacamata_hitam(98) | tema=cyber(30)/pantai(23) | subjek=tanpa(23)/tulisan(12) | [gambar:cyber] | gender=cowok(5, 1 bukti)
- `15590377869` It's Cold Makeup Cheeks Head Light Skin Tone — jenis=riasan(73) | tema=kawaii(35)/coquette(27) | subjek=tulisan(11)/kartun(10) | [gambar:kawaii] | gender=cewek(43, 7 bukti)
- `12355630947` 😶 Faceless 😶 — jenis=penutup_mata(30) | tema=militer(33)/gaun_elegan(9) | subjek=tanpa(28)/mahkota(16) | [gambar:militer] | gender=netral(0, 1 bukti)
- `16000385633` Cute Bangs (Black) — jenis=tindik(23) | tema=kawaii(35)/gothic(17) | subjek=pita(23)/wajah_anime(16) | [gambar:gothic] | gender=cewek(3, 1 bukti)
- `15288944836` Cute Freckled Green Eyed Blushing Makeup Face — jenis=riasan(81) | tema=kawaii(45)/coquette(25) | subjek=mata(10)/kartun(10) | [gambar:coquette] | gender=cewek(45, 1 bukti)
- `13905779728` (Cheeks) Eyeless — jenis=penutup_mata(25) | tema=militer(59)/polisi(26) | subjek=logo(26)/tanpa(21) | [gambar:militer] | gender=netral(0, 3 bukti)
- `11102921066` Nose piercing spikes — jenis=tindik(70) | tema=sekolah(9)/gaun_elegan(8) | subjek=mahkota(15)/tanpa(11) | [gambar:sekolah] | gender=cowok(3, 4 bukti)
- `14944985611` elf ear — jenis=tindik(46) | tema=kerajaan(34)/gaun_elegan(14) | subjek=mahkota(26)/bulan(12) | [gambar:kerajaan] | gender=netral(0, 1 bukti)
- `4708210325` Cracked Porcelain Face — jenis=kumis_jenggot(36) | tema=gaun_elegan(11)/punk(9) | subjek=laba_laba(29)/petir(14) | [gambar:gaun_elegan] | gender=cewek(2, 4 bukti)
- `12667908486` Eyebrow Cutted — jenis=kumis_jenggot(84) | tema=vampir(11)/ninja(7) | subjek=logo(23)/mata(14) | [gambar:vampir] | gender=cowok(34, 3 bukti)
- `14157137406` Old Retro Classic Face (Noob) — jenis=masker(28) | tema=novelty(45)/badut(9) | subjek=kartun(21)/logo(11) | [gambar:novelty] | gender=cewek(15, 1 bukti) | temaBukti=novelty(3 poin)
- `12064732367` 😄 Blushing Big Smile Face (3D) 😄 — jenis=riasan(57) | tema=coquette(13)/kawaii(12) | subjek=pita(10)/kucing(6) | [gambar:coquette] | gender=cewek(32, 62 bukti)
- `6564544342` Styled Edges v2 — jenis=kumis_jenggot(99) | tema=gothic(15)/coquette(15) | subjek=ular(32)/pita(15) | [gambar:gothic] | gender=cowok(26, 5 bukti)
- `14811617346` Spider Web Face Sticker 🕷️ — jenis=riasan(40) | tema=gothic(57)/halloween(17) | subjek=laba_laba(99)/kelelawar(0) | [gambar:gothic] | gender=cewek(21, 1 bukti)
- `15553320899` EPIC MONEY 🤑 — jenis=masker(34) | tema=vampir(28)/novelty(22) | subjek=uang(76)/buah(14) | [gambar:vampir] | gender=cewek(3, 9 bukti)
- `11108901454` West Elm Sophisticated Glasses — jenis=kacamata(97) | tema=formal(14)/medis(11) | subjek=tanpa(20)/tulisan(12) | [gambar:formal] | gender=cowok(6, 6 bukti)
- `9922633567` 🔴 Red Angry Anime Hitmarker Filter 🔴 — jenis=kumis_jenggot(22) | tema=anime(36)/iblis(13) | subjek=wajah_anime(35)/logo(33) | [gambar:iblis] | gender=cowok(20, 1 bukti)
- `13950662956` Tactical Black Neck Scarf — jenis=masker(64) | tema=polisi(40)/militer(37) | subjek=logo(15)/tanpa(12) | [gambar:polisi] | gender=cowok(1, 3 bukti)

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 299, malaikat 192, gothic 172, coquette 155, formal 140, kostum_hewan 131, punk 108, cyber 101, steampunk 100, iblis 100, militer 98, peri 96
- atas: kawaii 926, formal 648, gothic 263, biasa 255, punk 238, sporty 223, cyber 217, steampunk 217, militer 213, y2k 178, halloween 168, novelty 165
- bawah: formal 657, kawaii 616, y2k 422, biasa 350, gothic 328, punk 288, sekolah 261, coquette 245, musim_dingin 238, militer 196, maid 172, halloween 165
- kepala: coquette 231, kawaii 214, kerajaan 188, formal 165, malaikat 150, militer 140, gothic 126, peri 111, kostum_hewan 109, penyihir 98, iblis 98, polisi 94
- rambut: kawaii 431, gothic 397, coquette 218, anime 183, steampunk 169, gaun_elegan 169, koboi 148, musim_dingin 145, punk 138, malaikat 119, iblis 91, y2k 85
- sepatu: kawaii 317, coquette 268, musim_dingin 247, sporty 231, gothic 214, y2k 187, kostum_hewan 154, pantai 120, militer 100, punk 97, formal 90, koboi 79
- wajah: kawaii 432, steampunk 233, gothic 181, militer 173, cyber 158, coquette 141, malaikat 93, anime 89, polisi 81, iblis 77, pantai 70, bajak_laut 67

## Motif diukur dari piksel (rev 33, motif.py)

Klaim bila peluang >= ambang per grup/kelas (motif.KLAIM; 3D kotak/grafis tidak diklaim). Presisi = uji silang 5 lipat terhadap kata motif di nama (batas bawah: nama bisa salah).

| grup | item berfitur | dilatih | kelas: benar/diklaim (recall) |
|---|---|---|---|
| baju | 12727 | 975 | garis 78/89 (54%), grafis 21/32 (22%), kotak 22/26 (22%), polos 307/352 (76%), ramai 47/54 (31%), taburan 12/12 (16%) |
| celana | 12498 | 1045 | garis 17/19 (17%), grafis 1/1 (3%), kotak 43/48 (28%), polos 455/573 (82%), ramai 50/60 (34%), taburan 1/1 (2%) |
| 3D | 5986 | 529 | garis 65/69 (47%), grafis 0/0 (0%), kotak 0/0 (0%), polos 66/90 (61%), ramai 54/69 (41%), taburan 0/0 (0%) |

Sebaran: tidak pasti 17815, polos 10441, ramai 1292, grafis 764, garis 610, kotak 267, taburan 22

