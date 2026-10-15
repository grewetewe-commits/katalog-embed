# Giliran Claude — 16 Oktober 2026 (bagian 2): "sistem tidak tahu itemnya apa"

Penulis: Claude (implementer). Status akhir: **READY_FOR_CODEX**. Tidak publish, tidak mengubah DataStore live/akun/billing, biaya Rp0.
**Save Studio belum terkonfirmasi** (Claude tidak punya alat Save; pemilik perlu Ctrl+S dan melihat "Saved new changes" di Output).

Keluhan pemilik: saat pemain memilih item, sistem tidak memahami item itu apa dan cocok dengan tema apa. Audit tema (13 item uji,
alat beku `ukur_rev24.py` + skrip tema terpisah) menemukan akar masalah, bukan sekadar kosakata.

## Akar masalah yang ditemukan (dengan bukti)

1. **Kategori gaya terlalu kasar.** Topi koboi hanya terbaca "vintage" (sama dengan plaid/retro), topi bajak laut "fantasi". Penata tidak punya
   konsep tema spesifik.
2. **Item setema tidak pernah masuk kolam kandidat.** `DesainerEngine.siapkan` mengambil kolam dari skor vektor (`kolamTeratas`); koreksi tema
   hanya mengurutkan ulang item yang kebetulan sudah masuk. Uji topi koboi: 0 kemeja/celana/sabuk western di kolam, padahal otak punya
   ±10 kemeja, 14 celana, 9 sabuk western.
3. **Gerbang mutu menolak susunan setema untuk tema langka.** Diag baru: susunan berisi pelengkap semotif yang lolos — koboi 7/71,
   Gojo 8/126, bajak laut 28/107 (malaikat, tema umum: 150/217). Otak belajar dari outfit populer; item tema langka hampir tak punya pasangan
   di data, jadi kecocokannya selalu rendah. Nilai yang gugur tersebar 0–49 (batas 50).
4. **Baju gaun 2D dipasangkan celana acak.** "Maid Dress" (baju) + celana "Jester"/"evade"/jas kantor: rok gaun ada di template celana
   pasangannya, jadi roknya hilang. Aturan "tiap kartu wajib pasangan atasan:bawahan baru" membuat celana pasangan hanya bisa dipakai 1x.
5. **Dorongan tema kategori rev 27 (temaJ) menurunkan jumlah kartu** (kolam condong ke item setema yang dinilai otak kurang serasi):
   koboi 64 → 40, jaket kulit 35 → 27.
6. Temuan kecil: topi yang diunggah sebagai aksesori wajah ("Fedora" tipe Face di bawah topi koboi = dua topi); "Knife In Torso" untuk
   telinga kucing kawaii; trisula/flintlock tidak terbaca senjata; jas + celana pendek ("Premium Black Suit" + "Long Boys Black Shorts");
   setelan jas abu 3 potong + jeans robek; fandom lain ikut (Gojo + rambut Gorillaz/Sans); "Sung Jin Woo" lolos saringan fandom.

## Perubahan (rev 28) — script Studio

| Script | Perubahan |
|---|---|
| StylistEngine (Revision 8) | `M.MOTIF` 50 motif spesifik (western, bajak laut, maid, ksatria, vampir, penyihir, malaikat, peri, iblis, militer, seragam sekolah, polisi, medis, ninja, samurai, busana Jepang/Tionghoa/Nusantara, jas formal, badut, kerajaan, tokoh anime per karakter dengan kata waralaba sebagai bobot setengah). `M.MotifJangkar(ids)`, `M.MotifBukti(setJangkar, pelengkap)`. Field `setelanFormal/jasFormal/namaBawah/celanaPendek`. `PelengkapTema`: setelan jas pilihan menolak bawahan otomatis yang jelas bertabrakan (shorts, joggers, sweatpants, cargo, ripped, baggy, sport); jeans polos tetap boleh. `Kesatuan`: tolak jas/blazer/tuxedo + celana pendek. |
| IndeksOutfitEngine | `siapkanGayaJangkar` mengisi `g.motif`; `op.motif` ke desainer; rangkai +8 per pelengkap otomatis semotif (maks +16); pesan "Tema item terbaca: …, pelengkap setema dicarikan". Motif langka (df kata ≤ 300) atau item pilihan pakaian inti: susunan ×1,6. **Pasangan gaun 2D**: baju/celana bernama dress/gown/gaun tanpa pasangannya → bagian set (kreator sama, satu set, nama paling mirip, bisa dibeli) ditambah sebagai item pilihan pendamping (`pendamping`), satu kelompok dengan jangkarnya, pesan "Celana pasangan gaun ikut dipasang…". `lolosPenata`: aksesori wajah bernama topi ditolak. Hook `OG.Mutu.buktiTema`. Diag baru: `nilaiGugur`, `nilaiLolos`, `motifCalon`, `motifJadi`, `motifGugur`. |
| DesainerEngine | Item kata-motif kuat dicari lewat indeks kata kolam (`K.pk`), maks clamp(nAmbil/2, 12, 48) per kunci, lewat saringan & aturan buang yang sama; pelengkap semotif +2 (kata waralaba +1); fandom lain −2 saat ada motif. Dorongan tema kategori rev 27 kini **berselang**: susunan ganjil memakai dorongan, genap netral (`x.tb`, batas pemangkasan disesuaikan `tbMaks`). Senjata/props: knife, knives, greatsword, longsword, machete, cleaver, trident, halberd, lance, flintlock(s), revolver(s), shotgun, musket, crossbow. Fandom: "jin"+"woo". `prof.motif`, `prof.motifDesain`. |
| MutuKit | `K.buktiTema` (hook). Bukti tema dari nama: +6 per pelengkap semotif, maks +12, sebelum batas 74/50. Gerbang data, item terburuk, gender, pasangan inti tidak berubah. |
| VisualOutfitKit | Gaun 2D + bawahan 3D otomatis (tipe 11/14/17) → penalti 14 (`gaunDitumpuk`). |

Tidak berubah: KatalogServerEngine, RankingOutfitKit, OtakGayaEngine, ShoePairKit.

Checksum (panjang/h·31+byte mod 2147483647), semua lolos `loadstring`:
StylistEngine 38605/673756166 · DesainerEngine 61979/1444705134 · IndeksOutfitEngine 154735/1491235189 · MutuKit 18466/2113704761 ·
VisualOutfitKit 27998/59119410 · KatalogServerEngine 237551/2080507141 · RankingOutfitKit 2097/415832698 · OtakGayaEngine 22000/994216217 ·
ShoePairKit 10769/764913020. Tidak ada flag uji tersisa (`UJI_X`, `_susunUlang`), objek `_Uji*` 0.

## Hasil ukur (Play Studio, 1 pemain, 120 kartu diminta, 24 kartu teratas untuk "setema")

Catatan penting: **otak berganti versi di tengah sesi** (1791739772 → 1792086980, FITB 0,80 → 0,81, kalibrasi peringkat ikut berubah). Kolom
"sebelum" diukur dengan otak lama; sebagian perubahan jumlah kartu berasal dari otak baru, bukan kode.

| Uji | sebelum (n, setema/24) | rev 27 (n, setema/24) | rev 28 (n, setema/24, skor) |
|---|---|---|---|
| T01 pastel goth (CEWE) | 120, 23 | 120, 24 | 120, 21, 77 |
| T02 telinga kucing kawaii | 86, 9 | 98, 22 | 97, 16, 77 |
| T03 jersey | 72, 24 | 70, 24 | 68, 24, 64 |
| T04 topi koboi | 36, 2 | 32, 4 | **48, 10**, 61 |
| T05 sayap malaikat | 120, 13 | 120, 20 | 120, 17, 96 |
| T06 tindik berdarah | 41, 10 | 40, 17 | 30, 15, 64 |
| T07 jas abu | 34, 24 | 38, 24 | **52**, 24, 73 |
| T09 pita coquette | 120, 14 | 120, 24 | 120, 24, 98 |
| T10 celana grunge | 120, 23 | 120, 24 | 120, 23, 78 |
| T11 wajah Gojo | 32, 4 | 20, 4 | **54, 9**, 68 (8 teratas semua bertema Gojo) |
| T12 topi bajak laut | 109, 2 | 91, 7 | 120, 8, 78 |
| T13 maid dress | 120, 3 | 66, 22 | **120, 24, 85**; celana bukan pasangan di 24 teratas 10 → 0 |

T08 (jaket 3D, AssetType 67) tidak terukur: server meminta pemain memilih bentuk badan dari preview (fitur BodyChoiceKit, 15 dtk) — perilaku
yang dirancang, bukan galat; perlu diuji dari klien.

Skenario beku S1–S12 (alat beku, 50 kartu pertama): atasan sama maks 2× semua, `AtasanUlang` 0, nama gender lawan hanya celana unisex
"girl boy" (S2 2, S6 4, S8 1 — sama seperti sebelumnya), tumpuk sekeluarga ≤ 1. Jumlah kartu: S1–S3/S6/S8/S9/S12 120, S7 (budget 50) 62,
S10 pedang 58 (r27b 120, otak lama), **S11 jaket kulit 26** (r27b 65). Uji pembanding tanpa dorongan tema kategori: S10 52, S11 35 → penurunan
S10 dari otak baru, S11 dari otak baru + dorongan tema. Waktu (hangat): T03 1,8–2,2 dtk, T04 3,6–3,9 dtk; dingin 3,7–6,3 dtk. S1–S12 2,7–7,2 dtk
(sama dengan r27b).

Konsol: hanya peringatan CorePackages UIBlox milik Roblox; tidak ada galat skrip proyek.

## Dicoba lalu dibatalkan (tidak terpasang)

- Syarat "bawahan formal" penuh untuk setelan jas: T07 30 → 8 kartu (nama celana Roblox jarang menyebut jenisnya). Diganti daftar tolak.
- Satu putaran ulang `cari` bila kandidat lolos < 40: T06 30 → 65 kartu tetapi 9 dtk; S11 tidak terpicu. Dibatalkan karena waktu.
- Motif "berdarah": menarik topi perawat berdarah untuk anak laki-laki. Dihapus.

## Batas klaim / belum diuji

- Belum ada render visual; angka di atas struktur & nama, bukan keindahan.
- Bukti tema dari NAMA bisa salah untuk nama menyesatkan; dibatasi maks +12 dan hanya kata motif kuat yang mencari item.
- Jumlah kartu < 50 masih terjadi untuk item yang jarang dipadukan otak (S11 26, T06 30, T04 48). Gerbang mutu sengaja tidak dilonggarkan.
- Pasangan gaun hanya dicari di kolam otak (bukan seluruh katalog); gaun yang pasangannya tidak ada di otak tetap memakai celana lain
  (dengan penalti visual `gaunTanpaPasangan`).

## Temuan terbuka

- D-02 `batasSeimbang` (dari giliran sebelumnya) masih terbuka.
- S10/S11 turun bersama otak 1792086980: perlu keputusan apakah batas skor 50 dikalibrasi ulang per versi otak (Codex/pemilik).
- BodyChoiceKit Offer 15 dtk untuk jaket 3D (T08) — perlu diprofil.
- Item tanpa nama di meta (kartu menampilkan nama kosong) masih muncul di beberapa kartu.

## Langkah berikutnya

Codex: review rev 28 (terutama `lengkapiGaun` + `pendamping` di `grupJangkar`, hook `MutuKit.buktiTema`, dorongan tema berselang), lalu
putuskan kebijakan jumlah minimum vs gerbang mutu untuk item yang jarang dipadukan. Pemilik: Ctrl+S, lalu coba sendiri topi koboi,
Maid Dress, Gojo.
