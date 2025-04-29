# app.py

import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd

# --- PAGE TITLE ---
st.title("🏡 Property Pal - Maryland Property Map")

# --- LOAD GEOJSON DATA ---
@st.cache_data
def load_data():
    gdf = gpd.read_file('Maryland_Property_Data_-_Tax_Map_Grids (1).geojson')
    return gdf

gdf = load_data()

# --- STREAMLIT UI ---
st.header("Search Maryland Properties")

address_query = st.text_input("Enter part of the Property Address")

# --- CREATE BASE MAP ---
map_center = [39.0458, -76.6413]  # Maryland center coordinates
m = folium.Map(location=map_center, zoom_start=8)

# --- FILTER BASED ON USER INPUT ---
if address_query:
    matches = gdf[gdf['PropertyAddress'].str.contains(address_query, case=False, na=False)]

    if not matches.empty:
        st.success(f"✅ Found {len(matches)} matching properties.")
        # Add matching properties to the map
        for _, row in matches.iterrows():
            coords = row.geometry.centroid.coords[0]  # Get the (lon, lat)
            folium.Marker(
                location=[coords[1], coords[0]],  # folium expects (lat, lon)
                popup=row['PropertyAddress'],
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(m)
    else:
        st.error("❌ No matching properties found.")
else:
    st.info("ℹ️ Enter a property address to search.")

# --- DISPLAY THE MAP ---
folium_static(m)

