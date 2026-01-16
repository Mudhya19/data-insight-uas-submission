"""
Social Media Engagement Dashboard - Data Insight UAS
Soal 1: Dataset Social Media Engagement - 6 Visualisasi + Deskripsi Insight
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors

def apply_skyblues_by_value(values, patches):
    """
    Nilai terbesar → warna paling pekat (gelap)
    Skema warna: Sky Blue
    Aman dari konflik variabel
    """
    cmap = plt.colormaps.get_cmap('Blues')  # Sky blue → biru tua
    norm = mcolors.Normalize(vmin=min(values), vmax=max(values))

    for v, p in zip(values, patches):
        p.set_facecolor(cmap(norm(v)))
        p.set_edgecolor('black')

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
    
    Dashboard ini menyajikan 6 visualisasi dari dataset Social Media Engagement
    beserta insight-insight yang dapat diambil dari data tersebut.
    """)
    
    # Load the dataset from the specified path
    @st.cache_data
    def load_data():
        df = pd.read_csv('database/data/social_media_engagement1.csv')
        # Convert post_time to datetime
        df['post_time'] = pd.to_datetime(df['post_time'])
        # Convert post_day to categorical
        df['post_day'] = df['post_day'].astype('category')
        # Explicitly set category order to avoid pandas deprecation warning later
        df['post_day'] = pd.Categorical(df['post_day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
        return df
    
    df = load_data()
    st.success(f"Dataset loaded successfully with shape: {df.shape}")
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    
    
    # Feature 1: Platform selection filter
    st.sidebar.header("Filters")
    platforms = st.sidebar.multiselect(
        'Select Platforms:',
        options=df['platform'].unique(),
        default=df['platform'].unique()
    )
    
    post_types = st.sidebar.multiselect(
        'Select Post Types:',
        options=df['post_type'].unique(),
        default=df['post_type'].unique()
    )
    
    # Apply filters
    filtered_df = df[(df['platform'].isin(platforms)) & (df['post_type'].isin(post_types))]
    
    st.subheader(f"Filtered Dataset ({len(filtered_df)} records)")
    st.dataframe(filtered_df.head())
    
    
    # Visualisasi 1: Distribution of Engagement Metrics with Consistent Sky Blue Palette
    st.header("Visualisasi 1: Distribusi Metrik Engagement")
    
    if len(filtered_df.columns) >= 3:
        numeric_cols = ['likes', 'comments', 'shares']  # Focus on the key engagement metrics
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Create histogram with sky blue color gradient based on value magnitude
            fig1 = go.Figure()
            hist_data = np.histogram(filtered_df['likes'], bins=20)
            values = hist_data[0]
            
            # Normalize values to use with Blues colormap
            norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
            cmap = plt.colormaps.get_cmap('Blues')
            
            colors = [mcolors.to_hex(cmap(norm(v))) for v in values]
            
            fig1.add_trace(go.Bar(
                x=hist_data[1][:-1],
                y=values,
                marker_color=colors,
                width=np.diff(hist_data[1])[0]
            ))
            fig1.update_layout(
                title="Distribusi Jumlah Likes",
                xaxis_title="Jumlah Likes",
                yaxis_title="Frekuensi"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Create histogram with sky blue color gradient based on value magnitude
            fig2 = go.Figure()
            hist_data = np.histogram(filtered_df['comments'], bins=20)
            values = hist_data[0]
            
            # Normalize values to use with Blues colormap
            norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
            cmap = plt.colormaps.get_cmap('Blues')
            
            colors = [mcolors.to_hex(cmap(norm(v))) for v in values]
            
            fig2.add_trace(go.Bar(
                x=hist_data[1][:-1],
                y=values,
                marker_color=colors,
                width=np.diff(hist_data[1])[0]
            ))
            fig2.update_layout(
                title="Distribusi Jumlah Comments",
                xaxis_title="Jumlah Comments",
                yaxis_title="Frekuensi"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            # Create histogram with sky blue color gradient based on value magnitude
            fig3 = go.Figure()
            hist_data = np.histogram(filtered_df['shares'], bins=20)
            values = hist_data[0]
            
            # Normalize values to use with Blues colormap
            norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
            cmap = plt.colormaps.get_cmap('Blues')
            
            colors = [mcolors.to_hex(cmap(norm(v))) for v in values]
            
            fig3.add_trace(go.Bar(
                x=hist_data[1][:-1],
                y=values,
                marker_color=colors,
                width=np.diff(hist_data[1])[0]
            ))
            fig3.update_layout(
                title="Distribusi Jumlah Shares",
                xaxis_title="Jumlah Shares",
                yaxis_title="Frekuensi"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("""
        **Insight 1:**
        Distribusi metrik engagement menunjukkan bahwa sebagian besar postingan mendapatkan jumlah likes, comments, dan shares yang bervariasi. 
        Dengan menggunakan histogram dengan warna biru (skala Blues) yang semakin pekat sesuai nilai frekuensi data, kita bisa melihat bagaimana penyebaran masing-masing metrik, apakah cenderung normal, skewed, atau memiliki outlier. 
        Ini membantu kita memahami pola umum keterlibatan pengguna di platform media sosial.
        """)
    
    # Visualisasi 2: Platform Performance Comparison with Consistent Sky Blue Palette
    st.header("Visualisasi 2: Perbandingan Kinerja Platform Media Sosial")
    
    platform_metrics = filtered_df.groupby('platform')[['likes', 'comments', 'shares']].mean().reset_index()
    
    # Combine all values to normalize across all metrics for consistent coloring
    all_values = list(platform_metrics['likes']) + list(platform_metrics['comments']) + list(platform_metrics['shares'])
    norm = mcolors.Normalize(vmin=min(all_values), vmax=max(all_values))
    cmap = plt.colormaps.get_cmap('Blues')
    
    fig_platform = go.Figure()
    
    fig_platform.add_trace(go.Bar(
        x=platform_metrics['platform'],
        y=platform_metrics['likes'],
        name='Rata-rata Likes',
        marker_color=[mcolors.to_hex(cmap(norm(val))) for val in platform_metrics['likes']]
    ))
    
    fig_platform.add_trace(go.Bar(
        x=platform_metrics['platform'],
        y=platform_metrics['comments'],
        name='Rata-rata Comments',
        marker_color=[mcolors.to_hex(cmap(norm(val))) for val in platform_metrics['comments']]
    ))
    
    fig_platform.add_trace(go.Bar(
        x=platform_metrics['platform'],
        y=platform_metrics['shares'],
        name='Rata-rata Shares',
        marker_color=[mcolors.to_hex(cmap(norm(val))) for val in platform_metrics['shares']]
    ))
    
    fig_platform.update_layout(
        title="Perbandingan Rata-rata Metrik Engagement Berdasarkan Platform",
        xaxis_title="Platform",
        yaxis_title="Jumlah Rata-rata",
        barmode='group'
    )
    
    st.plotly_chart(fig_platform, use_container_width=True)
    
    st.markdown("""
    **Insight 2:**
    Visualisasi ini menunjukkan perbedaan kinerja antar platform media sosial dalam hal engagement. 
    Dengan menggunakan bar chart grouped dalam skema warna biru (Blues) yang konsisten dan semakin gelap untuk nilai yang lebih tinggi, kita bisa membandingkan rata-rata jumlah likes, comments, dan shares 
    untuk setiap platform secara langsung. Ini membantu mengidentifikasi platform mana yang paling efektif 
    dalam meningkatkan engagement pengguna.
    """)
    
    # Visualisasi 3: Post Type Effectiveness with Consistent Sky Blue Palette
    st.header("Visualisasi 3: Efektivitas Jenis Postingan")
    
    post_type_metrics = filtered_df.groupby('post_type')[['likes', 'comments', 'shares']].mean().reset_index()
    
    # Melt the dataframe for easier plotting
    post_type_metrics_melted = post_type_metrics.melt(id_vars=['post_type'], 
                                                      value_vars=['likes', 'comments', 'shares'],
                                                      var_name='metric', 
                                                      value_name='average')
    
    # Normalize all values for consistent coloring
    all_values = post_type_metrics_melted['average'].tolist()
    norm = mcolors.Normalize(vmin=min(all_values), vmax=max(all_values))
    cmap = plt.colormaps.get_cmap('Blues')
    
    # Assign colors based on the normalized values
    colors = [mcolors.to_hex(cmap(norm(val))) for val in all_values]
    
    fig_post_type = go.Figure()
    
    for metric in post_type_metrics_melted['metric'].unique():
        metric_data = post_type_metrics_melted[post_type_metrics_melted['metric'] == metric]
        fig_post_type.add_trace(go.Bar(
            name=metric,
            x=metric_data['post_type'],
            y=metric_data['average'],
            marker_color=[mcolors.to_hex(cmap(norm(val))) for val in metric_data['average']]
        ))
    
    fig_post_type.update_layout(
        title="Rata-rata Engagement Berdasarkan Jenis Postingan",
        xaxis_title="Jenis Postingan",
        yaxis_title="Jumlah Rata-rata",
        barmode='group'
    )
    
    st.plotly_chart(fig_post_type, use_container_width=True)
    
    st.markdown("""
    **Insight 3:**
    Grafik ini menunjukkan seberapa efektif berbagai jenis postingan (image, video, carousel, dll.) dalam 
    menghasilkan engagement. Dengan memvisualisasikan data ini dalam bentuk grouped bar chart dengan skema warna biru (Blues) yang konsisten dan semakin gelap untuk nilai yang lebih tinggi, 
    kita bisa melihat jenis konten mana yang paling banyak mendapatkan likes, comments, dan shares, sehingga bisa 
    membantu dalam merancang strategi konten yang lebih efektif.
    """)
    
    # Visualisasi 4: Correlation Heatmap with Consistent Sky Blue Palette
    st.header("Visualisasi 4: Korelasi Antar Metrik Engagement")
    
    numeric_df = filtered_df[['likes', 'comments', 'shares']].corr()
    
    fig_corr = px.imshow(
        numeric_df,
        text_auto=True,
        aspect="auto",
        title="Heatmap Korelasi Antar Metrik Engagement",
        color_continuous_scale='Blues'  # Use blues color scale
    )
    fig_corr.update_layout(
        height=500
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("""
    **Insight 4:**
    Heatmap korelasi ini menunjukkan hubungan antara berbagai metrik engagement (likes, comments, shares) dengan menggunakan skala warna biru (Blues) yang konsisten. 
    Nilai korelasi yang tinggi (lebih gelap) menunjukkan bahwa ketika satu metrik tinggi, maka metrik lainnya juga cenderung tinggi. 
    Ini membantu memahami apakah metrik-metrik ini saling berkaitan dan bisa digunakan sebagai indikator engagement secara keseluruhan.
    """)
    
    # Visualisasi 5: Engagement Trend by Day of Week with Line Chart
    st.header("Visualisasi 5: Tren Engagement Berdasarkan Hari dalam Seminggu")
    
    # Group by day of week to get average engagement metrics
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_engagement = filtered_df.groupby('post_day', observed=False)[['likes', 'comments', 'shares']].mean().reindex(day_order)
    
    # Prepare data for line chart
    days = day_engagement.index
    likes_data = day_engagement['likes']
    comments_data = day_engagement['comments']
    shares_data = day_engagement['shares']
    
    # Create line chart with consistent sky blue palette
    fig_trend = go.Figure()
    
    # Normalize all values for consistent coloring
    all_values = list(likes_data) + list(comments_data) + list(shares_data)
    norm = mcolors.Normalize(vmin=min(all_values), vmax=max(all_values))
    cmap = plt.colormaps.get_cmap('Blues')
    
    fig_trend.add_trace(go.Scatter(
        x=days,
        y=likes_data,
        mode='lines+markers',
        name='Rata-rata Likes',
        line=dict(color=mcolors.to_hex(cmap(norm(max(likes_data))))),
        marker=dict(color=[mcolors.to_hex(cmap(norm(val))) for val in likes_data])
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=days,
        y=comments_data,
        mode='lines+markers',
        name='Rata-rata Comments',
        line=dict(color=mcolors.to_hex(cmap(norm(max(comments_data))))),
        marker=dict(color=[mcolors.to_hex(cmap(norm(val))) for val in comments_data])
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=days,
        y=shares_data,
        mode='lines+markers',
        name='Rata-rata Shares',
        line=dict(color=mcolors.to_hex(cmap(norm(max(shares_data))))),
        marker=dict(color=[mcolors.to_hex(cmap(norm(val))) for val in shares_data])
    ))
    
    fig_trend.update_layout(
        title="Tren Rata-rata Engagement Berdasarkan Hari dalam Seminggu",
        xaxis_title="Hari dalam Seminggu",
        yaxis_title="Jumlah Rata-rata",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("""
    **Insight 5:**
    Visualisasi line chart ini menunjukkan tren engagement berdasarkan hari dalam seminggu.
    Dengan menggunakan line chart dalam skema warna biru (Blues) yang konsisten dan semakin gelap untuk nilai yang lebih tinggi,
    kita bisa mengamati pola engagement harian - kapan engagement tertinggi dan terendah terjadi.
    Ini sangat berguna untuk menentukan waktu optimal untuk memposting konten di media sosial.
    """)

    # Visualisasi 6: Time Series Engagement Trend with Enhanced Line Chart
    st.header("Visualisasi 6: Tren Engagement Harian (Time Series)")

    # Extract date part from datetime for daily aggregation
    filtered_df_with_date = filtered_df.copy()
    filtered_df_with_date['date_only'] = pd.to_datetime(filtered_df_with_date['post_time']).dt.date
    
    # Group by date to get daily totals
    daily_engagement = filtered_df_with_date.groupby('date_only')[['likes', 'comments', 'shares']].sum().reset_index()
    
    # Create time series line chart
    fig_timeseries = go.Figure()
    
    # Normalize all values for consistent coloring
    all_values_ts = list(daily_engagement['likes']) + list(daily_engagement['comments']) + list(daily_engagement['shares'])
    norm_ts = mcolors.Normalize(vmin=min(all_values_ts), vmax=max(all_values_ts))
    cmap_ts = plt.colormaps.get_cmap('Blues')
    
    fig_timeseries.add_trace(go.Scatter(
        x=pd.to_datetime(daily_engagement['date_only']).dt.strftime('%Y-%m-%d'),
        y=daily_engagement['likes'],
        mode='lines+markers',
        name='Total Likes Harian',
        line=dict(color=mcolors.to_hex(cmap_ts(norm_ts(max(daily_engagement['likes']))))),
        marker=dict(color=[mcolors.to_hex(cmap_ts(norm_ts(val))) for val in daily_engagement['likes']])
    ))
    
    fig_timeseries.add_trace(go.Scatter(
        x=pd.to_datetime(daily_engagement['date_only']).dt.strftime('%Y-%m-%d'),
        y=daily_engagement['comments'],
        mode='lines+markers',
        name='Total Comments Harian',
        line=dict(color=mcolors.to_hex(cmap_ts(norm_ts(max(daily_engagement['comments']))))),
        marker=dict(color=[mcolors.to_hex(cmap_ts(norm_ts(val))) for val in daily_engagement['comments']])
    ))
    
    fig_timeseries.add_trace(go.Scatter(
        x=pd.to_datetime(daily_engagement['date_only']).dt.strftime('%Y-%m-%d'),
        y=daily_engagement['shares'],
        mode='lines+markers',
        name='Total Shares Harian',
        line=dict(color=mcolors.to_hex(cmap_ts(norm_ts(max(daily_engagement['shares']))))),
        marker=dict(color=[mcolors.to_hex(cmap_ts(norm_ts(val))) for val in daily_engagement['shares']])
    ))
    
    fig_timeseries.update_layout(
        title="Tren Total Engagement Harian (Time Series)",
        xaxis_title="Tanggal",
        yaxis_title="Jumlah Total",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_timeseries, use_container_width=True)
    
    st.markdown("""
    **Insight 6:**
    Visualisasi time series ini menunjukkan tren engagement harian dari postingan media sosial.
    Dengan menggunakan line chart dalam skema warna biru (Blues) yang konsisten,
    kita bisa mengamati fluktuasi engagement harian sepanjang periode waktu yang tersedia dalam dataset.
    Ini membantu mengidentifikasi pola musiman atau periode puncak engagement.
    """)

    # Visualisasi 7: Scatter Plot - Engagement Metrics Correlation
    st.header("Visualisasi 7: Scatter Plot - Hubungan Antar Metrik Engagement")
    
    fig_scatter = px.scatter(
        filtered_df,
        x='likes',
        y='comments',
        size='shares',
        color='platform',
        hover_data=['post_type', 'post_day'],
        title='Hubungan antara Likes, Comments, dan Shares (dengan ukuran Shares)',
        labels={'likes': 'Jumlah Likes', 'comments': 'Jumlah Comments'},
        opacity=0.7
    )
    fig_scatter.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("""
    **Insight 7:**
    Scatter plot ini menunjukkan hubungan antara jumlah likes dan comments, dengan ukuran titik menunjukkan jumlah shares.
    Warna berbeda mewakili platform yang berbeda, memungkinkan kita untuk melihat pola antar-platform.
    Visualisasi ini membantu memahami apakah postingan dengan banyak likes cenderung juga mendapatkan banyak komentar.
    """)

    # Visualisasi 8: Box Plot - Distribusi Engagement per Platform
    st.header("Visualisasi 8: Box Plot - Distribusi Engagement per Platform")
    
    # Melt the dataframe for box plot
    box_plot_data = filtered_df.melt(
        id_vars=['platform'],
        value_vars=['likes', 'comments', 'shares'],
        var_name='metric',
        value_name='count'
    )
    
    fig_box = px.box(
        box_plot_data,
        x='platform',
        y='count',
        color='metric',
        title='Distribusi Metrik Engagement per Platform',
        labels={'platform': 'Platform', 'count': 'Jumlah', 'metric': 'Metrik'}
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("""
    **Insight 8:**
    Box plot ini menunjukkan distribusi metrik engagement (likes, comments, shares) untuk setiap platform.
    Visualisasi ini membantu memahami sebaran data, median, serta adanya outlier pada masing-masing platform.
    Kita dapat melihat platform mana yang memiliki distribusi engagement lebih tinggi secara keseluruhan.
    """)

    # Visualisasi 9: Violin Plot - Distribusi Engagement per Hari
    st.header("Visualisasi 9: Violin Plot - Distribusi Engagement per Hari dalam Seminggu")
    
    # Prepare data for violin plot
    violin_data = filtered_df.melt(
        id_vars=['post_day'],
        value_vars=['likes', 'comments', 'shares'],
        var_name='metric',
        value_name='count'
    )
    
    fig_violin = px.violin(
        violin_data,
        x='post_day',
        y='count',
        color='metric',
        box=True,
        points='all',
        title='Distribusi dan Density Metrik Engagement per Hari',
        labels={'post_day': 'Hari dalam Seminggu', 'count': 'Jumlah', 'metric': 'Metrik'},
        category_orders={'post_day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    )
    st.plotly_chart(fig_violin, use_container_width=True)
    
    st.markdown("""
    **Insight 9:**
    Violin plot ini menunjukkan distribusi dan kepadatan metrik engagement untuk setiap hari dalam seminggu.
    Selain menunjukkan distribusi seperti box plot, violin plot juga menunjukkan kepadatan data (density).
    Ini membantu memahami tidak hanya statistik deskriptif tetapi juga bentuk distribusi data secara keseluruhan.
    """)

    # Visualisasi 10: 3D Scatter Plot - Engagement Metrics Relationship
    st.header("Visualisasi 10: 3D Scatter Plot - Hubungan Tiga Dimensi Metrik Engagement")
    
    fig_3d = px.scatter_3d(
        filtered_df,
        x='likes',
        y='comments',
        z='shares',
        color='platform',
        title='Hubungan Tiga Dimensi antara Likes, Comments, dan Shares',
        labels={'likes': 'Jumlah Likes', 'comments': 'Jumlah Comments', 'shares': 'Jumlah Shares'},
        opacity=0.7
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("""
    **Insight 10:**
    3D scatter plot ini menunjukkan hubungan tiga dimensi antara metrik engagement: likes, comments, dan shares.
    Setiap titik mewakili sebuah postingan dengan warna yang berbeda menunjukkan platform.
    Visualisasi ini memberikan perspektif yang lebih komprehensif tentang hubungan kompleks antar metrik engagement.
    """)

if __name__ == "__main__":
    main()
