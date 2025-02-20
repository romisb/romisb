import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Visualisasi Data Provider dari File Excel")

# 📥 Upload file Excel atau CSV
uploaded_file = st.file_uploader("📂 Upload file Excel atau CSV", type=["xlsx", "csv"])

if uploaded_file:
    # 📖 Baca data sesuai format file
    if uploaded_file.name.endswith('xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # 🕒 Konversi kolom 'Date' ke format datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    else:
        st.error("❌ Kolom 'Date' tidak ditemukan dalam file.")
        st.stop()

    # 🔄 Ubah data dari wide format ke long format
    provider_columns = [col for col in df.columns if col != 'Date']
    if not provider_columns:
        st.error("❌ Tidak ada kolom provider yang ditemukan.")
        st.stop()

    long_df = df.melt(id_vars='Date', value_vars=provider_columns, var_name='Provider', value_name='Value')

    # 🧹 Bersihkan data
    long_df['Value'] = pd.to_numeric(long_df['Value'], errors='coerce')
    long_df = long_df.dropna(subset=['Value'])

    # 📄 Tampilkan data setelah konversi
    st.subheader("📄 Data Setelah Dikonversi")
    st.dataframe(long_df, use_container_width=True)

    # 🎯 Pilihan filter visualisasi
    st.subheader("🔎 Filter Data")
    selected_providers = st.multiselect("Pilih Provider:", options=long_df['Provider'].unique(), default=long_df['Provider'].unique())
    date_range = st.date_input("Pilih Rentang Tanggal:", [long_df['Date'].min(), long_df['Date'].max()])

    filtered_df = long_df[(long_df['Provider'].isin(selected_providers)) & (long_df['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))]

    # 📊 Pilihan jenis grafik
    st.subheader("📈 Visualisasi Data")
    chart_type = st.selectbox("Pilih Jenis Grafik:", ["Line Chart", "Bar Chart", "Area Chart"])

    if not filtered_df.empty:
        if chart_type == "Line Chart":
            fig = px.line(filtered_df, x='Date', y='Value', color='Provider', markers=True, title="📈 Tren Provider dari Waktu ke Waktu")
        elif chart_type == "Bar Chart":
            fig = px.bar(filtered_df, x='Date', y='Value', color='Provider', barmode='group', title="📊 Perbandingan Provider per Tanggal")
        else:  # Area Chart
            fig = px.area(filtered_df, x='Date', y='Value', color='Provider', title="🌄 Tren Area Provider")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    st.info("🚀 Silakan upload file dengan kolom: Date, Provider, dan Value.")