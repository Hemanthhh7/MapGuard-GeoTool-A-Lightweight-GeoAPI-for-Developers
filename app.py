import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import random

# --- Streamlit Setup ---
st.set_page_config(page_title="🛡️ MapGuard GeoTool", layout="wide")
st.title("🛡️ MapGuard GeoTool")
st.markdown("A developer-friendly toolkit for geolocation, reverse geocoding, distance & simulated risk scoring.")

# --- Sidebar Selection ---
tool = st.sidebar.radio("Select Tool", ["Geocode", "Reverse Geocode", "Distance", "Risk Score"])

# --- Session State Defaults ---
if "geo_result" not in st.session_state:
    st.session_state.geo_result = None
if "reverse_result" not in st.session_state:
    st.session_state.reverse_result = None
if "distance_result" not in st.session_state:
    st.session_state.distance_result = None
if "risk_score" not in st.session_state:
    st.session_state.risk_score = None

# --- Utility Functions ---
def geocode_nominatim(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200 and r.json():
        d = r.json()[0]
        return float(d["lat"]), float(d["lon"])
    return None, None

def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json"}
    headers = {"User-Agent": "MapGuard-App"}
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        return r.json().get("display_name", "Unknown")
    return "Unknown"

# --- Geocode Tool ---
if tool == "Geocode":
    st.subheader("📍 Geocode: Address ➝ Coordinates")
    address = st.text_input("Enter Address", "Connaught Place, New Delhi")
    if st.button("🔍 Get Coordinates"):
        lat, lon = geocode_nominatim(address)
        if lat and lon:
            st.session_state.geo_result = {
                "lat": lat,
                "lon": lon,
                "address": address
            }
        else:
            st.error("❌ Failed to fetch coordinates.")

    if st.session_state.geo_result:
        lat = st.session_state.geo_result["lat"]
        lon = st.session_state.geo_result["lon"]
        address = st.session_state.geo_result["address"]
        st.success(f"📌 Address: `{address}`\n\n🧭 Latitude: `{lat}`, Longitude: `{lon}`")
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], popup=address).add_to(m)
        st_folium(m, width=700, height=500)

# --- Reverse Geocode Tool ---
elif tool == "Reverse Geocode":
    st.subheader("🗺️ Reverse Geocode: Coordinates ➝ Address")
    lat = st.number_input("Latitude", value=28.6328, format="%.6f")
    lon = st.number_input("Longitude", value=77.2197, format="%.6f")
    if st.button("🔁 Get Address"):
        address = reverse_geocode(lat, lon)
        st.session_state.reverse_result = {
            "lat": lat,
            "lon": lon,
            "address": address
        }

    if st.session_state.reverse_result:
        result = st.session_state.reverse_result
        st.success(f"📍 Address: `{result['address']}`")
        m = folium.Map(location=[result["lat"], result["lon"]], zoom_start=15)
        folium.Marker([result["lat"], result["lon"]], popup=result["address"]).add_to(m)
        st_folium(m, width=700, height=500)

# --- Distance Tool ---
elif tool == "Distance":
    st.subheader("📏 Distance Between Two Locations")
    col1, col2 = st.columns(2)
    with col1:
        addr1 = st.text_input("From Address", "Connaught Place, New Delhi")
    with col2:
        addr2 = st.text_input("To Address", "Red Fort, Delhi")
    if st.button("📐 Calculate Distance"):
        lat1, lon1 = geocode_nominatim(addr1)
        lat2, lon2 = geocode_nominatim(addr2)
        if lat1 and lat2:
            dist = geodesic((lat1, lon1), (lat2, lon2)).km
            st.session_state.distance_result = {
                "from": (lat1, lon1, addr1),
                "to": (lat2, lon2, addr2),
                "km": dist
            }
        else:
            st.error("❌ Failed to geocode one or both addresses.")

    if st.session_state.distance_result:
        res = st.session_state.distance_result
        st.success(f"🛣️ Distance between `{res['from'][2]}` and `{res['to'][2]}`: `{res['km']:.2f} km`")
        m = folium.Map(location=[(res['from'][0] + res['to'][0]) / 2,
                                 (res['from'][1] + res['to'][1]) / 2], zoom_start=13)
        folium.Marker([res['from'][0], res['from'][1]], popup="From").add_to(m)
        folium.Marker([res['to'][0], res['to'][1]], popup="To").add_to(m)
        folium.PolyLine([[res['from'][0], res['from'][1]], [res['to'][0], res['to'][1]]],
                        color="blue").add_to(m)
        st_folium(m, width=700, height=500)

# --- Risk Score Tool ---
elif tool == "Risk Score":
    st.subheader("⚠️ Simulated Risk Score (Demo)")
    area = st.text_input("Enter Area Name", "Seelampur, Delhi")
    if st.button("🚨 Generate Risk Score"):
        score = random.randint(1, 100)
        if score >= 75:
            level = "High"
            color = "red"
        elif score >= 40:
            level = "Moderate"
            color = "orange"
        else:
            level = "Low"
            color = "green"
        st.session_state.risk_score = {"area": area, "score": score, "level": level, "color": color}

    if st.session_state.risk_score:
        rs = st.session_state.risk_score
        st.markdown(f"### 🧪 Risk for `{rs['area']}`: **{rs['score']}** / 100")
        st.markdown(f"### 🧯 Level: **:{rs['color']}[{rs['level']}]**")
        st.progress(rs['score'] / 100)
