# Giliran Claude — 16 Oktober 2026 (bagian 5): pembaca item BERBUKTI & DIUKUR (rev 31)

Penulis: Claude (implementer). Status: **READY_FOR_CODEX**. Tidak publish, tidak mengubah DataStore live selain DataStore
baru `KatalogItemFisik_v1` (cache fakta item, pola sama dengan `KatalogItemUkuran_v2`), biaya Rp0. Save Studio rev 30
terkonfirmasi (Studio dibuka ulang dengan perubahan utuh); **Save rev 31 belum terkonfirmasi**. Kode GitHub: PR #5.

## Arahan pemilik (16:57)

Gender belum ketat; pembacaan item masih "oh jaket" — harus detail (jenis spesifik, bentuk keseluruhan, ketebalan, panjang,
tekstur, gender, bentuk dada; baju 2D: potongan leher — cewek lebih rendah, cowok menyentuh leher; vertex bila bisa);
tema **jangan ditebak**, harus ada sistem yang tahu tema & sambungan tema yang cocok; harus tetap benar setelah sesi ini.
Vercel dipakai atau tidak?

## Fakta yang dicek (bukan asumsi)

- Endpoint 3D Marketplace (`assets-thumbnail-3d`) wajib login sejak Maret 2026; Open Cloud API key butuh izin
  **thumbnails: read** (DevForum t/4435303). Kunci repo `ROBLOX_API_KEY` → 403 "Scope not authorized" (`uji3d/LOG.txt`).
  `mata3d.py` sudah siap (OBJ → verteks → ukuran, profil lebar/tebal per ketinggian, flare, tonjolan dada, simetri);
  jalan otomatis begitu pemilik menambah izin.
- Verteks di mesin Roblox: `AssetService:CreateEditableMeshAsync` → "no permission to load asset" untuk aset orang lain
  (diuji pada jaket Roblox & Duck-o-Lantern). Jadi verteks hanya lewat file 3D resmi di atas.
- Vercel: `VercelBankData` `AKTIF = false` (mode Rp0), satu-satunya pemanggil `vercel.app`. **Tidak dipakai** → pemilik boleh
  menghapus proyek Vercel; modul mati dibiarkan (usul hapus bersama Codex).

## GitHub (PR #5, branch `claude/kartu-item`) — kartu skema 4 (27 kolom)

1. **`bukti_item.py` — tema & gender dari BUKTI**
   - Sumber: nama, **unsur** yang terlihat (benda: labu/tanduk/mahkota/topi koboi/zirah/loreng… — CLIP andal untuk benda),
     gaya gambar (lemah, 1 poin), **pemakaian** di 73.233 outfit buatan manusia (data panen).
   - Tema diputuskan hanya bila poin ≥ 3 dan tidak sekadar gambar (kecuali benda khas jelas ≥ 60 + gaya setuju).
     Kurang bukti = **tidak bertema khusus** (115 rb item), bukan dipaksa. 15.814 item bertema berbukti.
   - Label emas 2D: saat memutuskan, **11/12 tepat** (kartu lama 36/60 karena selalu menjawab).
   - Gender: propagasi pemakaian dari item bernama jelas + benih bentuk diukur. Uji nama-tersembunyi (20% benih
     disembunyikan): **94,9% / 95,3% / 96,7%** benar pada ambang 0,10 / 0,15 / 0,25 (skor CLIP otak: 77,8%).
   - **`kartu/tema_graf.json`**: sambungan tema (PMI) dari outfit manusia, mis. punk↔gothic↔vampir↔iblis, malaikat↔peri,
     kawaii↔coquette, natal↔musim dingin, militer↔cyber.
2. **`bentuk2d.py` — potongan baju/celana 2D DIUKUR dari piksel** thumbnail resmi (manekin & kamera tetap; warna manekin
   diukur: r/g 1,000–1,008, b/g 0,975–0,984): kedalaman leher, bahu terbuka, panjang lengan, crop, panjang celana/rok
   (kesinambungan warna: kaus kaki/stoking tidak dihitung celana panjang), celana menutup badan, lapisan kulit.
   Uji emas: lapisan kulit 116/119, lengan panjang 22/24, tanpa lengan 6/6, crop 2/2, celana panjang 16/18, pendek/rok 11/16.
   **Hipotesis pemilik terbukti data**: di 331 baju yang gendernya jelas dari pemakaian, leher rendah 98% cewek,
   bahu terbuka 99%, crop 99% (dasar 79%) → dipakai sebagai benih gender. Diukur bertahap (cache `cache_bentuk/`),
   3.000/putaran uji, 6.000/putaran otak (±35 rb baju/celana 2D).
3. Workflow: `kartu-uji.yml` (tarik sebelum push, cache bentuk), `embed.yml` (cache bentuk, `tema_graf.json` ikut commit &
   purge CDN), `uji-bentuk2d.yml`, `uji-mata3d.yml`.

## Studio (rev 31)

| Script | Perubahan |
|---|---|
| KartuItemKit | 27 kolom; `GenderI`, `TemaB`, `TemaUtama` (skema ≥3 = tema berbukti), `TemaCocokI`, `Sambung` (graf), `BentukI` |
| IndeksOutfitEngine | kartuMusim & analisis item pilihan pakai tema berbukti; pesan "Tema terbukti: Halloween (terlihat di gambar (labu))" menyebut sumber bukti; rangkai: setema +8, **tema teman** (PMI ≥ 0,3) +4, tema bentrok −6/−3; buktiTema mutu menghitung tema teman; `klasikMenutup` (baju/celana lapisan kulit tidak dihitung atasan/bawahan) |
| DesainerEngine | indeks & koreksi kartu pakai tema berbukti + sambungan; `api.klasikMenutup` |
| KatalogServerEngine | gerbang gender: bukti pemakaian (|skor| ≥ 0,25, ≥ 2 bukti) berlaku **semua slot** (dulu nama + CLIP hanya slot inti) |
| FisikItemKit (BARU) | fakta fisik dari model LoadAsset yang sudah dimuat: titik pasang, Size/MeshSize, WrapLayer Order/Shrink/Puffiness, SurfaceAppearance (PBR), id template 2D; 256 shard DataStore, tulis lewat BudgetKit, TTL baca 30 mnt; antrean latar 1 item/2 dtk |
| UkuranItemEngine, ItemInspectorEngine | memanggil `FisikItemKit.Catat` pada model yang sama (tanpa LoadAsset ulang) |

Uji Play (R15 Gadis): COWO/CEWE tanpa item 120/120; Duck-o-Lantern 120 kartu "Tema terbukti: Halloween (terlihat di gambar
(labu))"; topi koboi "Koboi (terlihat di gambar, nama item)"; sayap "Malaikat (…, nama item)"; jas "Formal (nama item)".
Gerbang gender kini punya bukti jelas untuk ±16 rb item (mis. 2.737 aksen jelas feminin yang dulu lolos ke cowok).
FisikItemKit menulis shard (contoh: rambut HairAttachment 2,34×3,34×1,66; topi HatAttachment; aksen BodyFrontAttachment).
Konsol: tanpa galat proyek (satu peringatan ContentId 203785492 bukan dari kode rev 31, perlu dicek).

Checksum (panjang/h): IndeksOutfitEngine 164991/473806894 · DesainerEngine 65566/1746736450 · KartuItemKit 9853/1051098154 ·
FisikItemKit 6641/2099716507 · UkuranItemEngine 9820/1405774519 · ItemInspectorEngine 9372/573620953 ·
KatalogServerEngine 238880/999239103 · VisualOutfitKit 29768/2077036755. Semua lolos loadstring.

## Tambahan rev 31b (16 Okt sore) — bacaan item terlihat pemain, perbaikan bentuk

- **`KartuItemKit.Bacaan(id, fakta)`**: kalimat bacaan item HANYA dari fakta terukur/berbukti (bukan tebakan CLIP):
  bentuk 2D diukur (lengan, kerah menutup leher / leher sedang / leher rendah, bahu terbuka, crop, panjang bawahan,
  kaus kaki/stoking, menutup badan, lapisan kulit), gender dari pemakaian ("dipakai cewek (24 outfit)", uniseks), fakta fisik
  `FisikItemKit` (titik pasang → "dipasang di pinggang belakang", ukuran lebar×tinggi×tebal stud, lapisan 3D, tekstur PBR).
- **IndeksOutfitEngine** mengirim `Ringkasan.Bacaan` (maks 2 item pilihan) dan `Ringkasan.BuktiTema`; **KatalogUIController**
  menampilkannya lewat notifikasi yang sudah ada (`StarterGui.Notif`, 7 dtk + 5 dtk) setelah hasil siap. Dulu bukti tema hanya
  masuk `Memuat.Sub` (1 baris, 0,55 dtk, terpotong). Tanpa UI baru.
- **FisikItemKit**: `AmbilCepat` (tanpa menunggu DataStore di jalur pemain; shard dimuat di latar), memori dibatasi 60 rb item.
- **Python**: baju 2D yang diukur → panjang crop/normal (tebakan CLIP "crop" pada 41% baju terukur dibuang); laporan kartu
  menampilkan gender, tema bukti, bentuk DIUKUR. `bentuk2d.py` v4: celana sobek di lutut (pita tertutup beda warna) tetap
  panjang; paha terbuka tidak dilewati. Emas: celana panjang **17/18** (v2 16/18), pendek/rok tetap 11/16
  (v3 tanpa syarat tertutup sempat 7/16 → ditolak).
- Uji Play: CEWE + baju 78686093721077 → "Item dibaca: tanpa lengan, leher rendah, bahu terbuka (diukur dari gambar), dipakai
  cewek (24 outfit)" (114 kartu); COWO + 18444465194 → "lengan panjang, kerah menutup leher (diukur dari gambar), dipakai cowok
  (35 outfit)". Notifikasi 2 baris muat di layar 1136 px.

Checksum rev 31b (panjang/h, semua lolos loadstring): IndeksOutfitEngine 166254/614347281 · KartuItemKit 13862/883423193 ·
FisikItemKit 7423/453707953 · KatalogUIController 153301/1294242936 (lainnya sama dengan tabel di atas).

## Batas klaim

- Label emas 1 penilai, n kecil; tema berbukti cakupan rendah pada gaya abstrak (streetwear/y2k) — sengaja abstain.
- Bentuk 2D: thumbnail = manekin R6 sudut 3/4; rok yang dilukis di kaki terbaca seperti celana pendek; leher hanya baju 2D.
- Gender pemakaian mewarisi bias data panen (79% baju bergender jelas dipakai cewek).
- Verteks 3D menunggu izin API key; fakta fisik 3D di map baru terkumpul bertahap (belum dipakai penyusun).

## Untuk Codex

1. Review `bukti_item.py` (aturan poin & abstain, `UNSUR`), `bentuk2d.py` (koordinat wilayah, warna manekin), `mata3d.py`.
2. Gerbang gender baru (ambang 0,25 / bukti ≥ 2) dan efeknya pada jumlah kartu.
3. Penalti tema bentrok (PMI nil = −3) — terlalu keras/lunak?
4. `FisikItemKit`: pola DataStore shard + BudgetKit; aman untuk server live?
