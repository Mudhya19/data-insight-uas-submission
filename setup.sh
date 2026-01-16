#!/bin/bash

# ============================================================================
# Setup Script untuk Data Insight UAS Submission
# Nama Project: Data Insight UAS - Social Media Engagement & COVID-19 Dashboard
# Deskripsi: Inisialisasi environment dan struktur project flat root
# Author: Data Insight Student
# Date: December 2025
# ============================================================================

set -e  # Exit jika ada error

# Color codes untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNGSI HELPER
# ============================================================================

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# ============================================================================
# TAHAP 1: CEK PREREQUISITES
# ============================================================================

print_header "TAHAP 1: Cek Prerequisites"

# Cek Python installation
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
else
    # Try alternative method for Windows
    if command -v py &> /dev/null; then
        PYTHON_CMD="py"
        PYTHON_VERSION=$(py --version 2>&1 | awk '{print $2}')
    else
        print_error "Python tidak terinstall. Silakan install Python 3.9 atau lebih tinggi."
        exit 1
    fi
fi

print_success "Python $PYTHON_VERSION terdeteksi"

# Cek pip installation
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    # Try using Python to run pip
    if $PYTHON_CMD -m pip --version > /dev/null 2>&1; then
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        print_error "pip tidak terinstall. Silakan install pip."
        exit 1
    fi
fi

print_success "pip terdeteksi"

# Cek git installation
if ! command -v git &> /dev/null; then
    print_info "Git tidak terinstall. Beberapa fitur akan terbatas."
else
    print_success "Git terdeteksi"
fi

# ============================================================================
# TAHAP 2: BUAT STRUKTUR DIREKTORI MINIMAL (FLAT ROOT)
# ============================================================================

print_header "TAHAP 2: Membuat Struktur Flat Root Project"

PROJECT_NAME="Data Insight UAS Submission"
PROJECT_DIR=$(pwd)

# Hanya buat direktori yang diperlukan
DIRS=(
    ".venv"
    "config"
    "database"
    "docs"
    "images"
    "scripts"
    "src"
    "tests"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$PROJECT_DIR/$dir"
    if [ $? -eq 0 ]; then
        print_success "Direktori dibuat: $dir"
    else
        print_error "Gagal membuat direktori: $dir"
        exit 1
    fi
done

# ============================================================================
# TAHAP 3: SETUP PYTHON VIRTUAL ENVIRONMENT
# ============================================================================

print_header "TAHAP 3: Setup Python Virtual Environment"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]] || [[ "$OS" == "Windows_NT" ]]; then
        echo "windows"
    else
        echo "unix"
    fi
}

OS_TYPE=$(detect_os)

# Check if virtual environment exists properly
if [ "$OS_TYPE" = "windows" ]; then
    # Windows
    if [ -f ".venv/Scripts/activate" ]; then
        print_info "Virtual environment Windows sudah ada. Menggunakan existing environment..."
    else
        print_info "Membuat virtual environment Windows..."
        # For Windows, try different approaches to avoid the alias issue
        if [ "$PYTHON_CMD" = "py" ]; then
            py -m venv .venv 2>/dev/null || python -m venv .venv
        else
            $PYTHON_CMD -m venv .venv 2>/dev/null || python -m venv .venv
        fi
        print_success "Virtual environment Windows dibuat"
    fi
    source .venv/Scripts/activate
else
    # Unix/Linux/macOS
    if [ -f ".venv/bin/activate" ]; then
        print_info "Virtual environment Unix sudah ada. Menggunakan existing environment..."
    else
        print_info "Membuat virtual environment Unix..."
        $PYTHON_CMD -m venv .venv
        print_success "Virtual environment Unix dibuat"
    fi
    source .venv/bin/activate
fi
print_success "Virtual environment diaktifkan"

# Upgrade pip, setuptools, wheel
print_info "Upgrade pip, setuptools, dan wheel..."
if [ "$OS_TYPE" = "windows" ]; then
    # For Windows, use Python directly to avoid some issues
    python -m pip install --upgrade pip setuptools wheel || echo "Lanjutkan meskipun ada error upgrade pip"
else
    $PIP_CMD install --upgrade pip setuptools wheel
fi
print_success "pip, setuptools, dan wheel di-upgrade"

# ============================================================================
# TAHAP 4: INSTALL DEPENDENCIES
# ============================================================================

print_header "TAHAP 4: Install Dependencies"

# Buat requirements.txt dengan fokus pada dashboard data insight
cat > requirements.txt << 'EOF'
# Dashboard & Web Framework
streamlit
plotly

# Data Processing
pandas
numpy

# Data Visualization
matplotlib
seaborn
altair

# Data Loading & Sources
requests

# Utilities
python-dotenv
tqdm

# Jupyter & Notebooks
jupyter
EOF

print_success "requirements.txt dibuat"

# Install dependencies
print_info "Menginstall dependencies (ini mungkin memakan waktu beberapa menit)..."
if [ "$OS_TYPE" = "windows" ]; then
    # For Windows, install packages one by one to handle errors better
    while read requirement; do
        # Skip empty lines and comments
        if [[ -z "$requirement" || "$requirement" =~ ^[[:space:]]*# ]]; then
            continue
        fi
        
        print_info "Menginstall: $requirement"
        if $PIP_CMD install "$requirement" --only-binary=all; then
            print_success "✓ $requirement berhasil diinstall"
        else
            print_error "✗ Gagal menginstall $requirement, mencoba tanpa batasan binary..."
            if $PIP_CMD install "$requirement"; then
                print_success "✓ $requirement berhasil diinstall (tanpa batasan binary)"
            else
                print_error "✗ Gagal menginstall $requirement (kemungkinan tidak kompatibel di Windows)"
            fi
        fi
    done < requirements.txt
else
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Semua dependencies berhasil diinstall"
    else
        print_error "Gagal menginstall beberapa dependencies"
        exit 1
    fi
fi

print_success "Dependencies selesai diinstall (dengan atau tanpa error)"

# ============================================================================
# TAHAP 5: BUAT FILE KONFIGURASI & TEMPLATE DASHBOARD
# ============================================================================

print_header "TAHAP 5: Buat File Dashboard Templates"

# Main Social Media Engagement Dashboard
cat > dashboard_social_media_engagement.py << 'EOF'
"""
Social Media Engagement Dashboard - Data Insight UAS
Soal 1: Dataset Social Media Engagement - 5 Visualisasi + Deskripsi Insight
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Social Media Engagement Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📊 Social Media Engagement Dashboard")
    
    st.markdown("""
    ## Dataset Social Media Engagement Analysis
    
    Dashboard ini menyajikan 5 visualisasi dari dataset Social Media Engagement
    beserta insight-insight yang dapat diambil dari data tersebut.
    """)
    
    # Sample data - replace with actual dataset loading
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"Dataset loaded successfully with shape: {df.shape}")
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head())
        
        st.subheader("Dataset Info")
        st.write(df.info())
        
        # Visualisasi 1: Distribution of Engagement Metrics
        st.header("Visualisasi 1: Distribusi Metrik Engagement")
        
        if len(df.columns) >= 3:  # Assuming at least 3 numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = px.histogram(df, x=numeric_cols[0], title=f"Distribusi {numeric_cols[0]}")
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    fig2 = px.histogram(df, x=numeric_cols[1], title=f"Distribusi {numeric_cols[1]}")
                    st.plotly_chart(fig2, use_container_width=True)
                
                st.markdown(f"""
                **Insight 1:**
                Deskripsi insight tentang distribusi metrik engagement dari {numeric_cols[0]} dan {numeric_cols[1]}.
                """)
        
        # Visualisasi 2: Correlation Heatmap
        st.header("Visualisasi 2: Korelasi Antar Variabel")
        
        if len(df.select_dtypes(include=[np.number]).columns) > 1:
            numeric_df = df.select_dtypes(include=[np.number])
            corr_matrix = numeric_df.corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Heatmap Korelasi Antar Variabel"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.markdown("""
            **Insight 2:**
            Deskripsi insight tentang hubungan korelasi antar variabel dalam dataset.
            """)
        
        # Visualisasi 3: Trend Over Time (if date column exists)
        st.header("Visualisasi 3: Tren Metrik Engagement")
        
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        if date_cols:
            # Assuming first date column for time series
            time_col = date_cols[0]
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 1:
                fig_trend = px.line(df, x=time_col, y=numeric_cols[0], title=f"Tren {numeric_cols[0]} Seiring Waktu")
                st.plotly_chart(fig_trend, use_container_width=True)
                
                st.markdown("""
                **Insight 3:**
                Deskripsi insight tentang tren metrik engagement seiring waktu.
                """)
        else:
            st.info("Tidak ada kolom tanggal dalam dataset, visualisasi tren tidak dapat ditampilkan.")
        
        # Visualisasi 4: Scatter Plot
        st.header("Visualisasi 4: Hubungan Antar Metrik")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            col_x = st.selectbox("Pilih kolom X:", numeric_cols, index=0)
            col_y = st.selectbox("Pilih kolom Y:", numeric_cols, index=min(1, len(numeric_cols)-1))
            
            fig_scatter = px.scatter(df, x=col_x, y=col_y, title=f"Scatter Plot: {col_x} vs {col_y}")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown("""
            **Insight 4:**
            Deskripsi insight tentang hubungan antara dua metrik yang ditampilkan dalam scatter plot.
            """)
        
        # Visualisasi 5: Box Plot
        st.header("Visualisasi 5: Distribusi Metrik Berdasarkan Kategori")
        
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            cat_col = st.selectbox("Pilih kolom kategorikal:", categorical_cols)
            num_col = st.selectbox("Pilih kolom numerik:", numeric_cols)
            
            fig_box = px.box(df, x=cat_col, y=num_col, title=f"Box Plot: {num_col} Berdasarkan {cat_col}")
            st.plotly_chart(fig_box, use_container_width=True)
            
            st.markdown("""
            **Insight 5:**
            Deskripsi insight tentang distribusi metrik berdasarkan kategori.
            """)
        else:
            st.info("Tidak cukup kolom kategorikal atau numerik untuk box plot.")
    
    else:
        st.info("Silakan upload file CSV untuk memulai analisis.")

if __name__ == "__main__":
    main()
EOF

print_success "dashboard_social_media_engagement.py dibuat"

# Main COVID-19 Dashboard
cat > dashboard_covid19_united_states_view.py << 'EOF'
"""
COVID-19 United States Dashboard - Data Insight UAS
Soal 2: Analisis 2a-2e (insight, target user, elemen desain, hambatan, rekomendasi)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="COVID-19 United States Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🦠 COVID-19 United States Dashboard")
    
    st.markdown("""
    ## COVID-19 United States View Analysis
    
    Dashboard ini menyajikan analisis COVID-19 di Amerika Serikat dengan fokus pada:
    - Insight (Analisis 2a)
    - Target User (Analisis 2b)
    - Elemen Desain (Analisis 2c)
    - Hambatan dan Solusi (Analisis 2d)
    - Rekomendasi (Analisis 2e)
    """)
    
    # Upload data
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a COVID-19 CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"COVID-19 dataset loaded successfully with shape: {df.shape}")
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head())
        
        # Sample visualization - replace with actual COVID-19 data analysis
        st.header("COVID-19 Cases Visualization")
        
        # Prepare sample data if needed
        if 'date' in df.columns and 'cases' in df.columns:
            fig_cases = px.line(df, x='date', y='cases', title="Tren Kasus COVID-19")
            st.plotly_chart(fig_cases, use_container_width=True)
        else:
            # Create sample data for demonstration
            dates = pd.date_range(start='2020-01-01', periods=365, freq='D')
            cases = np.random.normal(loc=1000, scale=300, size=len(dates)).cumsum()
            cases = np.abs(cases)  # Ensure positive values
            
            sample_df = pd.DataFrame({'date': dates, 'cases': cases})
            fig_cases = px.line(sample_df, x='date', y='cases', title="Contoh Tren Kasus COVID-19 (Simulasi)")
            st.plotly_chart(fig_cases, use_container_width=True)
    
    else:
        st.info("Silakan upload file CSV dataset COVID-19 untuk memulai analisis.")
    
    # Analysis Section
    st.header("Analisis Dashboard COVID-19")
    
    # 2a - Insight
    st.subheader("2a. Insight dari Dashboard")
    st.markdown("""
    - **Tren Penyebaran**: Visualisasi garis menunjukkan pola penyebaran COVID-19 seiring waktu, 
      memungkinkan identifikasi gelombang pandemi dan efektivitas intervensi.
    
    - **Perbandingan Regional**: Heatmap atau peta choropleth memperlihatkan distribusi kasus 
      secara geografis, membantu mengidentifikasi hotspots dan daerah yang perlu perhatian lebih.
    
    - **Hubungan Antarmetrik**: Scatter plot antara kasus, kematian, dan tingkat vaksinasi 
      menunjukkan korelasi penting untuk pengambilan keputusan.
    
    - **Efektivitas Intervensi**: Perbandingan sebelum dan sesudah penerapan kebijakan 
      memungkinkan evaluasi dampak dari berbagai intervensi kesehatan masyarakat.
    """)
    
    # 2b - Target User
    st.subheader("2b. Target User Dashboard")
    st.markdown("""
    - **Pembuat Kebijakan**: Pejabat pemerintah yang membutuhkan data untuk membuat 
      keputusan strategis terkait kesehatan masyarakat.
    
    - **Profesional Kesehatan**: Dokter, perawat, dan tenaga medis yang perlu memahami 
      tren lokal untuk persiapan kapasitas rumah sakit.
    
    - **Peneliti dan Akademisi**: Ilmuwan data dan epidemiolog yang ingin menganalisis 
      pola penyebaran dan faktor-faktor yang mempengaruhi.
    
    - **Masyarakat Umum**: Warga yang ingin tetap terinformasi tentang situasi 
      COVID-19 di wilayah mereka dan nasional.
    """)
    
    # 2c - Elemen Desain
    st.subheader("2c. Elemen Desain Dashboard")
    st.markdown("""
    - **Visualisasi Multi-Dimensi**: Kombinasi grafik garis, heatmap, dan peta 
      untuk menyajikan data dalam berbagai perspektif.
    
    - **Filter Interaktif**: Slider tanggal, pemilihan wilayah, dan jenis metrik 
      untuk eksplorasi data yang fleksibel.
    
    - **Real-time Updates**: Integrasi dengan sumber data langsung untuk informasi 
      yang selalu terkini.
    
    - **Responsif**: Desain yang adaptif untuk berbagai ukuran layar dan perangkat.
    
    - **Legenda dan Informasi Kontekstual**: Penjelasan yang jelas tentang 
      makna warna, simbol, dan metrik yang digunakan.
    """)
    
    # 2d - Hambatan dan Solusi
    st.subheader("2d. Hambatan dan Solusi")
    st.markdown("""
    - **Kualitas Data**: Data COVID-19 sering tidak lengkap atau tidak konsisten 
      antar wilayah. Solusi: Gunakan teknik data cleaning dan imputasi yang robust.
    
    - **Privasi**: Perlindungan data individu sangat penting. Solusi: Agregasi 
      data hingga tingkat yang aman dan sesuai regulasi.
    
    - **Update Real-time**: Keterlambatan dalam pelaporan data. Solusi: Otomatisasi 
      proses pengumpulan data dan integrasi API.
    
    - **Literasi Data**: Tantangan dalam interpretasi data oleh pengguna umum. 
      Solusi: Sediakan penjelasan kontekstual dan panduan penggunaan.
    """)
    
    # 2e - Rekomendasi
    st.subheader("2e. Rekomendasi")
    st.markdown("""
    - **Peningkatan Akurasi Prediksi**: Gunakan model machine learning untuk 
      memprediksi gelombang berikutnya berdasarkan data historis dan faktor eksternal.
    
    - **Integrasi Data Multisumber**: Gabungkan data kesehatan, demografi, dan 
      mobilitas untuk analisis yang lebih komprehensif.
    
    - **Personalisasi Informasi**: Berikan informasi yang relevan dengan lokasi 
      spesifik pengguna dan faktor risiko pribadi.
    
    - **Aksesibilitas**: Pastikan dashboard dapat diakses oleh pengguna dengan 
      berbagai kemampuan, termasuk dukungan untuk pembaca layar.
    """)
    
    # Sample COVID-19 visualizations
    st.header("Contoh Visualisasi COVID-19")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sample bar chart
        states = ['California', 'Texas', 'Florida', 'New York', 'Illinois']
        cases = [800000, 750000, 650000, 550000, 450000]
        deaths = [10000, 12000, 8000, 9000, 7000]
        
        sample_data = pd.DataFrame({
            'State': states,
            'Cases': cases,
            'Deaths': deaths
        })
        
        fig_bar = px.bar(sample_data, x='State', y='Cases', title="Contoh Kasus per Negara Bagian (Simulasi)")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Sample scatter plot
        fig_scatter = px.scatter(sample_data, x='Cases', y='Deaths', 
                                color='State', title="Hubungan Kasus vs Kematian",
                                hover_data=['State'])
        st.plotly_chart(fig_scatter, use_container_width=True)

if __name__ == "__main__":
    main()
EOF

print_success "dashboard_covid19_united_states_view.py dibuat"

# .env
cat > .env << 'EOF'
# Configuration for Data Insight UAS Project

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info

# Data Configuration
DATA_PATH=./data
OUTPUT_PATH=./output

# Debug Mode
DEBUG=False
EOF

print_success ".env dibuat"

# config.py
cat > config/config.py << 'EOF'
"""
Configuration module untuk University Dashboard
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    APP_TITLE = os.getenv("APP_TITLE", "University Analytics Dashboard")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
class DatabaseConfig:
    """Database configuration"""
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", "./database/university.db")
    
class StreamlitConfig:
    """Streamlit-specific configuration"""
    SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
    LOGGER_LEVEL = os.getenv("STREAMLIT_LOGGER_LEVEL", "info")

class DataConfig:
    """Data configuration"""
    DATA_SOURCE = os.getenv("DATA_SOURCE", "local")
    DATA_PATH = os.getenv("DATA_PATH", "./database/data")
EOF

print_success "config/config.py dibuat"

# .gitignore
cat > .gitignore << 'EOF'
# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Streamlit
.streamlit/
cache/

# Database
*.db
*.sqlite
*.sqlite3

# Data files
*.csv
*.xlsx
*.json

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Output
output/
exports/
*.png
*.jpg
*.jpeg

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
EOF

print_success ".gitignore dibuat"

# ============================================================================
# TAHAP 6: BUAT DOCUMENTATION FILES
# ============================================================================

print_header "TAHAP 6: Buat Documentation Files"

# README
cat > README.md << 'EOF'
# Data Insight UAS Submission (Flat Root)

Submission UAS Mata Kuliah **Data Insight** (Take Home) dengan 2 deliverable utama:  
1) **Soal 1** — Dataset Social Media Engagement: buat **5 visualisasi** + deskripsi insight.  
2) **Soal 2** — Dashboard COVID-19 United States View: analisis **2a–2e** (insight, target user, elemen desain, hambatan, rekomendasi).

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
- Untuk soal 2: `analisis_soal2_[subbagian].[format]` (misal: `analisis_soal2_2a.docx`

---

## Struktur Proyek

```
data insight uas submission/
├── setup.sh                           # Setup script
├── requirements.txt                   # Dependencies
├── dashboard_social_media_engagement.py    # Soal 1
├── dashboard_covid19_united_states_view.py # Soal 2
├── config/                          # Configuration files
├── database/                        # Database files
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

---

## Catatan Penting

- Semua file harus berada di root directory (tidak ada subfolder)
- Dashboard dibuat menggunakan Streamlit untuk kemudahan deployment
- Kedua dashboard telah dilengkapi dengan template sesuai spesifikasi soal
- Data bisa diupload melalui interface dashboard

---

**Last Updated**: December 2025  
**Course**: Data Insight UAS Submission
EOF

print_success "README.md dibuat"

# ============================================================================
# TAHAP 7: BUAT REQUIREMENTS DAN SETUP SUMMARIES
# ============================================================================

print_header "TAHAP 7: Finalisasi Setup Files"

# Create a summary file
cat > SETUP_SUMMARY.txt << 'EOF'
================================================================================
DATA INSIGHT UAS SETUP SUMMARY
================================================================================

Setup Date: $(date)
Setup Location: $(pwd)

PROJECT STRUCTURE CREATED:
✓ .venv/                                    - Python virtual environment
✓ config/                                   - Configuration files
✓ database/                                 - Database files
✓ docs/                                     - Documentation
✓ images/                                   - Images and visualizations
✓ scripts/                                  - Utility scripts
✓ src/                                      - Source code
✓ tests/                                    - Test files

FILES CREATED:
✓ requirements.txt                          - Python dependencies
✓ dashboard_social_media_engagement.py     - Soal 1: Social Media Engagement Dashboard
✓ dashboard_covid19_united_states_view.py  - Soal 2: COVID-19 Dashboard
✓ .env                                     - Environment configuration
✓ config/config.py                         - Configuration module
✓ .gitignore                               - Git ignore patterns
✓ README.md                                - Main documentation
✓ setup.sh                                 - Setup script
✓ SETUP_SUMMARY.txt                        - This summary

NEXT STEPS:
1. Activate virtual environment: source .venv/bin/activate
2. Install dependencies: pip install -r requirements.txt
3. Run social media dashboard: streamlit run dashboard_social_media_engagement.py
4. Run covid dashboard: streamlit run dashboard_covid19_united_states_view.py
5. Open browser: http://localhost:8501

USEFUL COMMANDS:
- Run social media dashboard: streamlit run dashboard_social_media_engagement.py
- Run covid dashboard: streamlit run dashboard_covid19_united_states_view.py
- Install/update dependencies: pip install -r requirements.txt
- Activate venv: source .venv/bin/activate (Linux/Mac) or .venv\Scripts\activate (Windows)
- Deactivate venv: deactivate

DOCUMENTATION:
- README.md - Project overview and quick start
- Dashboard files contain detailed analysis as per assignment requirements

For more information, see README.md

================================================================================
EOF

cat SETUP_SUMMARY.txt

print_success "SETUP_SUMMARY.txt dibuat"

# ============================================================================
# FINISH
# ============================================================================
print_header "✅ SETUP SELESAI!"

echo -e "${GREEN}Project '${PROJECT_NAME}' berhasil di-setup dengan struktur flat root!${NC}\n"

echo "Next Steps:"
echo "1. Activate virtual environment:"
echo -e "   ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "2. Run social media dashboard:"
echo -e "   ${YELLOW}streamlit run dashboard_social_media_engagement.py${NC}"
echo ""
echo "3. Run COVID-19 dashboard:"
echo -e "   ${YELLOW}streamlit run dashboard_covid19_united_states_view.py${NC}"
echo ""
echo "4. Open browser: http://localhost:8501"
echo ""
echo -e "${BLUE}Happy coding! 🚀${NC}"
echo ""
