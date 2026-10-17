# Claude — rev 33 (17 Okt 2026): padanan 3D, judul gaya item pilihan, motif diukur dari piksel

Permintaan pemilik (17 Okt 06:12): rapikan GitHub; kekurangan celana/pakaian 3D langsung dibenahi (Codex = cek terakhir);
generator terasa "bimbang"; pengecekan item harus benar-benar akurat; gender diperkuat (perut, bahu, motif); motif detail.

## 1. Pakaian 3D untuk badan yang tidak cocok 2D (akar masalah "celana")
- Temuan: `jadikan3D`/`padanan3D`/`odLayerCukup` di IndeksOutfitEngine **tidak pernah dipanggil** (kode mati). Badan yang
  oleh BodyContextKit dinilai `upper_2d_unfit`/`lower_2d_unfit` membuat outfit referensi ber-baju/celana 2D langsung gugur
  di cek badan → hasil sedikit, celana 3D jarang.
- Perbaikan (IndeksOutfitEngine, cari `rev 33: PADANAN 3D`): `calonPadanan3D` (8 calon per item klasik+slot+gender, cache
  maks 20 rb), `pilihPadanan3D` (lolos cek badan, bergiliran antar outfit), `ganti2DKe3D` (atasan 10/13; bawahan 11/14,
  rok 17/14/11 bila nama rok, 14/11 bila kartu bilang pendek). Dipanggil di rangkai (cari `rev 33: badan yang tidak cocok`).
  Item pilihan pemain tidak pernah diganti.
- BodyContextKit (cari `rev 33: hanya bila zona itu BISA`): 2D-unfit hanya untuk R15 dengan sangkar di zona itu dan bawahan
  bukan Korblox (dulu avatar R6/tanpa sangkar bisa kehilangan 2D & 3D sekaligus).
- Uji Play (avatar pemilik diganti sementara ke badan "Gaya Anime 2", 95–97% pemakaian manusia 3D): tanpa item 108 outfit,
  atasan 3D 103/108, `padanan3D` 219; celana grunge 120 outfit, atasan 3D 120/120. Badan pemilik asli (torso Woman, 90%
  manusia memakai 2D): 2D tetap dipakai, celana 3D 40–49% dari desainer. Avatar dikembalikan.

## 2. "Bimbang"
- Diukur (Play, avatar pemilik): Goth Pastel → 120/120 kawaii; Jersey → 101/101 sporty; celana grunge → y2k/grunge 113/120;
  pita kawaii → coquette/kawaii/y2k. Pengecualian: **Maid** terbaca Coquette, isinya setema (topi maid, ekor kucing maid),
  tapi 120/120 kartu berjudul "Kasual" (klasifikasi kata nama outfit tidak mengenali maid).
- Perbaikan (IndeksOutfitEngine, cari `rev 33: outfit di sekitar item pilihan`): bila isi akhir hanya "kasual" dan item
  pilihan punya gaya terbukti, judul/gaya kartu = gaya item pilihan. Uji: Maid → 120/120 "Coquette".

## 3. Motif diukur dari piksel (`motif.py`, kartu skema 7 kolom 36–37)
- Dulu: map memakai motif dari NAMA saja (VisualOutfitKit `MOTIF`), kartu `pola` CLIP cocok nama 44–55%.
- Sekarang: fitur piksel per wilayah kain (manekin/latar dibuang): kontras, tepi tajam & detail, warna (k-means Lab), blok
  warna, autokorelasi 2D bertopeng (periodisitas x/y mentah, kisi 2D), energi gradien, frekuensi tinggi, taburan bercak,
  sebaran tengah/pinggir. Hutan keputusan per grup (baju 2D / celana 2D / 3D) dilatih dari item yang **nama**nya menunjuk
  tepat satu motif; **nama tidak masuk fitur**; item bernama-motif diberi prediksi uji-silang (bukan hafalan). Klaim bila
  peluang ≥ 0,5.
- Uji silang (LAPORAN_MOTIF.md, presisi saat diklaim vs nama — batas bawah karena nama bisa salah): baju garis 90%, kotak 92%,
  polos 85%, ramai 90%, taburan 100%, grafis (nama merch/logo) 70%; celana garis 88%, kotak 91%, polos 73%, ramai 82%;
  3D garis 94%, taburan 91%, polos 79%, ramai 73%. Label emas (dinilai mata): 30/36 cocok saat diklaim.
- Penilaian MATA item ACAK (nama tanpa kata motif; kartu/lembar/motif_*.jpg): baju polos 8/8, garis 4/4, kotak 5/6, ramai
  7/8, grafis 7/8 (31/35); celana polos 8/8, garis 4/6, kotak 3/4, ramai 8/8 (23/26); 3D polos 7/7, ramai ≥0,6 4/4, kotak 3/7,
  grafis 2–3/8 → `motif.KLAIM`: 3D kotak & grafis tidak diklaim, celana garis & taburan ≥ 0,6, 3D lain ≥ 0,6.
- Kekurangan jujur: ±60–75% item acak masih "tidak pasti" (kemeja/jas/kostum berdetail); itu tidak diklaim dan generator
  kembali ke bukti nama. Kartu skema 7 mengukur ulang semua baju/celana 2D (~36 rb) dan 3D (~15 rb) bertahap
  (35 + 10 menit per putaran kartu-uji).
- Map: KartuItemKit `K.MotifI` + kalimat bacaan "motif garis-garis (diukur dari gambar)"; VisualOutfitKit `features()`
  menambah corak terukur (cari `rev 33: MOTIF DIUKUR`): pattern = nama ATAU ukur; polos terukur hanya bila nama tidak
  menyebut corak; keluarga garis→stripe, kotak→plaid, taburan, grafis.

## 4. Gender
Sudah rev 32c (17 Okt pagi): benih dari bentuk terukur 2D (leher rendah/bahu terbuka/crop 98–99% cewek) + mesh 3D
(perut/crop 92:0, bahu 46:0, leher rendah 25:0) + kategori resmi DressSkirt; uji nama-tersembunyi 95,7–97,5% benar saat
diputuskan. Motif sebagai bukti gender BELUM dipakai (belum ada uji yang membuktikan).

## 5. GitHub
README baru = peta repo (dipakai map / alat uji / branch sisa) + alasan tetap publik (Actions gratis tanpa batas hanya
untuk repo publik; privat Free 2.000 menit/bulan sedangkan Otak ±8.000). Penghapusan branch lewat API diblokir proxy sesi
Claude (403) → pemilik menghapus 5 branch lewat UI GitHub.

## Checksum Studio (panjang/hash, semua lolos loadstring)
| Script | Checksum |
|---|---|
| IndeksOutfitEngine | 168900/628683919 |
| BodyContextKit | 20440/644621692 |
| KartuItemKit | 23276/866987087 |
| VisualOutfitKit | 30887/1094751351 |
| lainnya | tidak berubah dari rev 32 |

## Tugas Codex (hemat token, cek sempit)
1. IndeksOutfitEngine `rev 33: PADANAN 3D`: pastikan `ganti2DKe3D` tidak menyentuh `g.setJ`, tidak memasang calon yang
   `bodyItem(...).blocked`, dan `GraphicTShirt` otomatis dilepas hanya bila atasan 3D terpasang.
2. Titik panggil `rev 33: badan yang tidak cocok`: `dg`, `bodyItem`, `gender` (lokal per grup) dalam cakupan.
3. `rev 33: outfit di sekitar item pilihan`: hanya mengganti judul bila `k.kat.k == "kasual"` dan ada item pilihan.
4. BodyContextKit `rev 33: hanya bila zona itu BISA`.
5. KartuItemKit `K.MotifI` + `KOLOM = 37` (baris skema 6 = 35 kolom → kolom 36–37 terbaca kosong).
6. VisualOutfitKit `rev 33: MOTIF DIUKUR`: cache fitur ikut versi kartu (`kv`).
7. `kartu_item.py` `motif_kartu`: prediksi uji-silang untuk item bernama-motif (tidak bocor dari nama).
8. Setelah merge PR #5: kartu-uji hanya jalan dari push `claude/kartu-item` → perlu jadwal di `main`; `KartuItemKit.CABANG = "main"`.
9. (Selesai, bukan bug) Uji Play: generate kedua berjarak 1 dtk kembali kosong = jeda sengaja `JEDA_MIN_GENERATE`
   ("Mohon tunggu sebentar") di KatalogServerEngine.

Studio belum di-Save oleh pemilik setelah rev 33 (Ctrl+S). Tidak publish.

## Rev 33c (17 Okt sore) — keamanan, repo tidak menumpuk, seleksi ketat, sinkron data lama

### Keamanan (permintaan pemilik)
- Scan SEMUA cabang + seluruh riwayat git (pola token GitHub/Google/AWS/Slack/OpenAI/Anthropic, ROBLOSECURITY, kunci privat,
  Redis/Upstash, Authorization/x-api-key berisi nilai, string panjang mirip kunci): **0 temuan**. Kunci Open Cloud hanya lewat
  `secrets.ROBLOX_API_KEY`. Path admin (daftar secret, webhook, deploy key, kolaborator) ditolak proxy sesi Claude → pemilik
  cek sendiri di Settings.
- Studio: 236 script diperiksa; satu rahasia nyata `API_SECRET` Vercel di `ServerStorage.Cadangan_Rev32_20261016.VercelBankData`
  (arsip, tidak dipakai) → nilainya DIHAPUS. Nilai itu tidak pernah masuk git. Pemilik disarankan menghapus proyek Vercel
  (atau mengganti env API_SECRET) karena riwayat versi place masih menyimpan nilai lama.

### Repo tidak menumpuk: cabang `data`
- Ukuran repo 663 MB dalam 16 hari (data/ 361 MB, model/ 145 MB, kartu/ 95 MB di riwayat).
- `data_cabang.sh` + workflow: hasil buatan disimpan di cabang `data` sebagai SATU commit tanpa induk (force-with-lease, ulang
  bila balapan); tiap simpan hanya mengganti jalur milik workflow itu. Tanda `.sumber/<grup>`; selama tanda grup belum ada,
  `ambil` membaca main dulu (main penghasil segar sampai PR #5 digabung). `bersihkan-main`: sekali sesudah pindah, salinan lama
  dihapus dari main lewat worktree terpisah.
- Benih cabang `data` dibuat dari main + cabang kerja (4f6dcb9). Uji: motif-uji menyimpan ke `data` (1 commit, bertanda motif).
- Cabang kerja tidak lagi menyimpan kartu/fisik3d/laporan (dihapus dari cabang kode; .gitignore).
- Map (cari `rev 33`): OtakGayaEngine `ambilInfoTerbaru` (data vs main, versi terbaru; 404 cepat), ReadyLookSource (4 URL,
  install() hanya versi lebih baru, tanpa break), KartuItemKit `CABANG_KARTU` {data, claude/kartu-item, main} versi terbaru,
  CDN juga untuk @data. Dicek dari Studio: raw @data & jsDelivr @data terbaca, 404 terdeteksi.
- **Urutan merge:** setelah PR #5 digabung, putaran Otak pertama di main menulis ke `data` (+ tanda otak) lalu menghapus salinan
  lama di main. Map Studio (yang membaca data+main) boleh dipublish kapan saja (sebelum/sesudah).

### Seleksi ketat (keluhan "item rebutan")
- IndeksOutfitEngine (cari `rev 33b`): `temaJangkarCocok` (tema berbukti + PMI + gaya) dipakai `grupJangkar`: setema/tersambung
  → satu kelompok walau vektor ragu; tema beda tak tersambung → terpisah. `temaBentrok` = pelengkap otomatis bertema lawan
  ditolak di kolam penata, saringan desainer, dan gerbang akhir (`tema_bentrok`). Kelompok ganda: susunan min 110 (dulu 64).
- Uji Play (avatar pemilik): Goth Pastel + Jersey + Topi Koboi: dulu 2 kelompok (Goth Pastel DIGABUNG topi koboi), 14 kartu →
  kini 3 kelompok, 114 kartu, judul per kelompok konsisten (Kawaii 38/38, Sporty 38/38). Item tunggal tetap 120.
  Kenaikan minimum susunan 110 belum diuji ulang (Studio macet "Start play hasn't finished yet").

### Sinkron data lama
- Dulu item bank lama (v3) hanya terkirim lewat server map yang hidup (600/server, 200 per 4 menit) → lambat saat sepi.
- otak.py: baca langsung `KatalogItemMetaCache_v3` shard_0..19 lewat Open Cloud → semua masuk antrean diminta; batas antrean
  6000 → 25000. Berlaku setelah merge. Bila log Otak menulis "Open Cloud 403", API key perlu izin baca data store itu.

### Checksum Studio (rev 33c)
| Script | Checksum |
|---|---|
| IndeksOutfitEngine | 171565/1064448198 |
| OtakGayaEngine | 24076/1440998588 |
| ReadyLookSource | 5407/305700216 |
| KartuItemKit | 23924/545660441 |
| BodyContextKit | 20440/644621692 |
| VisualOutfitKit | 30887/1094751351 |

### Tugas Codex tambahan (cek sempit)
10. `data_cabang.sh`: simpan (lease, ulang, hanya jalur sendiri), ambil (urutan per tanda), bersihkan-main (hanya grup bertanda).
11. embed.yml / ready-outfits.yml: daftar jalur simpan lengkap & tidak saling timpa (bank/outfit_* vs bank/ready_outfits.json).
12. OtakGayaEngine `ambilInfoTerbaru` + shard dari cabang yang sama (versi dicek).
13. IndeksOutfitEngine `temaJangkarCocok` / `temaBentrok` (tidak terlalu ketat untuk item tanpa tema berbukti: harus nil/false).
