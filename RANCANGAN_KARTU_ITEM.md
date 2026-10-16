# Rancangan Kartu Item — map "tahu itemnya apa" (16 Okt 2026)

Penulis: Claude (implementer). Untuk direview Codex dan pemilik. Biaya Rp0 (GitHub Actions publik + CLIP lokal).

## Masalah (bukti)

Generate sudah pintar menyusun dan menilai, tetapi **tidak tahu item itu apa**. Data item yang dipakai map: tipe aset,
nama, warna dominan, dan vektor kecocokan 32 angka. Tema dibaca dari **nama**.

Kasus uji pemilik `126884250250747` **Duck-o-Lantern** (topi labu Halloween berwajah bebek, kreator Roblox). Nama tanpa kata
"pumpkin/halloween", jadi kunci tema Halloween tidak menyala; kata "duck" dan vektor menarik item bebek. Hasil Studio
16 Okt sebelum perubahan (24 kartu teratas COWO/CEWE): "Duck!!", "Duck Shirt :D", "Pajamas Boy Duck pjs", "Yellow Duck Pants",
"Duck Floaty", "Chick Backpack"; Ringkasan gaya kosong; tidak satu pun bernuansa Halloween.

Kasus ini dipakai sebagai **contoh**, bukan target tunggal: aturan tidak boleh menyebut bebek/labu. Lulus hanya bila
semua kelompok item (baju/celana 2D, atasan/bawahan 3D, topi, aksesori wajah, rambut, aksen) terbaca layak pada sampel acak.

## Sumber kebenaran (urut kekuatan)

| Sumber | Untuk | Status |
|---|---|---|
| Gambar item (thumbnail resmi, sudah di-embed CLIP oleh otak.py, 132 rb item) | semua kelompok | dipakai (fase 1) |
| Potongan pakaian 2D tanpa manekin (emb2d otak.py, 40 rb item) | jenis/pola baju & celana 2D | dipakai (fase 1) |
| Data 3D resmi `thumbnails.roblox.com/v1/assets-thumbnail-3d` (Beta) | bentuk & ukuran nyata, tampak multi-sudut | **terblokir**: API key repo ditolak "Scope not authorized" (probe 16 Okt). Perlu izin dari pemilik di Creator Dashboard; tidak memakai cookie akun. |
| Ukuran mesh di map (UkuranItemEngine/BodyContextKit) | ukuran pada badan | sudah ada di map, akan dihubungkan |
| Nama + kreator | bukti lemah (fusi 35%), nama tokoh/merek | dipakai |
| Tipe aset Roblox | kelompok slot | dipakai |

## Kartu (keluaran GitHub, `kartu/`)

`kartu/info.json` (versi, label, kalibrasi) + `kartu/kartu_{0..7}.json` (shard = id % 8, sama dengan `model/`). Baris per item:
`[kelompok, jenis, p, tema1, p, tema2, p, subjek1, p, subjek2, p, pola, p, lengan, panjang, fit, depan, temaGambar]`, p 0–100.

- **jenis**: per kelompok (atas 17, bawah 12, kepala 13, wajah 8, aksen 11 label).
- **tema**: 39 label (biasa, streetwear, sporty, formal, gaun_elegan, sekolah, militer, polisi, medis, koboi, bajak_laut,
  ksatria, kerajaan, maid, gothic, punk, kawaii, coquette, y2k, cyber, penyihir, peri, malaikat, iblis, vampir, halloween,
  horor, natal, pantai, musim_dingin, anime, kostum_hewan, novelty, tradisional, ninja, badut, superhero, antariksa, steampunk).
- **subjek**: 37 label gambar utama (labu, tengkorak, bebek, kucing, hati, bintang, api, tulisan, logo, …) — 2 teratas,
  supaya "labu 65 / bebek 35" terbaca sebagai labu yang berwajah bebek, bukan bebek.
- **pola**: 16 label; **bentuk**: lengan, panjang, longgar/ketat, jaket terbuka/tertutup (atas & bawah).
- Label hanya ditambah di akhir; mengubah urutan = naikkan `skema`.

Metode: zero-shot CLIP (model sama dengan otak.py) dengan ensemble kalimat per label, koreksi bias kalimat per kelompok
(alfa dipilih otomatis per facet dari data), fusi nama lunak. Hasil pertama Duck-o-Lantern: **tema halloween 100,
subjek labu 65 / bebek 35** (gambar saja juga halloween).

## Pemeriksaan mutu (bukan hanya angka)

1. Kecocokan gambar-vs-nama otomatis di tiap putaran (laporan `LAPORAN_KARTU.md`): batas bawah kasar, karena nama Roblox sering
   menyesatkan.
2. **Lembar kontak** `kartu/lembar/*.png`: thumbnail + kartu, 36 sampel acak per kelompok (seed tetap) + item uji. Diperiksa
   mata (pemilik/Codex/Claude) dan dijadikan **label emas** manual → akurasi sebenarnya per facet.
3. Pembanding model (fase 2, hanya bila label emas menunjukkan perlu): thumbnail 420 px vs 150 px, CLIP ViT-L/14,
   FashionCLIP. Dipilih yang terbaik pada label emas, tetap gratis di Actions (dicicil per putaran).

Penerimaan fase 1: item uji (Duck-o-Lantern + 13 item tema + 5 item skenario) terbaca benar; label emas tema ≥ 75% benar
untuk kelompok kepala/aksen/wajah dan ≥ 60% untuk baju/celana 2D (dilaporkan apa adanya bila belum tercapai).

## Pemakaian di map (Studio)

- `KartuItemKit` (ModuleScript baru, server): unduh kartu seperti shard otak (raw/CDN, cek versi, TTL 3 jam, semua HTTP pcall),
  simpan ringkas di buffer.
- **Memahami item pilihan**: tema & subjek utama dari kartu (gambar). Nama tinggal cadangan. Tema musiman (halloween, natal)
  dari kartu ikut menyalakan kunci tema yang sudah ada.
- **Kata nama tidak boleh menarik subjek sampingan**: kata nama item pilihan yang menunjuk subjek kedua (bukan utama) di
  gambar tidak dipakai sebagai tanda set/kemiripan.
- **Kandidat setema dari kartu**: item yang kartunya setema dimasukkan ke kolam kandidat (bukan hanya dari nama); tema
  bertentangan diturunkan; bukti tema di gerbang mutu memakai kartu.
- **Struktur pakaian dari jenis kartu**: gaun 2D, kostum penuh, jaket terbuka (butuh dalaman), crop — dari gambar, nama cadangan.
- Sepatu otomatis dimatikan (arahan pemilik 16 Okt); sepatu hanya dari pilihan pemain/outfit nyata.

## Data & DataStore

Tidak ada perubahan DataStore live pada fase ini. Pengumpulan ulang data item (usulan pemilik) diputuskan setelah kartu
terbukti; kartu dihitung dari embedding yang sudah ada sehingga tidak perlu panen ulang.

## Pembagian kerja

Claude: implementasi GitHub (`kartu_item.py`, `lembar_kartu.py`, workflow uji di branch `claude/kartu-item`) dan Studio.
Codex: review rancangan & kode, audit label emas independen dari lembar kontak, uji visual di Studio.
Penggabungan ke `main` (langkah kartu di workflow otak, `continue-on-error`) setelah review.
