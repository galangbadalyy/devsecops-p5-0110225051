# devsecops-p5-0110225051

## 1. Nama Aplikasi & Fungsi
**TaskManager** adalah aplikasi command line untuk mengelola daftar tugas: menambah, menampilkan (diurutkan berdasarkan prioritas), menandai selesai, menghapus, dan melihat statistik (termasuk tugas yang lewat tenggat). Data disimpan dalam file JSON.

Author: Muhammad Galang Badaly (STT Terpadu Nurul Fikri)

## 2. Bahasa / Framework
- Python 3.11+
- Library standar (`argparse`, `json`, `dataclasses`)
- `pytest` untuk unit test

## 3. Cara Menjalankan
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python src/main.py add "Kerjakan laporan" --priority high --due 2026-10-30
python src/main.py list
python src/main.py done 1
python src/main.py stats

pytest -v        # menjalankan unit test
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`, terpicu pada `push` dan `pull_request` ke branch `main`, berjalan di `ubuntu-latest`.

| Job | Fungsi |
|-----|--------|
| `build` | Install dependencies dan menjalankan unit test dengan pytest |
| `sast-scan` | Berjalan setelah `build` (`needs: build`). Menjalankan **Bandit**, mengunggah laporan JSON sebagai artifact, lalu menerapkan **Quality Gate**: pipeline gagal jika ditemukan temuan dengan severity MEDIUM atau lebih tinggi |

## Struktur Project
```
src/main.py
src/taskmanager/{models,validators,storage,service,cli}.py
tests/
.github/workflows/devsecops.yml
```
