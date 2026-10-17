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
