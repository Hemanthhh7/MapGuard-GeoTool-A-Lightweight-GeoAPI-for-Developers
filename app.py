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

# Function to call Nominatim
def geocode_with_nominatim(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data["lat"]), float(data["lon"])
    return None, None

# Initialize session state
if "lat" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None
    st.session_state.address_shown = ""

# Geocode Tool
if tool == "Geocode":
    address = st.text_input("Enter address", value="Connaught Place, New Delhi, India")

    if st.button("🔍 Get Coordinates"):
        lat, lon = geocode_with_nominatim(address)
        if lat and lon:
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.address_shown = address
        else:
            st.error("⚠️ Could not fetch coordinates. Try a different address.")

    # If lat/lon present in session state, show them and map
    if st.session_state.lat and st.session_state.lon:
        st.success(f"📍 Latitude: {st.session_state.lat}, Longitude: {st.session_state.lon}")
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=15)
        folium.Marker([st.session_state.lat, st.session_state.lon],
                      popup=st.session_state.address_shown).add_to(m)
        st_folium(m, width=700, height=500)
