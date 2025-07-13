import streamlit as st
import math

# Judul Aplikasi
st.title("Aplikasi Perhitungan EOQ (Economic Order Quantity)")

# Deskripsi
st.markdown("""
Aplikasi ini membantu menghitung jumlah pemesanan optimal (EOQ) untuk meminimalkan total biaya persediaan barang.  
Silakan masukkan data berikut atau gunakan studi kasus yang tersedia.
""")

# Inisialisasi default nilai input jika belum ada di session state
if 'D' not in st.session_state:
    st.session_state.D = 1
if 'S' not in st.session_state:
    st.session_state.S = 0.0
if 'H' not in st.session_state:
    st.session_state.H = 0.0

# Studi Kasus: Toko Alat Tulis Smart Office
if st.button("Toko Alat Tulis"):
    st.session_state.D = 5000         # Permintaan tahunan
    st.session_state.S = 200000.0     # Biaya pemesanan per pesanan (Rp)
    st.session_state.H = 5000.0       # Biaya penyimpanan per unit per tahun (Rp)
    st.success("Data studi kasus berhasil dimasukkan.")

# Input manual pengguna (jika tidak pakai studi kasus)
st.subheader("Masukkan Data Secara Manual")
st.session_state.D = st.number_input("Permintaan tahunan (unit)", min_value=1, value=st.session_state.D, step=1)
st.session_state.S = st.number_input("Biaya pemesanan per pesanan (Rp)", min_value=0.0, value=st.session_state.S, step=100.0)
st.session_state.H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", min_value=0.0, value=st.session_state.H, step=100.0)

# Tombol untuk menghitung EOQ
if st.button("Hitung EOQ"):
    D = st.session_state.D
    S = st.session_state.S
    H = st.session_state.H
    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        jumlah_pemesanan = D / EOQ
        total_biaya = (EOQ / 2 * H) + (D / EOQ * S)

        # Output hasil perhitungan
        st.subheader("Hasil Perhitungan EOQ:")
        st.write(f"🔹 **EOQ (Jumlah Pemesanan Optimal)**: {EOQ:.2f} unit")
        st.write(f"🔹 **Jumlah Pemesanan per Tahun**: {jumlah_pemesanan:.2f} kali")
        st.write(f"🔹 **Total Biaya Persediaan Tahunan**: Rp {total_biaya:,.2f}")
    else:
        st.error("Semua input harus lebih dari 0 untuk melakukan perhitungan.")
