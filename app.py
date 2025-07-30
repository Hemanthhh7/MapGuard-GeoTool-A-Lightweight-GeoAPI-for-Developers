import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# Page setup
st.set_page_config(page_title="MapGuard GeoTool", layout="wide")
st.title("🛡️ MapGuard GeoTool – Dev Utility for Geolocation APIs")
st.markdown("#### 🌍 Geocode: Address → Coordinates")

# Sidebar
tool = st.sidebar.radio("Choose a Tool", ["Geocode", "Reverse Geocode", "Distance", "Risk Score"])

# Geocode using OpenStreetMap Nominatim
def geocode_with_nominatim(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data["lat"]), float(data["lon"])
    else:
        return None, None

# Main logic
if tool == "Geocode":
    address = st.text_input("Enter address", "Connaught Place, New Delhi, India")
    if st.button("🔍 Get Coordinates"):
        lat, lon = geocode_with_nominatim(address)
        if lat and lon:
            st.success(f"📍 Latitude: {lat}, Longitude: {lon}")
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=address).add_to(m)
            st_folium(m, width=700)
        else:
            st.error("⚠️ Could not fetch coordinates. Try a different address.")

elif tool == "Reverse Geocode":
    st.info("🚧 Coming soon: Reverse Geocoding with OpenStreetMap")

elif tool == "Distance":
    st.info("🚧 Coming soon: Distance Calculator")

elif tool == "Risk Score":
    st.info("🚧 Coming soon: Risk Score Simulator")
