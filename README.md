# Data Insight UAS Submission (Flat Root)

Submission UAS Mata Kuliah **Data Insight** (Take Home) dengan 2 deliverable utama:

1. **Soal 1** — Dataset Social Media Engagement: buat **10 visualisasi** + deskripsi insight.
2. **Soal 2** — Dashboard COVID-19 United States View: analisis **2a–2e** (insight, target user, elemen desain, hambatan, rekomendasi).

> Konsep repo ini: **tidak ada folder**, semua file ada di **root** supaya simpel untuk submit.

---

## File di Root (wajib)

Pastikan semua file berada pada folder root yang sama:

- `setup.sh` (opsional; membantu setup environment cepat)
- `dashboard_social_media_engagement.py` (SOAL 1)
- `dashboard_covid19_united_states_view.py` (SOAL 2)

File data dan output juga disimpan di root (lihat bagian Output Naming).

---

## Prasyarat

- Python 3.9+ (disarankan)
- VSCode + Python extension (+ Jupyter jika pakai notebook)
- Internet (untuk install package / download Kaggle dataset)

---

## Setup Environment (sekali saja)

### A. Buat virtual environment

```bash
python -m venv .venv
```

### B. Aktifkan virtual environment

Linux/Mac:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### C. Install dependencies

```bash
pip install -r requirements.txt
```

### D. Jalankan setup otomatis (alternatif)

```bash
chmod +x setup.sh
./setup.sh
```

---

## Running Dashboards

Jalankan masing-masing dashboard dengan perintah:

### Social Media Engagement Dashboard

```bash
streamlit run dashboard_social_media_engagement.py
```

### COVID-19 Dashboard

```bash
streamlit run dashboard_covid19_united_states_view.py
```

Setelah dijalankan, buka browser di `http://localhost:8501`

---

## Output Naming

Format nama file output:

- Untuk soal 1: `visualisasi_soal1_[nomor].[format]` (misal: `visualisasi_soal1_1.png`)
- Untuk soal 2: `analisis_soal2_[subbagian].[format]` (misal: `analisis_soal2_2a.docx`)

---

## Struktur Proyek

```
data insight uas submission/
├── setup.sh                           # Setup script
├── requirements.txt                   # Dependencies
├── dashboard_social_media_engagement.py    # Soal 1 - Social Media Engagement Dashboard (10 visualisasi)
├── dashboard_covid19_united_states_view.py # Soal 2 - COVID-19 Dashboard (analisis 2a-2e)
├── docs/                            # Documentation
│   └── social_media_engagement_analysis_report.md # Laporan analisis mendalam soal 1
├── config/                          # Configuration files
├── database/                        # Database files
│   └── data/                        # Folder untuk menyimpan dataset (social_media_engagement1.csv)
├── docs/                            # Documentation
├── images/                          # Images and visualizations
├── scripts/                         # Utility scripts
├── src/                             # Source code
├── tests/                           # Test files
├── .gitignore                       # Git ignore patterns
└── README.md                        # This file
```

---

## Dependencies

Proyek ini menggunakan library berikut:

- streamlit: Framework dashboard interaktif
- pandas: Data manipulation
- numpy: Numerical computing
- plotly: Interactive visualizations
- matplotlib: Static visualizations
- seaborn: Statistical visualizations
- altair: Additional visualization library
- requests: Data loading from various sources
- python-dotenv: Environment variable management
- tqdm: Progress bar utilities
- jupyter: Notebook support

---

## Catatan Penting

- Semua file harus berada di root directory (tidak ada subfolder)
- Dashboard dibuat menggunakan Streamlit untuk kemudahan deployment
- Soal 1: Dashboard Social Media Engagement memiliki **10 visualisasi** interaktif:
  1. Distribusi Metrik Engagement
  2. Perbandingan Kinerja Platform Media Sosial
  3. Efektivitas Jenis Postingan
  4. Korelasi Antar Metrik Engagement
  5. Tren Engagement Berdasarkan Hari dalam Seminggu
  6. Tren Engagement Harian (Time Series)
  7. Scatter Plot - Hubungan Antar Metrik Engagement
  8. Box Plot - Distribusi Engagement per Platform
  9. Violin Plot - Distribusi Engagement per Hari
  10. 3D Scatter Plot - Hubungan Tiga Dimensi Metrik Engagement
- Soal 2: Dashboard COVID-19 United States View mencakup analisis 2a-2e:
  - 2a. Insight dari dashboard
  - 2b. Target user
  - 2c. Elemen desain
  - 2d. Hambatan dan solusi
  - 2e. Rekomendasi
- Dataset untuk soal 1 harus ditempatkan di `database/data/social_media_engagement1.csv`
- Dashboard memiliki fitur filter interaktif untuk platform dan jenis postingan
- Laporan analisis mendalam tersedia di `docs/social_media_engagement_analysis_report.md`

---

**Last Updated**: December 2025  
**Course**: Data Insight UAS Submission
