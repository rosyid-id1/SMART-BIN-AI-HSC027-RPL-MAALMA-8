import streamlit as st
import requests
import time


UBIDOTS_TOKEN = "BBUS-RP0OHVhu4wjCztt03F8vCDvxMIfzpz"
DEVICE_LABEL = "rpl-8"
VARIABLE_LABEL = "jarak-sampah"
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_LABEL}/lv"
HEADERS = {
    "X-Auth-Token": UBIDOTS_TOKEN,
    "Content-Type": "application/json"
}


st.set_page_config(page_title="Smart Trash Monitor", layout="centered")
st.title("🗑️ Smart Trash Monitoring")
st.subheader("📏 Jarak Sampah ke Tutup (dalam cm)")

refresh_rate = st.slider("Interval Refresh (detik)", 1, 60, 5)
placeholder = st.empty()

def get_distance():
    try:
        response = requests.get(UBIDOTS_URL, headers=HEADERS)
        if response.status_code == 200:
            return float(response.text)
        else:
            st.warning("Gagal mengambil data dari Ubidots.")
            return None
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return None

while True:
    distance = get_distance()
    if distance is not None:
        placeholder.metric(label="Jarak Ultrasonik", value=f"{distance:.2f} cm")
    time.sleep(refresh_rate)
