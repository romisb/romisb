import streamlit as st
import pandas as pd

st.title("📊 Visualisasi Data dari File Excel")

# Upload file Excel
uploaded_file = st.file_uploader("📂 Pilih file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Dapatkan semua sheet
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names

    st.subheader("📑 Pilih Sheet:")
    selected_sheet = st.selectbox("Pilih sheet dari file yang diupload:", sheet_names)

    # Baca data dari sheet yang dipilih
    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.subheader(f"📄 Data dari Sheet: {selected_sheet}")
    st.dataframe(df, use_container_width=True)

    # Pilih kolom untuk visualisasi
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    date_columns = df.select_dtypes(include=['datetime64[ns]', 'object']).columns.tolist()

    if numeric_columns and date_columns:
        x_axis = st.selectbox("📅 Pilih kolom untuk sumbu X (tanggal):", date_columns)
        y_axis = st.multiselect("📈 Pilih kolom untuk sumbu Y (nilai numerik):", numeric_columns, default=numeric_columns[:1])

        # Konversi kolom tanggal jika belum dalam format datetime
        df[x_axis] = pd.to_datetime(df[x_axis], errors='coerce')
        df = df.dropna(subset=[x_axis])
        df = df.sort_values(x_axis)

        chart_type = st.selectbox("📊 Pilih jenis grafik:", ["Line Chart", "Bar Chart", "Area Chart"])

        if y_axis:
            pivot_df = df[[x_axis] + y_axis].set_index(x_axis)

            st.subheader(f"📈 Visualisasi {chart_type}")
            if chart_type == "Line Chart":
                st.line_chart(pivot_df)
            elif chart_type == "Bar Chart":
                st.bar_chart(pivot_df)
            elif chart_type == "Area Chart":
                st.area_chart(pivot_df)
        else:
            st.warning("⚠️ Pilih setidaknya satu kolom untuk divisualisasikan.")
    else:
        st.warning("⚠️ Pastikan ada kolom tanggal dan kolom numerik di dataset.")
else:
    st.info("Silakan upload file Excel untuk memvisualisasikan data.")