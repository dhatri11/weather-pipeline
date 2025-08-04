from streamlit_autorefresh import st_autorefresh
import streamlit as st
import requests

# Auto-refresh every 10 seconds
st_autorefresh(interval=10_000, key="weather_refresh")

# Set page config
st.set_page_config(page_title="ClimaWatch: City Weather Tracker", layout="centered")

# Modern dark styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
        font-family: 'Segoe UI', sans-serif;
    }

    .big-font {
        font-size: 32px !important;
        color: #38bdf8;
        font-weight: bold;
        text-align: center;
    }

    .weather-box {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.5);
        text-align: left;
        transition: transform 0.2s ease-in-out;
    }

    .weather-box:hover {
        transform: scale(1.01);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }

    .alert {
        background-color: #ef4444;
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin-top: 18px;
        font-weight: bold;
        animation: blink 1.2s infinite;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="big-font">🌐  City Weather Tracker</h1>', unsafe_allow_html=True)

# API endpoint
API_URL = "http://localhost:5000/weather"

# Collect sidebar alerts
critical_alerts = []

try:
    response = requests.get(API_URL)
    weather_data = response.json()

    if isinstance(weather_data, list):
        for item in weather_data:
            city = item.get("city", "Unknown")
            temperature = item.get("temperature", "--")
            humidity = item.get("humidity", "--")
            description = item.get("description", "--")  # ✅ Make sure API sends this

            # Alert logic
            alert_message = ""
            if temperature != "--":
                if temperature > 40:
                    alert_message = "🔥 Heat Alert: Stay hydrated!"
                elif temperature < 5:
                    alert_message = "❄️ Cold Alert: Dress warmly!"
            if humidity != "--" and humidity > 85:
                alert_message += " 💧 Humidity Alert: Stay indoors if sensitive."

            # Collect sidebar alert
            if alert_message:
                critical_alerts.append(f"{city}: {alert_message}")

            # Display weather card
            with st.container():
                st.markdown('<div class="weather-box">', unsafe_allow_html=True)
                st.markdown(f"### 📍 City: {city}")
                st.markdown(f"🌡 **Temperature:** {temperature} °C")
                st.markdown(f"💧 **Humidity:** {humidity} %")
                st.markdown(f"☁️ **Condition:** {description}")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠ API did not return a list of cities.")

except Exception as e:
    st.error("⚠ Could not fetch weather data. Make sure your FastAPI server is running.")
    st.exception(e)

# Sidebar alert display
if critical_alerts:
    st.sidebar.markdown("### 🚨 Active Weather Alerts")
    for alert in critical_alerts:
        st.sidebar.warning(alert)
