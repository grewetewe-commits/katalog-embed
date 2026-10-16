# Checkpoint bersama — 16 Oktober 2026

## Status aktif — READY_FOR_CODEX (Claude, 16 Okt bagian 5, rev 31: pembaca item berbukti & diukur)

Baca [laporan rev 31](AI_CLAUDE_2026-10-16e.md). Ringkas:
- **Tema berbukti** (nama + benda terlihat + pemakaian di 73 rb outfit manusia; kurang bukti = tidak bertema) dan **peta
  sambungan tema** (PMI) dipakai penyusun; pesan ke pemain menyebut buktinya.
- **Gender** dari pemakaian (uji nama-tersembunyi 95–97%) + bentuk diukur; gerbang gender berlaku semua slot.
- **Bentuk 2D diukur dari piksel** (leher, bahu, lengan, crop, panjang celana, lapisan kulit); leher rendah/bahu terbuka/crop
  terbukti 98–99% dipakai cewek.
- **FisikItemKit** (map): titik pasang, ukuran mesh, lapisan 3D, tekstur PBR, template 2D.
- Verteks 3D: `mata3d.py` siap, menunggu izin API key **thumbnails: read** dari pemilik. Vercel tidak dipakai.
- **Save rev 31 belum terkonfirmasi** (rev 30 sudah tersimpan). Tidak publish.

Langkah berikut: Codex review PR #5 + patch Studio rev 30/31.

## Status sebelumnya — READY_FOR_CODEX (Claude, 16 Okt bagian 4, rev 30: 2D, headless, GUI)

Baca [laporan rev 30](AI_CLAUDE_2026-10-16d.md) dan PR #5 (branch `claude/kartu-item`). Ringkas:
- **Pakaian 2D**: label emas manual 175 item (`uji2d/`). Kartu skema 2 (probe dari nama + gambar; kolom `fungsi` kaos klasik).
  Akurasi kartu vs label emas: baju jenis 25→49%, baju tema 50→65%, celana jenis 42→56%, kaos fungsi 87%. Map: kaos
  shading/kalung/gambar tidak dihitung atasan (`kaosMenutup`).
- **Headless**: dulu 120/120 kartu tanpa rambut/topi/leher → kini mengikuti avatar pemain (`V.KepalaTersembunyi`).
- **GUI**: semua UI buatan script dipindah ke Studio (0 `Instance.new` kelas UI), label tanpa kurung/miring, `BodyChoiceDialog`
  ScreenGui baru, cadangan `ServerStorage.Cadangan_GUI_20261016`.
- Script: IndeksOutfitEngine, DesainerEngine, KartuItemKit, VisualOutfitKit, KatalogServerEngine, KatalogUIController,
  ResponsiveCatalogKit, BodyChoiceUI. **Save belum terkonfirmasi**. Tidak publish.

Langkah berikut: Codex review PR #5 (+ audit `uji2d/emas.json`) dan patch Studio rev 30; setelah merge `KartuItemKit.CABANG = "main"`.

## Status sebelumnya — READY_FOR_CODEX (Claude, 16 Okt bagian 3, rev 29 Kartu Item)

Baca [laporan rev 29](AI_CLAUDE_2026-10-16c.md) dan PR #5 (branch `claude/kartu-item`, `RANCANGAN_KARTU_ITEM.md`). Ringkas:
- **Kartu Item**: GitHub membaca GAMBAR 132 rb item (CLIP, gratis) → jenis, bentuk, tema, subjek gambar utama, pola. Map memakainya lewat `KartuItemKit` (baru).
- Kasus pemilik Duck-o-Lantern: dulu baju/celana bebek, kini outfit Halloween (koherensi tema-kartu 75–97%), pesan "Dibaca dari gambar item: tema Halloween (labu)".
- Sepatu otomatis dimatikan (arahan pemilik). Endpoint 3D resmi ditolak "Scope not authorized" untuk API key repo → menunggu pemilik.
- Script: KartuItemKit (baru), IndeksOutfitEngine, DesainerEngine. **Save belum terkonfirmasi**. Tidak publish.

Langkah berikut: Codex review PR #5 + patch Studio rev 29, audit label emas dari lembar kontak; setelah merge, `KartuItemKit.CABANG = "main"`.

## Status sebelumnya — READY_FOR_CODEX (Claude, 16 Okt bagian 2, rev 27 tema + rev 28)

Baca [laporan rev 28](AI_CLAUDE_2026-10-16b.md). Ringkas:
- Sistem kini mengenali **motif spesifik** item pilihan (50 motif: koboi, bajak laut, maid, jas, tokoh anime, …), mencari pelengkap setema lewat indeks kata kolam, memberi tahu pemain ("Tema item terbaca: …"), dan gerbang mutu menerima bukti tema dari nama (maks +12).
- **Baju gaun 2D** otomatis dipasangkan celana set-nya (Maid Dress: 24/24 setema, celana bukan pasangan 10 → 0, 120 kartu).
- Dorongan tema kategori rev 27 dibuat berselang (jumlah kartu koboi 40 → 48, jas 33 → 52).
- Script berubah: StylistEngine, IndeksOutfitEngine, DesainerEngine, MutuKit, VisualOutfitKit. **Save belum terkonfirmasi**. Tidak publish.
- Otak berganti versi di tengah sesi (1792086980): S10 120 → 58, S11 65 → 26 sebagian karena itu; gerbang mutu tidak dilonggarkan.

Langkah berikut: Codex review rev 28; putuskan kebijakan jumlah minimum vs gerbang mutu.

## Status sebelumnya — READY_FOR_CODEX (Claude, 16 Okt bagian 1)

Baca [laporan giliran Claude 16 Oktober](AI_CLAUDE_2026-10-16.md). Ringkas:
- R-01 direview Claude: **disetujui**, uji independen 17/17 pada source terpasang.
- R-02 ternyata **sudah terpasang** di Studio (identik dengan proposal); harness dijalankan pada source terpasang: 18/18.
- R-03 diperbaiki: `RankingOutfitKit.BatasAtasan` (preferensi yang dilaporkan, `od.AtasanUlang`, `Ringkasan.AtasanUlang`), uji 13/13.
- Performa: jumlah susunan desainer mengikuti jumlah kartu (`skala`), waktu Studio 4,0–10,4 → 2,9–6,2 dtk; semua skenario ≥ 50 kartu.
- Script berubah: RankingOutfitKit, KatalogServerEngine (`periksaFinal`), IndeksOutfitEngine (`susunDesainer`). **Save belum terkonfirmasi** (Claude tidak punya alat Save; pemilik Ctrl+S). Tidak publish.
- Temuan baru D-02: `batasSeimbang` memotong semua kelompok jangkar ke ukuran kelompok terkecil.

Langkah berikut: Codex review diff tersebut; lalu Claude Q-02 mulai dari uji visual 12 kombinasi.

## Status sebelumnya — READY_FOR_CLAUDE (15 Okt)

Baca [tugas dan bukti 15 Oktober](AI_WORKPLAN_2026-10-15.md). Pemilik menegaskan sepatu dan outfit ramai boleh bila sesuai tema/item/badan, dan biaya operasional layanan tambahan wajib Rp0. Codex sudah menyiapkan proposal R-02 serta uji terisolasi: kode sekarang 9/17 lulus, proposal 17/17 lulus. **Proposal belum dipasang ke Studio.** Claude berikutnya mereview R-01, mengintegrasikan R-02, lalu menangani penilaian komposisi Q-02; Codex mereview hasil integrasi. Claude belum menjalankan pekerjaan ini.

Studio dibaca langsung pada 15 Oktober, mode Edit. Main GitHub terakhir ef612d0; branch bersama sebelum pembaruan ini c805d61. Tidak ada edit/Save Studio baru pada giliran ini. Keterbatasan visual, R-03, dan audit biaya akun masih terbuka. Tidak ada layanan berbayar atau billing baru.

## Riwayat 14 Oktober — R-01

Status: **READY_FOR_CLAUDE_REVIEW — R-01 terpasang dan Save terkonfirmasi**. Pemilik sesi: tidak ada setelah giliran implementasi Codex selesai. Pemilik memberi izin khusus Codex memperbaiki R-01 di Studio; Claude mereview patch ini.

## Pembaruan terakhir: R-01

Baca [laporan implementasi dan bukti R-01](AI_R01_IMPLEMENTED_2026-10-14.md). Hanya VisualOutfitKit berubah: Rapikan dan Nilai kini memakai helper batas motif yang sama. Pemeriksaan Luau terisolasi: sebelum 14/18, sesudah 18/18, source terpasang 18/18. Source editor dan Instance.Source cocok. Save biasa terkonfirmasi melalui Output Studio pada 21:04:18 tanggal 14 Oktober. Tidak publish; visual outfit nyata belum diuji pada patch ini.

Tindakan berikut: Claude review patch aktual dan lanjut uji visual/manual. R-02/R-03 tetap terbuka. Catatan di bawah adalah review awal sebelum patch; keterangan belum tes/belum Save di bagian historis tersebut sudah digantikan oleh pembaruan ini. Main terakhir yang diperiksa pada giliran implementasi: b6f7590; branch panduan sebelum pembaruan ini: 2d19685.

## Sumber yang benar-benar diperiksa

- GitHub `main`: `00ef427063442200e746af105fe09d703f827fc3`, dibaca melalui fetch pada sesi ini. Commit berikutnya dapat berubah karena jadwal pengumpulan/pelatihan.
- Backend dibandingkan dengan checkout lama `d8129e8`: perubahan `otak.py` pada perbandingan ini hanya akhir baris; perubahan bermakna yang terlihat terutama hasil pengumpulan/model. Jangan menafsirkan nama commit otomatis sebagai implementasi baru oleh Claude.
- Roblox Studio: place `103437401207325`, universe `10753176264`, mode Edit. Source dibaca langsung dari editor pada 14 Oktober; ada `ServerStorage.Cadangan_Claude_20261014`.
- Dibaca penuh: DesainerEngine, VisualOutfitKit, IndeksOutfitEngine, StylistEngine, KonsepKit, ShoePairKit, OtakGayaEngine, MutuKit, RankingOutfitKit, WholeOutfitKit, BodyFitKit, GenderKit, BodyContextKit. KatalogServerEngine dibaca pada bagian filter jual/harga, pasangan sepatu, dan ranking akhir. Ini bukan audit semua script map.
- Folder `roblox-src` milik Codex terbukti tertinggal dari source Studio; jangan mengimpor ulang folder tersebut ke Studio.

## Perubahan Studio yang ditemukan

- Sepatu pasangan resmi dimasukkan ke kandidat desain; metadata harga/status bundle dipakai dan kaki kanan tanpa vektor dapat dinilai melalui pasangan kirinya.
- Kandidat inti diperluas untuk variasi warna; tambahan penyaringan fandom, aksesori berlabel R6, dan tumpukan rok.
- Aturan aksesori pada item bermotif/hoodie dilonggarkan; kandidat polos mendapat penalti tambahan.
- Prioritas hasil desain dari nol dipulihkan pada shortlist dan ranking akhir. Evaluasi visual belum membuktikan dampaknya.

## Pekerjaan berikutnya: KP-001R

Baca [review aktual Studio](AI_REVIEW_2026-10-14.md). **Mulai dari R-01: aturan jumlah aksesori pada item bermotif tidak konsisten antara perapian dan penilaian.** Perbaiki kontraknya dari source Studio terbaru, bukan menambah pengecualian untuk satu item.

Urutan berikut: R-02 kehilangan metadata sepatu setelah registrasi pasangan; R-03 batas pengulangan atasan pada hasil sedikit; kemudian keputusan prioritas sumber dan bukti ukuran. Jangan sekaligus mengganti seluruh arsitektur.

Penerimaan R-01: kebijakan yang sama dipakai pembentukan/perapian/penilaian; uji 0/1/2 jangkar bermotif dengan 0/1/2 aksen polos serta aksen besar/bermotif, item terkunci, dan headless. Lakukan pemeriksaan runtime relevan dan perbandingan visual sebelum/sesudah pada badan yang sama. Uji ini **belum dijalankan oleh Codex** pada giliran review ini.

## Data terbaru: konteks, bukan nilai keindahan

Laporan backend pada commit di atas: 62.911 outfit terkumpul, 7.983 lolos bank, 60.000 embedding item; FITB 0,806 pada soal memilih satu item di antara empat kandidat. Bank referensi publik terpisah berisi 281 record. Angka itu tidak berarti 80,6% outfit map pasti bagus, tidak membuktikan cakupan seluruh Marketplace, dan bukan bukti snapshot Studio sudah sama.

## Bukti dan keterbatasan giliran ini

- Dilakukan: membaca source editor, mengambil snapshot lokal terbatas, membandingkan dengan source lokal lama, membaca commit GitHub terbaru, meninjau alur source.
- Tidak dilakukan: Play, tes runtime, render outfit baru, pembelian, DataStore live, perubahan source Studio, Save Studio, atau publish. Tidak ada klaim visual PASS.
- Dokumentasi GitHub tidak menyertakan source snapshot Studio atau konfigurasi secret. Tidak ada penambahan layanan/API berbayar.
- Perlu uji manual pemilik dan persetujuan sebelum release. Target biaya nol untuk map komersial masih perlu penyelesaian hosting bila Vercel wajib digunakan.

## Isi checkpoint berikut

Tuliskan status, penulis, revisi GitHub, script Studio yang berubah dan versi sumbernya, Save terkonfirmasi/belum, hasil sebelum/sesudah, perintah uji dan keluaran sebenarnya, kasus gagal, temuan review yang ditutup dengan bukti, serta satu langkah berikut. Jika tidak ada akses menulis GitHub, laporkan checkpoint belum terunggah dan berikan teksnya kepada pemilik.
