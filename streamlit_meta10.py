import streamlit as st
import pandas as pd

# Fungsi untuk membaca data dengan cache
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # Bersihkan spasi di nama kolom
    return df

st.title("📊 Visualisasi Data Penjualan")

# Load data
df = load_data()

# Periksa apakah 'Date' ada di kolom
if 'Date' not in df.columns:
    st.error("Kolom 'Date' tidak ditemukan. Pastikan nama kolom sesuai.")
else:
    # Sidebar untuk filter
    st.sidebar.header("🔎 Filter Data")

    # Pilih kolom yang ingin divisualisasikan
    available_columns = [col for col in df.columns if col != 'Date']
    selected_columns = st.sidebar.multiselect(
        "Pilih operator yang ingin ditampilkan:",
        options=available_columns,
        default=available_columns[:3]  # Default pilih 3 kolom pertama
    )

    # Pilih rentang tanggal
    min_date, max_date = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input(
        "Pilih rentang tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter data berdasarkan tanggal
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    else:
        filtered_df = df.copy()

    # Menampilkan data yang difilter
    with st.expander("🔍 Lihat Data Tabel"):
        st.dataframe(filtered_df[['Date'] + selected_columns].reset_index(drop=True))

    # Visualisasi line chart
    st.subheader("📈 Line Chart Penjualan")
    if selected_columns:
        st.line_chart(filtered_df.set_index('Date')[selected_columns])
    else:
        st.warning("Silakan pilih minimal satu kolom untuk ditampilkan.")
