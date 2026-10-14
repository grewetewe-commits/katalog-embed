# Checkpoint bersama — 14 Oktober 2026

Status: **NEEDS_CHANGES — siap dilanjutkan Claude**. Pemilik sesi: tidak ada setelah giliran review Codex selesai.

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
