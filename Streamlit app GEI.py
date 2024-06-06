import streamlit as st
import pandas as pd
import pickle
import os

# Run filenya: "C:\Users\jeffr\OneDrive\Documents\python\Bisdig C\Streamlit app GEI.py"

#Test
st.set_page_config(page_title="Global Ekonomi Indikator", page_icon=":moneybag:")

st.markdown("<h1 style='text-align: center; color: #707070;'>GLOBAL EKONOMI INDIKATOR</h1>", unsafe_allow_html=True)

st.markdown("<style>.stButton button {background-color: #707070; color: #fff;}</style>", unsafe_allow_html=True)

st.markdown("<style>.stTextInput input {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)

st.markdown("<style>.stSelectbox select {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)


# Nama file .sav
sav_file_name = 'Global Economy Indicators.sav'

# Cek apakah file .sav ada
if os.path.exists(sav_file_name):
    try:
        # Memuat DataFrame dari file .sav menggunakan pickle
        with open(sav_file_name, 'rb') as file:
            data = pickle.load(file)
        data['Country'] = data['Country'].apply(lambda x: x.strip() if isinstance(x, str) else x)
        data['Currency'] = data['Currency'].apply(lambda x: x.strip() if isinstance(x, str) else x)

  # Mengganti nilai 0 dengan None
        data[['Population', 'Per capita GNI']] = data[['Population', 'Per capita GNI']].astype(float)
        data[['Population', 'Per capita GNI']] = data[['Population', 'Per capita GNI']].applymap(lambda x: int(x) if x.is_integer() else x)


        # Meminta input pengguna untuk negara dan tahun
        country = st.text_input("Masukkan nama negara:")
        year = st.number_input("Masukkan tahun:", min_value=1970, max_value=2021, step=1)

        # Tombol untuk memfilter data
        if st.button('Filter Data'):
            # Menyaring data berdasarkan negara dan tahun
            filtered_data = data[(data['Country'] == country) & (data['Year'] == year)]

            # Mengecek apakah ada data yang sesuai
            if not filtered_data.empty:
                # Menampilkan informasi
                for index, row in filtered_data.iterrows():
                    st.write(f"Negara: {row['Country']}")
                    st.write(f"Tahun: {int(row['Year'])}")
                    st.write(f"Populasi: {'' if pd.isnull(row['Population']) else int(row['Population'])}")
                    st.write(f"Kurs: {'' if pd.isnull(row['Currency']) else row['Currency']}")
                    st.write(f"GNI per Kapita: {'' if pd.isnull(row['Per capita GNI']) else int(row['Per capita GNI'])}")
            else:
                st.write(f"Tidak ada data untuk negara '{country}' pada tahun '{year}'.")

    except Exception as e:
        st.write(f"Terjadi kesalahan saat memuat file: {e}")
else:
    st.write(f"File {sav_file_name} tidak ditemukan.")
