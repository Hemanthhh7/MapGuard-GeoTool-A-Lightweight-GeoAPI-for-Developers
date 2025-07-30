import streamlit as st
import requests
from math import radians, sin, cos, sqrt, atan2
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MapGuard GeoTool", layout="wide")

# 🔑 Set your Google Maps API Key
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

st.title("🛡️ MapGuard GeoTool – Dev Utility for Geolocation APIs")

# 📍 Sidebar Navigation
choice = st.sidebar.radio("Choose a Tool", ["Geocode", "Reverse Geocode", "Distance", "Risk Score"])

# 🌐 Geocode
if choice == "Geocode":
    st.subheader("🌍 Geocode: Address → Coordinates")
    address = st.text_input("Enter address")
    if st.button("Get Coordinates"):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
        res = requests.get(url).json()
        if res["status"] == "OK":
            loc = res["results"][0]["geometry"]["location"]
            st.success(f"Lat: {loc['lat']} | Lng: {loc['lng']}")
            m = folium.Map(location=[loc['lat'], loc['lng']], zoom_start=15)
            folium.Marker([loc['lat'], loc['lng']], popup=address).add_to(m)
            st_folium(m, width=700)
        else:
            st.error(f"Error: {res['status']}")

# 📍 Reverse Geocode
elif choice == "Reverse Geocode":
    st.subheader("📍 Reverse Geocode: Coordinates → Address")
    lat = st.number_input("Latitude", format="%.6f")
    lng = st.number_input("Longitude", format="%.6f")
    if st.button("Get Address"):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={API_KEY}"
        res = requests.get(url).json()
        if res["status"] == "OK":
            addr = res["results"][0]["formatted_address"]
            st.success(f"Address: {addr}")
            m = folium.Map(location=[lat, lng], zoom_start=15)
            folium.Marker([lat, lng], popup=addr).add_to(m)
            st_folium(m, width=700)
        else:
            st.error(f"Error: {res['status']}")

# 📏 Distance Calculator
elif choice == "Distance":
    st.subheader("📏 Distance: Between Two Coordinates (km)")
    lat1 = st.number_input("Start Latitude", key="lat1", format="%.6f")
    lng1 = st.number_input("Start Longitude", key="lng1", format="%.6f")
    lat2 = st.number_input("End Latitude", key="lat2", format="%.6f")
    lng2 = st.number_input("End Longitude", key="lng2", format="%.6f")
    if st.button("Calculate Distance"):
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lng2 - lng1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        dist = R * c
        st.success(f"Distance: {round(dist, 2)} km")
        m = folium.Map(location=[(lat1+lat2)/2, (lng1+lng2)/2], zoom_start=10)
        folium.Marker([lat1, lng1], popup="Start", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([lat2, lng2], popup="End", icon=folium.Icon(color='red')).add_to(m)
        folium.PolyLine([[lat1, lng1], [lat2, lng2]], color="blue").add_to(m)
        st_folium(m, width=700)

# 🤖 Risk Score (Fake AI)
elif choice == "Risk Score":
    st.subheader("🤖 AI Risk Score (Dummy Logic)")
    lat = st.number_input("Latitude", key="rlat", format="%.6f")
    lng = st.number_input("Longitude", key="rlng", format="%.6f")
    if st.button("Get Risk Score"):
        score = (lat % 1 + lng % 1) * 50
        st.warning(f"Predicted Risk Score: {round(score, 2)}")
        m = folium.Map(location=[lat, lng], zoom_start=13)
        folium.Circle([lat, lng], radius=300, color="red", fill=True, popup=f"Risk Score: {round(score, 2)}").add_to(m)
        st_folium(m, width=700)
