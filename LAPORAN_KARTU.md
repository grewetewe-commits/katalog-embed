# Laporan Kartu Item (MATA v2) — versi 1792132306

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **133329**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 11653 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7512 | 0.0 | 57% | 69% | 57% | 54% |
| aksen/tema | 7653 | 0.75 | 29% | 42% | 28% | 28% |
| atas2D/jenis | 5742 | 1.0 | 15% | 23% | 8% | 15% |
| atas2D/pola | 1060 | 0.75 | 49% | 62% | 47% | 49% |
| atas2D/subjek | 2131 | 0.5 | 33% | 43% | 31% | 32% |
| atas2D/tema | 4285 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5365 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2051 | 0.5 | 55% | 66% | 51% | 53% |
| atas3D/subjek | 1991 | 0.25 | 30% | 40% | 30% | 29% |
| atas3D/tema | 3340 | 1.0 | 30% | 40% | 27% | 30% |
| bawah2D/jenis | 3982 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2393 | 1.0 | 44% | 56% | 35% | 44% |
| bawah2D/subjek | 1716 | 0.75 | 14% | 22% | 11% | 14% |
| bawah2D/tema | 4007 | 0.5 | 26% | 31% | 21% | 23% |
| bawah3D/jenis | 3158 | 0.75 | 52% | 72% | 51% | 52% |
| bawah3D/pola | 1981 | 1.0 | 50% | 62% | 45% | 50% |
| bawah3D/subjek | 932 | 0.25 | 27% | 36% | 27% | 24% |
| bawah3D/tema | 1961 | 0.25 | 20% | 30% | 20% | 19% |
| kepala/jenis | 9751 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5426 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 7006 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5220 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2324 | 0.5 | 22% | 32% | 21% | 20% |
| wajah/jenis | 3699 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1559 | 0.25 | 47% | 55% | 47% | 45% |
| wajah/tema | 2117 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Akurasi terhadap LABEL EMAS (dilihat mata, gambar 420 px; uji2d/emas.json)

Garis dasar fase 1 (16 Okt pagi, sampel sama, top-1 gambar saja): baju jenis 26%, celana jenis 14%, baju tema 41%,
celana tema 35%, pola 39-40%, kaos fungsi belum ada.

| tipe | facet | n | benar | akurasi | tanpa kartu |
|---|---|---|---|---|---|
| baju 2D | jenis | 57 | 27 | 47% | 0 |
| baju 2D | tema | 37 | 24 | 65% | 0 |
| baju 2D | pola | 54 | 17 | 31% | 0 |
| celana 2D | jenis | 43 | 23 | 53% | 0 |
| celana 2D | tema | 23 | 12 | 52% | 0 |
| celana 2D | pola | 48 | 20 | 42% | 0 |
| kaos klasik | fungsi | 55 | 48 | 87% | 0 |

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween]
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi]
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut]
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(40)/mata(16) | [gambar:steampunk]
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(79) | tema=maid(97)/punk(1) | subjek=salib(6)/rantai(6) | pola=bulu(56) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:maid]
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=jas(38) | tema=formal(97)/gothic(1) | subjek=kelelawar(10)/salib(8) | pola=bulu(47) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:formal]
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat]
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(50)/bulan(32) | [gambar:steampunk]
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(97) | tema=kawaii(82)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(100) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal]
- `382538059` Green Jersey (atas): jenis=jersey(100) | tema=sporty(100)/y2k(0) | subjek=katak(24)/bintang(9) | pola=bunga(68) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty]
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(45)/formal(19) | subjek=salib(23)/kelelawar(12) | pola=kulit(59) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic]
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette]
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(99) | tema=y2k(49)/punk(35) | subjek=bulan(6)/rantai(6) | pola=denim(99) | panjang=pendek fit=lebar | [gambar:gothic]
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(60) | tema=gothic(76)/punk(23) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(98) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber]
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii]
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan]
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(23)/tulisan(9) | [gambar:streetwear]
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii]
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween]
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=kaos(41) | tema=halloween(95)/kawaii(4) | subjek=labu(45)/beruang(19) | pola=pelangi(78) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween]
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=jeans(40) | tema=halloween(98)/kawaii(1) | subjek=labu(48)/beruang(18) | pola=kotak(36) | panjang=pendek fit=lebar | [gambar:halloween]

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=jaket(93) | tema=antariksa(79)/cyber(21) | subjek=wajah_anime(13)/tulisan(9) | pola=loreng(74) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis
- `1239904` Akatsuki — nama: anime | jenis=kaos(97) | tema=anime(97)/horor(2) | subjek=api(18)/buah(14) | pola=bulu(56) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:horor] | fungsi=grafis
- `1260428` Guitar Hero 2 Logo — nama: superhero | jenis=kaos(99) | tema=superhero(94)/punk(5) | subjek=logo(28)/musik(26) | pola=kotak(49) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:ninja] | fungsi=grafis
- `1397335` Me with snow wolf shirt. — nama: musim_dingin | jenis=hoodie(63) | tema=musim_dingin(97)/streetwear(2) | subjek=kartun(9)/hiu(7) | pola=polos(79) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:polisi] | fungsi=grafis
- `1431511` ninja shirt — nama: ninja | jenis=kaos(95) | tema=ninja(97)/biasa(2) | subjek=logo(25)/tulisan(9) | pola=catur(33) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori
- `1475939` Noob shirt — nama: novelty | jenis=kaos(56) | tema=novelty(100)/formal(0) | subjek=logo(8)/hati(7) | pola=pelangi(84) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan
- `1503598` Evil Camo V.S. Magma — nama: militer | jenis=jas(96) | tema=militer(50)/badut(22) | subjek=wajah_anime(9)/buah(9) | pola=loreng(89) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:iblis] | fungsi=grafis
- `1515399` My cute kitty! :) — nama: kawaii | jenis=kaos(95) | tema=kawaii(66)/superhero(25) | subjek=kucing(76)/anjing(6) | pola=polkadot(95) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis
- `1521989` shadow military lvl 1 — nama: militer | jenis=rompi(88) | tema=militer(93)/cyber(2) | subjek=logo(13)/katak(11) | pola=garis(34) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:pantai] | fungsi=grafis
- `1558188` Random Anime Character I made — nama: anime | jenis=jas(44) | tema=anime(84)/superhero(8) | subjek=wajah_anime(39)/naga(8) | pola=polos(98) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:vampir] | fungsi=grafis
- `1591061` Cute Wolf — nama: kawaii | jenis=kaos(99) | tema=kawaii(95)/punk(4) | subjek=anjing(69)/wajah_anime(5) | pola=grafis(82) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan] | fungsi=badan
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(57) | tema=sporty(96)/y2k(4) | subjek=tulisan(37)/petir(13) | pola=polkadot(98) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k] | fungsi=grafis
- `1621982` Yellow Dragon of the Western Winds — nama: koboi | jenis=kemeja(96) | tema=koboi(84)/y2k(6) | subjek=naga(92)/dinosaurus(2) | pola=grafis(96) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kerajaan] | fungsi=grafis
- `1636113` Ninja Drone Of Shadows Version 2 — nama: ninja | jenis=jas(82) | tema=ninja(91)/gothic(4) | subjek=laba_laba(87)/ular(1) | pola=renda(86) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori
- `1639327` Cyber Suit35 — nama: cyber | jenis=kostum_penuh(55) | tema=cyber(63)/sporty(31) | subjek=logo(32)/bendera(10) | pola=catur(52) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:sporty] | fungsi=grafis
- `1639359` Cyber Suit31 — nama: cyber | jenis=jas(73) | tema=cyber(99)/ninja(0) | subjek=pita(24)/rantai(15) | pola=catur(65) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:pantai] | fungsi=aksesori
- `1639368` Cyber Suit29 — nama: cyber | jenis=rompi(44) | tema=cyber(93)/kawaii(4) | subjek=bulan(7)/bunga(6) | pola=catur(100) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:peri] | fungsi=grafis
- `1639414` Cyber Suit22 — nama: cyber | jenis=kaos(65) | tema=cyber(99)/streetwear(0) | subjek=bendera(16)/logo(15) | pola=catur(68) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:musim_dingin] | fungsi=aksesori
- `1639419` Cyber Suit21 — nama: cyber | jenis=kaos(72) | tema=cyber(100)/malaikat(0) | subjek=petir(23)/hiu(12) | pola=pelangi(82) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:punk] | fungsi=grafis
- `1639424` Cyber Suit20 — nama: cyber | jenis=kaos(89) | tema=cyber(84)/antariksa(14) | subjek=bulan(14)/petir(11) | pola=bunga(84) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:kawaii] | fungsi=badan
- `1639431` Cyber ###### — nama: cyber | jenis=jas(70) | tema=cyber(97)/penyihir(2) | subjek=bintang(15)/bulan(14) | pola=kilau(87) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:steampunk] | fungsi=aksesori
- `1639438` Cyber Suit18 — nama: cyber | jenis=jubah(87) | tema=cyber(92)/musim_dingin(2) | subjek=bulan(29)/hiu(17) | pola=kilau(44) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:pantai] | fungsi=pakaian
- `1639470` Cyber Suit14 — nama: cyber | jenis=jaket(39) | tema=cyber(67)/gothic(21) | subjek=bulan(27)/rantai(17) | pola=catur(89) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:gothic] | fungsi=aksesori
- `1639518` Cyber ##### — nama: cyber | jenis=hoodie(58) | tema=cyber(100)/sporty(0) | subjek=hiu(18)/logo(17) | pola=kilau(56) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty] | fungsi=grafis
- `1648160` ninja — nama: ninja | jenis=jas(45) | tema=ninja(96)/badut(2) | subjek=logo(44)/tulisan(5) | pola=polkadot(50) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis
- `1705783` Halloween Tails — nama: halloween | jenis=jubah(72) | tema=halloween(57)/kostum_hewan(19) | subjek=kucing(43)/hiu(13) | pola=pelangi(42) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis
- `1726226` Cutsey_Cosplay_by_Halogrunt — nama: anime | jenis=kaos(70) | tema=anime(82)/badut(10) | subjek=kucing(27)/katak(17) | pola=bulu(80) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:badut] | fungsi=grafis
- `1740755` Get a suit — nama: formal | jenis=jas(78) | tema=badut(57)/formal(41) | subjek=logo(9)/bulan(9) | pola=garis(99) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut] | fungsi=grafis
- `1749694` Striped Suit — nama: formal | jenis=jas(89) | tema=cyber(57)/formal(36) | subjek=logo(23)/petir(9) | pola=garis(93) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:iblis] | fungsi=aksesori
- `1753596` Cowboy NeckHat — nama: koboi | jenis=kostum_penuh(92) | tema=koboi(90)/halloween(7) | subjek=labu(77)/makanan(3) | pola=bulu(87) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:halloween] | fungsi=aksesori
- `1756352` cute — nama: kawaii | jenis=hoodie(48) | tema=kawaii(58)/novelty(34) | subjek=api(27)/petir(11) | pola=pelangi(96) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis
- `1769012` CUTE! — nama: kawaii | jenis=hoodie(52) | tema=formal(52)/kawaii(45) | subjek=bebek(36)/logo(11) | pola=polkadot(83) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:kostum_hewan] | fungsi=grafis
- `1769022` I-Pod tux — nama: formal | jenis=hoodie(48) | tema=formal(74)/y2k(10) | subjek=bebek(40)/logo(8) | pola=garis(84) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis
- `1769048` Luke Tux — nama: formal | jenis=hoodie(81) | tema=formal(99)/kawaii(0) | subjek=bebek(31)/logo(11) | pola=bulu(84) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:bajak_laut] | fungsi=grafis
- `1769060` Metal Tux — nama: formal | jenis=jaket(42) | tema=formal(68)/natal(23) | subjek=bebek(17)/katak(13) | pola=bulu(79) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:natal] | fungsi=grafis
- `1769091` Robin Tux — nama: formal | jenis=jaket(73) | tema=formal(76)/ninja(9) | subjek=bebek(44)/katak(8) | pola=bulu(38) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:ninja] | fungsi=grafis
- `1769097` ROBO TUX BEEP BOOP BOP! — nama: formal | jenis=jas(84) | tema=formal(93)/novelty(3) | subjek=hati(41)/logo(12) | pola=pelangi(97) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:badut] | fungsi=grafis
- `1769130` Spy Tux — nama: formal | jenis=jaket(79) | tema=formal(76)/cyber(11) | subjek=katak(20)/bebek(11) | pola=garis(95) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:cyber] | fungsi=grafis
- `1769138` Super Tux!!! — nama: formal | jenis=jaket(47) | tema=formal(91)/novelty(7) | subjek=bebek(33)/logo(8) | pola=garis(62) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:superhero] | fungsi=grafis
- `1769153` Toxic Tux XD — nama: formal | jenis=jaket(66) | tema=kawaii(53)/formal(38) | subjek=katak(44)/bebek(12) | pola=pelangi(65) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:kawaii] | fungsi=grafis

## Contoh acak per kelompok

### aksen
- `11554857728` (BACK) Doll Pull String in White 3.0 — jenis=kalung(57) | tema=badut(11)/malaikat(9) | subjek=rantai(41)/bulan(31) | [gambar:badut]
- `5463688787` Dark Flame Aura — jenis=kalung(40) | tema=steampunk(25)/malaikat(15) | subjek=api(36)/rantai(29) | [gambar:steampunk]
- `7550747484` Red Royal Cape — jenis=jubah_belakang(100) | tema=kerajaan(37)/ksatria(23) | subjek=kelelawar(38)/api(14) | [gambar:ksatria]
- `10016283188` Sunny Coat — jenis=jubah_belakang(59) | tema=musim_dingin(26)/tradisional(17) | subjek=mahkota(58)/beruang(7) | [gambar:musim_dingin]
- `4146870364` Rey’s Staff — jenis=senjata(60) | tema=ninja(36)/militer(18) | subjek=petir(17)/musik(14) | [gambar:ninja]
- `4645922861` Bait Box Backpack — jenis=tas(52) | tema=pantai(89)/bajak_laut(3) | subjek=dinosaurus(24)/hiu(14) | [gambar:pantai]
- `12725520054` Candy Lollipop — jenis=ekor(43) | tema=badut(71)/novelty(10) | subjek=makanan(88)/buah(5) | [gambar:badut]
- `501938437` Shoulder Raccoon — jenis=boneka(63) | tema=kostum_hewan(75)/iblis(4) | subjek=anjing(78)/kucing(5) | [gambar:kostum_hewan]
- `12460103329` cute paper wings — jenis=sayap(78) | tema=kawaii(36)/formal(10) | subjek=kelelawar(15)/pita(15) | [gambar:formal]
- `10781435597` Spiked Blue Curled Dragon Wings — jenis=sayap(56) | tema=punk(35)/peri(23) | subjek=naga(48)/kelelawar(39) | [gambar:peri]
- `7214682455` Snake Chain Black — jenis=kalung(93) | tema=punk(50)/gothic(44) | subjek=rantai(77)/ular(19) | [gambar:punk]
- `7486208318` Cute Bat Backpack — jenis=boneka(45) | tema=kawaii(35)/vampir(24) | subjek=kelelawar(99)/kucing(0) | [gambar:vampir]
- `12853218935` AURA GALAXY 🌌 — jenis=alat_musik(19) | tema=antariksa(59)/penyihir(21) | subjek=bulan(89)/bintang(5) | [gambar:antariksa]
- `11993116080` Giant Panda Baby Pet Black Backpack White Animal — jenis=boneka(70) | tema=kostum_hewan(82)/formal(3) | subjek=beruang(54)/kartun(14) | [gambar:kostum_hewan]
- `4376960922` Police Utility Belt — jenis=sabuk(67) | tema=polisi(67)/militer(7) | subjek=petir(15)/salib(11) | [gambar:polisi]
- `12420961119` Cute Ruffled Bow Collar in White and Black — jenis=lain(60) | tema=maid(38)/coquette(20) | subjek=pita(80)/bunga(17) | [gambar:maid]
- `5505289480` [1.0] Red Shirt Collar — jenis=sabuk(36) | tema=iblis(44)/vampir(13) | subjek=logo(38)/pita(9) | [gambar:iblis]
- `6202789866` High Fashion Fuzzy & Fab Phone Case — jenis=kalung(66) | tema=peri(50)/kawaii(23) | subjek=pita(28)/kupu_kupu(14) | [gambar:peri]
- `356210971` Sophisticated Crow — jenis=sayap(83) | tema=vampir(31)/formal(22) | subjek=kelelawar(57)/bebek(9) | [gambar:vampir]
- `7853207982` Demon Tail Black — jenis=ekor(78) | tema=iblis(48)/ninja(15) | subjek=bulan(15)/logo(15) | [gambar:ninja]
- `8850987938` Rainbow Dark Matter Aura — jenis=alat_musik(41) | tema=y2k(11)/antariksa(9) | subjek=bintang(23)/musik(19) | [gambar:y2k]
- `6005520101` Candycane Wings — jenis=sayap(67) | tema=natal(52)/peri(23) | subjek=pita(85)/kupu_kupu(5) | [gambar:natal]
- `8212895789` Big Back Walrus Buddy — jenis=boneka(70) | tema=kostum_hewan(89)/novelty(3) | subjek=beruang(17)/hiu(16) | [gambar:kostum_hewan]
- `5255905993` Cartoony Rainbow Sword — jenis=senjata(93) | tema=pantai(28)/penyihir(23) | subjek=petir(66)/bunga(10) | [gambar:pantai]
- `6797949923` Cyan Mecha Arms (Under-Hanging) - LIGHT SERIES — jenis=kalung(24) | tema=cyber(56)/coquette(7) | subjek=rantai(34)/hati(7) | [gambar:cyber]

### atas
- `4959177259` T Shirt — jenis=kaos(86) | tema=biasa(77)/gothic(4) | subjek=kelelawar(9)/salib(8) | pola=polos(100) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:gothic]
- `72083925872383` ꒰ ♡ ꒱: pink ruffly sleeves — jenis=zirah(80) | tema=steampunk(35)/ksatria(13) | subjek=rantai(30)/hantu(8) | pola=polos(40) | lengan=tanpa panjang=panjang fit=pas depan=tertutup | [gambar:steampunk]
- `9239352995` Dark Blue Denim Jacket — jenis=jaket(77) | tema=formal(22)/polisi(17) | subjek=bulan(13)/tanpa(12) | pola=denim(91) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:formal]
- `14011573651` Y2K Sweater Striped Pattern Dark Purple — jenis=sweater(53) | tema=y2k(38)/antariksa(7) | subjek=beruang(10)/tanpa(9) | pola=garis(43) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:antariksa]
- `14021071118` Connect 2023 T-shirt — jenis=kaos(83) | tema=cyber(19)/y2k(14) | subjek=logo(38)/tulisan(20) | pola=tulisan(44) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:cyber]
- `3559538167` ouran — jenis=jas(100) | tema=formal(100)/sekolah(0) | subjek=pita(7)/uang(6) | pola=kilau(92) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `5446553424` Pink baby looney tunes crop — jenis=crop(95) | tema=kawaii(98)/peri(1) | subjek=makanan(12)/bunga(9) | pola=pelangi(100) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii]
- `13409194429` 🎇Glowing Wizard Staff on Hand - Black — jenis=kaos(37) | tema=steampunk(56)/penyihir(35) | subjek=petir(38)/musik(14) | pola=polos(23) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:steampunk]
- `1636113` Ninja Drone Of Shadows Version 2 — jenis=jas(82) | tema=ninja(91)/gothic(4) | subjek=laba_laba(87)/ular(1) | pola=renda(86) | lengan=panjang panjang=crop fit=pas depan=tertutup | [gambar:steampunk] | fungsi=aksesori
- `71870711226994` Cute Ruffled Bunny Bow Sleeves in Pink  — jenis=gaun(63) | tema=kawaii(29)/gaun_elegan(26) | subjek=hantu(38)/kelinci(20) | pola=renda(70) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:gaun_elegan]
- `12767304443` 💅Long French Tip Nails - White — jenis=tanktop(19) | tema=kawaii(27)/coquette(11) | subjek=petir(36)/pita(11) | pola=garis(59) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:kawaii]
- `4352782701` Astolfo — jenis=seragam(39) | tema=koboi(33)/kerajaan(19) | subjek=mahkota(20)/naga(5) | pola=bulu(92) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:steampunk]
- `12250528705` Logo White Piqué Polo — jenis=kemeja(38) | tema=sporty(68)/biasa(5) | subjek=logo(39)/bintang(16) | pola=polos(64) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:sporty]
- `5046688487` FNAF — jenis=seragam(33) | tema=halloween(91)/penyihir(3) | subjek=kupu_kupu(9)/kelelawar(7) | pola=kilau(93) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:penyihir]
- `18810149315` Hex Purple Hoodie With White Logo — jenis=hoodie(96) | tema=sporty(45)/musim_dingin(10) | subjek=logo(47)/bintang(19) | pola=polos(41) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:sporty]
- `14966571421` businessman suit — jenis=jas(80) | tema=formal(99)/gothic(0) | subjek=tanpa(15)/salib(14) | pola=polos(43) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:formal]
- `4995876755` Tupac '96 Tee — jenis=kaos(90) | tema=anime(33)/malaikat(30) | subjek=wajah_anime(8)/hantu(6) | pola=grafis(63) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:malaikat]
- `383137196` Rainbow Model Hoodie — jenis=hoodie(98) | tema=badut(34)/cyber(26) | subjek=kupu_kupu(17)/pita(8) | pola=pelangi(100) | lengan=panjang panjang=crop fit=pas depan=terbuka | [gambar:badut]
- `6473942024` Stich — jenis=crop(66) | tema=kawaii(39)/antariksa(17) | subjek=beruang(13)/kelinci(7) | pola=polos(75) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kawaii]
- `6465374553` FNF — jenis=kaos(99) | tema=novelty(85)/iblis(8) | subjek=bendera(9)/kartun(7) | pola=polos(38) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:novelty]
- `5044152285` USSF Uniform - Urban Shirt (2020) — jenis=seragam(60) | tema=militer(100)/ksatria(0) | subjek=ular(11)/bendera(7) | pola=loreng(100) | lengan=tanpa panjang=normal fit=longgar depan=terbuka | [gambar:militer]
- `12767112374` 💅French Tip Nails - Pink — jenis=tanktop(32) | tema=kawaii(88)/coquette(2) | subjek=wajah_anime(18)/buah(12) | pola=garis(33) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii]
- `16313741407` white cat plush (holdable) — jenis=jaket(41) | tema=gothic(39)/peri(20) | subjek=kucing(37)/bunga(14) | pola=bunga(29) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:gothic]
- `9239956594` Black Vest — jenis=rompi(50) | tema=formal(56)/gaun_elegan(18) | subjek=salib(33)/tanpa(24) | pola=kulit(65) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:formal]
- `6011527357` purple — jenis=crop(31) | tema=punk(43)/y2k(22) | subjek=bulan(10)/bintang(9) | pola=kilau(98) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:gothic]

### bawah
- `6554515689` Snow pants☃️❄️ — jenis=legging(77) | tema=musim_dingin(58)/biasa(8) | subjek=mahkota(12)/rantai(6) | pola=polos(49) | panjang=selutut fit=lebar | [gambar:biasa]
- `16766000908` ☆ grey high waist pleated skirt — jenis=rok_pendek(72) | tema=sekolah(34)/formal(17) | subjek=kelelawar(28)/salib(10) | pola=polos(25) | panjang=pendek fit=ketat | [gambar:sekolah]
- `6002275179` [REALE] Legitimate Business — jenis=bawahan_gaun(75) | tema=formal(92)/tradisional(3) | subjek=salib(20)/laba_laba(6) | pola=garis(90) | panjang=panjang fit=ketat | [gambar:formal]
- `9353911507` Cute Blue Checkered Goth Pleated Skirt — jenis=rok_pendek(71) | tema=gothic(21)/kawaii(18) | subjek=musik(35)/bendera(8) | pola=kotak(64) | panjang=pendek fit=lebar | [gambar:punk]
- `5500894433` Mariachi Sombrero (-) — jenis=zirah_bawah(86) | tema=kerajaan(92)/formal(4) | subjek=mahkota(21)/tengkorak(17) | pola=kilau(52) | panjang=panjang fit=ketat | [gambar:bajak_laut]
- `6566410954` Grey gothic high waisted pants — jenis=jeans(93) | tema=gothic(84)/punk(13) | subjek=tengkorak(7)/logo(6) | pola=denim(90) | panjang=panjang fit=lebar | [gambar:formal]
- `12788765480` Long Flowy Skirt - Blue — jenis=rok_panjang(54) | tema=gaun_elegan(65)/penyihir(11) | subjek=petir(21)/bendera(18) | pola=pelangi(32) | panjang=selutut fit=lebar | [gambar:gaun_elegan]
- `5323898396` Hod [-] — jenis=celana_kain(100) | tema=formal(100)/kerajaan(0) | subjek=labu(9)/salib(7) | pola=polos(68) | panjang=panjang fit=ketat | [gambar:formal]
- `4787878139` Lulu Lemon Yoga pants & Air Force 1s — jenis=legging(65) | tema=biasa(54)/musim_dingin(11) | subjek=salib(5)/kelelawar(5) | pola=polos(59) | panjang=panjang fit=lebar | [gambar:formal]
- `6106663574` pink skirt  — jenis=rok_pendek(95) | tema=kawaii(92)/coquette(6) | subjek=pita(9)/buah(9) | pola=garis(56) | panjang=selutut fit=lebar | [gambar:kawaii]
- `89872257725735` Skirt Black Chic Layered Ruffle Mini Short Y2K — jenis=rok_pendek(40) | tema=y2k(35)/gaun_elegan(19) | subjek=bunga(28)/pita(15) | pola=polos(27) | panjang=selutut fit=lebar | [gambar:gaun_elegan]
- `15815643357` Ankle Snow Boots — jenis=zirah_bawah(29) | tema=musim_dingin(40)/medis(15) | subjek=mahkota(21)/makanan(8) | pola=garis(30) | panjang=pendek fit=lebar | [gambar:medis]
- `86660277439344`  1.0 Blocky Belted Jeans and Shoes — jenis=jeans(44) | tema=koboi(16)/kerajaan(12) | subjek=mahkota(41)/bulan(8) | pola=denim(53) | panjang=pendek fit=lebar | [gambar:koboi]
- `15253448762` Phoenix UFO Aura — jenis=bawahan_gaun(42) | tema=penyihir(25)/superhero(18) | subjek=bintang(38)/bulan(12) | pola=pelangi(62) | panjang=selutut fit=ketat | [gambar:penyihir]
- `4822560548` Bluey (Pants) — jenis=overall(81) | tema=kostum_hewan(45)/kawaii(23) | subjek=hantu(12)/hiu(10) | pola=denim(92) | panjang=pendek fit=lebar | [gambar:kawaii]
- `5168804217` pants fuego arcoiris cool 😎😎😎👍 — jenis=rok_pendek(42) | tema=streetwear(32)/antariksa(27) | subjek=api(15)/petir(9) | pola=pelangi(100) | panjang=pendek fit=lebar | [gambar:y2k]
- `7124183470` [𝓚] Donald - — jenis=celana_kain(63) | tema=polisi(80)/anime(5) | subjek=bulan(5)/bintang(5) | pola=denim(81) | panjang=pendek fit=lebar | [gambar:biasa]
- `76315271208132` Vintage Baggy Skater Pants (Grey) — jenis=jeans(49) | tema=punk(17)/y2k(15) | subjek=tanpa(21)/salib(11) | pola=denim(66) | panjang=selutut fit=lebar | [gambar:punk]
- `96622013932427` 2000s mini dress with flowy sleeves black — jenis=bawahan_gaun(57) | tema=y2k(35)/formal(34) | subjek=salib(13)/tanpa(9) | pola=polos(37) | panjang=selutut fit=ketat | [gambar:formal]
- `1047501012` Jeans — jenis=jeans(99) | tema=koboi(58)/biasa(13) | subjek=tanpa(5)/buah(4) | pola=denim(100) | panjang=pendek fit=lebar | [gambar:biasa]
- `83884066853774` Baggy Jeans w/ Crosses Blocky 1.0 — jenis=jeans(39) | tema=gothic(36)/militer(16) | subjek=salib(69)/rantai(5) | pola=denim(46) | panjang=pendek fit=lebar | [gambar:gothic]
- `17731146547` Silk Zebra Dress — jenis=bawahan_gaun(54) | tema=gothic(19)/kostum_hewan(10) | subjek=rantai(29)/ular(21) | pola=motif_hewan(67) | panjang=pendek fit=ketat | [gambar:gothic]
- `6575860593` POOP STAINS (green) — jenis=jogger(95) | tema=cyber(16)/y2k(16) | subjek=petir(6)/mahkota(6) | pola=denim(88) | panjang=panjang fit=lebar | [gambar:formal]
- `6522289448` King Fallen Pant - TDS — jenis=celana_kain(53) | tema=kerajaan(41)/formal(33) | subjek=salib(5)/bebek(4) | pola=polos(68) | panjang=panjang fit=lebar | [gambar:formal]
- `4527755510` Dark Cult Robe — jenis=celana_kain(39) | tema=formal(35)/militer(10) | subjek=salib(4)/kelelawar(4) | pola=kulit(34) | panjang=panjang fit=lebar | [gambar:vampir]

### kepala
- `6133255800` Snow Fuzzy Headband — jenis=pita_bando(43) | tema=musim_dingin(39)/medis(13) | subjek=hantu(19)/makanan(15) | [gambar:medis]
- `12227529573` emo — jenis=pita_bando(65) | tema=punk(36)/maid(18) | subjek=pita(89)/kupu_kupu(4) | [gambar:maid]
- `3875347091` Lovely White Bow — jenis=pita_bando(97) | tema=coquette(57)/maid(16) | subjek=pita(98)/kupu_kupu(1) | [gambar:coquette]
- `12292228590` Dotted Pink Headphones — jenis=headphone(98) | tema=kawaii(60)/coquette(33) | subjek=buah(16)/bunga(12) | [gambar:kawaii]
- `12740758463` Black Faceless — jenis=topi_formal(46) | tema=polisi(21)/formal(20) | subjek=tanpa(35)/salib(10) | [gambar:polisi]
- `7608762387` Black Striped Halloween Trendy Hat — jenis=topi_lain(40) | tema=halloween(41)/sporty(34) | subjek=bendera(50)/labu(7) | [gambar:sporty]
- `7133655402` White Cross Hairpins — jenis=topi_formal(35) | tema=maid(10)/sekolah(9) | subjek=salib(42)/tanpa(10) | [gambar:maid]
- `7168335822` Plush Panda Beanie — jenis=kupluk(39) | tema=bajak_laut(29)/kostum_hewan(18) | subjek=tengkorak(46)/kartun(8) | [gambar:bajak_laut]
- `8129419516` Cute Hair Sidebows (Black)  — jenis=pita_bando(78) | tema=kawaii(35)/formal(21) | subjek=pita(81)/laba_laba(3) | [gambar:formal]
- `116778296` Wide-brimmed Straw Cap — jenis=topi_baseball(36) | tema=pantai(41)/koboi(26) | subjek=tanpa(20)/ular(15) | [gambar:pantai]
- `12734699091` fedora — jenis=topi_formal(97) | tema=formal(76)/gothic(4) | subjek=tanpa(26)/salib(16) | [gambar:formal]
- `5102415222` Luxury Stylish Hat — jenis=topi_formal(47) | tema=gothic(53)/formal(14) | subjek=bintang(11)/bulan(10) | [gambar:gothic]
- `49763737` Rockstar Disguise — jenis=topi_formal(44) | tema=formal(39)/gothic(7) | subjek=salib(9)/bunga(9) | [gambar:formal]
- `5505899608` Pink Pointy Fluffy Ears — jenis=telinga(45) | tema=coquette(45)/musim_dingin(35) | subjek=naga(14)/kelelawar(13) | [gambar:coquette]
- `10715216622` Faceless Skin Color Head — jenis=topeng_kepala(38) | tema=militer(39)/biasa(8) | subjek=tanpa(20)/mahkota(16) | [gambar:militer]
- `4584029953` International Fedora - Poland — jenis=topi_formal(74) | tema=natal(24)/iblis(12) | subjek=bendera(26)/bunga(8) | [gambar:natal]
- `12604641002` Horns — jenis=tanduk(45) | tema=kostum_hewan(10)/tradisional(9) | subjek=bulan(19)/logo(13) | [gambar:kostum_hewan]
- `10592950837` White Practical Headphones — jenis=headphone(98) | tema=malaikat(28)/antariksa(17) | subjek=rantai(27)/musik(16) | [gambar:malaikat]
- `74939231` Emerald Crystal Circlet — jenis=mahkota(34) | tema=y2k(49)/penyihir(16) | subjek=katak(16)/naga(13) | [gambar:y2k]
- `311450131` Sparkle Time Classic Pumpkin — jenis=anting(25) | tema=halloween(99)/penyihir(0) | subjek=labu(99)/hantu(0) | [gambar:halloween]
- `5644892394` Chill Hoodie — jenis=headphone(34) | tema=gothic(26)/polisi(9) | subjek=tanpa(17)/musik(12) | [gambar:gothic]
- `8845164263` Black Bonnet — jenis=topi_formal(24) | tema=polisi(30)/gothic(16) | subjek=tanpa(30)/mata(12) | [gambar:polisi]
- `6409887220` Cute Lil' White Unicorn Hood 🦄 — jenis=telinga(50) | tema=kawaii(87)/coquette(7) | subjek=kelinci(67)/kucing(9) | [gambar:kawaii]
- `47702745` Sk10r Boi — jenis=topi_baseball(30) | tema=y2k(28)/streetwear(11) | subjek=kelelawar(10)/tanpa(8) | [gambar:y2k]
- `11631083376` Gobble Gobble Googly Eyes — jenis=telinga(60) | tema=kostum_hewan(60)/novelty(6) | subjek=mata(47)/anjing(14) | [gambar:kostum_hewan]

### rambut
- `5945433814` Blonde Ethereal Hairstyle — tema=gaun_elegan(26)/malaikat(8) | [gambar:gaun_elegan]
- `14313837666` Cute Curly Low Pigtails Green — tema=kawaii(87)/peri(2) | [gambar:kawaii]
- `13541329614` Long Lush Wavy Fairy Hair (Ginger) — tema=peri(38)/gaun_elegan(7) | [gambar:gaun_elegan]
- `430062818` Stylish Purple Hair — tema=halloween(17)/iblis(10) | [gambar:halloween]
- `158066100` Master Fighter — tema=iblis(38)/vampir(20) | [gambar:iblis]
- `11440502335` Black Anime Hair Orange Tie Band Long Bangs Bun  — tema=anime(36)/formal(25) | [gambar:formal]
- `13841658114` Long Length Messy Hair(White) — tema=malaikat(43)/antariksa(8) | [gambar:malaikat]
- `9244033194` Surfer - Brown — tema=koboi(43)/militer(7) | [gambar:koboi]
- `12615477430` Y2K Curly Clipped Grunge Messy Ponytail in Blonde — tema=kawaii(35)/y2k(18) | [gambar:kawaii]
- `6323945641` Brown Side-Swept Fringe Hair — tema=steampunk(15)/ksatria(15) | [gambar:steampunk]
- `12799138756` Short Y2K Shaggy Layered Hair Black — tema=y2k(36)/formal(17) | [gambar:formal]
- `12967525008` Siren TwinTails in Fairy Green — tema=peri(50)/horor(10) | [gambar:peri]
- `13953214922` Layered Jellyfish Messy Hair (Cotton Candy) — tema=kawaii(78)/malaikat(8) | [gambar:kawaii]
- `15155195162` Xiao Pigtails  — tema=pantai(19)/koboi(13) | [gambar:pantai]
- `11215846877` Fluffy Edgar Taper Fade — tema=musim_dingin(35)/gothic(11) | [gambar:gothic]
- `11387308898` Y2K Swirly Pigtail Hair (Pink) — tema=kawaii(51)/y2k(35) | [gambar:kawaii]
- `7145043296` Pink Fluffy Mullet — tema=kawaii(59)/musim_dingin(35) | [gambar:kawaii]
- `14221698106` Aesthetic Low Ponytail ( Brown ) — tema=tradisional(11)/medis(9) | [gambar:tradisional]
- `15412855918` 2 Strand Twists — tema=steampunk(37)/halloween(16) | [gambar:steampunk]
- `13552700208` Black to Red Dreads — tema=iblis(25)/badut(20) | [gambar:iblis]
- `13032211771` Rockstar Wolfcut (Blonde) — tema=kawaii(33)/coquette(8) | [gambar:kawaii]
- `553722174` Crimson Shaggy 2.0 — tema=iblis(25)/natal(12) | [gambar:iblis]
- `14497441240` Black Anime Hair — tema=anime(35)/gothic(9) | [gambar:gothic]
- `12755917283` Stylish Hair 2.0 — tema=gothic(20)/punk(12) | [gambar:gothic]
- `15351795963` Long Wavy Brown & Blonde Hair — tema=gaun_elegan(19)/coquette(12) | [gambar:gaun_elegan]

### sepatu
- `77118745512423` Black Platform Boots — tema=gothic(58)/punk(9) | [gambar:gothic]
- `82319896933578` Hunter Rain Boots Brown Rubber High Military Y2K — tema=musim_dingin(27)/militer(21) | [gambar:musim_dingin]
- `93285837720978` pink doll platform shoes — tema=kawaii(81)/coquette(17) | [gambar:kawaii]
- `91024739893003` Brown Y2K Chunky Sneakers — tema=militer(53)/y2k(35) | [gambar:militer]
- `86159445138757` Shoes W/Leg Warmers White — tema=maid(30)/penyihir(12) | [gambar:maid]
- `76889312779623` UNC Carolina Blue Highs [B… - Right Shoe Accessory — tema=antariksa(17)/bajak_laut(13) | [gambar:antariksa]
- `83611891612545` Blue Y2K Knee High Gyaru Fluffy Faux Fur Boots — tema=kostum_hewan(25)/y2k(21) | [gambar:kostum_hewan]
- `85889902730289` Balen Speed Trainer White Shoes — tema=sporty(14)/streetwear(12) | [gambar:sporty]
- `79292163393601` Mary Janes — tema=formal(21)/medis(11) | [gambar:formal]
- `85221623991826` sneaker shoes pink — tema=kawaii(93)/coquette(4) | [gambar:kawaii]
- `74470761238781` kitty cat gray cute sleepy slippers / shoes ♡ — tema=kawaii(35)/militer(30) | [gambar:militer]
- `72543948108868` Canvas Knee High Sneakers (Black) — tema=polisi(49)/bajak_laut(26) | [gambar:polisi]
- `81385371972955` Bl - Left Shoe Accessory — tema=sporty(40)/streetwear(16) | [gambar:sporty]
- `78598805235746` Fluffy Winter Boots Beige — tema=musim_dingin(38)/natal(11) | [gambar:natal]
- `89897239903811` Y2K Cute Pink Leg Warmers w/ Shoes — tema=kawaii(34)/y2k(18) | [gambar:kawaii]
- `83468433488916` red star doll mary janes — tema=natal(23)/iblis(22) | [gambar:natal]
- `89434864807214` Black Patent Leather Shoes — tema=formal(59)/gothic(15) | [gambar:formal]
- `97211121873211` Lavender Blue Suede Clogs — tema=kawaii(17)/pantai(14) | [gambar:kawaii]
- `92974579787803` Leopard boots [black] — tema=gothic(42)/halloween(14) | [gambar:gothic]
- `73417876905201` Cute Pink Bow Slides Sandals - Left Shoe Accessory — tema=coquette(66)/kawaii(26) | [gambar:coquette]
- `87295732037161` Cute Cloud Slippers Green[MAX] — tema=kawaii(81)/coquette(6) | [gambar:kawaii]
- `82809329538705` black slides - Right Shoe Accessory — tema=formal(44)/gothic(9) | [gambar:formal]
- `85339403260424` 3.0 Red Shoes - Right Shoe Accessory — tema=ninja(27)/iblis(13) | [gambar:ninja]
- `94718317918187` Cyber Boots Black Emo Midnight Leg Warmers Y2K — tema=gothic(38)/punk(19) | [gambar:gothic]
- `87319719022012` 67 Yellow Shoes — tema=badut(32)/halloween(19) | [gambar:badut]

### wajah
- `5728744669` Void Mask — jenis=masker(41) | tema=polisi(20)/maid(15) | subjek=tanpa(25)/logo(11) | [gambar:polisi]
- `6782786966` White Medical Eyepatch — jenis=penutup_mata(45) | tema=maid(16)/medis(15) | subjek=petir(52)/hantu(7) | [gambar:maid]
- `13542400994` Silly Happy Face Yelo (3D) — jenis=masker(38) | tema=badut(20)/novelty(12) | subjek=mahkota(18)/logo(17) | [gambar:badut]
- `4875723549` Gold Aviator Sunglasses — jenis=kacamata_hitam(94) | tema=steampunk(51)/militer(7) | subjek=tanpa(10)/mahkota(9) | [gambar:steampunk]
- `6376603866` Dark Polar Cub Mask — jenis=masker(49) | tema=gothic(32)/kostum_hewan(26) | subjek=beruang(32)/kucing(24) | [gambar:gothic]
- `13554150465` ✅ Red shades — jenis=kacamata_hitam(87) | tema=pantai(14)/iblis(13) | subjek=buah(35)/mata(24) | [gambar:pantai]
- `15762371942` ♡ cwute pink hairclip  — jenis=tindik(24) | tema=coquette(56)/kawaii(35) | subjek=pita(30)/logo(16) | [gambar:coquette]
- `14182306688` Troll Face — jenis=riasan(50) | tema=novelty(38)/badut(36) | subjek=kartun(13)/rantai(11) | [gambar:badut]
- `15762883036` Meme Sunglasses — jenis=kacamata_hitam(88) | tema=novelty(35)/cyber(8) | subjek=logo(9)/tanpa(9) | [gambar:cyber]
- `12369162675` Heart Valentines Day Piercing Set — jenis=tindik(69) | tema=steampunk(36)/ksatria(5) | subjek=hati(36)/rantai(30) | [gambar:steampunk]
- `16166773087` ♡ pink kawaii pastel half anime ribbon glasses — jenis=kacamata(81) | tema=coquette(61)/kawaii(25) | subjek=pita(57)/wajah_anime(18) | [gambar:coquette]
- `15485977797` Low Ruffle Lace Eyepatch Blue — jenis=penutup_mata(41) | tema=steampunk(24)/ksatria(15) | subjek=pita(30)/petir(12) | [gambar:steampunk]
- `14018980938` Naruto Baryon Face — jenis=riasan(67) | tema=anime(35)/ninja(17) | subjek=kucing(46)/petir(10) | [gambar:ninja]
- `11134072195` Scruffy Beard In White — jenis=kumis_jenggot(56) | tema=malaikat(58)/peri(18) | subjek=kelelawar(46)/petir(10) | [gambar:malaikat]
- `15069348322` Maki — jenis=riasan(75) | tema=musim_dingin(26)/peri(5) | subjek=mata(16)/wajah_anime(12) | [gambar:musim_dingin]
- `4735388946` Bunny Fashion Mask — jenis=masker(42) | tema=kawaii(88)/coquette(6) | subjek=kelinci(36)/hati(35) | [gambar:kawaii]
- `12741140426` Stylized Light Goatee Beard — jenis=kumis_jenggot(56) | tema=badut(14)/ninja(13) | subjek=musik(78)/logo(8) | [gambar:badut]
- `14256035493` ❤️ Cheeks Blank Face (Nougat) — jenis=masker(32) | tema=militer(34)/koboi(7) | subjek=tanpa(19)/mahkota(16) | [gambar:militer]
- `12266877860` Hollow Panther Mask — jenis=masker(91) | tema=ksatria(43)/maid(13) | subjek=hiu(67)/naga(12) | [gambar:ksatria]
- `6659960984` Cheek Piercing Woman — jenis=tindik(47) | tema=steampunk(36)/maid(5) | subjek=rantai(8)/bulan(6) | [gambar:steampunk]
- `14918812977` ୨୧ pink bow ribbon hairclip — jenis=riasan(31) | tema=coquette(80)/kawaii(15) | subjek=pita(92)/bunga(1) | [gambar:coquette]
- `15717236397` GOLD CROSS EARRINGS — jenis=tindik(95) | tema=gothic(49)/malaikat(15) | subjek=salib(92)/rantai(7) | [gambar:gothic]
- `11152088240` Y2K Heart Glasses on Head - Red — jenis=kacamata(54) | tema=y2k(35)/vampir(28) | subjek=hati(85)/buah(5) | [gambar:vampir]
- `10314940368` Pretty Black G Shades  — jenis=kacamata_hitam(87) | tema=polisi(17)/streetwear(13) | subjek=tanpa(33)/tulisan(9) | [gambar:polisi]
- `14065056400` Cold Blushy Cute Girl [2.0] — jenis=riasan(84) | tema=kawaii(48)/coquette(22) | subjek=mata(13)/bulan(7) | [gambar:coquette]

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 293, malaikat 194, gothic 179, coquette 152, formal 138, kostum_hewan 130, punk 107, steampunk 105, cyber 99, militer 99, peri 98, iblis 96
- atas: kawaii 919, formal 647, biasa 278, gothic 269, punk 259, sporty 229, steampunk 216, militer 213, cyber 204, y2k 175, coquette 165, halloween 162
- bawah: formal 655, kawaii 616, y2k 425, biasa 360, gothic 327, punk 282, sekolah 274, coquette 245, musim_dingin 234, militer 184, maid 179, halloween 161
- kepala: coquette 238, kawaii 216, kerajaan 176, formal 163, malaikat 148, militer 142, gothic 122, peri 113, kostum_hewan 110, iblis 100, penyihir 98, polisi 94
- rambut: kawaii 436, gothic 388, coquette 234, anime 182, steampunk 171, gaun_elegan 166, koboi 152, musim_dingin 142, punk 136, malaikat 119, iblis 90, y2k 83
- sepatu: kawaii 348, gothic 249, coquette 246, sporty 205, musim_dingin 191, y2k 157, kostum_hewan 146, pantai 130, militer 113, punk 110, gaun_elegan 97, formal 89
- wajah: kawaii 434, steampunk 236, gothic 179, militer 167, cyber 163, coquette 143, malaikat 92, anime 90, polisi 82, iblis 75, vampir 70, pantai 69
