""" PROJECT DESCRIPTION: 
PROJECT ini adalah Bike Sharing Analysis yang ditunjukkan dalam bentuk Dashboard menggunakan Streamlit.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    return pd.read_csv('dataset/hour.csv')

def create_daily_patterns(df):
    return df.groupby(['workingday', 'hr'])[['casual', 'registered', 'cnt']].mean()

def plot_daily_patterns(hourly_data, sample_size=None):
    """
    Plot daily patterns with optional sample size control
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Tambahkan Sample Size jika diberikan
    if sample_size:
        scale_factor = sample_size / hourly_data['cnt'].max()
        sampled_data = hourly_data.copy()
        for col in ['casual', 'registered', 'cnt']:
            sampled_data[col] = hourly_data[col] * scale_factor
    else:
        sampled_data = hourly_data
    
    # Plot untuk hari kerja
    sampled_data.loc[1]['casual'].plot(ax=ax1, color='blue', label='Casual')
    sampled_data.loc[1]['registered'].plot(ax=ax1, color='green', label='Registered')
    sampled_data.loc[1]['cnt'].plot(ax=ax1, color='red', linestyle='--', label='Total')
    ax1.set_title('Pola Penggunaan Sepeda pada Hari Kerja')
    ax1.set_xlabel('Jam')
    ax1.set_ylabel('Rata-rata Pengguna')
    ax1.grid(True)
    ax1.legend(loc='upper left')
    
    # Plot untuk hari libur
    sampled_data.loc[0]['casual'].plot(ax=ax2, color='blue', label='Casual')
    sampled_data.loc[0]['registered'].plot(ax=ax2, color='green', label='Registered')
    sampled_data.loc[0]['cnt'].plot(ax=ax2, color='red', linestyle='--', label='Total')
    ax2.set_title('Pola Penggunaan Sepeda pada Hari Libur')
    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Rata-rata Pengguna')
    ax2.grid(True)
    ax2.legend(loc='upper left')
    
    plt.tight_layout()
    return fig


def plot_weather_analysis(df):
    # Inisialisasi Waktu Periode dalam bentuk kategori
    df['time_period'] = pd.cut(df['hr'], 
                              bins=[0, 6, 12, 18, 24],
                              labels=['Subuh 0-6', 'Pagi 7-12', 'Siang 13-18', 'Malam 19-24'])
    
    # Kita buat 2 sub plot agar bisa ditunjukkan secara bersamaan (Basic dan Detailed Weather Analysis)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    #Plot Pertama: Basic weather boxplot
    sns.boxplot(data=df, x='weathersit', y='cnt', ax=ax1)
    ax1.set_title('Distribusi Penggunaan Sepeda Sewa berdasarkan Cuaca (Basic Analysis)')
    ax1.set_xlabel('Kondisi Cuaca (1:Clear, 2:Misty, 3:Light Rain, 4:Heavy Rain)')
    ax1.set_ylabel('Jumlah Pengguna')
    ax1.grid(True)
    
    #Plot Kedua: Detailed weather boxplot
    sns.boxplot(data=df, x='time_period', y='cnt', hue='weathersit', ax=ax2,
                palette=['green', 'yellow', 'orange', 'red'])
    ax2.set_title('Distribusi Pemakaian Sepeda Sewa berdasarkan Periode Waktu dan Cuaca')
    ax2.set_xlabel('Periode Waktu')
    ax2.set_ylabel('Jumlah Pengguna')
    ax2.legend(title='Kondisi Cuaca')
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

# FUNGSI MENGANALISIS POLA MUSIM 
def plot_seasonal_patterns(df, selected_season=None):
    seasons = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    
    if selected_season:
        # Single season plot
        fig, ax = plt.subplots(figsize=(12, 8))
        season_data = df[df['season'] == selected_season]
        sns.lineplot(data=season_data, x='hr', y='cnt', hue='workingday', ax=ax)
        ax.set_title(f'Penggunaan Sepeda Sewa - {seasons[selected_season]}')
        ax.grid(True)
        ax.legend(['Hari Libur', 'Hari Kerja'])
    else:
        # All seasons plot (2x2)
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        for season_num, (i, j) in zip(seasons.keys(), [(0,0), (0,1), (1,0), (1,1)]):
            season_data = df[df['season'] == season_num]
            sns.lineplot(data=season_data, x='hr', y='cnt', hue='workingday', ax=axes[i,j])
            axes[i,j].set_title(f'Penggunaan Sepeda Sewa - {seasons[season_num]}')
            axes[i,j].grid(True)
            axes[i,j].legend(['Hari Libur', 'Hari Kerja'])
    
    plt.tight_layout()
    return fig

def main():
    st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
    
    st.title("Analisis Penggunaan Sepeda")
    
    try:
        hour_df = load_data()
    except FileNotFoundError:
        st.error("Error: File 'hour.csv' tidak ditemukan!")
        return
    
    # Sidebar UI elements (Scrollable)
    st.sidebar.header("Filters")
    analysis_type = st.sidebar.selectbox(
        "Pilih Tipe Analisis",
        ["Pola Harian (24 jam)", "Pengaruh Cuaca", "Pola Musiman", "Dataset Source"]
    )
    
    if analysis_type == "Pola Harian (24 jam)":
        st.header("Pola Penggunaan Harian")
        
        # Add sample size slider
        max_records = int(hour_df['cnt'].max())
        sample_size = st.slider(
            "Jumlah Records",
            min_value=0,
            max_value=max_records,
            value=max_records,
            step=50
        )
        
        # Menampilkan informasi jumlah data yang ditampilkan
        st.info(f"Menampilkan data dengan {sample_size:,} records dari total {max_records:,} records")
        
        # Buat pola harian
        hourly_patterns = create_daily_patterns(hour_df)
        fig = plot_daily_patterns(hourly_patterns, sample_size=sample_size)
        st.pyplot(fig)
        
        # Menampilkan informasi tambahan
        if sample_size < max_records:
            st.write(f"Scale Factor: {(sample_size/max_records):.2%}")
            
        
        st.markdown("""
            **Insight:**
            1. Penggunaan Hari Kerja
            - **Peak Volume**: Mencapai maksimum tertinggi pada jam-jam sibuk
            - **Distribusi**: Tidak merata sepanjang hari
            - Pagi (07:00-09:00): Peak pertama 
            - Sore (17:00-19:00): Peak kedua
            2. Penggunaan Hari Libur
            - **Distribusi**: Lebih merata dan konsisten
            - Mulai meningkat: 10:00 pagi
            - Tetap tinggi hingga: 17:00 sore
            - **Volume**: Lebih rendah dari hari kerja
            - **Durasi**: Periode penggunaan aktif lebih panjang

            3. Perbandingan Karakteristik
                Hari Kerja:
            - Volume tinggi tapi tidak stabil
            - Pola penggunaan predictable
            - Fokus pada commuting

                Hari Libur:
            - Volume lebih rendah tapi stabil
            - Distribusi lebih merata
            - Dominan penggunaan rekreasional

            **Jawaban** 
            Terdapat perbedaan rata-rata penyewaan sepeda pada hari kerja sebesar 6.50% namun dari grafis pattern perbedaan pola tersebut menunjukkan bahwa pemakaian sepeda sewa lebih panjang di hari libur dibandingkan pemakaian sepeda di hari kerja. 

        """)
        
    elif analysis_type == "Pengaruh Cuaca":
        st.header("Analisis Pengaruh Cuaca")
        fig = plot_weather_analysis(hour_df)
        st.pyplot(fig)
        
        # Kalkulasi statistik untuk setiap cluster waktu-cuaca
        weather_time_clusters = hour_df.groupby(['time_period', 'weathersit'])['cnt'].agg([
            'mean',
            'count',
            'std'
        ]).round(2)
        
        st.markdown("""
        ### Kondisi Cuaca:
        1. Clear/Partly Cloudy (Green)
        2. Misty/Cloudy (Yellow)
        3. Light Rain/Snow (Orange)
        4. Heavy Rain/Snow (Red)
        
        ### Analisis Cluster Waktu-Cuaca:
        """)
        
        st.markdown("""
        # Analisis Lanjutan: Clustering Berbasis Waktu dan Cuaca

        ## Teknik Analisis yang Digunakan
        ### 1. Categorical Binning (Pengelompokan Kategorikal)
        - **Metode**: Manual clustering menggunakan `pd.cut()`
        - **Variabel**: Periode waktu (time_period)
        - **Pembagian**:
        - Subuh (00:00-06:00)
        - Pagi (07:00-12:00)
        - Siang (13:00-18:00)
        - Malam (19:00-24:00)

        ### 2. Time-Weather Clustering
        - **Metode**: Multi-dimensional grouping
        - **Variabel**: 
        - Periode waktu (time_period)
        - Kondisi cuaca (weathersit)
        - **Metrik**: mean, count, standard deviation

        ## Tujuan Analisis
        1. Memahami pola penggunaan berdasarkan periode waktu
        2. Mengukur dampak cuaca pada setiap periode waktu
        3. Mengidentifikasi peak hours di setiap kondisi cuaca

        ## Hasil Analisis

        ### 1. Pola Waktu-Cuaca
        - Penggunaan tertinggi: Pagi-Siang dengan cuaca cerah
        - Penggunaan terendah: Subuh-Malam dengan cuaca hujan
        - Variabilitas tertinggi: Periode Pagi (7-12)

        ### 2. Implikasi Bisnis
        - Alokasi sepeda optimal berdasarkan waktu dan cuaca
        - Strategi maintenance saat periode penggunaan rendah
        - Perencanaan staf berdasarkan prediksi kebutuhan

        ### 3. Insight Operasional
        - Fokus layanan pada periode pagi-siang
        - Antisipasi penurunan penggunaan saat cuaca buruk
        - Optimasi distribusi berdasarkan pola harian

        ## Manfaat Penerapan
        1. **Perencanaan Lebih Akurat**:
        - Prediksi kebutuhan per periode
        - Antisipasi dampak cuaca

        2. **Efisiensi Operasional**:
        - Distribusi sepeda optimal
        - Penggunaan sumber daya efektif

        3. **Peningkatan Layanan**:
        - Ketersediaan sepeda sesuai kebutuhan
        - Respons cepat terhadap perubahan cuaca """)
        
        st.dataframe(weather_time_clusters)
        
    elif analysis_type == "Pola Musiman":
        st.header("Analisis Pola Musiman")
        
        # Add season filter dalam bentuk dictionary
        season_options = {
            'Semua Musim': None,
            'Spring': 1,
            'Summer': 2,
            'Fall': 3,
            'Winter': 4
        }
        
        selected_season = st.selectbox(
            "Pilih Musim",
            options=list(season_options.keys())
        )
        
        # Konvesi nama musim ke angka
        season_num = season_options[selected_season]
        
        # Plot with selected season
        fig = plot_seasonal_patterns(hour_df, selected_season=season_num)
        st.pyplot(fig)
        
        # Show different insights based on selection
        if season_num:
            st.markdown(f"""
            ### Insight untuk {selected_season}:
            - Peak Hours: {hour_df[hour_df['season'] == season_num]['cnt'].max():.0f} pengguna
            - Rata-rata: {hour_df[hour_df['season'] == season_num]['cnt'].mean():.0f} pengguna
            """)
        else:
            st.markdown("""
            ### Insight Semua Musim:
            - Spring: Moderate usage, transitional pattern
            - Summer: High usage, extended daylight hours
            - Fall: Peak usage, optimal weather conditions
            - Winter: Lowest usage, weather dependent
            """)
        
        st.markdown("""
        ### Insight:
        # Analisis Musiman (Seasonal Analysis)

        ## Teknik Analisis
        ### Seasonal Pattern Analysis
        - **Metode**: Time-based clustering per Seasons (Pengelompokan berdasarkan waktu per musim)
        - **Variabel**:  (1:Spring, 2:Summer, 3:Fall, 4:Winter)
        - **Metrik**: Rata-rata penggunaan, pola harian, pengaruh cuaca

        ## Hasil Analisis per Musim

        ### 1. Musim Semi (Spring)
        - **Volume**: Moderate (rata-rata 188.5 rentals/hari)
        - **Pola**: 
        - Peningkatan bertahap dari pagi
        - Peak hours konsisten dengan pola umum
        - **Karakteristik**:
        - Cuaca berubah-ubah mempengaruhi penggunaan
        - Adaptasi pengguna terhadap perubahan suhu

        ### 2. Musim Panas (Summer)
        - **Volume**: High (rata-rata 220.4 rentals/hari)
        - **Pola**:
        - Extended usage hours
        - Peak di sore hari lebih tinggi
        - **Karakteristik**:
        - Penggunaan maksimal saat cuaca cerah
        - Durasi penggunaan lebih panjang

        ### 3. Musim Gugur (Fall)
        - **Volume**: Highest (rata-rata 233.8 rentals/hari)
        - **Pola**:
        - Konsisten dengan pola umum
        - Peak hours paling tinggi
        - **Karakteristik**:
        - Suhu optimal untuk bersepeda
        - Kombinasi commuter dan recreational users

        ### 4. Musim Dingin (Winter)
        - **Volume**: Lowest (rata-rata 153.2 rentals/hari)
        - **Pola**:
        - Penggunaan terbatas di siang hari
        - Peak hours lebih rendah
        - **Karakteristik**:
        - Sangat dipengaruhi cuaca
        - Dominasi pengguna regular
        """)
        
    else:
        st.header("Dataset yang digunakan")
        st.write(hour_df)
        st.markdown("""
        **Dataset Information:**
        - Nama Dataset: Bike Sharing Dataset
        - Link: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data
        """)
        

if __name__ == "__main__":
    main()