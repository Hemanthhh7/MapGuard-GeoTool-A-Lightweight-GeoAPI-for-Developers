import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# --- PAGE CONFIG ---
st.set_page_config(page_title="MapGuard GeoTool", layout="wide")
st.title("🛡️ MapGuard GeoTool – Dev Utility for Geolocation APIs")

# --- SIDEBAR TOOL SELECT ---
tool = st.sidebar.radio("Choose a Tool", ["Geocode", "Reverse Geocode", "Distance", "Risk Score"])

# --- STATE ---
if "geo" not in st.session_state:
    st.session_state.geo = {"lat": None, "lon": None, "address": ""}

# --- COMMON FUNCTION ---
def geocode_nominatim(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200 and r.json():
        d = r.json()[0]
        return float(d["lat"]), float(d["lon"])
    return None, None

def reverse_geocode_nominatim(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        return r.json().get("display_name", "Unknown")
    return "Unknown"

# --- GEOCODE ---
if tool == "Geocode":
    st.markdown("#### 📍 Geocode: Address ➝ Coordinates")
    addr = st.text_input("Enter Address", value="Connaught Place, New Delhi, India")
    if st.button("🔍 Get Coordinates"):
        lat, lon = geocode_nominatim(addr)
        if lat:
            st.session_state.geo = {"lat": lat, "lon": lon, "address": addr}
            st.success(f"Latitude: {lat}, Longitude: {lon}")
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=addr).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.error("Failed to geocode. Try a different address.")

# --- REVERSE GEOCODE ---
elif tool == "Reverse Geocode":
    st.markdown("#### 🗺️ Reverse Geocode: Coordinates ➝ Address")
    lat = st.number_input("Latitude", value=28.6328, format="%.6f")
    lon = st.number_input("Longitude", value=77.2197, format="%.6f")
    if st.button("🔁 Get Address"):
        addr = reverse_geocode_nominatim(lat, lon)
        st.success(f"📍 Address: {addr}")
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], popup=addr).add_to(m)
        st_folium(m, width=700, height=500)

# --- DISTANCE ---
elif tool == "Distance":
    st.markdown("#### 📏 Distance Between Two Locations")
    col1, col2 = st.columns(2)
    with col1:
        from_addr = st.text_input("From Address", "Connaught Place, New Delhi")
    with col2:
        to_addr = st.text_input("To Address", "Red Fort, Delhi")
    if st.button("📐 Calculate Distance"):
        lat1, lon1 = geocode_nominatim(from_addr)
        lat2, lon2 = geocode_nominatim(to_addr)
        if lat1 and lat2:
            dist = geodesic((lat1, lon1), (lat2, lon2)).km
            st.success(f"🛣️ Distance: {dist:.2f} km")
            m = folium.Map(location=[(lat1+lat2)/2, (lon1+lon2)/2], zoom_start=13)
            folium.Marker([lat1, lon1], popup="From").add_to(m)
            folium.Marker([lat2, lon2], popup="To").add_to(m)
            folium.PolyLine([[lat1, lon1], [lat2, lon2]], color="blue").add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.error("Geocoding failed for one or both addresses.")

# --- RISK SCORE (DEMO) ---
elif tool == "Risk Score":
    st.markdown("#### ⚠️ Area Risk Score (Simulated)")
    area = st.text_input("Enter Area Name", "Seelampur, Delhi")
    if st.button("🚨 Get Risk Score"):
        import random
        score = random.randint(1, 100)
        if score > 75:
            level = "High"
            color = "red"
        elif score > 40:
            level = "Moderate"
            color = "orange"
        else:
            level = "Low"
            color = "green"
        st.markdown(f"**🧪 Risk Score for `{area}`: `{score}` ({level})**")
        st.progress(score / 100)
