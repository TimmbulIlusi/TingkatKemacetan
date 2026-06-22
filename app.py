import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Fuzzy Tingkat Kemacetan",
    page_icon="🚦",
    layout="centered"
)

# ==========================
# IDENTITAS
# ==========================
st.title("🚦 Sistem Fuzzifikasi Tingkat Kemacetan")


st.markdown("---")

st.write("""
Aplikasi ini digunakan untuk menentukan tingkat kemacetan
berdasarkan jumlah kendaraan menggunakan Logika Fuzzy.
""")

# ==========================
# INPUT
# ==========================
kendaraan = st.number_input(
    "Masukkan Jumlah Kendaraan",
    min_value=0,
    max_value=1000,
    value=700,
    step=1
)

# ==========================
# FUNGSI KEANGGOTAAN
# ==========================

def lancar(x):
    if x <= 300:
        return 1
    elif 300 < x < 600:
        return (600 - x) / 300
    else:
        return 0


def padat(x):
    if x <= 300 or x >= 900:
        return 0
    elif 300 < x < 600:
        return (x - 300) / 300
    elif 600 <= x < 900:
        return (900 - x) / 300
    else:
        return 0


def macet(x):
    if x <= 600:
        return 0
    elif 600 < x < 900:
        return (x - 600) / 300
    else:
        return 1


# ==========================
# TOMBOL PROSES
# ==========================
if st.button("Hitung Tingkat Kemacetan"):

    nilai_lancar = round(lancar(kendaraan), 2)
    nilai_padat = round(padat(kendaraan), 2)
    nilai_macet = round(macet(kendaraan), 2)

    # ==========================
    # TABEL HASIL
    # ==========================
    st.subheader("Hasil Fuzzifikasi")

    hasil = pd.DataFrame({
        "Jumlah Kendaraan": [kendaraan],
        "Lancar": [nilai_lancar],
        "Padat": [nilai_padat],
        "Macet": [nilai_macet]
    })

    st.table(hasil)

    # ==========================
    # PERHITUNGAN
    # ==========================
    st.subheader("Perhitungan")

    # Lancar
    if kendaraan <= 300:
        st.write("μ Lancar = 1")
    elif kendaraan < 600:
        st.write(
            f"μ Lancar = (600 - {kendaraan}) / 300 = {nilai_lancar}"
        )
    else:
        st.write("μ Lancar = 0")

    # Padat
    if 300 < kendaraan < 600:
        st.write(
            f"μ Padat = ({kendaraan} - 300) / 300 = {nilai_padat}"
        )
    elif 600 <= kendaraan < 900:
        st.write(
            f"μ Padat = (900 - {kendaraan}) / 300 = {nilai_padat}"
        )
    else:
        st.write(f"μ Padat = {nilai_padat}")

    # Macet
    if kendaraan <= 600:
        st.write("μ Macet = 0")
    elif kendaraan < 900:
        st.write(
            f"μ Macet = ({kendaraan} - 600) / 300 = {nilai_macet}"
        )
    else:
        st.write("μ Macet = 1")

    # ==========================
    # KATEGORI DOMINAN
    # ==========================
    kategori = {
        "Lancar": nilai_lancar,
        "Padat": nilai_padat,
        "Macet": nilai_macet
    }

    hasil_tertinggi = max(kategori, key=kategori.get)

    st.subheader("Kategori Dominan")
    st.success(f"Tingkat Kemacetan: {hasil_tertinggi}")

    # ==========================
    # GRAFIK
    # ==========================
    st.subheader("Grafik Fungsi Keanggotaan")

    x = np.arange(0, 1001, 1)

    y_lancar = [lancar(i) for i in x]
    y_padat = [padat(i) for i in x]
    y_macet = [macet(i) for i in x]

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(x, y_lancar, linewidth=2, label="Lancar")
    ax.plot(x, y_padat, linewidth=2, label="Padat")
    ax.plot(x, y_macet, linewidth=2, label="Macet")

    # garis input
    ax.axvline(
        kendaraan,
        linestyle="--",
        linewidth=1.5,
        label=f"Input = {kendaraan}"
    )

    # titik hasil
    ax.scatter(kendaraan, nilai_lancar, s=60)
    ax.scatter(kendaraan, nilai_padat, s=60)
    ax.scatter(kendaraan, nilai_macet, s=60)

    ax.set_title("Grafik Tingkat Kemacetan")
    ax.set_xlabel("Jumlah Kendaraan")
    ax.set_ylabel("Derajat Keanggotaan")
    ax.set_ylim(0, 1.1)

    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
