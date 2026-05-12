# Fashion Studio ETL Pipeline

## Overview

Fashion Studio ETL Pipeline adalah proyek ETL (Extract, Transform, Load) sederhana berbasis Python yang dibuat untuk mengambil data produk fashion dari website kompetitor, membersihkan data, dan menyimpannya ke beberapa repository data.

Website sumber data:  
https://fashion-studio.dicoding.dev

Proyek ini dikembangkan sebagai submission kelas **Belajar Fundamental Pemrosesan Data** Dicoding.

---

## Features

- Web scraping produk fashion dari website
- Extract data dari 50 halaman website
- Transformasi dan pembersihan data
- Konversi mata uang USD ke IDR
- Menghapus data invalid, null, dan duplicate
- Menyimpan data ke:
  - CSV
  - Google Sheets
  - PostgreSQL
- Unit testing
- Test coverage
- Error handling
- Modular code architecture

---

## Tech Stack

- Python
- Pandas
- BeautifulSoup4
- Requests
- Pytest
- PostgreSQL
- Google Sheets API
- SQLAlchemy

---

## Project Structure

```txt
submission-pemda/
│
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── main.py
├── requirements.txt
├── submission.txt
├── products.csv
├── google-sheets-api.json
├── .env
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/username/fashion-studio-etl.git
```

Masuk ke folder project:

```bash
cd fashion-studio-etl
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Buat file `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fashion_db
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Running ETL Pipeline

```bash
python main.py
```

---

## Running Unit Test

```bash
python -m pytest tests
```

---

## Running Test Coverage

```bash
python -m pytest tests --cov=utils --cov-report=term-missing
```

---

## Test Coverage Result

- Extract: 100%
- Transform: 100%
- Load: 100%
- Total Coverage: 100%

---

## Google Sheets

Hasil ETL juga disimpan ke Google Sheets.

Pastikan:
- Google Sheets API aktif
- Google Drive API aktif
- `google-sheets-api.json` tersedia
- Spreadsheet telah di-share ke service account

---

## PostgreSQL

Pastikan PostgreSQL aktif sebelum menjalankan pipeline.

Buat database terlebih dahulu:

```sql
CREATE DATABASE fashion_db;
```

---

## Author

Septiyana Putri Isnaini
