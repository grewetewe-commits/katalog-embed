# Otak Katalog Praktis

Generator outfit Roblox memakai model CLIP lokal dan model kecocokan milik proyek ini.
Tidak membutuhkan API ChatGPT, Claude, Gemini, atau backend Vercel saat pemain membuat outfit.

## Operasi tanpa langganan

- Map memuat snapshot model dari ServerStorage lebih dahulu. GitHub/CDN hanya untuk pembaruan opsional.
- Pelatihan memakai runner standar GitHub Actions pada repo publik; tidak memakai runner besar berbayar.
- Secret `ROBLOX_API_KEY` opsional untuk membaca umpan balik dari map melalui Open Cloud.
- Workflow tidak memasukkan secret Gemini; kode tidak mengirim permintaan ke API generatif.
- Batas provider tetap berlaku. Jika pembaruan berhenti, snapshot map tetap dapat dipakai.

## Ekspor model

Vektor dipilih setelah bank final diketahui: item yang diminta pemain, kedua kaki sepatu,
item bank final, kemudian item katalog lain. Outfit yang tidak punya vektor lengkap tidak diekspor.
Semua shard mempunyai versi yang sama. Menggabungkan vektor dari versi latihan berbeda tidak diperbolehkan.

Jempol bawah dihitung sebagai masukan agregat yang dapat berubah; satu suara tidak menjadi larangan permanen.
Peringkat model adalah alat menyaring dan mengurutkan, bukan jaminan probabilitas bahwa semua pemain menyukai outfit.
