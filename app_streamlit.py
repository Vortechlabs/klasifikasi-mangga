import streamlit as st
import pandas as pd
import joblib

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Kualitas Mangga",
    page_icon="🥭",
    layout="centered"
)

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load('model_klasifikasi_mangga.joblib')
    except:
        st.error("Model tidak ditemukan! Pastikan file 'model_klasifikasi_mangga.joblib' tersedia.")
        return None

model = load_model()

# Data pilihan dari dataset
ASAL_DAERAH_OPTIONS = ["Gedong Gincu", "Manalagi", "Indramayu", "Arumanis", "Golek"]
WARNA_OPTIONS = ["kuning", "hijau", "hijau kekuningan"]
MUSIM_PANEN_OPTIONS = ["kemarau", "hujan"]

# Header utama
st.title("Prediksi Kualitas Mangga")
st.markdown("Aplikasi untuk memprediksi kualitas mangga menjadi **Bagus, Sedang, atau Jelek** berdasarkan karakteristik fisik dan geografis")

# Tabs utama
tab1, tab2 = st.tabs(["Prediksi", "Informasi"])

with tab1:
    st.header("Karakteristik Mangga")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ukuran & Berat")
        diameter = st.slider("Diameter (cm)", 5.0, 15.0, 8.5, 0.1)
        berat = st.slider("Berat (gram)", 100.0, 500.0, 250.0, 5.0)

    with col2:
        st.subheader("Kualitas Buah")
        tebal_kulit = st.slider("Tebal Kulit (mm)", 0.5, 3.0, 1.2, 0.1)
        kadar_gula = st.slider("Kadar Gula (Brix°)", 8.0, 25.0, 16.0, 0.5)

    st.subheader("Karakteristik Lainnya")
    col3, col4, col5 = st.columns(3)

    with col3:
        asal_daerah = st.pills(
            "Asal Daerah",
            ASAL_DAERAH_OPTIONS,
            selection_mode="single"
        )

    with col4:
        warna = st.pills(
            "Warna Kulit",
            WARNA_OPTIONS,
            selection_mode="single"
        )

    with col5:
        musim_panen = st.pills(
            "Musim Panen",
            MUSIM_PANEN_OPTIONS,
            selection_mode="single"
        )

    # Tombol prediksi
    if st.button("Prediksi Kualitas", type="primary", use_container_width=True):
        if model is not None:
            # Validasi input
            if not asal_daerah or not warna or not musim_panen:
                st.error("Harap pilih semua opsi untuk karakteristik lainnya!")
            else:
                # Buat dataframe input
                input_data = pd.DataFrame({
                    'diameter': [diameter],
                    'berat': [berat],
                    'tebal_kulit': [tebal_kulit],
                    'kadar_gula': [kadar_gula],
                    'asal_daerah': [asal_daerah],
                    'warna': [warna],
                    'musim_panen': [musim_panen]
                })

                try:
                    # Prediksi
                    prediction = model.predict(input_data)[0]
                    probabilities = model.predict_proba(input_data)[0]

                    # Tampilkan hasil utama
                    st.markdown("---")
                    if prediction == "Bagus":
                        st.success(f"## Hasil Prediksi: **{prediction}**")
                    elif prediction == "Sedang":
                        st.warning(f"## Hasil Prediksi: **{prediction}**")
                    else:
                        st.error(f"## Hasil Prediksi: **{prediction}**")

                    # Probabilitas
                    st.subheader("Probabilitas Kualitas:")
                    quality_labels = model.named_steps['model'].classes_

                    for quality, prob in zip(quality_labels, probabilities):
                        col_proba, col_bar = st.columns([1, 3])
                        with col_proba:
                            if quality == "Bagus":
                                st.markdown(f"**{quality}**: {prob*100:.2f}%")
                            elif quality == "Sedang":
                                st.markdown(f"**{quality}**: {prob*100:.2f}%")
                            else:
                                st.markdown(f"**{quality}**: {prob*100:.2f}%")
                        with col_bar:
                            st.progress(float(prob))

                    # Rekomendasi
                    st.subheader("Rekomendasi:")
                    if prediction == "Bagus":
                        st.success("Kualitas premium, cocok untuk ekspor dan pasar high-end dengan harga premium")
                    elif prediction == "Sedang":
                        st.warning("Kualitas standar, cocok untuk pasar lokal dengan harga kompetitif")
                    else:
                        st.error("Disarankan untuk olahan industri seperti jus atau selai")

                except Exception as e:
                    st.error(f"Terjadi error dalam prediksi: {e}")
        else:
            st.error("Model tidak dapat dimuat. Silakan periksa file model.")

with tab2:
    st.header("Informasi Aplikasi")

    st.subheader("Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini menggunakan model machine learning untuk memprediksi kualitas mangga
    berdasarkan berbagai karakteristik fisik dan geografis. Model dilatih menggunakan
    data historis kualitas mangga dengan akurasi yang tinggi.
    """)

    st.subheader("Fitur yang Digunakan")

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("""
        **Karakteristik Fisik:**
        - Diameter: Ukuran buah dalam cm
        - Berat: Berat buah dalam gram
        - Tebal Kulit: Ketebalan kulit dalam mm
        - Kadar Gula: Tingkat kemanisan dalam Brix°
        """)

    with col_info2:
        st.markdown(f"""
        **Karakteristik Lain:**
        - Asal Daerah: {', '.join(ASAL_DAERAH_OPTIONS)}
        - Warna Kulit: {', '.join(WARNA_OPTIONS)}
        - Musim Panen: {', '.join(MUSIM_PANEN_OPTIONS)}
        """)

    st.subheader("Kategori Kualitas")

    col_qual1, col_qual2, col_qual3 = st.columns(3)

    with col_qual1:
        st.markdown("""
        **Bagus**
        - Kualitas premium
        - Harga tinggi
        - Pasar ekspor
        """)

    with col_qual2:
        st.markdown("""
        **Sedang**
        - Kualitas standar
        - Harga menengah
        - Pasar lokal
        """)

    with col_qual3:
        st.markdown("""
        **Jelek**
        - Kualitas rendah
        - Harga industri
        - Untuk olahan
        """)

    st.subheader("Cara Penggunaan")
    st.markdown("""
    1. Pilih tab **Prediksi**
    2. Atur slider untuk karakteristik fisik
    3. Pilih opsi untuk karakteristik lainnya menggunakan pills
    4. Klik tombol **Prediksi Kualitas**
    5. Lihat hasil prediksi dan rekomendasi
    """)

# Footer
st.markdown("---")
st.caption("Dibuat dengan 🥭 oleh Al Zaki Ibra Ramadani | Model Klasifikasi Mangga")
