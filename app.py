import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("📊 Dashboard Monitoring Vibrasi Bearing Pompa")

# Load data historis
hist_df = pd.read_csv("historis_vibrasi_simulasi.csv")
hist_df["Timestamp"] = pd.to_datetime(hist_df["Timestamp"])

# Load data prediksi
forecast_df = pd.read_csv("forecast_vibrasi_7hari.csv")
forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])

# Batas getaran aman
threshold = 0.04

# Layout dua kolom
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Tren Historis Vibrasi")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(hist_df["Timestamp"], hist_df["Acceleration RMS (g)"], label="Vibrasi RMS")
    ax.axhline(threshold, color='r', linestyle='--', label='Ambang Batas')
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Vibrasi (g)")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("🔮 Prediksi Vibrasi 7 Hari ke Depan")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(forecast_df["ds"], forecast_df["yhat"], label="Prediksi")
    ax2.fill_between(forecast_df["ds"], forecast_df["yhat_lower"], forecast_df["yhat_upper"], alpha=0.3, label="Confidence Interval")
    ax2.axhline(threshold, color='r', linestyle='--', label='Ambang Batas')
    ax2.set_xlabel("Waktu")
    ax2.set_ylabel("Vibrasi (g)")
    ax2.legend()
    st.pyplot(fig2)

# Alert jika prediksi melebihi batas
alert_df = forecast_df[forecast_df["yhat"] > threshold][["ds", "yhat"]]
if not alert_df.empty:
    st.warning(f"⚠️ {len(alert_df)} jam ke depan diprediksi melebihi batas vibrasi!")
    st.dataframe(alert_df.rename(columns={"ds": "Waktu", "yhat": "Prediksi Vibrasi (g)"}))
else:
    st.success("✅ Semua prediksi berada di bawah ambang batas.")
