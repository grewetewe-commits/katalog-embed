# Laporan verifikasi sidik jari visual

- Item berhasil: **1321** | gagal (thumbnail/placeholder): **0** | model: `openai/clip-vit-base-patch32`
- Mode: **JALAN PENUH**

## 1. Kesehatan data
- Rata-rata kemiripan antar item acak (mentah): 0.678 (CLIP wajar 0,4 sampai 0,8; di atas 0,95 = runtuh)
- Dimensi efektif (participation ratio): 23.2 (di bawah 3 = hampir satu titik)
- Pasangan hampir identik (>0,999): 0.00%
- Tingkat gagal thumbnail: 0.0%

## 2. Apakah sidik jari ini membawa informasi keserasian?
- Item berlabel tema: 1296 | berlabel kreator (grup >= 3 item): 421

| Ukuran | Representasi | AUC | Penilaian |
|---|---|---|---|
| Tema, LINTAS slot (relevan untuk outfit) | mentah (CLIP apa adanya) | 0.544 | TIDAK INFORMATIF |
| Tema, dalam slot yang sama | mentah (CLIP apa adanya) | 0.627 | LEMAH |
| Kreator/set, LINTAS slot | mentah (CLIP apa adanya) | 0.686 | SEDANG |
| Tema, LINTAS slot (relevan untuk outfit) | gaya (slot dinetralkan) | 0.605 | LEMAH |
| Tema, dalam slot yang sama | gaya (slot dinetralkan) | 0.711 | SEDANG |
| Kreator/set, LINTAS slot | gaya (slot dinetralkan) | 0.647 | LEMAH |

- Tetangga terdekat lintas slot (gaya): 30.3% se-tema vs 11.4% bila acak (**2.7x** lebih baik dari acak)
- Tetangga terdekat lintas slot (mentah): 24.5% se-tema vs 11.2% bila acak (**2.2x** lebih baik dari acak)

## 3. Keputusan
- **BELUM LAYAK**: AUC tema lintas slot = 0.60. Sidik jari ini belum cukup memisahkan tema. Jangan diintegrasikan; kita pakai jalur lain (warna asli, kreator, penilaianmu).
- Kesamaan kreator/set (AUC lintas slot terbaik): 0.69

## 4. Tag zero-shot (gaya) terhadap tema yang sudah diketahui
- Item dengan minimal 1 tag gaya (>=12%): 1321/1321 (100%)

| Tema | Tag yang diharapkan | Di tema itu | Di semua item | Lipat |
|---|---|---|---|---|
| Angel & Divine | angel | 58% | 14% | 4.3x |
| Horror | horror/gothic/demon | 77% | 45% | 1.7x |
| Anime | kawaii/y2k | 13% | 8% | 1.5x |
| Ancient Egypt | royal/fantasy | 58% | 17% | 3.4x |
| Assassin | military/gothic | 45% | 26% | 1.7x |
- Lipat di atas 1,5 berarti tag itu memang lebih sering muncul di tema yang sesuai (tanda tag masuk akal).


_Catatan jujur: label tema berasal dari hasil pencarian per-tema (bukan penilaian manusia), jadi AUC tinggi berarti_
_sidik jari menangkap kesamaan tema/gaya; belum membuktikan outfit hasil susunan itu enak dipandang. Itu tetap diuji dengan penilaianmu._
