# Tugas bersama — komposisi outfit dan biaya nol

Tanggal 15 Oktober 2026. Arahan pemilik: sepatu, aksesori besar, motif, dan susunan ramai boleh bila tepat pada tema/item/badan. Satu item dapat mendukung beberapa tema. Keberhasilan tidak diukur dari banyaknya aksesori, banyaknya kartu, atau skor internal saja.

Status: **READY_FOR_CLAUDE**. Codex selesai membaca source dan menyiapkan proposal R-02 beserta regresi terisolasi. Claude belum menjalankan giliran ini; dokumen tidak mengirim chat atau menjalankan Claude otomatis. Hanya satu penulis Studio aktif.

## Sumber diperiksa

- Studio Katalog Praktis, place 103437401207325, mode Edit. OtakGayaEngine dan ShoePairKit dibaca penuh langsung dari Studio; VisualOutfitKit dan KatalogServerEngine dibaca pada rentang penilaian/registrasi/ranking relevan.
- Main GitHub terakhir diperiksa ef612d0. Perubahan sejak b6f7590 berisi data/model/laporan, bukan patch penilaian runtime.
- Branch bersama sebelum unggahan ini c805d61. Folder roblox-src tetap tertinggal; tidak boleh diimpor sebagai sumber terbaru.
- R-01 masih terpasang: helper batas motif sama pada Rapikan/Nilai. Review independen Claude dan visual masih pending.
- Tidak ada edit source Studio, Play, Save baru, publish, perubahan DataStore, atau pengaturan billing dalam giliran 15 Oktober ini.

## Paket R-02: langkah pertama Claude

File [R02_REGISTER_PROPOSAL.luau](R02_REGISTER_PROPOSAL.luau) berisi fungsi pengganti yang diusulkan, **belum diimplementasikan ke Studio**. Codex menyiapkan proposal teknis, Claude memeriksa dan mengintegrasikannya sesuai aturan implementer. Jangan menyebut patch telah ditinjau independen oleh penulisnya sendiri.

Akar sebab: registrasi mengganti record bermetadata dengan tabel id/bundle saja. Metadata awal diwariskan memakai __index; table.clone tidak menyalin nilai warisan. Proposal menyalin field eksplisit hanya bila bundle, kedua sisi, dan pasangan id cocok. Registrasi identitas berbeda tidak mewarisi harga/status lama. Data snapshot tetap berlabel GITHUB_BUNDLE dan tidak dianggap harga live.

[Harness regresi](R02_REGRESSION.luau) memuat potongan aktual fungsi registrasi, Peek, PeekAny, Fold yang dibaca dari Studio, serta proposal. Ia hanya menggunakan tabel, clock buatan, dan require stub; tidak me-require module produksi. Jalankan melalui Luau test runner terisolasi; jangan memasangnya sebagai script game yang aktif.

[Hasil dijalankan](R02_RESULTS.json):
- Kode sebelum: **9/17 lulus, 8/17 gagal**.
- Proposal: **17/17 lulus**.
- Cakupan: metadata __index, prioritas live, detik 599/600, eviction, pengulangan registrasi, false offsale, harga nol, bundle/pasangan/sisi berubah, pasangan baru, record salah identitas, ID invalid, source metadata tidak dimutasi, dua kaki menjadi satu baris bundle sesudah expiry, satu kaki tidak dianggap sepasang.

Batas tes: expiry/eviction disimulasikan dengan clock/cache; bukan TTL nyata atau panggilan marketplace. Belum uji outfit nyata, checkout pembelian, seluruh caller, metadata kedaluwarsa lintas versi, atau pembersihan reverse mapping pihak ketiga saat pasangan berganti. Jangan memperluas jaminan dari 17 kasus.

Claude:
1. Baca source terbaru, bandingkan fungsi aktual dengan before dalam harness. Jika berubah, perbarui diagnosis sebelum menerapkan.
2. Review proposal khususnya metadata warisan, identitas dua kaki, invalid input, perubahan pasangan dan sisa reverse mapping.
3. Terapkan koreksi terfokus, jalankan regresi terhadap source terpasang (bukan hanya salinan proposal).
4. Save biasa dan catat konfirmasi. Berikan diff dan bukti untuk review Codex. Jangan publish.

## Tugas utama berikutnya: Q-02 penilaian komposisi utuh

### Kontrak produk

- Pertahankan item yang dicentang. Pisahkan kelompok bila item jangkar bertentangan secara teknis/desain; jelaskan alasan.
- Identifikasi beberapa tema masuk akal untuk jangkar dan tingkat kepastian datanya. Pilih satu arah komposisi per kandidat; label sama saja belum membuktikan keserasian.
- Sepatu dipilih berdasarkan pasangan resmi, bentuk kaki, potongan bawahan, tema, volume dan gaya yang dipilih pemain. Jangan melarang sepatu secara umum.
- Preferensi gaya COWO/CEWE/NETRAL berasal dari pilihan pemain. Jangan menyamakan badan tertentu dengan identitas gender pemain.
- Ramai/polos adalah pilihan komposisi. Jangan menolak hanya karena jumlah motif/aksesori. Larangan teknis tetap dipisahkan dari preferensi keindahan.
- 2D/3D/gabungan diputuskan menurut hasil pada badan target, bukan generalisasi bahwa semua pakaian 3D selalu jelek pada semua badan kotak.
- Ketika jangkar tidak cocok badan, pilihan badan pengganti harus diperiksa, ditampilkan sebagai preview, dan diterapkan atas pilihan pemain. Pertahankan pasangan kaki.

### Perubahan yang harus dirancang dan diukur

1. Pisahkan alasan gagal teknis (jangkar hilang, pasangan salah, rig tidak didukung, data invalid) dari biaya komposisi (fokus, motif, warna, volume, siluet, preferensi).
2. Telusuri keseluruhan jalur Rapikan -> Nilai -> MutuKit -> RankingOutfitKit -> pengurutan KatalogServerEngine. Rapikan jangan membuang kandidat yang hendak dinilai Q-02 sebelum penilai dapat melihatnya.
3. Pada VisualOutfitKit, gerbang motif/besar dan batas jumlah adalah kebijakan lama. Pengganti harus membandingkan fungsi tiap elemen dan komposisi utuh. Jangan sekadar menghapus semua batas, memperbanyak keyword, atau menaikkan ambang.
4. Simpan sumber bukti per ciri: metadata resmi, embedding, nama, pengukuran badan, atau render. Unknown tetap unknown; jangan mengubahnya menjadi verified atau nilai tinggi otomatis.
5. Rancangan output diagnostik: versi kebijakan/model, identitas badan/skala/rig, tema kandidat, jangkar dipertahankan, alasan gagal teknis, komponen komposisi, bukti hilang, asal kandidat. Batasi ukuran; jangan log inventory/secret.
6. Skor tambahan untuk satu aksesori harus memperhitungkan seluruh susunan, termasuk elemen yang sudah dipilih. Aksesori yang serasi dengan jangkar saja masih dapat bertabrakan dengan pelengkap lain.
7. Tentukan perlakuan data visual belum tersedia berdasarkan tingkat risiko. Ukuran mesh saja tidak membuktikan deformasi atau clipping; jangan memberi label sudah cocok pada badan tanpa bukti.
8. Evaluasi prioritas DisusunDariNol yang saat ini mengalahkan skor. Usulkan keputusan berdasarkan perbandingan tampilan dengan referensi, bukan memilih asal generator secara mutlak.
9. R-03 pengulangan atasan tetap perlu koreksi; jangan mengorbankan kualitas/kejujuran jumlah demi memenuhi target 50.
10. Jaga biaya: shortlist sebelum render, preview bertahap, cache berbatas, batalkan pekerjaan usang. Kunci cache harus memuat badan/skala/rig, item/layer, jangkar, preferensi, versi model/kebijakan. Tidak merender ratusan avatar sekaligus di setiap request.

### Bukti penerimaan visual

Bekukan input/model sebelum membandingkan. Awali 12 kombinasi nyata: 4 jenis jangkar (2D bermotif, 3D outerwear, aksesori besar, sepatu) x 3 badan (kotak R15, tinggi/ramping, campuran/Korblox). Ini minimum terarah, bukan cakupan semua avatar. Tambahkan R6/headless dan kombinasi baru sesudahnya.

Untuk setiap kombinasi, simpan:
- ID input, body parts/scales, rig, preferensi dan versi model;
- hasil sebelum/sesudah termasuk yang ditolak atau kosong;
- render outfit utuh dari depan/samping/belakang, jumlah unik dan waktu;
- penilaian manusia: item utama tetap bermakna, tema koheren, motif tidak bertentangan, proporsi/volume layak, tidak ada distorsi/clipping yang terlihat;
- alasan gagal yang spesifik, bukan hanya skor total.

Kasus khusus: dua motif senada boleh lolos penilaian gaya; motif bertentangan tidak lolos hanya karena warnanya sama; satu tema yang tepat pada dua badan belum tentu memakai pelengkap identik; ramai yang rapi dan polos yang tepat sama-sama dapat menjadi hasil baik.

Setelah koreksi, pakai kumpulan item berbeda sebagai pembanding baru. Persentase keberhasilan hanya dihitung dari sampel dan rubrik yang jelas; jangan menjanjikan 98% seluruh Marketplace.

## Batas biaya operasional: wajib Rp0 layanan tambahan

- Tidak menambah API generatif berbayar, kredit, trial Pro, large runner, billing atau overage.
- Inti generate memakai model/snapshot di Roblox. Pembaruan GitHub opsional; ketika gagal, pakai snapshot terakhir yang valid dan laporkan status.
- Vercel Hobby hanya personal nonkomersial. Untuk target map dimonetisasi, jalur komersial tidak boleh bergantung pada deployment Hobby. Verifikasi dan nonaktifkan ketergantungan itu melalui perubahan terpisah yang direview, bukan upgrade paket.
- GitHub Actions standard runner pada repo publik gratis untuk komputasi runner; larger runner berbayar. Artifact/cache punya aturan dan batas tersendiri. Jangan mengklaim seluruh akun bebas tagihan hanya dari runs-on.
- Workflow yang dibaca menggunakan ubuntu-latest/ubuntu-24.04. Dua workflow audit mengunggah artifact dengan retensi 7 hari; cache digunakan pelatihan. Pemakaian nyata dan konfigurasi budget akun **belum diaudit**, tidak diubah.
- Uji gangguan CDN/GitHub/Vercel dengan mock/adapter terisolasi sebelum klaim snapshot menjaga map berjalan. Jangan memutus layanan akun atau mengubah DataStore live untuk tes.

Sumber resmi diperiksa 15 Oktober:
[GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) dan [Vercel Hobby](https://vercel.com/docs/plans/hobby).

## Pembagian kerja berikutnya

Claude: review R-01, integrasi R-02, lalu implementasi Q-02 bertahap dengan bukti visual. Catat status sebelum mengerjakan, hentikan bila ada penulis lain.

Codex: review independen diff integrasi Claude, pemeriksaan regresi/caller, perbandingan visual dan audit jalur biaya. Jika pemilik memberi Codex tugas implementasi spesifik lagi, Claude menjadi reviewer patch tersebut.

Perbarui AI_STATE.md dengan revisi nyata, file berubah, hasil gagal/lulus, Save, dan bagian belum diuji. Persetujuan pemilik serta uji Studio manual tetap wajib sebelum release. Jangan menandai pekerjaan Claude selesai hanya karena proposal tersedia.
