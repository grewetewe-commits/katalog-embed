# Mulai di sini — kolaborasi Katalog Praktis

Pemilik memakai Codex Desktop dan Claude Desktop secara bergantian. Panduan ini berada di GitHub agar keduanya dapat membacanya walaupun Claude bekerja melalui koneksi Roblox Studio dan tidak membuka folder lokal Codex.

## Sebelum bekerja

1. Baca [status dan tugas aktif](AI_STATE.md), lalu laporan review yang ditautkan di sana. Sebutkan revisi GitHub yang benar-benar dibaca dan status koneksi Studio.
2. Untuk backend/data, periksa `main` terbaru. Untuk kode map, baca sumber dari Studio yang sedang dibuka. Salinan lokal, commit backend, dan Studio adalah tiga keadaan yang berbeda; jangan menganggap salah satunya otomatis memperbarui yang lain.
3. Pastikan AI sebelumnya sudah berhenti menulis. Hanya satu implementer aktif. Jika tidak mempunyai akses baca ke Studio/GitHub, sebutkan bagian yang belum dapat diperiksa; jangan mengaku memakai versi terbaru.
4. Pertahankan perubahan yang sudah ada. Jangan menimpa Studio dengan ekspor lokal lama. Simpan snapshot/diff seperlunya secara lokal dan catat identitas sumbernya.

## Peran dan batas kerja

Pengecualian khusus 14 Oktober: pemilik mengizinkan Codex memperbaiki R-01 di Studio dan Save biasa tanpa publish. Patch sudah terpasang; Claude menjadi reviewer untuk patch tersebut. Ini tidak mengubah aturan otomatisasi atau memberi izin umum untuk patch Studio lain. Lihat AI_STATE.md.

- Claude mengimplementasikan; Codex melakukan diagnosis dan review independen. Keduanya boleh memperbaiki rancangan berdasarkan bukti. Jangan menyebut patch sendiri telah mendapat review independen.
- Sesi desktop manual dapat membaca Studio untuk membandingkan perubahan. Aturan proyek saat ini melarang Codex mengedit Studio melalui MCP; otomatisasi tetap hanya mengerjakan file lokal. Izin mengedit pada sesi implementer harus mengikuti instruksi pemilik dan aturan yang berlaku pada sesi itu.
- Jangan menyentuh controller/`automation/`, melakukan publish, mengubah DataStore live, membeli aset, atau mengubah pengaturan akun. Release tetap membutuhkan persetujuan pemilik dan uji Studio manual pada versi yang sama.
- Setelah implementasi Studio yang diizinkan, Save biasa dan laporkan apakah Save benar-benar terkonfirmasi. Jangan menyamakan perubahan editor dengan file sudah tersimpan atau game sudah dirilis.

## Tujuan produk

Arahan terbaru 15 Oktober: sepatu, motif, aksesori besar, dan outfit ramai boleh bila komposisi utuh sesuai item/tema/badan. Label tema dan jumlah aksesori bukan bukti mutu. Baca AI_WORKPLAN_2026-10-15.md untuk proposal R-02, pekerjaan komposisi Q-02, bukti uji dan batas biaya Rp0. Jangan menganggap proposal sudah terpasang atau Claude sudah bekerja hanya karena dokumen diperbarui.

Pemain mencentang item yang disukai; sistem menyusun outfit utuh yang mendukung item itu dan cocok pada tubuh pemain. Jangkar yang cocok digabung, yang bertentangan dipisahkan menjadi kelompok yang jelas. Jangkar tetap dipertahankan.

Penilaian mencakup tema, motif/gambar pakaian, warna, siluet, volume, fokus, preferensi gaya yang dipilih pemain, kombinasi 2D/3D, serta bentuk dan bagian tubuh sebenarnya. R6/R15, kotak, tinggi/ramping, badan campuran, headless, Korblox, dan pasangan sepatu/kaki harus masuk kasus uji. Nama item dan skor model adalah bukti terbatas, bukan pengganti pemeriksaan render.

Kualitas hasil utuh menjadi sasaran. Jangan menambah daftar kata, bobot, kuota, atau aksesori semata-mata agar jumlah hasil meningkat. Target pemilik minimal 50 hasil unik untuk input yang didukung; hasil lebih banyak harus dimuat bertahap. Kekurangan kandidat dilaporkan, bukan ditutupi dengan duplikat atau outfit buruk.

## Cara menyelesaikan satu tugas

Kasus gagal yang tersimpan -> telusuri penyebab pada versi aktual -> satu koreksi yang dapat ditinjau -> pemeriksaan relevan -> review independen -> uji visual/manual -> keputusan.

- Catat input item, tubuh/skala/rig, preferensi, anggaran, versi model, dan batas jumlah hasil. Bedakan kasus tetap dengan kasus baru.
- Ukur kandidat masuk/ditolak, alasan penolakan, komponen skor, keluaran unik, dan waktu. Diagnostik harus berbatas dan tidak menjadi pemindaian berat setiap request.
- Bandingkan sebelum/sesudah pada input sama; tampilkan kegagalan juga. Lulus pemeriksaan kode bukan bukti outfit terlihat bagus.
- Jika dua koreksi belum menjawab kasus yang sama, ulangi diagnosis dari trace, jangan terus menebak bobot.
- Jaga alur cari, edit, favorit, apply, beli, pembatalan, cache, validasi server, dan banyak server. Jangan mengumumkan siap rilis jika belum diperiksa.

## Checkpoint dan pergantian

Status: `READY_FOR_CLAUDE -> IMPLEMENTING -> READY_FOR_CODEX -> REVIEWING -> NEEDS_CHANGES / READY_FOR_MANUAL_TEST -> VERIFIED`.

Perbarui [AI_STATE.md](AI_STATE.md) sebelum limit habis: penulis/status, sumber yang dibaca, file/script berubah, alasan, pemeriksaan yang benar-benar dijalankan, bukti hasil, kegagalan, bagian belum diuji, dan satu langkah berikutnya. Simpan laporan panjang terpisah dan tautkan. Jika tidak bisa menulis GitHub, berikan teks checkpoint siap salin kepada pemilik dan nyatakan bahwa checkpoint remote belum diperbarui.

GitHub menyimpan catatan bersama; file ini tidak menjalankan AI, menyinkronkan Studio, atau meneruskan percakapan secara otomatis. Pemilik memulai giliran berikut. Jangan menunggu limit benar-benar habis untuk menyimpan checkpoint.

## Biaya dan kerahasiaan

- Jangan menambahkan API AI berbayar, billing, upgrade, atau overage tanpa instruksi baru pemilik. Inti generate harus dapat berjalan dengan snapshot yang sudah ada dan batas kerja yang terkendali.
- GitHub publik memang diminta pemilik. Jangan mengunggah secret, token, cookie, isi konfigurasi autentikasi Studio, ekspor seluruh workspace, atau data pribadi pemain. URL yang tidak disebarkan bukan pengamanan akses backend.
- Pembatasan map/backend harus diperiksa di server; identitas map kiriman client bukan bukti autentikasi.
- Batas layanan gratis tetap harus diperiksa. Vercel Hobby dibatasi untuk penggunaan personal nonkomersial; jalur komersial berbiaya nol masih perlu dipastikan sebelum monetisasi. Jangan menjanjikan gratis selamanya atau jumlah pemain/penghasilan tertentu.
- Stack saat ini Luau, Python, dan JavaScript/Node.js. Tambah bahasa/layanan hanya jika ada kebutuhan yang dibuktikan dan biaya pemeliharaannya masuk akal.

## Pesan yang cukup dikirim saat berganti AI

> Baca COLLAB.md dan AI_STATE.md dari tautan GitHub panduan bersama ini. Periksa main GitHub dan source Roblox Studio yang terbaru, bukan mengandalkan folder lama. Sebutkan versi yang berhasil dibaca. Lanjutkan tugas aktif sesuai peranmu, catat hasil dan kegagalan, lalu simpan checkpoint sebelum berhenti. Jangan publish.

Jika panduan masih berada pada branch dokumentasi, buka tautan branch yang diberikan pemilik; jangan menganggap file tersebut sudah ada di main.
