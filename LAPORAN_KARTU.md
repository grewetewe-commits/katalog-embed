# Laporan Kartu Item (MATA v2) — versi 1792126476

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **132196**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 11498 | 0.5 | 76% | 86% | 74% | 74% |
| aksen/subjek | 7464 | 0.0 | 57% | 69% | 57% | 54% |
| aksen/tema | 7591 | 0.75 | 29% | 42% | 28% | 28% |
| atas/jenis | 11035 | 1.0 | 29% | 42% | 26% | 29% |
| atas/pola | 3089 | 0.75 | 53% | 65% | 49% | 52% |
| atas/subjek | 4087 | 0.5 | 31% | 41% | 30% | 31% |
| atas/tema | 7563 | 1.0 | 30% | 39% | 27% | 30% |
| bawah/jenis | 7084 | 1.0 | 36% | 50% | 32% | 36% |
| bawah/pola | 4344 | 1.0 | 46% | 59% | 42% | 46% |
| bawah/subjek | 2628 | 0.75 | 18% | 27% | 17% | 18% |
| bawah/tema | 5918 | 0.75 | 25% | 32% | 22% | 23% |
| kepala/jenis | 8527 | 0.75 | 52% | 69% | 48% | 51% |
| kepala/subjek | 5386 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 6957 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5178 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2316 | 0.5 | 22% | 32% | 21% | 20% |
| wajah/jenis | 3675 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1545 | 0.25 | 47% | 55% | 47% | 45% |
| wajah/tema | 2096 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=topi_lain(16) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween]
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi]
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(44) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut]
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(40)/mata(16) | [gambar:steampunk]
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(37) | tema=maid(51)/bajak_laut(5) | subjek=rantai(11)/hantu(8) | pola=polos(13) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:maid]
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=jas(25) | tema=formal(66)/polisi(5) | subjek=kelelawar(12)/salib(10) | pola=polos(42) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:formal]
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat]
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(50)/bulan(32) | [gambar:steampunk]
- `126582482792163` Pastel Goth (atas): jenis=kostum_penuh(30) | tema=kawaii(55)/gothic(18) | subjek=pita(34)/hantu(18) | pola=polkadot(73) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(51) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal]
- `382538059` Green Jersey (atas): jenis=jersey(83) | tema=sporty(86)/militer(3) | subjek=uang(18)/katak(17) | pola=loreng(29) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty]
- `7192553841` Zip Hoodie - Black (atas): jenis=hoodie(45) | tema=gothic(69)/gaun_elegan(7) | subjek=salib(20)/kelelawar(11) | pola=kulit(60) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic]
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette]
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=jeans(26) | tema=punk(20)/y2k(19) | subjek=rantai(7)/tanpa(6) | pola=kulit(36) | panjang=pendek fit=lebar | [gambar:gothic]
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=korset(40) | tema=gothic(74)/punk(9) | subjek=tengkorak(48)/rantai(13) | pola=kulit(37) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(80) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber]
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii]
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan]
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(23)/tulisan(9) | [gambar:streetwear]
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii]
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(39) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween]
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=crop(44) | tema=halloween(44)/kawaii(27) | subjek=labu(37)/beruang(20) | pola=bulu(60) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:kawaii]
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=kargo(18) | tema=halloween(50)/kawaii(10) | subjek=labu(54)/beruang(18) | pola=catur(32) | panjang=pendek fit=lebar | [gambar:halloween]

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1064059` space c.bmp — nama: antariksa | jenis=zirah(44) | tema=cyber(52)/antariksa(38) | subjek=ular(10)/wajah_anime(9) | pola=loreng(28) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:cyber]
- `1591061` Cute Wolf — nama: kawaii | jenis=hoodie(27) | tema=kostum_hewan(56)/kawaii(37) | subjek=anjing(67)/tulisan(3) | pola=bulu(89) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kostum_hewan]
- `138971959` Gusmanak's Suit Top (Gold) — nama: formal | jenis=zirah(57) | tema=steampunk(59)/formal(35) | subjek=katak(28)/ular(10) | pola=loreng(55) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:steampunk]
- `190809853` Gift Wrapped - Teal Ribbon — nama: coquette | jenis=jubah(68) | tema=peri(50)/coquette(37) | subjek=pita(50)/bunga(42) | pola=bunga(64) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:peri]
- `437419872` Green Suit — nama: formal | jenis=zirah(62) | tema=militer(53)/formal(35) | subjek=uang(19)/katak(11) | pola=loreng(86) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:militer]
- `1160341862` anime — nama: anime | jenis=kostum_penuh(40) | tema=kawaii(62)/anime(36) | subjek=wajah_anime(86)/kelinci(2) | pola=pelangi(37) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii]
- `1298799077` Orange Tuxedo — nama: formal | jenis=jas(85) | tema=formal(50)/halloween(32) | subjek=labu(78)/api(3) | pola=catur(28) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:halloween]
- `2673618259` DEVIL — nama: iblis | jenis=zirah(77) | tema=iblis(50)/vampir(17) | subjek=kelelawar(9)/bendera(8) | pola=kulit(25) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:vampir]
- `3376990530` purple space — nama: antariksa | jenis=jubah(35) | tema=antariksa(51)/kawaii(30) | subjek=bulan(31)/hantu(9) | pola=garis(68) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:kawaii]
- `4776407187` Cat Suit [+] — nama: formal | jenis=jas(36) | tema=kawaii(56)/formal(35) | subjek=kucing(36)/hantu(10) | pola=polos(34) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `4937511721` Green Formal robes [+] — nama: formal | jenis=zirah(49) | tema=militer(50)/formal(35) | subjek=katak(13)/ular(9) | pola=loreng(54) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:militer]
- `4975679890` Green Kimono (+) — nama: tradisional | jenis=zirah(54) | tema=militer(54)/tradisional(35) | subjek=katak(19)/ular(14) | pola=loreng(90) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:militer]
- `5448562629` galaxy — nama: antariksa | jenis=jubah(26) | tema=kawaii(55)/antariksa(35) | subjek=hantu(22)/pita(14) | pola=renda(24) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `5509859720` goth — nama: gothic | jenis=korset(16) | tema=gothic(53)/punk(31) | subjek=rantai(97)/laba_laba(2) | pola=renda(23) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:punk]
- `5532806467` y2k Black Aesthetic — nama: y2k | jenis=zirah(68) | tema=formal(53)/y2k(35) | subjek=kelelawar(9)/uang(7) | pola=polos(50) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `5608626226` Angel D Top | Hazbin Hotel ❣️ — nama: malaikat | jenis=korset(24) | tema=coquette(53)/malaikat(35) | subjek=pita(47)/hati(24) | pola=garis(61) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `5831429758` ━☆Red GAP Devil Hoodie☆━ — nama: iblis | jenis=zirah(52) | tema=iblis(52)/vampir(22) | subjek=hati(18)/tulisan(11) | pola=tulisan(43) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:vampir]
- `5900163546` Red Tuxedo w Gloves[T] — nama: formal | jenis=jas(54) | tema=formal(50)/vampir(21) | subjek=buah(15)/api(10) | pola=kulit(24) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:vampir]
- `6091258936` kawaii pink tube top w straps — nama: kawaii | jenis=korset(36) | tema=kawaii(65)/coquette(31) | subjek=pita(44)/hati(6) | pola=renda(49) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `6107426591` pink christmas — nama: natal | jenis=sweater(40) | tema=kawaii(51)/natal(35) | subjek=makanan(21)/pita(17) | pola=bunga(47) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6113877369` Unicorn Suit [-] — nama: formal | jenis=jas(38) | tema=kawaii(56)/formal(35) | subjek=hantu(35)/petir(7) | pola=pelangi(99) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6233629794` school boy shirt — nama: sekolah | jenis=jas(60) | tema=formal(59)/sekolah(36) | subjek=salib(10)/kelelawar(7) | pola=polos(35) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `6347879531` preppy boho pink cowgirl hat matching top! — nama: koboi | jenis=crop(19) | tema=kawaii(55)/koboi(35) | subjek=pita(39)/hati(9) | pola=polos(21) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:kawaii]
- `6396210261` Simple Purple Crop Top & Underline — nama: biasa | jenis=crop(45) | tema=kawaii(61)/biasa(35) | subjek=pita(11)/hantu(10) | pola=tulisan(28) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6479702245` Biggest Cake Head Suit Top — nama: formal | jenis=jas(36) | tema=kawaii(63)/formal(35) | subjek=makanan(42)/buah(7) | pola=pelangi(24) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6516689943` Fishy Army Purple Easter Hoodie — nama: militer | jenis=hoodie(35) | tema=kawaii(59)/militer(35) | subjek=makanan(15)/pita(11) | pola=catur(26) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6535421412` cute adorable butterfly neck lace🦋 — nama: kawaii | jenis=kemeja(15) | tema=kawaii(50)/malaikat(25) | subjek=kupu_kupu(41)/rantai(18) | pola=renda(48) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:malaikat]
- `6539597184` Pink maid — nama: maid | jenis=korset(36) | tema=kawaii(50)/maid(36) | subjek=pita(17)/hati(14) | pola=renda(45) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6554202849` Crimson Suit w/ Black Vest [+] — nama: formal | jenis=jas(28) | tema=formal(51)/vampir(17) | subjek=buah(17)/hati(6) | pola=kotak(14) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:vampir]
- `1081300` Golden Crown — nama: kerajaan | jenis=halo(58) | tema=kerajaan(62)/steampunk(30) | subjek=mahkota(81)/rantai(9) | [gambar:steampunk]
- `1323384` The Ice Crown — nama: kerajaan | jenis=mahkota(75) | tema=kerajaan(58)/penyihir(30) | subjek=mahkota(56)/petir(22) | [gambar:penyihir]
- `10770304` Crown of Golden Laurels — nama: kerajaan | jenis=halo(62) | tema=kerajaan(52)/militer(22) | subjek=mahkota(46)/rantai(31) | [gambar:militer]
- `13149660` Crimson Wizard Hat of Dragonkind — nama: penyihir | jenis=tanduk(38) | tema=iblis(51)/penyihir(36) | subjek=naga(52)/api(16) | [gambar:iblis]
- `33337024` Viking Knight — nama: ksatria | jenis=tanduk(65) | tema=ksatria(50)/iblis(22) | subjek=tengkorak(37)/beruang(9) | [gambar:iblis]
- `37747682` Brighteyes' Halloween Leftovers — nama: halloween | jenis=topi_baseball(79) | tema=sporty(58)/halloween(38) | subjek=logo(34)/labu(15) | [gambar:sporty]
- `42847590` Ice King — nama: kerajaan | jenis=mahkota(91) | tema=kerajaan(54)/musim_dingin(34) | subjek=mahkota(49)/bulan(9) | [gambar:musim_dingin]
- `102619342` Punk Kid — nama: punk | jenis=topeng_kepala(35) | tema=steampunk(55)/punk(35) | subjek=anjing(17)/mahkota(14) | [gambar:steampunk]
- `128207806` Red Rising Sun Samurai — nama: ninja | jenis=tanduk(48) | tema=iblis(62)/ninja(35) | subjek=kelelawar(36)/api(21) | [gambar:iblis]
- `162067805` Adurite Crown of Speedy Feet — nama: kerajaan | jenis=halo(38) | tema=iblis(60)/kerajaan(35) | subjek=mahkota(35)/api(22) | [gambar:iblis]
- `493491411` Neon Pink Banded Top Hat — nama: cyber | jenis=topi_formal(81) | tema=formal(54)/cyber(35) | subjek=pita(21)/hati(9) | [gambar:formal]

## Contoh acak per kelompok

### aksen
- `11695372929` Pastel Blue Plaid Scarf — jenis=syal(99) | tema=kawaii(40)/musim_dingin(27) | subjek=pita(64)/bunga(5) | [gambar:musim_dingin]
- `5505987520` Fairy Wings of Darkness — jenis=sayap(93) | tema=peri(83)/malaikat(12) | subjek=kupu_kupu(87)/pita(5) | [gambar:peri]
- `7609219485` 3.0 Silver Cross Necklace — jenis=kalung(97) | tema=malaikat(87)/kawaii(2) | subjek=salib(91)/rantai(5) | [gambar:malaikat]
- `10154337402` Wings — jenis=sayap(98) | tema=malaikat(98)/peri(0) | subjek=pita(44)/salib(21) | [gambar:malaikat]
- `4211442628` Mimic Hoodie — jenis=alat_musik(58) | tema=vampir(25)/horor(20) | subjek=mata(50)/buah(5) | [gambar:vampir]
- `4684604534` Red Wooden Bead Necklace — jenis=kalung(81) | tema=steampunk(18)/natal(16) | subjek=buah(40)/rantai(16) | [gambar:steampunk]
- `12785592157` Dark Gray Trench Raider Armor — jenis=tas(29) | tema=ksatria(37)/polisi(29) | subjek=tanpa(19)/salib(16) | [gambar:polisi]
- `501941432` Jade Katana Swordpack — jenis=senjata(97) | tema=ninja(68)/penyihir(5) | subjek=salib(39)/pita(17) | [gambar:ninja]
- `12500861409` ✅ Bag — jenis=kalung(47) | tema=gaun_elegan(61)/formal(8) | subjek=rantai(87)/bulan(2) | [gambar:gaun_elegan]
- `10905429074` CHM Compass Necklace  — jenis=kalung(88) | tema=punk(49)/iblis(7) | subjek=rantai(70)/logo(10) | [gambar:punk]
- `7241634848` Star Pendant — jenis=kalung(92) | tema=penyihir(23)/y2k(13) | subjek=bintang(50)/bulan(13) | [gambar:penyihir]
- `7498753952` Black Jewel Cross Necklace 1.0 — jenis=kalung(97) | tema=gothic(90)/punk(6) | subjek=salib(96)/rantai(3) | [gambar:gothic]
- `12903860222` White Hero Cape — jenis=jubah_belakang(72) | tema=superhero(41)/ksatria(10) | subjek=logo(19)/hiu(12) | [gambar:ksatria]
- `12103270510` Emirates Mini A380 — jenis=sayap(45) | tema=malaikat(32)/antariksa(15) | subjek=logo(27)/bebek(22) | [gambar:malaikat]
- `4416812356` Davy Bazooka - Bazooka — jenis=senjata(32) | tema=antariksa(33)/cyber(18) | subjek=petir(32)/api(9) | [gambar:antariksa]
- `12460327531` cute paper bowtie — jenis=ekor(25) | tema=kawaii(35)/gothic(31) | subjek=kelelawar(64)/pita(5) | [gambar:gothic]
- `5510009981` Purple Flame Wings — jenis=sayap(94) | tema=gothic(44)/malaikat(23) | subjek=api(36)/kelelawar(22) | [gambar:gothic]
- `6203388165` Pink Mecha Arms (Over-Hanging) - LIGHT SERIES — jenis=senjata(27) | tema=coquette(47)/cyber(40) | subjek=hati(25)/pita(14) | [gambar:coquette]
- `382881521` Tix Bling — jenis=sabuk(42) | tema=y2k(25)/halloween(14) | subjek=rantai(23)/tulisan(23) | [gambar:y2k]
- `7901626380` (1.0) Walkboy Retro Music Player — jenis=alat_musik(23) | tema=polisi(38)/cyber(13) | subjek=petir(38)/musik(36) | [gambar:polisi]
- `8948027890` Blue Magical Staff of the Elements — jenis=ekor(35) | tema=badut(22)/kerajaan(9) | subjek=pita(16)/ular(16) | [gambar:badut]
- `6042477338` Savannah Cat Tail - Wonder Woman — jenis=ekor(94) | tema=kostum_hewan(50)/badut(29) | subjek=kucing(37)/ular(36) | [gambar:kostum_hewan]
- `8347408324` Eternal Light — jenis=lain(40) | tema=steampunk(58)/kerajaan(20) | subjek=mahkota(50)/bintang(14) | [gambar:steampunk]
- `5270552011` Colonial Lantern — jenis=sabuk(24) | tema=militer(12)/penyihir(11) | subjek=salib(17)/petir(13) | [gambar:militer]
- `6829556357` Poster Girl Record - Zara Larsson — jenis=ekor(32) | tema=y2k(30)/vampir(11) | subjek=mata(11)/hantu(11) | [gambar:y2k]

### atas
- `1053191480` Studs — jenis=sweater(19) | tema=malaikat(16)/kawaii(15) | subjek=hantu(12)/wajah_anime(8) | pola=pelangi(14) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:malaikat]
- `6468030826` polo  — jenis=kemeja(39) | tema=vampir(21)/iblis(17) | subjek=salib(13)/kelelawar(10) | pola=polos(46) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:vampir]
- `5120683049` Brandy Melville car tank — jenis=tanktop(59) | tema=maid(16)/kawaii(11) | subjek=hantu(12)/kucing(10) | pola=renda(30) | lengan=tanpa panjang=crop fit=longgar depan=terbuka | [gambar:maid]
- `5722279602` LGBTQ+ — jenis=sweater(14) | tema=badut(41)/y2k(6) | subjek=bendera(56)/pita(11) | pola=pelangi(99) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:badut]
- `5720327350` cute halloween tied top w/ black hair ext — jenis=zirah(22) | tema=halloween(35)/kawaii(18) | subjek=kelelawar(16)/tengkorak(12) | pola=motif_hewan(43) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:halloween]
- `444269814` Power (Purple) — jenis=jersey(20) | tema=kawaii(31)/cyber(27) | subjek=petir(100)/logo(0) | pola=pelangi(31) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:kawaii]
- `2047289669` Craig — jenis=zirah(45) | tema=polisi(17)/sekolah(15) | subjek=bintang(11)/kartun(7) | pola=denim(96) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:polisi]
- `5608626226` Angel D Top | Hazbin Hotel ❣️ — jenis=korset(24) | tema=coquette(53)/malaikat(35) | subjek=pita(47)/hati(24) | pola=garis(61) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `1567847` ######## #### ####### — jenis=hoodie(53) | tema=steampunk(16)/kawaii(14) | subjek=anjing(75)/tulisan(4) | pola=kotak(56) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:steampunk]
- `6462905711` -summer shirt- — jenis=kaos(38) | tema=kawaii(45)/pantai(35) | subjek=pita(20)/hati(17) | pola=polos(16) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `5529360063` [🍉] gender fluid flag top — jenis=crop(18) | tema=kawaii(77)/coquette(12) | subjek=bendera(40)/pita(15) | pola=pelangi(50) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:kawaii]
- `643396428` Jedi Shadow Robes +  — jenis=zirah(53) | tema=formal(23)/maid(13) | subjek=kelelawar(9)/tanpa(6) | pola=kulit(30) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `5393947263` Cute Sleeves — jenis=tanktop(20) | tema=kawaii(43)/malaikat(12) | subjek=hantu(14)/rantai(6) | pola=polos(28) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:malaikat]
- `1181856003` blue and black checkers checkers — jenis=kemeja(46) | tema=sekolah(12)/polisi(10) | subjek=logo(23)/ular(20) | pola=catur(96) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:sekolah]
- `6380030062` white chanel tennis shirt — jenis=kaos(37) | tema=malaikat(24)/bajak_laut(10) | subjek=hantu(13)/salib(11) | pola=polos(31) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:malaikat]
- `5877817244` Puff Coat CROP (Zipper) — jenis=zirah(26) | tema=gothic(26)/maid(9) | subjek=salib(12)/kelelawar(7) | pola=polos(36) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic]
- `1097254362` GoldenGlare OFFICIAL Shirt! — jenis=zirah(63) | tema=kerajaan(37)/ksatria(34) | subjek=mahkota(48)/naga(7) | pola=kilau(21) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kerajaan]
- `1705820` Double Trouble Comics — jenis=kostum_penuh(25) | tema=badut(66)/natal(9) | subjek=bebek(23)/kartun(15) | pola=pelangi(57) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:badut]
- `4901751550` SCP Guard Shirt — jenis=zirah(42) | tema=cyber(19)/polisi(12) | subjek=petir(13)/uang(13) | pola=garis(19) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:cyber]
- `4877360786` gun necklace — jenis=kemeja(25) | tema=kawaii(28)/malaikat(17) | subjek=logo(22)/hati(8) | pola=polos(22) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:kawaii]
- `1169443047` Trenchcoat — jenis=jas(97) | tema=formal(99)/polisi(0) | subjek=kelelawar(13)/uang(10) | pola=kulit(32) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `5528491245` Mentalist+ — jenis=jas(33) | tema=formal(76)/gothic(5) | subjek=kelelawar(19)/uang(6) | pola=polos(39) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:formal]
- `6103043935` strwberi cake ଘ(੭ˊᵕˋ)੭* ੈ✩‧˚ — jenis=tanktop(21) | tema=kawaii(38)/horor(7) | subjek=makanan(38)/hantu(11) | pola=loreng(25) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `5124061955` Cat Suit 🐱 — jenis=zirah(53) | tema=formal(38)/kawaii(9) | subjek=kucing(36)/hantu(8) | pola=polos(39) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:kawaii]
- `3510892792` Roarkel® - Black Velvet Tuxedo Overcoat — jenis=jas(99) | tema=formal(99)/polisi(0) | subjek=uang(15)/kelelawar(7) | pola=kulit(74) | lengan=panjang panjang=panjang fit=longgar depan=tertutup | [gambar:formal]

### bawah
- `5330739256` black glitter dress — jenis=bawahan_gaun(52) | tema=gothic(63)/maid(7) | subjek=salib(15)/rantai(10) | pola=kilau(42) | panjang=selutut fit=lebar | [gambar:gothic]
- `6286198921` fall — jenis=kargo(18) | tema=koboi(37)/pantai(5) | subjek=beruang(13)/makanan(6) | pola=kotak(84) | panjang=selutut fit=lebar | [gambar:koboi]
- `4681519643` Chino pants — jenis=celana_kain(26) | tema=medis(12)/anime(7) | subjek=tanpa(8)/hantu(8) | pola=denim(35) | panjang=selutut fit=lebar | [gambar:medis]
- `5944247407` Pixels — jenis=bawahan_gaun(55) | tema=gothic(18)/ksatria(17) | subjek=bintang(14)/salib(11) | pola=kilau(53) | panjang=selutut fit=lebar | [gambar:gothic]
- `3623826967` [SALE!!]Ripped Denim Overalls & Sunflowers — jenis=overall(52) | tema=antariksa(21)/ksatria(14) | subjek=hantu(13)/labu(11) | pola=denim(76) | panjang=pendek fit=lebar | [gambar:antariksa]
- `5363002816` Jinbei [One Piece] - — jenis=zirah_bawah(37) | tema=ksatria(32)/bajak_laut(20) | subjek=labu(32)/api(10) | pola=kotak(26) | panjang=pendek fit=lebar | [gambar:ksatria]
- `6058629077` christmas  — jenis=legging(23) | tema=natal(80)/peri(5) | subjek=bunga(27)/buah(11) | pola=bunga(32) | panjang=pendek fit=lebar | [gambar:natal]
- `3382062227` Ripped Jeans — jenis=jeans(83) | tema=medis(10)/polisi(6) | subjek=hantu(7)/hiu(7) | pola=denim(80) | panjang=selutut fit=lebar | [gambar:medis]
- `2280044492` Goth Dress — jenis=bawahan_gaun(36) | tema=gothic(36)/iblis(15) | subjek=api(13)/musik(8) | pola=catur(18) | panjang=panjang fit=lebar | [gambar:iblis]
- `4802314774` Frisk [ - ] — jenis=rok_panjang(14) | tema=kawaii(17)/badut(14) | subjek=naga(10)/bendera(7) | pola=pelangi(72) | panjang=pendek fit=ketat | [gambar:kawaii]
- `7058205880` brown skirt w shoes/socks [cottage core] — jenis=rok_pendek(40) | tema=biasa(9)/koboi(7) | subjek=makanan(5)/tanpa(5) | pola=garis(19) | panjang=selutut fit=lebar | [gambar:biasa]
- `6224433565` Pilot Uniform (Pants) — jenis=celana_kain(15) | tema=formal(15)/polisi(7) | subjek=tanpa(7)/salib(6) | pola=polos(34) | panjang=selutut fit=lebar | [gambar:formal]
- `6962898847` Black and Gold Knight Pants — jenis=zirah_bawah(60) | tema=ksatria(40)/kerajaan(18) | subjek=mahkota(25)/tengkorak(23) | pola=motif_hewan(40) | panjang=pendek fit=lebar | [gambar:kerajaan]
- `6188410840` Black boots — jenis=zirah_bawah(21) | tema=maid(12)/formal(11) | subjek=rantai(16)/musik(5) | pola=catur(15) | panjang=selutut fit=lebar | [gambar:maid]
- `2365704136` finalmaple2 — jenis=zirah_bawah(64) | tema=kerajaan(48)/ksatria(26) | subjek=mahkota(55)/naga(10) | pola=motif_hewan(22) | panjang=pendek fit=lebar | [gambar:kerajaan]
- `2973066216` Spider-Man (Future Foundation) — jenis=bawahan_gaun(51) | tema=maid(52)/gaun_elegan(13) | subjek=laba_laba(40)/pita(28) | pola=garis(38) | panjang=selutut fit=lebar | [gambar:maid]
- `5773815109` Halloween outfit — jenis=rok_panjang(50) | tema=halloween(73)/pantai(4) | subjek=labu(81)/api(2) | pola=motif_hewan(53) | panjang=selutut fit=lebar | [gambar:halloween]
- `6596380127` Blu Furred Dragon alt V2 [-] — jenis=bawahan_gaun(25) | tema=ksatria(35)/kerajaan(7) | subjek=naga(38)/hiu(16) | pola=denim(57) | panjang=selutut fit=lebar | [gambar:ksatria]
- `6608113853` Black Cargo — jenis=kargo(43) | tema=formal(14)/gothic(10) | subjek=salib(6)/kelelawar(5) | pola=polos(20) | panjang=selutut fit=lebar | [gambar:formal]
- `391933134` Black Slacks — jenis=celana_kain(45) | tema=formal(15)/polisi(8) | subjek=tanpa(7)/salib(6) | pola=polos(29) | panjang=selutut fit=lebar | [gambar:formal]
- `6878463533` preppy jean shorts w shoes  fairy, ext — jenis=jeans(71) | tema=peri(36)/kawaii(8) | subjek=hiu(9)/hantu(7) | pola=denim(94) | panjang=selutut fit=lebar | [gambar:kawaii]
- `6380504180` ♥- spider — jenis=jogger(16) | tema=formal(15)/polisi(13) | subjek=laba_laba(35)/hantu(5) | pola=tulisan(17) | panjang=pendek fit=lebar | [gambar:formal]
- `5373223341` Billie Eillish white outfit 🤍🖤 — jenis=bawahan_gaun(27) | tema=formal(16)/maid(7) | subjek=rantai(24)/musik(9) | pola=catur(16) | panjang=panjang fit=lebar | [gambar:formal]
- `5303694784` Missing texture — jenis=bawahan_gaun(57) | tema=y2k(12)/coquette(7) | subjek=naga(12)/hati(10) | pola=catur(62) | panjang=selutut fit=lebar | [gambar:y2k]
- `1879128806` Brite Bomber pants — jenis=jeans(37) | tema=kawaii(9)/cyber(6) | subjek=hantu(14)/uang(5) | pola=pelangi(34) | panjang=pendek fit=lebar | [gambar:kawaii]

### kepala
- `6187113962` Gold Hoop Earrings — jenis=halo(71) | tema=steampunk(97)/kerajaan(1) | subjek=rantai(41)/mahkota(15) | [gambar:steampunk]
- `12293991165` Earmuffs — jenis=telinga(49) | tema=gothic(16)/formal(6) | subjek=musik(23)/tanpa(9) | [gambar:gothic]
- `3963907137` The Escape Artist — jenis=halo(55) | tema=antariksa(66)/y2k(4) | subjek=mata(52)/katak(28) | [gambar:antariksa]
- `12310612074` Black Mixpat FAST Helmet — jenis=helm(72) | tema=sporty(69)/polisi(18) | subjek=kelelawar(15)/tanpa(12) | [gambar:sporty]
- `12789114477` Shadow Boy — jenis=topeng_kepala(36) | tema=gothic(34)/iblis(26) | subjek=kelelawar(24)/mata(13) | [gambar:gothic]
- `7668537321` Black Plaid Fedora — jenis=topi_formal(85) | tema=formal(49)/koboi(19) | subjek=tanpa(24)/salib(11) | [gambar:formal]
- `7168593722` Wicked and Vile — jenis=tanduk(52) | tema=gothic(61)/vampir(12) | subjek=kelelawar(41)/naga(19) | [gambar:gothic]
- `7212278970` Golden Headphones - KSI — jenis=telinga(48) | tema=steampunk(35)/militer(19) | subjek=musik(52)/rantai(10) | [gambar:steampunk]
- `8151404994` Hovering UFO — jenis=halo(99) | tema=cyber(67)/antariksa(9) | subjek=petir(31)/bintang(13) | [gambar:cyber]
- `116778296` Wide-brimmed Straw Cap — jenis=topi_baseball(36) | tema=pantai(41)/koboi(26) | subjek=tanpa(20)/ular(15) | [gambar:pantai]
- `12785419589` Kitsune Mask — jenis=topeng_kepala(53) | tema=iblis(35)/vampir(25) | subjek=kucing(42)/anjing(17) | [gambar:iblis]
- `5132802731` Pink Pom poms — jenis=pita_bando(36) | tema=kawaii(58)/coquette(34) | subjek=bunga(29)/makanan(20) | [gambar:kawaii]
- `49763737` Rockstar Disguise — jenis=topi_formal(45) | tema=formal(39)/gothic(7) | subjek=salib(9)/bunga(9) | [gambar:formal]
- `5511283469` Silver Stars and Moons Confetti — jenis=mahkota(19) | tema=antariksa(33)/peri(15) | subjek=bulan(51)/bintang(46) | [gambar:antariksa]
- `10816577500` Black Star Beanie Y2k Trending Emo Gangster — jenis=kupluk(41) | tema=punk(21)/y2k(20) | subjek=bintang(36)/beruang(22) | [gambar:halloween]
- `4584972547` Blue Crystallized Horns — jenis=tanduk(50) | tema=penyihir(25)/kerajaan(21) | subjek=kelelawar(26)/petir(25) | [gambar:penyihir]
- `12651685566` Classic Skybox Top Hat — jenis=topi_formal(39) | tema=kawaii(40)/malaikat(33) | subjek=bunga(16)/bulan(14) | [gambar:kawaii]
- `10717262789` Red Flannel Head — jenis=kupluk(39) | tema=natal(24)/tradisional(21) | subjek=hati(25)/bendera(11) | [gambar:natal]
- `74939231` Emerald Crystal Circlet — jenis=mahkota(41) | tema=y2k(49)/penyihir(16) | subjek=katak(16)/naga(13) | [gambar:y2k]
- `321570512` Chill Cap — jenis=topi_baseball(74) | tema=streetwear(21)/kawaii(18) | subjek=tulisan(29)/logo(25) | [gambar:streetwear]
- `5674051153` Photo Drone — jenis=halo(22) | tema=malaikat(12)/cyber(9) | subjek=kelelawar(24)/laba_laba(16) | [gambar:malaikat]
- `8918829397` Red Garden Horns — jenis=tanduk(40) | tema=iblis(39)/peri(19) | subjek=bunga(86)/pita(7) | [gambar:iblis]
- `6431950467` Miau Glitter Hair Clips Black — jenis=topi_formal(19) | tema=formal(19)/kerajaan(10) | subjek=ular(15)/musik(11) | [gambar:formal]
- `47702745` Sk10r Boi — jenis=topi_baseball(27) | tema=y2k(28)/streetwear(11) | subjek=kelelawar(10)/tanpa(8) | [gambar:y2k]
- `11705401570` Downfall Cowlick [Pink] — jenis=pita_bando(24) | tema=coquette(44)/tradisional(9) | subjek=petir(15)/hiu(8) | [gambar:coquette]

### rambut
- `5945436918` Light Brown Ethereal Hairstyle — tema=koboi(16)/pantai(7) | [gambar:koboi]
- `14335650219` Brown Vampire Boy Hair — tema=vampir(36)/kostum_hewan(7) | [gambar:kostum_hewan]
- `13564616891` Harajuku Pin Straight Dark Brown Hair  — tema=sekolah(22)/biasa(6) | [gambar:sekolah]
- `430063008` Strawberry Ice Cream Hair — tema=kawaii(79)/penyihir(5) | [gambar:kawaii]
- `168167496` Aqua Dream Hair — tema=kawaii(26)/cyber(19) | [gambar:kawaii]
- `11489004241` Blowout Waves in Red — tema=iblis(21)/vampir(14) | [gambar:iblis]
- `13863653796` Low Braided Pigtails(Blonde) — tema=kawaii(34)/coquette(20) | [gambar:kawaii]
- `9244082349` Sideswept Dreads - Red — tema=steampunk(26)/koboi(19) | [gambar:steampunk]
- `12652803319` Wavy Full Messy Boy Hair (Black) — tema=gothic(19)/halloween(10) | [gambar:gothic]
- `6343731057` Fashionable Headband Hair in Blonde — tema=coquette(51)/kawaii(21) | [gambar:coquette]
- `12826504773` Chic Style Hair(Ash) — tema=musim_dingin(10)/punk(9) | [gambar:musim_dingin]
- `13002817579` Stylish Messy Hair(Blue) — tema=gothic(12)/steampunk(8) | [gambar:gothic]
- `13966145054` Braids with Side Part in Blonde — tema=coquette(33)/kawaii(16) | [gambar:coquette]
- `15227706321` Straight Hair with Headphones(Black) — tema=gothic(31)/steampunk(4) | [gambar:gothic]
- `11281462227` Curly Low Pigtails in Brown — tema=coquette(34)/formal(8) | [gambar:coquette]
- `11436258613` Short Wavy White Hair — tema=antariksa(17)/malaikat(15) | [gambar:antariksa]
- `7154637981` Aesthetic brown ponytail — tema=coquette(15)/tradisional(11) | [gambar:coquette]
- `14231264895` Blonde Middle Parted Hair  — tema=koboi(14)/kawaii(10) | [gambar:koboi]
- `15450313731` Black Layered Kawaii Hair w/ Fluffy Kitty Beanie ♡ — tema=maid(44)/kawaii(19) | [gambar:maid]
- `13570499846` Messy Anime Fluffy Ponytail Black to Red — tema=iblis(27)/horor(27) | [gambar:iblis]
- `13050492929` Soft Waves Hair(Black) — tema=gothic(25)/punk(15) | [gambar:gothic]
- `553892446` Mint Ice Cream Hair — tema=kawaii(63)/penyihir(10) | [gambar:kawaii]
- `14529374375` Luscious Half Up Hair With Pink Bows Blonde — tema=coquette(78)/kawaii(18) | [gambar:coquette]
- `12799138756` Short Y2K Shaggy Layered Hair Black — tema=y2k(36)/formal(17) | [gambar:formal]
- `15418595153` Lewis Hair Brown — tema=koboi(19)/militer(7) | [gambar:koboi]

### sepatu
- `77159442679603` Sleek High Boots (It-Girl) — tema=malaikat(52)/ksatria(9) | [gambar:malaikat]
- `82383963451044` Gray Y2K Chunky Platform Boots 1.0 — tema=y2k(38)/musim_dingin(23) | [gambar:musim_dingin]
- `93332847283875` Rubber Boots in Yellow — tema=koboi(38)/halloween(13) | [gambar:koboi]
- `91135777947474` Doll Platform Shoes Pink - Right Shoe Accessory — tema=kawaii(91)/coquette(4) | [gambar:kawaii]
- `86257202393171` Black Slippers - Left Shoe Accessory — tema=pantai(31)/formal(12) | [gambar:pantai]
- `76951995906138` Halloween - Left Shoe Accessory — tema=halloween(87)/kostum_hewan(9) | [gambar:halloween]
- `83685623616547` Jey 4's Light Blue - Left Shoe Accessory — tema=sporty(62)/streetwear(6) | [gambar:sporty]
- `85968100576132` Chunky Lace-Up Platform Sne… - Left Shoe Accessory — tema=punk(23)/bajak_laut(21) | [gambar:punk]
- `79326695483103` Cute Pink & White Frilly Heart Bow Shoes — tema=kawaii(40)/coquette(33) | [gambar:kawaii]
- `85334270905474` Blue Alien Bunny Slippers - Right Shoe Accessory — tema=antariksa(37)/kostum_hewan(7) | [gambar:kostum_hewan]
- `74478766354807` Suede High Top Boots in Grey — tema=koboi(17)/musim_dingin(12) | [gambar:koboi]
- `72565393005399` Dark Red Canvas Shoes — tema=natal(26)/iblis(15) | [gambar:natal]
- `81445257247010` ✨ Blue Chunky Trainers w Bubble Sole Sporty — tema=sporty(41)/antariksa(27) | [gambar:antariksa]
- `78645048183020` Charm Clogs with Socks (Whi… - Left Shoe Accessory — tema=antariksa(33)/kawaii(27) | [gambar:antariksa]
- `90018373285533` Doll Platform Shoes - Left Shoe Accessory — tema=musim_dingin(24)/maid(23) | [gambar:musim_dingin]
- `83532570160614` Pink Ice Skates — tema=kawaii(65)/coquette(31) | [gambar:kawaii]
- `89489255228809` ✨ Princess Pink Heels 3.0 S… - Left Shoe Accessory — tema=coquette(53)/peri(23) | [gambar:coquette]
- `97317966069390` adidas F50 Anime Aura - Left Shoe Accessory — tema=anime(35)/sporty(28) | [gambar:sporty]
- `93213379445532` White Model Doll Heels - Right Shoe Accessory — tema=gaun_elegan(35)/malaikat(32) | [gambar:gaun_elegan]
- `73440928529704` Chicago Colorway Basketball High-Tops — tema=sporty(46)/streetwear(12) | [gambar:streetwear]
- `87352569992717` Black Fuzzy Slide Slippers - Right Shoe Accessory — tema=gothic(57)/punk(18) | [gambar:gothic]
- `82907354089354` Black High Top Sneakers w/… - Right Shoe Accessory — tema=punk(59)/musim_dingin(16) | [gambar:punk]
- `85400299367038` Blue Denim Sneakers — tema=sporty(29)/antariksa(22) | [gambar:sporty]
- `94851404988930` High Heels Boots White Leat… - Left Shoe Accessory — tema=malaikat(30)/coquette(22) | [gambar:malaikat]
- `87408951962879` Dr. Martens Mega Lace Boot… - Right Shoe Accessory — tema=punk(46)/musim_dingin(12) | [gambar:punk]

### wajah
- `5763987265` Angry Brows — jenis=kumis_jenggot(89) | tema=kostum_hewan(11)/superhero(9) | subjek=kelelawar(35)/logo(18) | [gambar:kostum_hewan]
- `6808010154` Ballistic Mask — jenis=masker(86) | tema=polisi(27)/gothic(18) | subjek=salib(17)/logo(15) | [gambar:polisi]
- `13555332687` Glasses — jenis=kacamata(45) | tema=cyber(21)/bajak_laut(9) | subjek=bebek(12)/mata(8) | [gambar:cyber]
- `4904137145` Emotimask : Relax — jenis=penutup_mata(24) | tema=malaikat(20)/maid(15) | subjek=bulan(20)/logo(9) | [gambar:malaikat]
- `6380189626` Cute Kitty Bandage Blue — jenis=riasan(40) | tema=kawaii(96)/coquette(1) | subjek=kucing(82)/kelinci(2) | [gambar:kawaii]
- `13582677692` gas mask — jenis=masker(60) | tema=cyber(32)/polisi(28) | subjek=tanpa(35)/tengkorak(8) | [gambar:cyber]
- `15850150581` Piercing — jenis=tindik(57) | tema=steampunk(17)/badut(10) | subjek=musik(19)/logo(16) | [gambar:steampunk]
- `14215984289` Neco Cat Face — jenis=masker(34) | tema=kawaii(53)/coquette(5) | subjek=kucing(36)/beruang(7) | [gambar:kawaii]
- `15850429545` Piercing — jenis=tindik(58) | tema=antariksa(8)/cyber(8) | subjek=logo(25)/rantai(14) | [gambar:antariksa]
- `12383395027` Faceless — jenis=riasan(53) | tema=militer(84)/ksatria(2) | subjek=tanpa(21)/mahkota(16) | [gambar:militer]
- `16301971909` Cute Rainbow Makeup — jenis=riasan(95) | tema=kawaii(77)/coquette(14) | subjek=makanan(9)/mata(9) | [gambar:kawaii]
- `15538782992` Snow Goggles — jenis=kacamata_hitam(88) | tema=musim_dingin(36)/cyber(33) | subjek=tanpa(18)/tulisan(11) | [gambar:cyber]
- `14053682976` Simply Tired Face — jenis=kacamata_hitam(79) | tema=militer(15)/streetwear(15) | subjek=tanpa(24)/kartun(7) | [gambar:militer]
- `11157490951` Brown Straight 3D Eyebrows — jenis=masker(23) | tema=antariksa(20)/iblis(10) | subjek=bulan(19)/mata(11) | [gambar:antariksa]
- `15105681014` Chibi Doll Cheek Piercing — jenis=tindik(43) | tema=steampunk(8)/maid(8) | subjek=pita(10)/rantai(6) | [gambar:steampunk]
- `4735714475` Bandana of Conflict — jenis=masker(37) | tema=vampir(40)/gothic(11) | subjek=kelelawar(57)/pita(8) | [gambar:vampir]
- `12780948340` [ Head ] Noob Yellow Tone Blank Faceless Mask — jenis=masker(47) | tema=novelty(36)/kerajaan(28) | subjek=mahkota(68)/logo(6) | [gambar:kerajaan]
- `14291032983` Kawaii Face Sticker — jenis=riasan(49) | tema=kawaii(35)/natal(18) | subjek=bendera(27)/logo(14) | [gambar:natal]
- `12299698092` Cute Star Face Sticker - White — jenis=riasan(46) | tema=kawaii(35)/bajak_laut(7) | subjek=bintang(82)/bendera(7) | [gambar:bajak_laut]
- `6684190641` Handsome Mask — jenis=masker(46) | tema=bajak_laut(14)/cyber(8) | subjek=tanpa(12)/hiu(8) | [gambar:bajak_laut]
- `14951226834` Spiral Pearl Earring (White) — jenis=riasan(54) | tema=maid(23)/ksatria(9) | subjek=rantai(41)/hati(10) | [gambar:maid]
- `15788572631` cool rainbow flaming tactical sunglasses — jenis=kacamata_hitam(92) | tema=militer(35)/cyber(25) | subjek=api(38)/petir(13) | [gambar:cyber]
- `11177732943` Cute Pink Hair Flower — jenis=riasan(87) | tema=peri(39)/kawaii(36) | subjek=bunga(88)/pita(6) | [gambar:peri]
- `10502435473` Square Aviator Shades - Black & Blue — jenis=kacamata_hitam(94) | tema=militer(15)/polisi(14) | subjek=tanpa(16)/rantai(6) | [gambar:militer]
- `14111604181` 😔 Sleepy Thinking Face (3D) 😔 — jenis=tindik(18) | tema=maid(18)/musim_dingin(7) | subjek=wajah_anime(17)/tanpa(4) | [gambar:maid]

## Sebaran tema (fusi) per kelompok

- aksen: kawaii 295, malaikat 201, gothic 177, coquette 152, formal 136, kostum_hewan 127, punk 108, steampunk 107, militer 101, cyber 99, peri 97, iblis 97
- atas: kawaii 575, formal 393, gothic 163, malaikat 157, steampunk 123, militer 115, halloween 104, cyber 80, natal 79, maid 79, sporty 78, polisi 73
- bawah: formal 670, kawaii 517, malaikat 143, vampir 137, maid 127, militer 119, gothic 115, halloween 104, kerajaan 67, y2k 66, ksatria 61, polisi 61
- kepala: coquette 240, kawaii 215, kerajaan 180, formal 162, malaikat 149, militer 142, gothic 122, peri 114, kostum_hewan 109, iblis 99, penyihir 97, polisi 94
- rambut: kawaii 434, gothic 388, coquette 231, steampunk 182, anime 181, gaun_elegan 165, koboi 151, musim_dingin 141, punk 136, malaikat 116, iblis 92, y2k 82
- sepatu: kawaii 351, gothic 247, coquette 245, sporty 202, musim_dingin 193, y2k 158, kostum_hewan 145, pantai 132, militer 113, punk 108, gaun_elegan 97, formal 89
- wajah: kawaii 437, steampunk 235, gothic 179, militer 166, cyber 160, coquette 143, malaikat 91, anime 88, polisi 84, iblis 75, vampir 71, pantai 69
