#!/usr/bin/env bash
# CABANG `data` (rev 33): semua hasil buatan workflow (model, meta, bank, data panen, kartu, fisik3d, laporan) disimpan di
# cabang `data` sebagai SATU commit tanpa riwayat yang DITIMPA tiap kali disimpan. Dulu hasil di-commit ke main tiap 6 jam
# sehingga riwayat menumpuk (repo 663 MB dalam 16 hari). Sekarang versi lama tidak dirujuk lagi dan dibersihkan GitHub;
# cabang kode tetap kecil dan riwayatnya hanya perubahan kode.
#
# Tiap kelompok hasil punya PENGHASIL (grup): otak (model/meta/bank outfit/panen/kartu harian), ready (koleksi siap pakai),
# kartu (uji kartu di cabang kerja), mata3d (fisik3d), motif (uji motif). Saat menyimpan, cabang data diberi tanda
# `.sumber/<grup>`. Masa pindah: selama tanda grup belum ada di cabang data, hasil grup itu masih dibaca dari main (main
# penghasil lama yang masih segar); sesudah tanda ada, cabang data yang dipakai.
#
#   bash data_cabang.sh ambil <grup> jalur...          -> salin versi terbaru jalur ke folder kerja (tidak di-stage)
#   bash data_cabang.sh simpan <grup> "pesan" jalur...  -> ganti HANYA jalur itu di cabang data (jalur grup lain tetap),
#                                                          commit tanpa induk, push --force-with-lease, ulang bila balapan
#   bash data_cabang.sh segarkan jalur...               -> bersihkan cache CDN jsDelivr @data untuk file itu
set -uo pipefail
CABANG="${CABANG_DATA:-data}"
REPO="${GITHUB_REPOSITORY:-grewetewe-commits/katalog-embed}"
perintah="${1:-}"; shift || true

ambil_ref() { git fetch -q --depth 1 origin "refs/heads/$1:refs/remotes/origin/$1" 2>/dev/null; }

case "$perintah" in
  ambil)
    grup="${1:?grup}"; shift
    ada_data=0; ambil_ref "$CABANG" && ada_data=1
    ambil_ref main || true
    if [ "$ada_data" = 1 ] && git cat-file -e "origin/$CABANG:.sumber/$grup" 2>/dev/null; then urutan="$CABANG main"
    else urutan="main $CABANG"; fi
    echo "ambil ($grup): urutan cabang = $urutan"
    for p in "$@"; do
      dapat=""
      for c in $urutan; do
        if git cat-file -e "origin/$c:$p" 2>/dev/null; then
          rm -rf -- "$p"
          git checkout "origin/$c" -- "$p" && dapat="$c" && break
        fi
      done
      echo "  $p <- ${dapat:-(tidak ada di cabang mana pun, pakai folder kerja)}"
    done
    git reset -q
    ;;
  simpan)
    grup="${1:?grup}"; pesan="${2:?pesan}"; shift 2
    [ "$#" -gt 0 ] || { echo "simpan: tidak ada jalur"; exit 1; }
    git config user.name "github-actions[bot]"
    git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
    mkdir -p .sumber && date -u +%Y-%m-%dT%H:%M:%SZ > ".sumber/$grup"
    for coba in 1 2 3 4 5 6; do
      idx="$(mktemp)"; rm -f "$idx"
      export GIT_INDEX_FILE="$idx"
      if ambil_ref "$CABANG"; then
        lama="$(git rev-parse "origin/$CABANG")"
        git read-tree "origin/$CABANG"
      else
        lama=""
        git read-tree --empty
      fi
      for p in "$@" ".sumber/$grup"; do
        git rm -r -q --cached --ignore-unmatch -- "$p" >/dev/null
        if [ -e "$p" ]; then git add -f -- "$p"; fi
      done
      tree="$(git write-tree)"
      unset GIT_INDEX_FILE; rm -f "$idx"
      commit="$(printf '%s\n\n(cabang %s = satu commit tanpa riwayat, ditimpa tiap simpan; grup %s)\n' "$pesan" "$CABANG" "$grup" | git commit-tree "$tree")"
      if git push -q --force-with-lease="refs/heads/$CABANG:$lama" origin "$commit:refs/heads/$CABANG"; then
        echo "simpan ($grup): cabang $CABANG = $commit ($# jalur, coba $coba)"; exit 0
      fi
      echo "simpan ($grup): balapan dengan workflow lain, ulang ($coba)"; sleep $((coba * 7))
    done
    echo "simpan ($grup): GAGAL setelah 6 kali"; exit 1
    ;;
  bersihkan-main)
    # Sekali setelah pindah: salinan LAMA hasil grup yang sudah bertanda di cabang data dihapus dari main (main = kode saja).
    # Dikerjakan di worktree terpisah supaya folder kerja workflow (yang berisi hasil terbaru) tidak terganggu.
    ambil_ref "$CABANG" || { echo "bersihkan-main: cabang $CABANG belum ada"; exit 0; }
    ambil_ref main || exit 0
    hapus=()
    git cat-file -e "origin/$CABANG:.sumber/otak" 2>/dev/null && hapus+=(model meta bank/outfit_0.json bank/outfit_1.json \
      bank/outfit_2.json bank/outfit_3.json data/panen.json.gz out LAPORAN_OTAK.md LOG_TERAKHIR.txt)
    git cat-file -e "origin/$CABANG:.sumber/ready" 2>/dev/null && hapus+=(bank/ready_outfits.json data/ready_outfit_cursor.json \
      data/ready_outfit_report.json)
    [ "${#hapus[@]}" -gt 0 ] || { echo "bersihkan-main: belum ada grup yang pindah"; exit 0; }
    wt="$(mktemp -d)"
    git worktree add -q --detach "$wt" origin/main || exit 0
    (
      cd "$wt" || exit 0
      git config user.name "github-actions[bot]"
      git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
      ada=0
      for p in "${hapus[@]}"; do
        if [ -n "$(git ls-files -- "$p")" ]; then git rm -r -q -- "$p" && ada=1; fi
      done
      if [ "$ada" = 1 ]; then
        git commit -q -m "Pindah selesai: hasil buatan kini hanya di cabang data (main = kode saja, riwayat tidak menumpuk lagi)"
        for coba in 1 2 3; do
          git push -q origin HEAD:main && { echo "bersihkan-main: salinan lama dihapus dari main"; break; }
          git pull -q --rebase origin main || true
        done
      else
        echo "bersihkan-main: main sudah bersih"
      fi
    )
    git worktree remove --force "$wt" 2>/dev/null || true
    ;;
  segarkan)
    for f in "$@"; do curl -s -m 20 -o /dev/null -w "%{http_code} $f\n" "https://purge.jsdelivr.net/gh/$REPO@$CABANG/$f" || true; done
    ;;
  *)
    echo "pakai: ambil <grup> jalur... | simpan <grup> \"pesan\" jalur... | segarkan jalur..."; exit 2 ;;
esac
