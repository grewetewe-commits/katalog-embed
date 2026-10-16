# Laporan Kartu Item (MATA v2) — versi 1792126773

Kartu dibaca dari GAMBAR item (CLIP zero-shot, model sama dengan otak.py); nama hanya bukti tambahan.

- Item berkartu: **132196**

## Kalibrasi & akurasi gambar saja vs nama

Label nama hanya dipakai bila nama menunjuk tepat satu label (bukan label netral). alfa = koreksi bias kalimat CLIP
yang dipilih otomatis (kecocokan top-1 tertinggi).

| kelompok/facet | n | alfa dipilih | top-1 | top-2 | top-1 alfa 0 | top-1 alfa 1 |
|---|---|---|---|---|---|---|
| aksen/jenis | 11564 | 0.25 | 75% | 85% | 74% | 73% |
| aksen/subjek | 7464 | 0.0 | 57% | 69% | 57% | 54% |
| aksen/tema | 7591 | 0.75 | 29% | 42% | 28% | 28% |
| atas2D/jenis | 5681 | 1.0 | 15% | 23% | 8% | 15% |
| atas2D/pola | 1046 | 0.75 | 50% | 62% | 47% | 50% |
| atas2D/subjek | 2103 | 0.5 | 32% | 43% | 31% | 32% |
| atas2D/tema | 4235 | 0.75 | 30% | 39% | 27% | 30% |
| atas3D/jenis | 5354 | 0.0 | 46% | 61% | 46% | 43% |
| atas3D/pola | 2043 | 0.5 | 55% | 66% | 51% | 53% |
| atas3D/subjek | 1984 | 0.25 | 30% | 40% | 30% | 29% |
| atas3D/tema | 3328 | 0.75 | 30% | 40% | 27% | 30% |
| bawah2D/jenis | 3934 | 1.0 | 23% | 34% | 20% | 23% |
| bawah2D/pola | 2364 | 1.0 | 43% | 56% | 35% | 43% |
| bawah2D/subjek | 1700 | 0.75 | 14% | 22% | 11% | 14% |
| bawah2D/tema | 3958 | 0.5 | 25% | 31% | 21% | 23% |
| bawah3D/jenis | 3150 | 0.75 | 52% | 72% | 51% | 52% |
| bawah3D/pola | 1980 | 1.0 | 50% | 63% | 45% | 50% |
| bawah3D/subjek | 928 | 0.25 | 27% | 36% | 27% | 24% |
| bawah3D/tema | 1960 | 0.25 | 20% | 30% | 20% | 19% |
| kepala/jenis | 9684 | 1.0 | 50% | 66% | 44% | 50% |
| kepala/subjek | 5386 | 0.5 | 49% | 58% | 48% | 48% |
| kepala/tema | 6957 | 0.5 | 34% | 45% | 33% | 34% |
| rambut/tema | 5178 | 1.0 | 17% | 26% | 9% | 17% |
| sepatu/tema | 2316 | 0.5 | 22% | 32% | 21% | 20% |
| wajah/jenis | 3675 | 1.0 | 69% | 85% | 60% | 69% |
| wajah/subjek | 1545 | 0.25 | 47% | 55% | 47% | 45% |
| wajah/tema | 2096 | 1.0 | 21% | 35% | 15% | 21% |

Catatan: angka ini batas bawah kasar — nama Roblox sering tidak menyebut apa yang terlihat, dan label nama sendiri bisa salah.

## Item uji

- `126884250250747` Duck-o-Lantern (kepala): jenis=kupluk(22) | tema=halloween(100)/vampir(0) | subjek=labu(65)/bebek(35) | [gambar:halloween]
- `72558563872966` Black Cowboy Hat (kepala): jenis=topi_koboi(81) | tema=koboi(100)/formal(0) | subjek=rantai(12)/tanpa(12) | [gambar:koboi]
- `1028859` Pirate Captain's Hat (kepala): jenis=topi_lain(41) | tema=bajak_laut(100)/halloween(0) | subjek=tengkorak(86)/hantu(3) | [gambar:bajak_laut]
- `14328141014` Gojo (wajah): jenis=kacamata_hitam(74) | tema=anime(37)/steampunk(9) | subjek=bulan(40)/mata(16) | [gambar:steampunk]
- `8565346973` 🤍 Maid Dress (atas): jenis=gaun(38) | tema=maid(41)/formal(6) | subjek=salib(6)/rantai(6) | pola=polos(14) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:maid]
- `6554200369` Grey Suit w/ Black Vest [+] (atas): jenis=jas(28) | tema=formal(61)/gothic(6) | subjek=kelelawar(10)/salib(8) | pola=polos(32) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:formal]
- `192557913` Sparkling Angel Wings (aksen): jenis=sayap(98) | tema=malaikat(88)/peri(10) | subjek=bulan(23)/kupu_kupu(21) | [gambar:malaikat]
- `78504769792948` Bloody Silver Dermal Piercing Under Eye Right (wajah): jenis=tindik(78) | tema=horor(45)/steampunk(26) | subjek=mata(50)/bulan(32) | [gambar:steampunk]
- `126582482792163` Pastel Goth (atas): jenis=kemeja(29) | tema=kawaii(34)/gothic(18) | subjek=pita(23)/hantu(9) | pola=polkadot(54) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `93519364113971` kawaii curious droopy cat ears in full black (kepala): jenis=telinga(46) | tema=kawaii(35)/formal(13) | subjek=kucing(36)/bulan(17) | [gambar:formal]
- `382538059` Green Jersey (atas): jenis=jersey(84) | tema=sporty(80)/militer(3) | subjek=katak(24)/bintang(9) | pola=loreng(22) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:sporty]
- `7192553841` Zip Hoodie - Black (atas): jenis=jaket(49) | tema=gothic(39)/formal(25) | subjek=salib(23)/kelelawar(12) | pola=kulit(59) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:gothic]
- `14027730224` ♡ kawaii baby pink pastel bow headband (kepala): jenis=pita_bando(93) | tema=coquette(79)/kawaii(19) | subjek=pita(79)/kelinci(4) | [gambar:coquette]
- `15901064855` black grunge dark y2k dh emo boy punk evade (bawah): jenis=kargo(27) | tema=punk(20)/y2k(20) | subjek=bulan(6)/rantai(6) | pola=kulit(30) | panjang=pendek fit=lebar | [gambar:gothic]
- `98089688160090` 🖤 Black leather jacket with spikes and skull  (atas): jenis=jaket(40) | tema=gothic(68)/punk(10) | subjek=tengkorak(44)/laba_laba(11) | pola=kulit(39) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `116973312880668` Arisu's Sword of Light: Supernova MK.II (aksen): jenis=senjata(74) | tema=cyber(64)/polisi(9) | subjek=petir(50)/hiu(6) | [gambar:cyber]
- `98757749181872` ♡ coquette curls with pink bow blonde (rambut): tema=coquette(62)/kawaii(37) | [gambar:kawaii]
- `5731050224` Gold Crown of O’s (kepala): jenis=mahkota(100) | tema=kerajaan(100)/gaun_elegan(0) | subjek=mahkota(100)/rantai(0) | [gambar:kerajaan]
- `301820310` Lin's Glasses (wajah): jenis=kacamata(96) | tema=streetwear(13)/medis(11) | subjek=tanpa(23)/tulisan(9) | [gambar:streetwear]
- `18832937926` ♡ kawaii pumpkin bear hood (kepala): jenis=tudung(37) | tema=kawaii(76)/halloween(18) | subjek=beruang(63)/labu(18) | [gambar:kawaii]
- `122234019472336` Spooky Halloween Pumpkin Cat Hat (kepala): jenis=topi_lain(38) | tema=halloween(99)/kostum_hewan(0) | subjek=labu(82)/kucing(18) | [gambar:halloween]
- `132200141502925` ★🧸🎃˚. ɞ Preppy Halloween pumpkin bear ˚. ᵎᵎ (atas): jenis=crop(30) | tema=halloween(47)/kawaii(10) | subjek=labu(45)/beruang(19) | pola=bulu(41) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:halloween]
- `83668736552435` ★🧸🎃˚. ɞ Halloween jellycat pumpkin bear pjs˚. ᵎᵎ (bawah): jenis=celana_pendek(17) | tema=halloween(48)/kawaii(7) | subjek=labu(48)/beruang(18) | pola=catur(21) | panjang=pendek fit=lebar | [gambar:halloween]

## Contoh: tema dari nama ≠ tema dari gambar (gambar yakin)

- `1591061` Cute Wolf — nama: kawaii | jenis=hoodie(44) | tema=kostum_hewan(58)/kawaii(36) | subjek=anjing(69)/wajah_anime(5) | pola=bulu(89) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:kostum_hewan]
- `1606929` the football shirt for eagles22 — nama: sporty | jenis=kaos(39) | tema=sporty(52)/y2k(20) | subjek=tulisan(37)/petir(13) | pola=garis(15) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:y2k]
- `138971959` Gusmanak's Suit Top (Gold) — nama: formal | jenis=jas(36) | tema=steampunk(52)/formal(35) | subjek=katak(37)/ular(7) | pola=loreng(46) | lengan=panjang panjang=crop fit=longgar depan=tertutup | [gambar:steampunk]
- `190809853` Gift Wrapped - Teal Ribbon — nama: coquette | jenis=jubah(36) | tema=peri(50)/coquette(38) | subjek=pita(47)/bunga(41) | pola=bunga(59) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:peri]
- `437419872` Green Suit — nama: formal | jenis=zirah(46) | tema=militer(53)/formal(35) | subjek=katak(15)/uang(10) | pola=loreng(84) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:militer]
- `1553196442` Emirates ~ Captain Blazer — nama: formal | jenis=jas(60) | tema=formal(58)/polisi(26) | subjek=mahkota(17)/bendera(8) | pola=loreng(29) | lengan=pendek panjang=normal fit=longgar depan=tertutup | [gambar:polisi]
- `2954251301` Cutie Shirt Sleeves — nama: kawaii | jenis=kaos(38) | tema=kawaii(63)/coquette(29) | subjek=pita(16)/buah(10) | pola=polos(14) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `4937511721` Green Formal robes [+] — nama: formal | jenis=zirah(28) | tema=militer(51)/formal(35) | subjek=katak(15)/bendera(10) | pola=loreng(52) | lengan=pendek panjang=panjang fit=longgar depan=tertutup | [gambar:militer]
- `4975679890` Green Kimono (+) — nama: tradisional | jenis=zirah(41) | tema=militer(52)/tradisional(36) | subjek=katak(25)/ular(9) | pola=loreng(89) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:militer]
- `5034130585` 🍓Cute🍓 — nama: kawaii | jenis=crop(13) | tema=kawaii(53)/coquette(36) | subjek=pita(14)/bunga(12) | pola=bunga(20) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `5230319278` kawaii — nama: kawaii | jenis=sweater(13) | tema=kawaii(53)/coquette(20) | subjek=pita(9)/hati(7) | pola=renda(23) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `5526639228` 🔻CUTE🔻LIGHT RED CROP TOP — nama: kawaii | jenis=crop(41) | tema=kawaii(50)/coquette(18) | subjek=buah(16)/bunga(8) | pola=kotak(21) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `5608626226` Angel D Top | Hazbin Hotel ❣️ — nama: malaikat | jenis=jas(14) | tema=coquette(51)/malaikat(35) | subjek=pita(37)/hati(23) | pola=garis(46) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `5823975489` 🌈CUTE PINS🌈 — nama: kawaii | jenis=kemeja(17) | tema=kawaii(53)/peri(34) | subjek=hati(73)/kupu_kupu(5) | pola=pelangi(99) | lengan=panjang panjang=crop fit=longgar depan=terbuka | [gambar:peri]
- `6029367212` kawaii — nama: kawaii | jenis=korset(44) | tema=kawaii(59)/coquette(32) | subjek=pita(38)/hati(14) | pola=garis(29) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `6233629794` school boy shirt — nama: sekolah | jenis=jas(59) | tema=formal(55)/sekolah(36) | subjek=salib(9)/kelelawar(7) | pola=polos(29) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:formal]
- `6245495705` Kawaii — nama: kawaii | jenis=korset(32) | tema=kawaii(57)/coquette(31) | subjek=bunga(32)/pita(14) | pola=bunga(49) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:coquette]
- `6303965964` pink cute sakura antlers preppy valentines soft — nama: kawaii | jenis=korset(15) | tema=kawaii(61)/coquette(28) | subjek=hati(29)/pita(17) | pola=renda(42) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `6328026068` kawaii — nama: kawaii | jenis=gaun(20) | tema=kawaii(57)/coquette(38) | subjek=pita(24)/bunga(21) | pola=bunga(39) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:coquette]
- `6405121100` kawaii.  — nama: kawaii | jenis=korset(33) | tema=kawaii(57)/coquette(28) | subjek=bunga(22)/pita(16) | pola=bunga(41) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:coquette]
- `6479702245` Biggest Cake Head Suit Top — nama: formal | jenis=jas(38) | tema=kawaii(51)/formal(35) | subjek=makanan(40)/bunga(7) | pola=pelangi(32) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:kawaii]
- `6554208237` Orange Suit w/ Black Vest [+] — nama: formal | jenis=jas(60) | tema=formal(52)/halloween(23) | subjek=labu(69)/bebek(3) | pola=bulu(18) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:halloween]
- `9066128818` Gold Spiked Jacket — nama: punk | jenis=zirah(56) | tema=steampunk(63)/punk(35) | subjek=mahkota(50)/dinosaurus(11) | pola=motif_hewan(71) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:steampunk]
- `9133604198` Cute & Chic Cardigan (Full Pink) — nama: kawaii | jenis=sweater(37) | tema=kawaii(50)/coquette(30) | subjek=kelinci(57)/beruang(12) | pola=polos(33) | lengan=tanpa panjang=panjang fit=longgar depan=terbuka | [gambar:coquette]
- `9239724660` White Fluffy Shawl — nama: musim_dingin | jenis=zirah(27) | tema=malaikat(59)/musim_dingin(36) | subjek=naga(22)/hantu(15) | pola=bulu(98) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:malaikat]
- `9242440006` Y2K Butterfly Fantasy Top Rainbow Sequin — nama: y2k | jenis=korset(58) | tema=peri(59)/y2k(35) | subjek=kupu_kupu(97)/pita(3) | pola=pelangi(49) | lengan=tanpa panjang=crop fit=pas depan=terbuka | [gambar:peri]
- `9342424285` Pink Bow Off Shoulder — nama: coquette | jenis=kemeja(31) | tema=coquette(61)/kawaii(26) | subjek=pita(48)/hati(16) | pola=kotak(73) | lengan=tanpa panjang=normal fit=longgar depan=terbuka | [gambar:kawaii]
- `9342870671` 🔥 Blood Flame Shirt 🔥 — nama: horor | jenis=kaos(62) | tema=horor(58)/vampir(25) | subjek=api(53)/tengkorak(9) | pola=polos(27) | lengan=pendek panjang=normal fit=longgar depan=terbuka | [gambar:vampir]
- `9726844011` Giraffe Suit — nama: formal | jenis=kostum_penuh(57) | tema=kostum_hewan(64)/formal(35) | subjek=beruang(53)/anjing(17) | pola=motif_hewan(96) | lengan=panjang panjang=panjang fit=longgar depan=terbuka | [gambar:kostum_hewan]
- `10321652755` Kawaii Arm Bandaids — nama: kawaii | jenis=gaun(19) | tema=kawaii(50)/peri(16) | subjek=laba_laba(14)/kupu_kupu(9) | pola=pelangi(42) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:peri]
- `11301280260` Elton John - Dodgers Suit Top — nama: formal | jenis=jersey(61) | tema=sporty(60)/formal(35) | subjek=petir(38)/logo(15) | pola=polkadot(16) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:sporty]
- `11704143482` Medical Scrubs Purple Pattern  — nama: medis | jenis=kaos(42) | tema=kawaii(52)/medis(38) | subjek=hati(71)/kupu_kupu(8) | pola=polkadot(52) | lengan=pendek panjang=crop fit=longgar depan=terbuka | [gambar:kawaii]
- `11706995759` Oversized Knitted Christmas Sweater Red — nama: natal | jenis=sweater(96) | tema=natal(62)/musim_dingin(35) | subjek=beruang(42)/hati(7) | pola=kotak(31) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:musim_dingin]
- `11753651411` Open Pirate Jacket (Black) — nama: bajak_laut | jenis=jaket(77) | tema=bajak_laut(51)/polisi(22) | subjek=salib(10)/bendera(9) | pola=loreng(46) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:polisi]
- `11836159950` Fashionable Fur Coat with Bow - Red — nama: coquette | jenis=jaket(46) | tema=natal(58)/coquette(35) | subjek=pita(44)/kartun(7) | pola=bulu(40) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:natal]
- `12438803140` 🦋 Butterfly Y2K Crop Top - Yellow — nama: y2k | jenis=crop(59) | tema=kerajaan(54)/y2k(35) | subjek=mahkota(64)/kupu_kupu(35) | pola=kulit(39) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:kerajaan]
- `12730748589` White Suit 1.0 — nama: formal | jenis=jas(67) | tema=formal(53)/medis(41) | subjek=hantu(17)/salib(15) | pola=polos(80) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:medis]
- `12777289091` CYBERpunk Arm Warmers Pink and Black — nama: cyber | jenis=jubah(22) | tema=coquette(57)/cyber(35) | subjek=musik(82)/pita(6) | pola=loreng(25) | lengan=tanpa panjang=panjang fit=pas depan=tertutup | [gambar:coquette]
- `12851573808` 3.0 Simple Bracelet Set - Gold — nama: biasa | jenis=seragam(31) | tema=steampunk(57)/biasa(35) | subjek=mahkota(91)/rantai(2) | pola=garis(28) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:steampunk]
- `13022027698` Devil Hunter's Coat (1.0) — nama: iblis | jenis=zirah(53) | tema=iblis(50)/vampir(23) | subjek=beruang(19)/salib(14) | pola=kulit(28) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:vampir]

## Contoh acak per kelompok

### aksen
- `11695372929` Pastel Blue Plaid Scarf — jenis=syal(99) | tema=kawaii(40)/musim_dingin(27) | subjek=pita(64)/bunga(5) | [gambar:musim_dingin]
- `5505987520` Fairy Wings of Darkness — jenis=sayap(93) | tema=peri(83)/malaikat(12) | subjek=kupu_kupu(87)/pita(5) | [gambar:peri]
- `7609219485` 3.0 Silver Cross Necklace — jenis=kalung(96) | tema=malaikat(87)/kawaii(2) | subjek=salib(91)/rantai(5) | [gambar:malaikat]
- `10154337402` Wings — jenis=sayap(98) | tema=malaikat(98)/peri(0) | subjek=pita(44)/salib(21) | [gambar:malaikat]
- `4211442628` Mimic Hoodie — jenis=alat_musik(48) | tema=vampir(25)/horor(20) | subjek=mata(50)/buah(5) | [gambar:vampir]
- `4684604534` Red Wooden Bead Necklace — jenis=kalung(78) | tema=steampunk(18)/natal(16) | subjek=buah(40)/rantai(16) | [gambar:steampunk]
- `12785592157` Dark Gray Trench Raider Armor — jenis=ekor(25) | tema=ksatria(37)/polisi(29) | subjek=tanpa(19)/salib(16) | [gambar:polisi]
- `501941432` Jade Katana Swordpack — jenis=senjata(96) | tema=ninja(68)/penyihir(5) | subjek=salib(39)/pita(17) | [gambar:ninja]
- `12500861409` ✅ Bag — jenis=kalung(44) | tema=gaun_elegan(61)/formal(8) | subjek=rantai(87)/bulan(2) | [gambar:gaun_elegan]
- `10905429074` CHM Compass Necklace  — jenis=kalung(87) | tema=punk(49)/iblis(7) | subjek=rantai(70)/logo(10) | [gambar:punk]
- `7241634848` Star Pendant — jenis=kalung(91) | tema=penyihir(23)/y2k(13) | subjek=bintang(50)/bulan(13) | [gambar:penyihir]
- `7498753952` Black Jewel Cross Necklace 1.0 — jenis=kalung(97) | tema=gothic(90)/punk(6) | subjek=salib(96)/rantai(3) | [gambar:gothic]
- `12903860222` White Hero Cape — jenis=jubah_belakang(72) | tema=superhero(41)/ksatria(10) | subjek=logo(19)/hiu(12) | [gambar:ksatria]
- `12103270510` Emirates Mini A380 — jenis=sayap(47) | tema=malaikat(32)/antariksa(15) | subjek=logo(27)/bebek(22) | [gambar:malaikat]
- `4416812356` Davy Bazooka - Bazooka — jenis=senjata(26) | tema=antariksa(33)/cyber(18) | subjek=petir(32)/api(9) | [gambar:antariksa]
- `12460327531` cute paper bowtie — jenis=ekor(30) | tema=kawaii(35)/gothic(31) | subjek=kelelawar(64)/pita(5) | [gambar:gothic]
- `5510009981` Purple Flame Wings — jenis=sayap(94) | tema=gothic(44)/malaikat(23) | subjek=api(36)/kelelawar(22) | [gambar:gothic]
- `6203388165` Pink Mecha Arms (Over-Hanging) - LIGHT SERIES — jenis=sayap(20) | tema=coquette(47)/cyber(40) | subjek=hati(25)/pita(14) | [gambar:coquette]
- `382881521` Tix Bling — jenis=sabuk(43) | tema=y2k(25)/halloween(14) | subjek=rantai(23)/tulisan(23) | [gambar:y2k]
- `7901626380` (1.0) Walkboy Retro Music Player — jenis=headphone(47) | tema=polisi(38)/cyber(13) | subjek=petir(38)/musik(36) | [gambar:polisi]
- `8948027890` Blue Magical Staff of the Elements — jenis=ekor(44) | tema=badut(22)/kerajaan(9) | subjek=pita(16)/ular(16) | [gambar:badut]
- `6042477338` Savannah Cat Tail - Wonder Woman — jenis=ekor(96) | tema=kostum_hewan(50)/badut(29) | subjek=kucing(37)/ular(36) | [gambar:kostum_hewan]
- `8347408324` Eternal Light — jenis=lain(50) | tema=steampunk(58)/kerajaan(20) | subjek=mahkota(50)/bintang(14) | [gambar:steampunk]
- `5270552011` Colonial Lantern — jenis=sabuk(25) | tema=militer(12)/penyihir(11) | subjek=salib(17)/petir(13) | [gambar:militer]
- `6829556357` Poster Girl Record - Zara Larsson — jenis=ekor(35) | tema=y2k(30)/vampir(11) | subjek=mata(11)/hantu(11) | [gambar:y2k]

### atas
- `4975679890` Green Kimono (+) — jenis=zirah(41) | tema=militer(52)/tradisional(36) | subjek=katak(25)/ular(9) | pola=loreng(89) | lengan=tanpa panjang=crop fit=pas depan=tertutup | [gambar:militer]
- `72204689358397` Gothic Sleeves - Black and Gold — jenis=jubah(74) | tema=gothic(40)/kerajaan(32) | subjek=musik(18)/pita(15) | pola=motif_hewan(89) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:kerajaan]
- `9239352995` Dark Blue Denim Jacket — jenis=jaket(77) | tema=formal(23)/sekolah(18) | subjek=bulan(13)/tanpa(12) | pola=denim(91) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:formal]
- `14066809751` Denim Jacket and White Hoodie outfit — jenis=jaket(62) | tema=koboi(21)/y2k(10) | subjek=tanpa(14)/bulan(13) | pola=denim(99) | lengan=panjang panjang=normal fit=longgar depan=terbuka | [gambar:koboi]
- `14088245235` Gorilla Blox Plushie — jenis=jaket(24) | tema=formal(47)/gaun_elegan(10) | subjek=salib(30)/musik(29) | pola=polos(69) | lengan=tanpa panjang=normal fit=pas depan=tertutup | [gambar:formal]
- `3616417322` [UFOs] I let the dogs out — jenis=rompi(11) | tema=novelty(13)/formal(8) | subjek=tulisan(37)/kucing(4) | pola=tulisan(65) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:novelty]
- `5470052468` Black Gentleman Hat Suit [Top] — jenis=jas(59) | tema=formal(82)/gothic(6) | subjek=kelelawar(12)/laba_laba(8) | pola=kulit(28) | lengan=panjang panjang=panjang fit=pas depan=tertutup | [gambar:formal]
- `13479261772` Fingerless Gloves — jenis=kostum_penuh(40) | tema=coquette(23)/badut(16) | subjek=pita(43)/buah(10) | pola=garis(51) | lengan=pendek panjang=panjang fit=longgar depan=tertutup | [gambar:coquette]
- `1636151` Random Design 1 Yellow [Transparent] — jenis=sweater(21) | tema=kawaii(16)/malaikat(15) | subjek=petir(12)/logo(12) | pola=garis(35) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:kawaii]
- `72012744074825` Traditional Chinese White Hanfu Cloak — jenis=jubah(36) | tema=tradisional(36)/malaikat(14) | subjek=hiu(29)/kelelawar(24) | pola=polos(48) | lengan=panjang panjang=normal fit=pas depan=terbuka | [gambar:malaikat]
- `12779250207` Undisputed Hoodie 1.0 — jenis=zirah(43) | tema=vampir(32)/gothic(14) | subjek=salib(16)/logo(15) | pola=polos(44) | lengan=pendek panjang=normal fit=pas depan=tertutup | [gambar:vampir]
- `4426853252` layer — jenis=kemeja(47) | tema=sekolah(12)/biasa(8) | subjek=logo(28)/tanpa(10) | pola=polos(22) | lengan=pendek panjang=normal fit=pas depan=terbuka | [gambar:sekolah]
- `12283600662` Cartoony Rainbow Animated Void Arms — jenis=seragam(23) | tema=peri(36)/pantai(20) | subjek=pita(31)/laba_laba(10) | pola=pelangi(78) | lengan=panjang panjang=normal fit=pas depan=tertutup | [gambar:peri]
- `5080987186` gentleman shirt — jenis=kaos(38) | tema=gothic(32)/formal(16) | subjek=kelelawar(31)/laba_laba(7) | pola=kulit(30) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic]
- `18845749164` Nails — jenis=tanktop(15) | tema=peri(12)/kawaii(10) | subjek=laba_laba(20)/petir(10) | pola=polkadot(22) | lengan=tanpa panjang=normal fit=longgar depan=tertutup | [gambar:peri]
- `15037115293` ⚡ Cyber Superhero Gloves ⚡ — jenis=kostum_penuh(21) | tema=cyber(20)/superhero(18) | subjek=musik(23)/petir(19) | pola=pelangi(34) | lengan=tanpa panjang=panjang fit=longgar depan=tertutup | [gambar:penyihir]
- `5024371981` LULULEMON- white sports top — jenis=hoodie(15) | tema=malaikat(7)/gaun_elegan(6) | subjek=hantu(7)/tanpa(6) | pola=renda(20) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:malaikat]
- `393552544` Postmodern Black Vest with Teal LS Polo — jenis=rompi(24) | tema=gothic(7)/medis(6) | subjek=naga(7)/uang(7) | pola=kulit(23) | lengan=pendek panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `6492661787` Hello kitty-Grunge Black Shirt — jenis=kaos(38) | tema=punk(41)/gothic(12) | subjek=kucing(38)/tengkorak(6) | pola=kilau(17) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:gothic]
- `6481297386` Military Physical Training Shirt — jenis=kaos(39) | tema=militer(52)/vampir(4) | subjek=katak(6)/kelelawar(6) | pola=loreng(48) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:militer]
- `5072650475` GamingWithKev Shirt — jenis=kaos(40) | tema=badut(9)/natal(8) | subjek=katak(20)/bendera(11) | pola=pelangi(28) | lengan=tanpa panjang=crop fit=longgar depan=tertutup | [gambar:badut]
- `12777289091` CYBERpunk Arm Warmers Pink and Black — jenis=jubah(22) | tema=coquette(57)/cyber(35) | subjek=musik(82)/pita(6) | pola=loreng(25) | lengan=tanpa panjang=panjang fit=pas depan=tertutup | [gambar:coquette]
- `16355368906` Black Pirate Outfit — jenis=jaket(89) | tema=bajak_laut(50)/steampunk(23) | subjek=kelelawar(11)/salib(10) | pola=kulit(58) | lengan=tanpa panjang=panjang fit=longgar depan=terbuka | [gambar:steampunk]
- `9239956594` Black Vest — jenis=rompi(50) | tema=formal(65)/gaun_elegan(11) | subjek=salib(33)/tanpa(24) | pola=kulit(65) | lengan=tanpa panjang=normal fit=pas depan=terbuka | [gambar:formal]
- `6049198454` black — jenis=zirah(28) | tema=gothic(51)/formal(6) | subjek=laba_laba(15)/tengkorak(9) | pola=renda(18) | lengan=panjang panjang=normal fit=longgar depan=tertutup | [gambar:gothic]

### bawah
- `6563249518` heart overall — jenis=overall(40) | tema=coquette(58)/peri(17) | subjek=hati(48)/bunga(14) | pola=renda(35) | panjang=selutut fit=lebar | [gambar:coquette]
- `16810686161` Icy Figure Skating Pants - Purple — jenis=legging(54) | tema=penyihir(13)/novelty(9) | subjek=bintang(12)/salib(10) | pola=pelangi(46) | panjang=selutut fit=ketat | [gambar:penyihir]
- `6019330519` Krew District // Custom Chained Jeans — jenis=jeans(37) | tema=formal(11)/biasa(5) | subjek=laba_laba(6)/musik(5) | pola=denim(36) | panjang=panjang fit=lebar | [gambar:formal]
- `9358418596` Fuzzy Bunny Sleepwear Shorts White — jenis=celana_pendek(41) | tema=medis(11)/malaikat(10) | subjek=kelinci(37)/tengkorak(31) | pola=pelangi(58) | panjang=pendek fit=lebar | [gambar:medis]
- `5533178473` Cifonelli - Old Fashion  — jenis=kargo(13) | tema=formal(9)/biasa(7) | subjek=kelelawar(5)/salib(5) | pola=polos(20) | panjang=panjang fit=lebar | [gambar:formal]
- `6602926937` ✿preppy flamingo swimsuit — jenis=jeans(21) | tema=kawaii(16)/coquette(10) | subjek=hati(19)/bunga(12) | pola=bunga(48) | panjang=selutut fit=lebar | [gambar:kawaii]
- `12811971877` Short Hearts & Skulls Leg Warmers 3.0 — jenis=celana_pendek(39) | tema=bajak_laut(40)/halloween(14) | subjek=tengkorak(73)/hati(23) | pola=tulisan(26) | panjang=pendek fit=lebar | [gambar:bajak_laut]
- `5339782257` President's Suit [ 2008 Style / OG / OLD ROBLOX ] — jenis=legging(12) | tema=formal(43)/biasa(5) | subjek=salib(5)/tanpa(4) | pola=kulit(18) | panjang=pendek fit=lebar | [gambar:formal]
- `4820072092` [ Content Deleted ] — jenis=jogger(11) | tema=vampir(19)/iblis(12) | subjek=api(7)/musik(6) | pola=motif_hewan(18) | panjang=panjang fit=lebar | [gambar:vampir]
- `6115495280` Tartan pants! ✰ — jenis=celana_kain(23) | tema=sekolah(22)/tradisional(19) | subjek=bendera(22)/pita(7) | pola=kotak(99) | panjang=panjang fit=lebar | [gambar:sekolah]
- `90012329737847` Green Y2K Checkered Chain Mini Skirt [PBR] — jenis=rok_pendek(47) | tema=militer(38)/y2k(35) | subjek=rantai(35)/beruang(11) | pola=catur(58) | panjang=pendek fit=lebar | [gambar:militer]
- `15832449047` ʚ cargo pants  — jenis=kargo(82) | tema=koboi(31)/militer(10) | subjek=beruang(13)/mahkota(11) | pola=loreng(27) | panjang=pendek fit=lebar | [gambar:koboi]
- `86792633171666` Boxer Jeans Dirty Blue — jenis=jeans(96) | tema=streetwear(18)/koboi(16) | subjek=rantai(15)/tanpa(11) | pola=denim(97) | panjang=pendek fit=lebar | [gambar:streetwear]
- `15286119141` 💯 White Fuzzy Fur Slippers — jenis=bawahan_gaun(49) | tema=kostum_hewan(40)/musim_dingin(26) | subjek=naga(26)/ular(8) | pola=bulu(94) | panjang=selutut fit=lebar | [gambar:kostum_hewan]
- `4835471905` Galaxy Pants — jenis=bawahan_gaun(35) | tema=antariksa(38)/gothic(14) | subjek=bulan(12)/salib(10) | pola=polos(23) | panjang=pendek fit=lebar | [gambar:gothic]
- `5196364021` denim ripped short jeans aesthetic cute trendy — jenis=jeans(60) | tema=kawaii(44)/biasa(4) | subjek=hantu(6)/hiu(6) | pola=denim(69) | panjang=panjang fit=lebar | [gambar:kawaii]
- `7151637870` denim ୨୧ — jenis=jeans(59) | tema=novelty(7)/kostum_hewan(6) | subjek=hiu(5)/ular(5) | pola=denim(48) | panjang=selutut fit=lebar | [gambar:novelty]
- `76436181339322` ✅Brown Emo  Checkered Ruffle Skirt✅ — jenis=rok_pendek(57) | tema=punk(35)/halloween(15) | subjek=labu(34)/beruang(15) | pola=kotak(58) | panjang=pendek fit=lebar | [gambar:halloween]
- `96794685714412` Black Techwear Cargo Pants — jenis=kargo(51) | tema=cyber(36)/polisi(13) | subjek=tanpa(25)/salib(9) | pola=polos(48) | panjang=pendek fit=lebar | [gambar:polisi]
- `1072794008` Midnight sparkle time Pants [LIMITED TIME ONLY] — jenis=zirah_bawah(34) | tema=kerajaan(13)/penyihir(9) | subjek=petir(10)/naga(6) | pola=kilau(47) | panjang=panjang fit=lebar | [gambar:kerajaan]
- `84005541727136` Ripped Jeans w/ Chain & Shoes (Light Grey) — jenis=jeans(98) | tema=punk(35)/streetwear(21) | subjek=rantai(54)/bulan(7) | pola=denim(95) | panjang=panjang fit=lebar | [gambar:punk]
- `17747079720` Chibi Doll Skirt — jenis=rok_pendek(65) | tema=sekolah(35)/maid(12) | subjek=hati(10)/bunga(7) | pola=catur(30) | panjang=pendek fit=lebar | [gambar:sekolah]
- `6638644409` (🦪) 𝙎𝙞𝙡𝙫𝙚𝙧 𝙀𝙭𝙩𝙧𝙖𝙫𝙖𝙜𝙖𝙣𝙯𝙖 - Dress — jenis=bawahan_gaun(46) | tema=y2k(8)/formal(8) | subjek=petir(11)/hantu(8) | pola=pelangi(17) | panjang=selutut fit=ketat | [gambar:y2k]
- `6539338064` Bunny Bow Satin Dress w/ Jelly Sandals in Pink — jenis=bawahan_gaun(47) | tema=coquette(59)/peri(18) | subjek=pita(22)/kelinci(21) | pola=bunga(44) | panjang=panjang fit=lebar | [gambar:coquette]
- `4556542661` [AA] Universal Pants  — jenis=rok_pendek(11) | tema=formal(9)/biasa(8) | subjek=salib(6)/tanpa(5) | pola=polos(26) | panjang=pendek fit=lebar | [gambar:formal]

### kepala
- `6187113962` Gold Hoop Earrings — jenis=anting(51) | tema=steampunk(97)/kerajaan(1) | subjek=rantai(41)/mahkota(15) | [gambar:steampunk]
- `12293991165` Earmuffs — jenis=headphone(100) | tema=gothic(16)/formal(6) | subjek=musik(23)/tanpa(9) | [gambar:gothic]
- `3963907137` The Escape Artist — jenis=halo(49) | tema=antariksa(66)/y2k(4) | subjek=mata(52)/katak(28) | [gambar:antariksa]
- `12310612074` Black Mixpat FAST Helmet — jenis=helm(69) | tema=sporty(69)/polisi(18) | subjek=kelelawar(15)/tanpa(12) | [gambar:sporty]
- `12789114477` Shadow Boy — jenis=topeng_kepala(38) | tema=gothic(34)/iblis(26) | subjek=kelelawar(24)/mata(13) | [gambar:gothic]
- `7668537321` Black Plaid Fedora — jenis=topi_formal(86) | tema=formal(49)/koboi(19) | subjek=tanpa(24)/salib(11) | [gambar:formal]
- `7168593722` Wicked and Vile — jenis=tanduk(45) | tema=gothic(61)/vampir(12) | subjek=kelelawar(41)/naga(19) | [gambar:gothic]
- `7212278970` Golden Headphones - KSI — jenis=headphone(99) | tema=steampunk(35)/militer(19) | subjek=musik(52)/rantai(10) | [gambar:steampunk]
- `8151404994` Hovering UFO — jenis=halo(99) | tema=cyber(67)/antariksa(9) | subjek=petir(31)/bintang(13) | [gambar:cyber]
- `116778296` Wide-brimmed Straw Cap — jenis=topi_baseball(36) | tema=pantai(41)/koboi(26) | subjek=tanpa(20)/ular(15) | [gambar:pantai]
- `12785419589` Kitsune Mask — jenis=topeng_kepala(55) | tema=iblis(35)/vampir(25) | subjek=kucing(42)/anjing(17) | [gambar:iblis]
- `5132802731` Pink Pom poms — jenis=pita_bando(26) | tema=kawaii(58)/coquette(34) | subjek=bunga(29)/makanan(20) | [gambar:kawaii]
- `49763737` Rockstar Disguise — jenis=topi_formal(44) | tema=formal(39)/gothic(7) | subjek=salib(9)/bunga(9) | [gambar:formal]
- `5511283469` Silver Stars and Moons Confetti — jenis=kupluk(15) | tema=antariksa(33)/peri(15) | subjek=bulan(51)/bintang(46) | [gambar:antariksa]
- `10816577500` Black Star Beanie Y2k Trending Emo Gangster — jenis=kupluk(46) | tema=punk(21)/y2k(20) | subjek=bintang(36)/beruang(22) | [gambar:halloween]
- `4584972547` Blue Crystallized Horns — jenis=tanduk(46) | tema=penyihir(25)/kerajaan(21) | subjek=kelelawar(26)/petir(25) | [gambar:penyihir]
- `12651685566` Classic Skybox Top Hat — jenis=topi_formal(40) | tema=kawaii(40)/malaikat(33) | subjek=bunga(16)/bulan(14) | [gambar:kawaii]
- `10717262789` Red Flannel Head — jenis=kupluk(48) | tema=natal(24)/tradisional(21) | subjek=hati(25)/bendera(11) | [gambar:natal]
- `74939231` Emerald Crystal Circlet — jenis=mahkota(34) | tema=y2k(49)/penyihir(16) | subjek=katak(16)/naga(13) | [gambar:y2k]
- `321570512` Chill Cap — jenis=topi_baseball(76) | tema=streetwear(21)/kawaii(18) | subjek=tulisan(29)/logo(25) | [gambar:streetwear]
- `5674051153` Photo Drone — jenis=halo(18) | tema=malaikat(12)/cyber(9) | subjek=kelelawar(24)/laba_laba(16) | [gambar:malaikat]
- `8918829397` Red Garden Horns — jenis=tanduk(39) | tema=iblis(39)/peri(19) | subjek=bunga(86)/pita(7) | [gambar:iblis]
- `6431950467` Miau Glitter Hair Clips Black — jenis=anting(34) | tema=formal(19)/kerajaan(10) | subjek=ular(15)/musik(11) | [gambar:formal]
- `47702745` Sk10r Boi — jenis=topi_baseball(30) | tema=y2k(28)/streetwear(11) | subjek=kelelawar(10)/tanpa(8) | [gambar:y2k]
- `11705401570` Downfall Cowlick [Pink] — jenis=pita_bando(23) | tema=coquette(44)/tradisional(9) | subjek=petir(15)/hiu(8) | [gambar:coquette]

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
- atas: kawaii 757, formal 680, gothic 368, militer 265, coquette 257, sporty 232, malaikat 232, steampunk 216, iblis 191, halloween 157, cyber 154, kerajaan 141
- bawah: formal 941, kawaii 535, gothic 385, y2k 364, biasa 362, coquette 309, punk 206, sekolah 203, militer 198, maid 179, halloween 154, musim_dingin 145
- kepala: coquette 240, kawaii 215, kerajaan 180, formal 162, malaikat 149, militer 142, gothic 122, peri 114, kostum_hewan 109, iblis 99, penyihir 97, polisi 94
- rambut: kawaii 434, gothic 388, coquette 231, steampunk 182, anime 181, gaun_elegan 165, koboi 151, musim_dingin 141, punk 136, malaikat 116, iblis 92, y2k 82
- sepatu: kawaii 351, gothic 247, coquette 245, sporty 202, musim_dingin 193, y2k 158, kostum_hewan 145, pantai 132, militer 113, punk 108, gaun_elegan 97, formal 89
- wajah: kawaii 437, steampunk 235, gothic 179, militer 166, cyber 160, coquette 143, malaikat 91, anime 88, polisi 84, iblis 75, vampir 71, pantai 69
