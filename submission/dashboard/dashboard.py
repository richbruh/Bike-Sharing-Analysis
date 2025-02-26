""" PROJECT DESCRIPTION: 
PROJECT ini adalah Bike Sharing Analysis yang ditunjukkan dalam bentuk Dashboard menggunakan Streamlit.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    return pd.read_csv('./dataset/hour.csv')

def create_daily_patterns(df):
    return df.groupby(['workingday', 'hr'])[['casual', 'registered', 'cnt']].mean()

def plot_daily_patterns(hourly_data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot untuk hari kerja
    hourly_data.loc[1]['casual'].plot(ax=ax1, color='blue', label='Casual')
    hourly_data.loc[1]['registered'].plot(ax=ax1, color='green', label='Registered')
    hourly_data.loc[1]['cnt'].plot(ax=ax1, color='red', linestyle='--', label='Total')
    ax1.set_title('Pola Penggunaan Sepeda pada Hari Kerja')
    ax1.set_xlabel('Jam')
    ax1.set_ylabel('Rata-rata Pengguna')
    ax1.grid(True)
    ax1.legend(loc='upper left')
    
    # Plot untuk hari libur
    hourly_data.loc[0]['casual'].plot(ax=ax2, color='blue', label='Casual')
    hourly_data.loc[0]['registered'].plot(ax=ax2, color='green', label='Registered')
    hourly_data.loc[0]['cnt'].plot(ax=ax2, color='red', linestyle='--', label='Total')
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
def plot_seasonal_patterns(df):
    seasons = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    
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
        ["Pola Harian", "Pengaruh Cuaca", "Pola Musiman", "Dataset Source"]
    )
    
    if analysis_type == "Pola Harian":
        st.header("Pola Penggunaan Harian")
        hourly_patterns = create_daily_patterns(hour_df)
        fig = plot_daily_patterns(hourly_patterns)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:**
        1. Penggunaan Hari Kerja
        - **Peak Volume**: 490 pada jam 08:00 dan 530 pada jam 17:00
        - **Pola**: Banyak pengguna di pagi hari dan sore hari
        - **Distribusi**: Tidak merata sepanjang hari
        - Pagi (07:00-09:00): Peak pertama 
        - Sore (17:00-19:00): Peak kedua
        - **Volume**: Tinggi di pagi dan sore hari
        - **Durasi**: Periode penggunaan aktif lebih pendek
        2. Penggunaan Hari Libur
        - **Peak Volume**: 300 pada jam 13:00
        - **Pola**: Tidak ada peak volume yang signifikan
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

        Perbandingan Karakteristik Hari Libur:
        - Volume lebih rendah tapi stabil
        - Distribusi lebih merata
        - Dominan penggunaan rekreasional

        """)
        
    elif analysis_type == "Pengaruh Cuaca":
        st.header("Analisis Pengaruh Cuaca")
        fig = plot_weather_analysis(hour_df)
        st.pyplot(fig)
        
        # Calculate and display weather-time clusters
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
        **Periode Waktu vs Jumlah Pengguna**

        Pagi (7-12) dan Siang (13-18) memiliki jumlah pemakaian sepeda tertinggi dibanding periode lainnya sedangkan Subuh memiliki jumlah pengguna terendah.
        Malam (19-24) memiliki jumlah pengguna lebih banyak dibanding subuh tetapi masih lebih rendah dari siang dan pagi.
        Pengaruh Cuaca terhadap Pemakaian Sepeda

        Semakin berat hujan akan semakin dikit para pengguna sepeda sewa untuk bertransportasi. Alasan ini logis karena orang-orang rentan tidak ingin terkena hujan karena takut basah. """)
        
        st.dataframe(weather_time_clusters)
        
    elif analysis_type == "Pola Musiman":
        st.header("Analisis Pola Musiman")
        fig = plot_seasonal_patterns(hour_df)
        st.pyplot(fig)
        
        st.markdown("""
        ### Insight:
        - Puncak penggunaan sepeda sewa di hari kerja lebih tinggi dibandingkan di hari libur. Hal ini bisa disebabkan karena banyak orang menggunakan sepeda sebagai moda transportasi saat bekerja.
        - Tren ini mengonfirmasi bahwa adanya penggunaan sepeda sewa di hari kerja lebih dipagi hari berhubungan dengan pergi ke kantor/sekolah, sedangkan di hari libur lebih banyak digunakan untuk rekreasi atau aktivitas santai.
        - Puncak penggunaan sepeda di sore hari cukup tinggi di kedua jenis hari, menunjukkan bahwa banyak orang tetap menggunakan sepeda sebagai moda transportasi di sore hari baik saat bekerja maupun berlibur.
        - Penggunaan Trend tiap jam di Musim-musim berbeda tetap menunjukkan pattern yang sama namun yang membedakan adalah volume pemakaian sepeda tersebut.
        - Penggunaan sepeda sewa di musim semi dan musim gugur lebih tinggi dibandingkan musim panas dan musim dingin. Hal ini bisa disebabkan karena cuaca yang lebih nyaman di musim semi dan musim gugur.
        - Penggunaan sepeda sewa di musim panas lebih rendah dibandingkan musim semi dan musim gugur. Hal ini bisa disebabkan karena cuaca yang lebih panas di musim panas.
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