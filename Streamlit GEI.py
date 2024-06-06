import streamlit as st
import pandas as pd
import pickle
import os
import json
import requests
import matplotlib.pyplot as plt
import base64

st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("""
<style>
[data-testid="stSidebar"] {
  background-color: #29465b;
  font-family: sans-serif
}
</style>
""", unsafe_allow_html=True)

# Function to save blog posts
def save_blog_post(title, content):
    blog_posts = load_blog_posts()
    blog_posts.append({"title": title, "content": content})
    with open("blog_posts.json", "w") as file:
        json.dump(blog_posts, file)

# Function to load blog posts
def load_blog_posts():
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r") as file:
            blog_posts = json.load(file)
    else:
        blog_posts = []
    return blog_posts

# Function to delete a blog post
def delete_blog_post(index):
    blog_posts = load_blog_posts()
    if 0 <= index < len(blog_posts):
        blog_posts.pop(index)
        with open("blog_posts.json", "w") as file:
            json.dump(blog_posts, file)

# Page to write and view blog posts
def page_blog():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
           data = f.read()
        return base64.b64encode(data).decode()
        
    img = get_img_as_base64("images/blogfix.jpeg")
    
    page_bg_img = f"""
    <style>
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,{img}");
        background-repeat: no-repeat;
        background-size: cover;
        background-color: #f6f9fb;
        background-position: 80%;
        filter: blur(6px);
        z-index: -1;
    
    }}
    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);    
    }}

    </style>
    
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)    
    # Section to write a new blog post
    st.subheader("Menulis Blog")
    title = st.text_input("Judul")
    content = st.text_area("Konten")
    if st.button("Submit"):
        if title and content:
            save_blog_post(title, content)
            st.success("Blog sudah dipost")
        else:
            st.error("Judul dan konten tidak boleh kosong")

    # Section to view and delete blog posts
    st.subheader("Blog-Blog yang Tersedia")
    blog_posts = load_blog_posts()
    Pjir51 = st.text_input("Enter admin password to delete posts:", type="password", key="delete_auth")
    if blog_posts:
        for i, post in enumerate(blog_posts):
            st.header(post["title"])
            st.write(post["content"])
            if Pjir51 == "Pjir51":
                if st.button(f"Hapus Post {i+1}", key=f"delete_{i}"):
                    delete_blog_post(i)
                    st.experimental_rerun()  # Refresh the page to reflect deletion
    else:
        st.write("Tidak ditemukan blog.")

# Page to display currency exchange rates
def CurrencyExchangeRate():
    response = requests.get("https://open.er-api.com/v6/latest/USD")
    if response.status_code == 200:
        currency_data = response.json()
        rates = currency_data["rates"]
        
        currencies = list(rates.keys())
        
        st.markdown("""
            <style>
              .stApp {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: rgb(2,0,36);
                background: linear-gradient(to bottom, rgba(2,0,36,1) 0%, rgba(252,255,255,1) 0%, rgba(23,180,212,1) 50%);
                color: #333; /* Warna teks */
              }
              
                [data-testid="stHeader"] {
                background-color: rgba(0, 0, 0, 0)
                }
                
              .container {
                width: 90%;
                margin: 50px auto;
                text-align: center;
              }
              
              .exchange-form {
                background-color:  rgba(38, 39, 48, 1); /* Warna latar belakang formulir */
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* Bayangan formulir */
                color: #0000;   
              }
              
              .exchange-form h2{
                color: white;    
                }
                    
              .exchange-form label {
                font-family: Arial, sans-serif; /* Set desired font family */
                color: #white /* Set desired font color (same as body text)
              }
                    
              .input-field {
                width: 70%;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                margin-bottom: 10px;
                color: #0000;
              }
              
              .convert-button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #3498db; /* Warna tombol konversi */
                color: #fff; /* Warna teks tombol konversi */
                border: none;
                border-radius: 5px;
                cursor: pointer;
              }
            h2 {
                 color: #000;   
            }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="container">
              <div class="exchange-form">
                <h2>Penukaran Mata Uang</h2>
            """, unsafe_allow_html=True)
        
        base_currency = st.selectbox("Mata uang referensi:", currencies, index=currencies.index("USD"), key="base_currency")
        target_currency = st.selectbox("Mata uang kutipan:", currencies, index=currencies.index("EUR"), key="target_currency")
        amount = st.text_input("Masukkan jumlah uang:", "1", key="amount")
 
        st.markdown("""
                <button class="convert-button">Tukar</button>
              </div>
            </div>
            """, unsafe_allow_html=True)

        if base_currency and target_currency and amount:
            try:
                amount = float(amount)
                if base_currency != target_currency:
                    base_rate = rates[base_currency]
                    target_rate = rates[target_currency]
                    exchange_rate = target_rate / base_rate
                    converted_amount = amount * exchange_rate
                    st.write(f"{amount} {base_currency} = {converted_amount:.4f} {target_currency}")
                else:
                    st.warning("Mata uang referensi dan mata uang kutipan tidak bisa sama.")
            except ValueError:
                st.error("Masukkan jumlah yang sah.")
    else:
        st.error("Gagal mengambil nilai tukar mata uang.")


# Page to display global economy indicators
def page_GEI():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
           data = f.read()
        return base64.b64encode(data).decode()
        
    img = get_img_as_base64("images/bg.jpeg")
    
    page_bg_img = f"""
    <style>
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,{img}");
        background-repeat: repeat;
        background-size: cover;
        background-color: #f6f9fb;
        filter: blur(6px);
        z-index: -1;
    
    }}
    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);    
    }}

    </style>
    
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Indikator Global Ekonomi Tahun 1970-2021")
    sav_file_name = 'Global Economy Indicators.sav'
    if os.path.exists(sav_file_name):
        try:
            with open(sav_file_name, 'rb') as file:
                data = pickle.load(file)
            data['Country'] = data['Country'].apply(lambda x: x.strip() if isinstance(x, str) else x)
            data['Currency'] = data['Currency'].apply(lambda x: x.strip() if isinstance(x, str) else x)
            data[['Population', 'Per capita GNI']] = data[['Population', 'Per capita GNI']].astype(float)
            data[['Population', 'Per capita GNI']] = data[['Population', 'Per capita GNI']].applymap(lambda x: int(x) if x.is_integer() else x)
            country = st.text_input("Masukkan nama negara:")
            year_start = st.number_input("Masukkan tahun awal:", min_value=1970, max_value=2021, step=1)
            year_end = st.number_input("Masukkan tahun akhir:", min_value=1971, max_value=2021, step=1)
            show_gdp = st.checkbox('GDP')
            show_gni = st.checkbox('GNI')
            show_population = st.checkbox('Populasi')
            visualization_type = st.radio("Pilih metode visualisasi:", ["Table", "Matplotlib Chart"])
            if st.button('Tampilkan'):
                filtered_data = data[(data['Country'] == country) & (data['Year'] >= year_start) & (data['Year'] <= year_end)]
                if not filtered_data.empty:
                    if visualization_type == "Table":
                        columns_to_show = ['Year', 'Country']
                        if show_gdp:
                            columns_to_show.append('Gross Domestic Product (GDP)')
                        if show_gni:
                            columns_to_show.append('Per capita GNI')
                        if show_population:
                            columns_to_show.append('Population')
                        st.dataframe(filtered_data[columns_to_show])
                    elif visualization_type == "Matplotlib Chart":
                        if show_gdp:
                            plt.figure(figsize=(10, 6))
                            plt.plot(filtered_data['Year'], filtered_data['Gross Domestic Product (GDP)'], marker='o')
                            plt.title('GDP Selama Bertahun-Tahun')
                            plt.xlabel('Tahun')
                            plt.ylabel('GDP')
                            plt.grid(True)
                            st.pyplot()
                        if show_gni:
                            plt.figure(figsize=(10, 6))
                            plt.plot(filtered_data['Year'], filtered_data['Per capita GNI'], marker='o')
                            plt.title('GNI per Kapita Selama Bertahun-Tahun')
                            plt.xlabel('Tahun')
                            plt.ylabel('GNI per Kapita')
                            plt.grid(True)
                            st.pyplot()
                        if show_population:
                            plt.figure(figsize=(10, 6))
                            plt.plot(filtered_data['Year'], filtered_data['Population'], marker='o')
                            plt.title('Populasi Selama Bertahun-Tahun')
                            plt.xlabel('Tahun')
                            plt.ylabel('Populasi')
                            plt.grid(True)
                            st.pyplot()
                else:
                    st.write(f"Tidak ada data untuk negara '{country}' dalam rentang tahun '{year_start}' sampai '{year_end}'.")
        except Exception as e:
            st.write(f"Error loading file: {e}")
    else:
        st.write(f"File {sav_file_name} not found.")

def page_help():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
           data = f.read()
        return base64.b64encode(data).decode()
        
    img = get_img_as_base64("images/bantuanfix.jpeg")
    
    page_bg_img = f"""
    <style>
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,{img}");
        background-repeat: no-repeat;
        background-size: cover;
        background-color: #f6f9fb;
        filter: blur(6px);
        z-index: -1;
    
    }}
    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);    
    }}
    .help-container {{
    background-color: rgba(0, 0, 0, 0.6); /* Adjust the alpha value to control opacity */
    padding: 20px;
    border-radius: 10px;
    color: white; /* Change text color to white */
    }}
    </style>
    
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            body {
                background-color: #9cbbd2;
            }
        </style>
        <div class="help-container">
             <h2>Instruksi Penggunaan</h2>
            <h3>Cara mencari indikator ekonomi suatu negara</h3>
            <ol>
                <li>Pilih negara</li>
                <li>Ketik rentang tahun yang ingin dicari</li>
                <li>Ceklis data yang ingin ditampilkan (GDP, GNI, atau Populasi)</li>
                <li>Pilih bentuk data yang ingin ditampilkan</li>
                <li>Klik tampilkan</li>
            </ol>
            <h3>Cara mengetahui hasil kurs uang</h3>
            <ol>
                <li>Pilih mata uang negara yang ingin diubah kursnya atau mata uang referensi</li>
                <li>Pilih mata uang negara yang dituju atau mata uang kutipan</li>
                <li>Ketik nominal uang</li>
                <li>Klik tukar</li>
            </ol>
            <h3>Cara menulis di Blog</h3>
            <ol>
                <li>Ketik di bagian judul untuk menulis judul dari blog anda</li>
                <li>Ketik di bagian konten untuk menulis isi dari blog anda</li>
                <li>Klik submit</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

def page_aboutus():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
           data = f.read()
        return base64.b64encode(data).decode()
        
    img = get_img_as_base64("images/bg.jpeg")
    
    page_bg_img = f"""
    <style>
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuuDpZZAo7gemta_YmRY3d6KObTl-2gwl-u_wq6TXIh59584xIL5U8R0Q&s=10");
        background-repeat: repeat;
        background-size: cover;
        background-color: #f6f9fb;
        filter: blur(6px);
        z-index: -1;
    
    }}
    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);    
    }}

    </style>
    
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(
        """
        
        </style>
        <div class="aboutus-container">
            <h1>Liberci</h1>
            <p>Kami adalah tim yang bersemangat dan berdedikasi untuk memberikan informasi terkait ekonomi global. Dengan pengalaman yang luas dan komitmen untuk kualitas, kami siap membantu Anda untuk mengetahui informasi tentang populasi, GNI, dan GNP suatu negara. Kami percaya bahwa setiap pelanggan adalah prioritas utama kami. Kami berusaha untuk memenuhi dan melampaui harapan Anda dengan pendekatan yang personal dan solusi yang disesuaikan.</p>
            <p>Kami berkomitmen terhadap informasi dalam setiap langkah yang kami ambil. Tim kami yang terdiri dari lima mahasiswa berusaha memastikan bahwa semua informasi yang kami berikan adalah akurat dan dapat diandalkan. Jadi, hubungi kami hari ini dan temukan bagaimana kami dapat membantu Anda mendapatkan informasi yang tepat apa pun yang Anda butuhkan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Apply custom CSS for background
def apply_custom_css():
    css = """
    <style>
    .stApp {
        background: url("https://www.example.com/path-to-your-image.jpg");
        background-size: cover;
    }
    .sidebar .sidebar-content {
        background: url("https://www.example.com/path-to-your-image.jpg");
        background-size: cover;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Dasbor")
pages = {
    "Indikator Global Ekonomi": page_GEI,
    "Kurs": CurrencyExchangeRate,
    "Blog": page_blog,
    "Bantuan": page_help,
    "Mengenai Kami": page_aboutus
}

selection = st.sidebar.radio("Pergi ke", list(pages.keys()))
apply_custom_css()
pages[selection]()
