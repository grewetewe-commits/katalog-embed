# Giliran Claude — 16 Oktober 2026 (bagian 3): Kartu Item, map membaca item dari GAMBAR (rev 29)

Penulis: Claude (implementer). Status: **READY_FOR_CODEX**. Tidak publish, tidak mengubah DataStore live/akun/billing, biaya Rp0.
**Save Studio belum terkonfirmasi** (pemilik Ctrl+S). Rancangan: `RANCANGAN_KARTU_ITEM.md` di PR #5 (branch `claude/kartu-item`).

## Arahan pemilik

Sistem harus tahu item itu APA (jenis, bentuk, tema, gambar utama) untuk semua item — bukan dari nama. Kasus uji:
`126884250250747` Duck-o-Lantern (topi labu Halloween berwajah bebek). Kasus ini contoh, bukan target tunggal.
Sepatu otomatis tidak cocok → dimatikan; fokus outfit + kecocokan item + badan.

## Bukti masalah (Studio, sebelum)

Duck-o-Lantern, 24 kartu teratas COWO/CEWE: "Duck!!", "Duck Shirt :D", "Pajamas Boy Duck pjs", "Yellow Duck Pants",
"Duck Floaty", "Chick Backpack"; Ringkasan gaya kosong. Nama tanpa "pumpkin/halloween" → kunci tema Halloween mati.

## GitHub (PR #5, belum digabung)

- `kartu_item.py`: zero-shot CLIP ViT-B/32 dari embedding thumbnail yang SUDAH ada di cache otak (132.196 item, 41 dtk di
  Actions). Kartu: kelompok, jenis (per kelompok), tema 2 teratas (39 label), subjek gambar utama 2 teratas (37), pola (16),
  bentuk (lengan/panjang/fit/depan), tema menurut gambar saja. Baju/celana 2D memakai kalimat "manekin kotak" (tanpa itu
  9/36 baju 2D terbaca zirah). Alfa koreksi bias kalimat dipilih per facet dari data. Nama = fusi lunak 35%.
- `lembar_kartu.py`: lembar kontak (thumbnail + kartu), 36 sampel acak per kelompok + item uji → diperiksa mata.
- `embed.yml`: langkah kartu setelah otak (`continue-on-error`), ikut commit & purge CDN. `kartu-uji.yml`: uji di branch.
- Probe endpoint 3D resmi (`/v1/assets-thumbnail-3d`, Beta): anonim 403 "Invalid authentication", API key repo 403
  **"Scope not authorized"**. Data bentuk 3D asli menunggu izin pemilik; tidak memakai cookie akun.

Hasil pemeriksaan mata (lembar kontak): topi/aksesori/wajah/3D umumnya benar (topi koboi, baret loreng→militer, topi
penyihir, helm→ksatria, tanduk→iblis, sayap, tas, senjata, syal). Baju/celana 2D paling lemah (thumbnail 150 px di
manekin): jenis sering salah, tema item polos berderau. Angka kecocokan gambar-vs-nama ada di `LAPORAN_KARTU.md`
(batas bawah kasar karena nama Roblox menyesatkan).

## Studio (rev 29)

| Script | Perubahan |
|---|---|
| KartuItemKit (BARU, ModuleScript) | unduh `kartu/info.json` + shard (raw; CDN bila cabang main), cek versi, ulang tiap 3 jam, semua HTTP pcall, buffer u8 18 kolom. API `TemaI/SubjekI/TemaGambarI/Kartu/NamaTema/IdxTema`. `CABANG = "claude/kartu-item"` sampai PR #5 digabung. |
| IndeksOutfitEngine | `jenisItem`: Halloween dari gambar (tema ≥ 70, gambar setuju, subjek labu/hantu/kelelawar/laba-laba) → kunci tema Halloween yang sudah ada. Natal tetap dari nama (gambar sering keliru: bendera merah-hijau, stroberi). `siapkanGayaJangkar`: tema & subjek utama/sampingan item pilihan dari kartu; gaya dari gambar bila nama tidak menyebut; bila nama & gambar bertentangan, gambar dipakai hanya ≥ 85. Rangkai: pelengkap setema kartu +8 (maks 16), subjek = subjek sampingan item pilihan & tema lain −10 (maks 20). Hook mutu `buktiTema`: maks(nama, kartu). Pesan: "Dibaca dari gambar item: tema Halloween (labu)". Init KartuItemKit, `api.kartu`. Diag `kartuSetema/kartuGema`. |
| DesainerEngine | `indeksKartu` (per kunci kolam & tema, sekali per versi); kandidat setema dari kartu disuntik ke kolam (maks clamp(nAmbil/2,12,48)); koreksi +1,5 setema, −2,5 gema subjek sampingan. Sepatu otomatis mati (`D.SEPATU_OTOMATIS = false`). |

Checksum (panjang/h): KartuItemKit 6173/2034636827 · IndeksOutfitEngine 161989/1017014915 · DesainerEngine 64654/154649419 ·
StylistEngine 38605/673756166 · MutuKit 18466/2113704761 · VisualOutfitKit 27998/59119410. Semua lolos loadstring.

## Hasil (Play Studio; otak berganti 1792086980 → 1792102571 di tengah sesi)

Duck-o-Lantern sesudah: 120 kartu, Ringkasan "Horor", pesan "Item bertema Halloween…; Dibaca dari gambar item: tema
Halloween (labu)". 24 teratas: kemeja "Halloween", celana plaid Halloween, kalung labu, Jack-O-Lantern. Koherensi tema
menurut kartu: COWO 63/84 (75%), CEWE 75/77 (97%); item bebek bertema lain 3 (COWO), 0 (CEWE).

Koherensi tema-kartu 24 kartu teratas (rev 28 → rev 29): jersey 2→26%, koboi 18→32%, sayap malaikat 42→53%, jas 42→62%,
pita coquette 67→94%, topi bajak laut 6→23%, maid 42→47%, Gojo 33→17% lalu diperbaiki (subjek sampingan derau tidak dipakai): 12 teratas berisi 6 kartu
bertema JJK (Megumi, Itadori, Miwa, plush/kacamata Gojo), sisanya streetwear biru; 58 kartu. Pastel goth 59→58%.

Jumlah kartu: koboi 48→120, jas 52→72, kawaii cat ears 97→112, bajak laut 120→113, Gojo 54→68.
Skenario beku (alat beku): S10 pedang 58→120 (skor median 58,5→75), S11 jaket kulit 26→41, S12 skor 66→79,5,
S1/S2/S3/S8 skor median naik 2–7 poin; atasan sama maks 2× semua; nama gender lawan hanya celana unisex "girl boy"
(S2 2, S6 3, S8 2). S9 3D-lengkap 62%→40% (masih 50/50 kartu, ≥85: 43/50).
Waktu hangat: Duck 2,2 dtk, S2 4,6 dtk, S6 4,1–4,4 dtk; panggilan pertama setelah kartu dimuat lebih lambat (cache jenisItem
dibangun ulang). Konsol: tanpa galat skrip proyek.

## Belum / batas klaim

- Belum render visual outfit; koherensi diukur dengan kartu yang sama (bukan penilai independen).
- Baju/celana 2D: fase 2 (thumbnail 420 px, model lebih kuat) setelah label emas manual dari lembar kontak.
- Bentuk 3D asli: perlu izin API key (pemilik). Ukuran mesh di map (UkuranItemEngine) belum dihubungkan ke kartu.
- Kartu di Studio dibaca dari branch PR; bila PR digabung, ganti `CABANG` ke "main".

## Untuk Codex

Review PR #5 (`kartu_item.py`, `lembar_kartu.py`, workflow) dan patch Studio rev 29 (KartuItemKit, ambang kartuMusim,
aturan gambar-vs-nama, gema subjek). Usulan: audit label emas independen dari `kartu/lembar/*.png`.
