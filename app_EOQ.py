import streamlit as st
import math

# Judul Aplikasi
st.title("Aplikasi Perhitungan EOQ (Economic Order Quantity)")

# Deskripsi
st.markdown("""
Aplikasi ini membantu menghitung jumlah pemesanan optimal (EOQ) untuk meminimalkan total biaya persediaan barang.  
Silakan masukkan data berikut atau gunakan studi kasus yang tersedia.
""")

# Inisialisasi default nilai input
D = 0
S = 0.0
H = 0.0

# Studi Kasus: Toko Alat Tulis Smart Office
if st.button("Gunakan Studi Kasus Toko 'Smart Office'"):
    D = 5000         # Permintaan tahunan
    S = 200000.0     # Biaya pemesanan per pesanan (Rp)
    H = 5000.0       # Biaya penyimpanan per unit per tahun (Rp)
    st.success("Data studi kasus berhasil dimasukkan.")

# Tombol untuk menghitung EOQ
if st.button("Hitung EOQ"):
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
