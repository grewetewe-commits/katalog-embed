# Giliran Claude — 16 Oktober 2026 (bagian 4): pakaian 2D, badan headless, GUI tanpa script (rev 30)

Penulis: Claude (implementer). Status: **READY_FOR_CODEX**. Tidak publish, tidak mengubah DataStore live/akun/billing, biaya Rp0.
**Save Studio belum terkonfirmasi** (pemilik Ctrl+S). Lanjutan dari [rev 29](AI_CLAUDE_2026-10-16c.md) dan PR #5 (`claude/kartu-item`).

## Arahan pemilik (12:30)

1. Pembacaan item sudah lumayan, **pakaian 2D** masih bermasalah → benerin.
2. **Aman untuk bentuk avatar apa pun.**
3. GUI map dirapikan (sekarang "bikin pusing"), **dibuat di ScreenGui, bukan script**.
4. Perkuat sistem, baru lolos tahap satu, belum dicek Codex → harus benar-benar benar.

## 1. Pakaian 2D (GitHub, PR #5)

### Bukti dulu: label emas
- `uji_mata2d.py` + workflow `uji-mata2d.yml`: sampel acak beku 175 item (60 baju, 60 celana, 55 kaos klasik;
  `uji2d/sampel.json`), thumbnail 420 px, potongan pakaian (manekin, wajah manekin, latar dibuang), lembar kontak.
- **Label emas manual** (`uji2d/emas.json`) dari lembar 420 px: jenis, pola, tema, dan facet baru **fungsi**.
- Temuan penting: **39 dari 55 kaos klasik (TShirt) BUKAN gambar kaos** — 21 shading kulit (perut/otot/tulang selangka),
  12 kalung/rantai dilukis, 6 "pakaian" (rompi/jas dilukis); baju/celana 2D juga ada lapisan kulit (blush, tekstur lengan).
- Varian dibandingkan pada label emas (top-1): zero-shot B/32 150 px (lama), potongan 150, B/32 & FashionCLIP & ViT-L/14
  pada potongan 420, dan **probe** (regresi softmax di atas embedding gambar, dilatih dari NAMA ribuan item lain;
  sampel uji dikeluarkan). Ringkasan (`uji2d/logit.npz`, skrip penilai di laporan):

| facet | lama (gambar) | probe+gambar 150 (murah) | terbaik mahal |
|---|---|---|---|
| baju jenis | 15/57 | 28/57 | 35/57 (probe + ViT-L/14) |
| baju tema | 15/37 | 23/37 | 25/37 (ViT-L/14) |
| celana jenis | 6/43 | 23/43 | 24/43 |
| celana tema | 8/23 | 10/23 | 12/23 |
| pola baju / celana | 21/54, 19/48 | 23/54, 22/48 | 29/54, 28/48 (FashionCLIP 420) |
| kaos fungsi | — | 49/55 (potongan 150) | — |

ViT-L/14 di runner gratis ≈ 1 dtk/gambar (37 rb item 2D ≈ 10 jam) → **tidak dipakai sekarang**; jalur murah tidak
mengunduh gambar baru (embedding sudah ada di cache otak).

### Dipasang: `kartu_item.py` skema 2
- Baju/celana 2D: P(gambar zero-shot) digabung probe nama (rata-rata log; label < 15 contoh = probe netral), lalu fusi
  nama item sendiri 35% seperti sebelumnya. Kata "shirt" tidak dihitung bukti kaos (ada di hampir semua nama aset Shirt).
- Kolom ke-19 **fungsi** untuk kaos klasik: pakaian / badan / aksesori / grafis (zero-shot potongan, kalimat foto produk).
- `LAPORAN_KARTU.md` kini memuat akurasi kartu AKHIR terhadap label emas. Versi kartu 1792132593 (133.329 item).

| facet (kartu akhir, setelah fusi nama) | rev 29 | rev 30 |
|---|---|---|
| baju 2D jenis | 25% | **49%** |
| baju 2D tema | 50% | **65%** |
| celana 2D jenis | 42% | **56%** |
| celana 2D tema | 52% | 52% |
| baju / celana 2D pola | 26% / 47% | 31% / 42% |
| kaos klasik fungsi | — | **87%** |

Batas klaim: n kecil (23–57 per facet), label emas dari satu penilai (Claude); pola tidak membaik konsisten.

### Map (Studio)
- `KartuItemKit`: 19 kolom (kartu skema 1 tetap terbaca), API `FungsiI(id)`, `Kartu(id).fungsi`.
- `IndeksOutfitEngine`: `kaosMenutup(id)` — kaos klasik yang menurut gambar shading/kalung/gambar **tidak dihitung
  penutup atasan** (pakaianLengkap & item pilihan). `DesainerEngine` memakai `api.kaosMenutup` yang sama.
  Uji (R15 Gadis, kaos sebagai item pilihan): shading otot 62/62 kartu punya atasan (47 baju 2D + 15 atasan 3D),
  kalung 34/34, kaos grafis 25/25; kaos "cat suit" (fungsi pakaian) tetap dianggap atasan: 9/45 ditambah baju.
  Sebelumnya semua kaos klasik dianggap atasan → shading/kalung tanpa baju.

## 2. Badan: headless aman

Matriks uji (generate lewat remote, Play Studio): avatar sendiri (headless + rambut + 2 topi), R15 Gadis, R6 Boy,
racikan Korblox + headless; kasus: tanpa item, jaket 3D, gaun 3D, baju 2D.

- **Bug**: badan headless → 120/120 kartu tanpa rambut, topi, **kalung/leher**, wajah (`VisualOutfitKit.Rapikan` membuang
  slot 1/2/3/4/18/19, `V.Nilai` menghukum +30, `DesainerEngine` tidak menyiapkan slot 1/3/4 & menganggap rambut sudah ada).
- **Perbaikan**: `V.KepalaTersembunyi(t, body)` — wajah/alis/bulu mata selalu disembunyikan; rambut & topi hanya bila
  pemain sendiri tidak memakai rambut/topi (headless murni); leher selalu boleh. `KatalogServerEngine` menyalin profil
  headless + `rambutSendiri/topiSendiri` dari karakter (salinan, cache badan racikan tidak tercemar).
- Hasil: headless + rambut → rambut 120/120, topi 89, leher 79, wajah 0. Headless murni (rambut/topi dilepas sementara)
  → rambut 0, topi 0, leher 108, semua kartu ≥ 1 aksesori. Korblox + headless: 120 kartu, 0 pakaian 3D bawah.
  Jaket/gaun 3D pada badan tak terverifikasi tetap diminta pilih badan (packet BodyChoice) — perilaku lama, benar.
- Catatan: kasus baju 2D sebagai item pilihan menghasilkan lebih sedikit kartu (20–47) di semua badan — bukan masalah
  badan, perlu ditelusuri terpisah.

## 3. GUI (Studio, ScreenGui — tanpa UI dari script)

Cadangan sebelum edit: `ServerStorage.Cadangan_GUI_20261016` (semua ScreenGui, modul & LocalScript lama, nonaktif).
- 48 tombol/label: kurung `[CARI]` dan huruf miring SourceSans dibuang → BuilderSans Bold, ukuran dicek muat (TextBounds).
  Judul langkah "1 · PILIH ITEM". Tombol tutup panel/profil: kotak 34 px di dalam header (dulu wajik merah menonjol).
  Notif tidak lagi menimpa navigasi (IgnoreGuiInset false). Panel buram 0.04 → 0.
- **Semua UI yang dulu dibuat script kini ada di Studio** (pemindai: tidak ada `Instance.new` kelas UI tersisa):
  `Template.AssetStatus` (clone), 3× `HalamanBerikut`, `BadanPanel.PeriksaBentuk3D`, `Panel.PortraitScrollHint`,
  `Template.GridNav/GridTabs`, `Panel.Halaman` kini ScrollingFrame di Studio, ScreenGui **`BodyChoiceDialog`** baru
  (dulu seluruh dialog dibuat `BodyChoiceUI` saat runtime; modul kini hanya mengisi & clone `Template.KartuBadan`),
  `StarterGui._WadahTema` (wadah kiriman tema). Script yang menunggu elemen memberi `warn` bila elemen hilang.
- Teks kartu "Pakaian dan aksesori disusun menjadi satu outfit" (sama di semua kartu) → isi nyata:
  "Disusun: atasan, bawahan, rambut, topi, leher" / "1 item pilihan + kemeja 3D, rambut, topi, punggung".
- Diuji Play: desktop, simulasi HP lanskap (skala 0,79) & potret (grid tab dari Template), tombol halaman berikut (1 tombol,
  muncul), dialog BodyChoice (paket uji), konsol klien & server tanpa galat proyek.

## Checksum Studio (panjang/h, h = (h*31+byte) mod 2147483647) — semua lolos loadstring

IndeksOutfitEngine 162547/1989230662 · DesainerEngine 65063/215226216 · KartuItemKit 6610/289532197 ·
VisualOutfitKit 29768/2077036755 · KatalogServerEngine 238120/1886231485 · KatalogUIController 152749/942582511 ·
ResponsiveCatalogKit 11870/2094024998 · BodyChoiceUI 6224/122706689. Tidak berubah: StylistEngine 38605/673756166,
MutuKit 18466/2113704761.

## Untuk Codex (review)

1. PR #5: `kartu_item.py` (probe, fungsi, nilai_emas), `uji_mata2d.py`, `uji2d/emas.json` — audit label emas independen
   (lihat `uji2d/lembar_*.png`), terutama tema & fungsi.
2. Kebijakan headless (`V.KepalaTersembunyi`, `rambutSendiri/topiSendiri`) — apakah sesuai maksud rev Codex sebelumnya.
3. `kaosMenutup`: kaos fungsi "grafis" tidak dihitung atasan (gambar di dada butuh baju). Setuju?
4. GUI: struktur baru `BodyChoiceDialog`, `Halaman` ScrollingFrame, tombol `HalamanBerikut` di Studio.

Belum: pola 2D (FashionCLIP 420 butuh unduh ±37 rb gambar bertahap), deteksi lapisan kulit pada baju/celana 2D
(butuh cakupan piksel dari otak.py), badan Rthro/mini belum diuji, render visual banding sebelum/sesudah belum dibuat.
Setelah PR #5 digabung: `KartuItemKit.CABANG = "main"`.
