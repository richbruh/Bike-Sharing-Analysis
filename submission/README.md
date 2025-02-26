# Bike Sharing Analysis Dashboard

## Author Information
```
Name: Richie Zakaria 
Class: MC-07
Cohort ID: richie_rich100
```

## Ringkasan
Proyek ini menganalisis pola penggunaan sepeda sewa untuk menunjukkan tren penggunaan serta perbedaan antara hari libur dan hari kerja.

## Fitur Utama
- **Analisis Pola Harian**: Pola penggunaan 24 jam dengan skala interaktif
- **Pengaruh Cuaca**: Analisis dampak cuaca terhadap pola penyewaan
- **Tren Musiman**: Analisis variasi musiman secara interaktif
- **Informasi Dataset**: Eksplorasi dataset secara menyeluruh

## Struktur Proyek
```
submission/
├── dashboard/
│   └── dashboard.py
├── dataset/
│   └── hour.csv
├── notebook/
│   └── analysis.ipynb
├── README.md
└── requirements.txt
```

## Panduan Instalasi

### Persiapan Lingkungan
```bash
# Membuat dan mengaktifkan environment conda
conda create --name main-ds python=3.9
conda activate main-ds

# Instalasi package yang dibutuhkan
pip install -r requirements.txt
```

### Package yang Dibutuhkan
```txt
streamlit==1.10.0
pandas==1.3.0
numpy==1.21.0
matplotlib==3.4.0
seaborn==0.11.0
scikit-learn==0.24.2
```

## Menjalankan Dashboard
```bash
# Pindah ke direktori proyek
cd submission

# Menjalankan dashboard Streamlit
streamlit run dashboard/dashboard.py
```
## Teknologi yang Digunakan
- Python 3.9
- Streamlit untuk dashboard
- Pandas untuk manipulasi data
- Matplotlib/Seaborn untuk visualisasi
- Scikit-learn untuk analisis