# Otak & Mata Katalog Praktis

Repo ini = **dapur data** map Roblox *Katalog Praktis*. GitHub Actions (gratis untuk repo publik) memanen outfit
publik, melatih model kecocokan, dan **membaca item** (gambar, bentuk, mesh 3D, motif). Map hanya **mengunduh hasilnya**
(file JSON). Tidak ada API berbayar, tidak ada server, tidak ada secret di repo ini. Script map (Luau) **tidak** disimpan di
sini — hanya di Roblox Studio.

## Peta isi (apa itu, dipakai map atau tidak)

| Folder / file | Isinya | Dipakai map? | Dibuat oleh |
|---|---|---|---|
| `model/` | model kecocokan: vektor gaya, gender, warna per item | **ya** (OtakGayaEngine) | `otak.py` (Otak, tiap 6 jam) |
| `meta/` | nama/harga/status jual (snapshot), sepatu, badan | **ya** | `otak.py` |
| `bank/` | outfit buatan manusia yang lolos saring + outfit siap pakai publik | **ya** | `otak.py`, `ready_outfits.mjs` |
| `kartu/` | **kartu item**: jenis, tema berbukti, gender berbukti, bentuk 2D/3D diukur, motif diukur | **ya** (KartuItemKit) | `kartu_item.py` |
| `fisik3d/` | daftar item yang perlu diukur fisiknya (titik pasang, ukuran) | **ya** (FisikItemKit) | `mata3d.py` |
| `data/` | bahan mentah panen (dibaca workflow, bukan map) | tidak | `otak.py`, `ready_outfits.mjs` |
| `out/raw.npz` | cadangan sidik jari gambar lama (dibaca `otak.py`) | tidak | lama |
| `uji2d/`, `uji3d/` | **bukti akurasi**: label emas dinilai mata, contoh gambar, angka uji | tidak | alat uji |
| `LAPORAN_*.md`, `LOG_*.txt` | laporan terakhir tiap workflow (angka akurasi, sebaran) | tidak | workflow |
| `RANCANGAN_KARTU_ITEM.md`, `READY_OUTFITS.md` | rancangan & catatan | tidak | — |

### Kode
| File | Fungsi |
|---|---|
| `otak.py` | panen outfit publik + latih model kecocokan |
| `kartu_item.py` | membuat kartu item (CLIP + bukti + bentuk + motif) |
| `bukti_item.py` | gender & tema dari bukti (nama, bentuk diukur, kategori resmi, pemakaian di outfit manusia) |
| `bentuk2d.py` | bentuk baju/celana 2D diukur dari piksel (leher, lengan, crop, panjang) |
| `bentuk3d.py`, `mata3d.py` | bentuk atasan/bawahan 3D diukur dari mesh resmi Roblox |
| `badan_bentuk.py` | badan avatar: manusia atau bukan, dan cara manusia memakainya (2D/3D) |
| `motif.py` | motif diukur dari piksel (polos/garis/kotak/taburan/ramai/grafis) |
| `ready_outfits.mjs`, `ready_import.py` | koleksi outfit siap pakai publik |
| `uji_*.py`, `cek_lembar3d.py`, `lembar_kartu.py`, `visual_audit.py`, `test_*` | **alat uji** (mengukur akurasi, lembar kontak untuk dinilai mata, tes otomatis) |

### Workflow (`.github/workflows/`)
| Workflow | Jalan kapan | Untuk |
|---|---|---|
| `embed.yml` (Otak Katalog Praktis) | otomatis tiap 6 jam | model, meta, bank |
| `ready-outfits.yml` | otomatis tiap 6 jam | outfit siap pakai |
| `mata3d-panen.yml` | otomatis 4×/hari (jadwal hanya jalan dari `main`) | ukur mesh 3D bertahap |
| `kartu-uji.yml`, `motif-uji.yml` | saat kode kartu/motif berubah di `claude/kartu-item` | kartu item + laporan akurasi (setelah digabung: perlu jadwal di `main`) |
| `body-context.yml`, `ready-outfits-ci.yml` | saat PR/push | tes otomatis |
| `uji-*.yml`, `cek-lembar3d.yml`, `visual-audit.yml`, `coverage-audit.yml` | manual / saat alat uji berubah | alat ukur akurasi & audit Codex |

## Branch
| Branch | Status |
|---|---|
| `main` | **produksi** — yang dibaca map |
| `claude/kartu-item` | kerja Claude (PR #5), digabung ke `main` setelah dicek Codex |
| `codex/shared-handoff-20261014` | catatan serah-terima Claude ↔ Codex |
| lainnya (`codex/body-context`, `codex/outfit-anchor-quality`, `codex/ready-outfit-foundations`, `codex/visual-audit-20261011`, `radar`) | **sisa lama, sudah tergabung / tidak dipakai — boleh dihapus** |

## Kenapa repo ini publik (dan sebaiknya tetap publik)

- **Gratis permanen hanya bila publik.** GitHub Actions gratis tanpa batas untuk repo publik; repo privat (akun Free)
  hanya dapat 2.000 menit/bulan, sedangkan Otak saja memakai ±8.000 menit/bulan → privat = berhenti atau bayar.
- **Map mengunduh lewat alamat publik** (raw.githubusercontent / CDN jsDelivr). Repo privat butuh token di dalam map, dan
  CDN gratis tidak melayani repo privat.
- **Yang terlihat publik hanya data & kode dapur**: ID item, outfit publik, angka model. Tidak ada token, cookie, API key,
  atau script map. Menyamarkan nama file (obfuscation) tidak menambah keamanan karena isinya tetap terbaca.
- Secret (mis. `ROBLOX_API_KEY` opsional) disimpan di *Settings → Secrets* GitHub, bukan di file.

## Prinsip
- Semua yang diklaim map tentang item **diukur atau berbukti** (angka akurasinya di `LAPORAN_*.md`); yang tidak pasti tidak
  diklaim.
- Map memuat snapshot model dari ServerStorage lebih dahulu; GitHub/CDN hanya pembaruan. Kalau pembaruan berhenti, map tetap
  jalan.
- Peringkat model adalah alat menyaring dan mengurutkan, bukan jaminan semua pemain suka.
