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
