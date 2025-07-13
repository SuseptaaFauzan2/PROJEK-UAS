import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Set page config for better appearance
st.set_page_config(
    page_title="EOQ Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .result-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        background-color: white;
        margin-bottom: 1.5rem;
    }
    .highlight {
        color: #4CAF50;
        font-weight: bold;
    }
    .header {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.markdown("### Tentang EOQ")
    st.markdown("""
    Economic Order Quantity (EOQ) adalah model inventaris yang menentukan jumlah pesanan optimal
    yang meminimalkan total biaya persediaan.
    """)

# Main content
st.title("📊 Aplikasi Perhitungan EOQ")
st.markdown("## Perhitungan Kuantitas Pesanan")

# Custom formatter for currency
def format_rp(x, pos):
    return f"Rp {x:,.0f}"

# Initialize session state
if 'input_values' not in st.session_state:
    st.session_state.input_values = {'D': 1, 'S': 0.0, 'H': 0.0}

# Case studies
case_studies = {
    "Manual": {'D': 1, 'S': 0.0, 'H': 0.0},
    "Toko Alat Tulis Smart Office": {'D': 5000, 'S': 200000.0, 'H': 5000.0}
}

# Input section in two columns
col1, col2 = st.columns([0.4, 0.6], gap="large")

with col1:
    with st.expander("📋 Input Data", expanded=True):
        selected_case = st.selectbox(
            "Pilih studi kasus:",
            options=list(case_studies.keys()),
            index=0,
            key="case_study"
        )
        
        if selected_case != "Manual":
            st.session_state.input_values = case_studies[selected_case]
            st.success(f"Data studi kasus '{selected_case}' berhasil dimasukkan.")

        st.session_state.input_values['D'] = st.number_input(
            "Permintaan tahunan (unit)",
            min_value=1,
            value=st.session_state.input_values['D'],
            step=1,
            key="D_input"
        )
        st.session_state.input_values['S'] = st.number_input(
            "Biaya pemesanan per pesanan (Rp)",
            min_value=0.0,
            value=st.session_state.input_values['S'],
            step=100.0,
            key="S_input"
        )
        st.session_state.input_values['H'] = st.number_input(
            "Biaya penyimpanan per unit per tahun (Rp)",
            min_value=0.0,
            value=st.session_state.input_values['H'],
            step=100.0,
            key="H_input"
        )

        calculate = st.button("**Hitung EOQ**", use_container_width=True)

with col2:
    if calculate and st.session_state.input_values['D'] > 0 and st.session_state.input_values['S'] > 0 and st.session_state.input_values['H'] > 0:
        D = st.session_state.input_values['D']
        S = st.session_state.input_values['S']
        H = st.session_state.input_values['H']
        
        EOQ = math.sqrt((2 * D * S) / H)
        jumlah_pemesanan = D / EOQ
        total_biaya = (EOQ / 2 * H) + (D / EOQ * S)
        
        with st.container():
            st.subheader("📋 Hasil Perhitungan")
            
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.markdown(f"""
                <div class="result-card">
                    <h4>EOQ Optimal</h4>
                    <h2 style="color:#4CAF50;">{EOQ:.2f}</h2>
                    <p>unit per pesanan</p>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col2:
                st.markdown(f"""
                <div class="result-card">
                    <h4>Frekuensi Pemesanan</h4>
                    <h2 style="color:#4CAF50;">{jumlah_pemesanan:.2f}</h2>
                    <p>kali per tahun</p>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col3:
                st.markdown(f"""
                <div class="result-card">
                    <h4>Total Biaya Tahunan</h4>
                    <h2 style="color:#4CAF50;">Rp {round(total_biaya):,}</h2>
                    <p>biaya persediaan total</p>
                </div>
                """, unsafe_allow_html=True)

        # Visualization
        st.markdown("---")
        st.subheader("📊 Visualisasi Hasil")

        order_quantities = np.linspace(1, 2 * EOQ, 100)
        total_costs = (order_quantities / 2 * H) + (D / order_quantities * S)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(order_quantities, total_costs, label='Total Biaya', color='#3498db', linewidth=2.5)
        ax.axvline(x=EOQ, color='#e74c3c', linestyle='--', linewidth=1.5, label='EOQ Optimal')
        ax.scatter(EOQ, total_biaya, color='#e74c3c', s=100, zorder=5)
        ax.set_title('Hubungan Kuantitas Pesanan dan Total Biaya', fontsize=14, pad=20)
        ax.set_xlabel('Kuantitas Pesanan (unit)', fontsize=12)
        ax.set_ylabel('Total Biaya (Rp)', fontsize=12)
        ax.yaxis.set_major_formatter(FuncFormatter(format_rp))
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)

        with st.expander("🔍 Detail Perhitungan"):
            st.markdown(f"""
            **Rumus EOQ**:  
            `EOQ = √(2 * D * S / H)`  
            Dimana:  
            - D = Permintaan tahunan (`{D:.0f} unit`)  
            - S = Biaya pemesanan (`{S:,.0f} per pesanan`)  
            - H = Biaya penyimpanan (`{H:,.0f} per unit/tahun`)  
            
            **Perhitungan**:  
            EOQ = √(2 × {D} × {S:,.0f} ÷ {H:,.0f}) = **{EOQ:.2f} unit**
            """)
    elif calculate:
        st.error("⚠️ Mohon lengkapi semua input dengan nilai lebih dari 0")
        
# 👣 Footer
st.markdown('<div class="footer"> TUGAS ASWA SEPTIAN</div>', unsafe_allow_html=True)
