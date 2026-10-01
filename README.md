# katalog-embed — sidik jari visual item avatar (Katalog Praktis)

Repo ini menghitung "sidik jari visual" (angka) untuk setiap item di `items.json` memakai model CLIP,
lalu menyimpan hasilnya di folder `out/`. Server Roblox nanti mengunduh `out/embeddings.json` dan `out/tags.json`.

Isi repo hanya ID item katalog publik dan angka. **Jangan pernah menaruh password, token, atau API secret di repo ini** (repo-nya publik).

## Cara pakai (sekali jalan, tidak perlu coding)

### 1. Buat repo
1. Buka https://github.com/new
2. Repository name: `katalog-embed`
3. Pilih **Public** (wajib, supaya Actions gratis). Jangan centang "Add a README".
4. Klik **Create repository**.

### 2. Unggah 3 file
Di halaman repo kosong klik **uploading an existing file** (atau Add file > Upload files), lalu seret:
- `items.json`
- `embed.py`
- `README.md`

Klik **Commit changes**.

### 3. Buat file workflow (satu langkah ini tidak bisa diunggah, harus dibuat manual)
1. Add file > **Create new file**
2. Pada kolom nama ketik persis: `.github/workflows/embed.yml`
   (saat mengetik tanda `/`, GitHub otomatis membuat folder)
3. Buka file `workflow-embed.yml` dari paket ini, salin SEMUA isinya, tempel ke kotak isi.
4. Klik **Commit changes**.

### 4. Izinkan Actions menulis hasil
Settings > Actions > General > bagian **Workflow permissions** > pilih **Read and write permissions** > Save.
(Kalau tab Actions meminta konfirmasi mengaktifkan workflow, klik tombol hijau untuk mengaktifkan.)

### 5. Uji kecil dulu (20 item)
1. Tab **Actions** > klik **Hitung sidik jari visual** di daftar kiri > **Run workflow**
2. Kolom "batas" biarkan `20` > **Run workflow**
3. Tunggu sekitar 5 sampai 10 menit (pertama kali mengunduh model, lebih lama).
4. Buka jalannya (klik namanya) > langkah **Hitung sidik jari visual**. Berhasil bila ada baris `SELESAI: ... item`.
5. Kembali ke halaman utama repo, folder `out/` akan berisi hasil, termasuk `tetangga_contoh.txt`.

**Kalau gagal atau merah:** salin 20 baris terakhir log lalu kirim ke Claude. Jangan mengubah apa pun dulu.

### 6. Jalankan semua item
Kalau uji 20 berhasil: Run workflow lagi, isi "batas" = `0` (semua 1.321 item). Perkiraan 15 sampai 30 menit.

### 7. Kirim ke Claude
Cukup kirim tautan repo (mis. `https://github.com/NAMAMU/katalog-embed`). Tidak perlu kata sandi atau token.

## Keterangan teknis
- Thumbnail diambil dari `https://thumbnails.roblox.com/v1/assets` (terdokumentasi di Roblox Creator Hub).
- Model: `openai/clip-vit-base-patch32` lewat pustaka `transformers`. Lisensi: periksa kartu model di
  https://huggingface.co/openai/clip-vit-base-patch32 sebelum dipakai di luar uji ini.
- Penggunaan GitHub Actions gratis untuk repo publik pada runner standar (dokumentasi GitHub).
- Skrip bisa dilanjutkan: kalau berhenti di tengah, jalankan lagi, item yang sudah dihitung tidak diulang.
- Hasil `embeddings.json`: vektor 32 angka bulat per item (PCA dari embedding yang sudah dinetralkan terhadap jenis slot).
- Hasil `tags.json`: tag gaya dan atribut perkiraan (zero-shot). Ini tebakan model, belum divalidasi dengan penilaianmu.
