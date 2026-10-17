# Otak & Mata Katalog Praktis

Repo ini = **dapur data** map Roblox *Katalog Praktis*. GitHub Actions (gratis untuk repo publik) memanen outfit
publik, melatih model kecocokan, dan **membaca item** (gambar, bentuk, mesh 3D, motif). Map hanya **mengunduh hasilnya**
(file JSON). Tidak ada API berbayar, tidak ada server, tidak ada secret di repo ini. Script map (Luau), DataStore, dan GUI
**tidak** ada di sini — hanya di Roblox Studio / server Roblox.

## Dua cabang utama (rev 33)

| Cabang | Isi | Riwayat |
|---|---|---|
| `main` | **kode saja** (Python, workflow, alat uji, label emas) | normal, hanya perubahan kode |
| `data` | **hasil buatan** workflow: `model/`, `meta/`, `bank/`, `data/`, `kartu/`, `fisik3d/`, `out/`, `LAPORAN_*.md`, `LOG_*.txt` | **selalu 1 commit** — ditimpa tiap putaran, versi lama tidak menumpuk |

Dulu hasil di-commit ke `main` tiap 6 jam → repo 663 MB dalam 16 hari. Sekarang semua workflow memakai `data_cabang.sh`:
`ambil` (bahan terbaru), `simpan` (ganti hanya jalur milik workflow itu, commit tanpa induk, force-push aman dengan lease),
`bersihkan-main` (sekali sesudah pindah: salinan lama dihapus dari `main`). Map membaca cabang `data` (jatuh ke `main`
selama masa pindah; versi yang lebih baru yang dipakai).

## Peta isi cabang `data` (dipakai map)

| Folder / file | Isinya | Dipakai map? | Dibuat oleh |
|---|---|---|---|
| `model/` | model kecocokan: vektor gaya, gender, warna per item | **ya** (OtakGayaEngine) | `otak.py` (tiap 6 jam) |
| `meta/` | nama/harga/status jual (snapshot), sepatu, badan | **ya** | `otak.py` |
| `bank/` | outfit buatan manusia yang lolos saring + outfit siap pakai publik | **ya** | `otak.py`, `ready_outfits.mjs` |
| `kartu/` | **kartu item**: jenis, tema berbukti, gender berbukti, bentuk 2D/3D diukur, motif diukur | **ya** (KartuItemKit) | `kartu_item.py` |
| `fisik3d/` | item yang perlu diukur fisiknya, bentuk 3D | **ya** (FisikItemKit) | `mata3d.py` |
| `data/`, `out/` | bahan mentah panen (dibaca workflow, bukan map) | tidak | `otak.py`, `ready_outfits.mjs` |
| `LAPORAN_*.md`, `LOG_*.txt`, `.sumber/` | laporan & angka akurasi terakhir; tanda penghasil terakhir | tidak | workflow |

## Peta isi `main` (kode)

| File | Fungsi |
|---|---|
| `otak.py` | panen outfit publik + latih model kecocokan |
| `kartu_item.py` | membuat kartu item (CLIP + bukti + bentuk + motif) |
| `bukti_item.py` | gender & tema dari bukti (nama, bentuk diukur, kategori resmi, pemakaian di outfit manusia) |
| `bentuk2d.py` | bentuk baju/celana 2D diukur dari piksel (leher, lengan, crop, panjang) |
| `bentuk3d.py`, `mata3d.py` | bentuk atasan/bawahan 3D diukur dari mesh resmi Roblox |
| `badan_bentuk.py` | badan avatar: manusia atau bukan, dan cara manusia memakainya (2D/3D) |
| `motif.py` | motif diukur dari piksel (polos/garis/kotak/taburan/ramai/grafis) |
| `ready_outfits.mjs`, `ready_import.py`, `data/ready_outfit_sources.json` | koleksi outfit siap pakai publik (+ daftar sumbernya) |
| `data_cabang.sh` | simpan/ambil hasil di cabang `data` |
| `uji_*.py`, `cek_lembar3d.py`, `lembar_kartu.py`, `visual_audit.py`, `test_*`, `uji2d/`, `uji3d/` | **alat uji** + label emas dinilai mata (bukti akurasi) |

### Workflow (`.github/workflows/`)
| Workflow | Jalan kapan | Untuk |
|---|---|---|
| `embed.yml` (Otak Katalog Praktis) | otomatis tiap 6 jam | model, meta, bank, kartu → cabang `data` |
| `ready-outfits.yml` | otomatis tiap 6 jam | outfit siap pakai → cabang `data` |
| `mata3d-panen.yml` | otomatis 4×/hari (jadwal hanya jalan dari `main`) | ukur mesh 3D bertahap → cabang `data` |
| `kartu-uji.yml`, `motif-uji.yml` | saat kode kartu/motif berubah di cabang kerja | kartu + laporan akurasi → cabang `data` |
| `body-context.yml`, `ready-outfits-ci.yml` | saat PR/push | tes otomatis |
| `uji-*.yml`, `cek-lembar3d.yml`, `visual-audit.yml`, `coverage-audit.yml` | manual / saat alat uji berubah | alat ukur akurasi & audit Codex |

## Branch lain
| Branch | Status |
|---|---|
| `claude/kartu-item` | kerja Claude (PR #5), digabung ke `main` setelah dicek Codex |
| `codex/shared-handoff-20261014` | catatan serah-terima Claude ↔ Codex |
| `codex/body-context`, `codex/outfit-anchor-quality`, `codex/ready-outfit-foundations`, `codex/visual-audit-20261011`, `radar` | **sisa lama — boleh dihapus** (4 pertama sudah tergabung ke `main`; `radar` = sistem lama rev 20 yang tidak dipakai) |

## Keamanan & kenapa repo ini publik

- **Isi repo hanya data dapur & kode Python.** Diperiksa 17 Okt (semua cabang + seluruh riwayat): tidak ada token, cookie,
  API key, password. Kunci Open Cloud dipakai lewat *Settings → Secrets* (`secrets.ROBLOX_API_KEY`), nilainya tidak pernah
  tertulis di file dan disamarkan otomatis di log.
- **Yang berharga ada di map, bukan di sini**: script Luau, DataStore (data pemain, favorit, bank item), GUI, dan aturan
  komunikasi RemoteFunction ada di server Roblox. Orang yang menyalin repo ini hanya mendapat data katalog publik + cara
  mengolahnya; mereka tidak bisa membaca/menulis DataStore map ini (butuh kunci milik pemilik) dan tidak bisa memerintah
  server map.
- **Gratis permanen hanya bila publik.** GitHub Actions gratis tanpa batas untuk repo publik; repo privat (akun Free)
  hanya dapat 2.000 menit/bulan, sedangkan Otak saja memakai ±8.000 menit/bulan. Map juga mengunduh lewat alamat publik
  (raw.githubusercontent / CDN jsDelivr); repo privat butuh token di map dan CDN gratis tidak melayaninya.
- Menyamarkan nama file (obfuscation) tidak menambah keamanan karena isinya tetap terbaca.

## Prinsip
- Semua yang diklaim map tentang item **diukur atau berbukti** (angka akurasinya di `LAPORAN_*.md` cabang `data`); yang
  tidak pasti tidak diklaim.
- Map memuat snapshot model dari ServerStorage lebih dahulu; GitHub/CDN hanya pembaruan. Kalau pembaruan berhenti, map tetap
  jalan.
- Peringkat model adalah alat menyaring dan mengurutkan, bukan jaminan semua pemain suka.
