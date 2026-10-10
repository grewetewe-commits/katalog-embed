# API privat Katalog Praktis

Root Directory proyek Vercel: `services/catalog-api`. Framework preset: Other. Runtime Node 22. Tidak memerlukan database atau API model berbayar.

`outputDirectory` dibatasi ke `public`, yang hanya berisi `robots.txt`. Source `lib` dan `test` tidak boleh muncul dalam Static Assets deployment. File robots hanya meminta mesin pencari tidak mengindeks; perlindungan data tetap dilakukan oleh API secret.

Pertahankan environment `API_SECRET` yang sudah dipakai server Roblox. Nilainya minimal 16 karakter, tidak disimpan dalam Git. Semua endpoint memerlukan POST JSON dengan header `x-api-secret`; tanpa secret ditolak 401. Environment yang belum siap ditolak 503. Validasi ini kompatibel dengan panjang secret aktif yang sudah diperiksa, tanpa mengganti kredensial pemilik.

Endpoint:

- `/api/catalog`: `action: search`, `keyword`, `cursor`, `limit`, `category`, `sortType`, `minPrice`, `maxPrice`. Mengembalikan item resmi dan cursor, tidak membatasi ukuran total Marketplace.
- `/api/catalog`: `action: bundle`, `bundleId`, atau `action: assetBundles`, `assetId`, untuk bundle resmi dan pasangan sepatu.
- `/api/inspect`: `assetId`; inspeksi PNG dan metadata ekonomi publik. Warna sedikit ditandai sebagai bukti terbatas.

Cache dan single-flight di sini hanya per instance fungsi. Data permanen dan cache lintas server tetap dikelola Roblox DataStore. Autentikasi tidak digantikan oleh cache CDN dan tidak ada CORS untuk klien web umum.

Jalankan `npm ci`, `npm run check`, dan `npm test` sebelum deploy. Sambungkan repositori pada pengaturan Git Vercel; `vercel.json` sendiri tidak menyambungkan akun. Deploy preview dan periksa 401 tanpa secret serta respons resmi dengan secret sebelum memakai deployment produksi.

Layanan mempunyai deadline 11 detik dan durasi fungsi 15 detik, batas payload, allowlist tujuan, retry terbatas dengan jitter, penanganan 429/Retry-After, dan respons JSON saat layanan luar gagal. Tidak ada jaminan layanan Roblox atau Vercel selalu tersedia. Jalur katalog native di map tetap digunakan ketika Vercel tidak tersedia atau kuota gratis habis.

Vercel Hobby gratis tanpa siklus tagihan, tetapi memiliki kuota dan hanya mengizinkan penggunaan pribadi/nonkomersial. Untuk map yang dimonetisasi, jalur runtime tetap native Roblox dan layanan ini harus dinonaktifkan; jangan mengaktifkan Pro, trial, add-on, atau pemakaian berbayar untuk mencapai mode Rp0. Ketentuan: https://vercel.com/docs/plans/hobby dan https://vercel.com/docs/limits/fair-use-guidelines.
