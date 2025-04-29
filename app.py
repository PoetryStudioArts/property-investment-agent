# --- LOAD GEOJSON DATA ---
import os
import json
import geopandas as gpd
import streamlit as st
import pydeck as pdk

@st.cache_data
def load_data():
    filename = 'Maryland_Property_Data_-_Tax_Map_Grids (1).geojson'

    # Step 1: Check if the file exists
    if not os.path.exists(filename):
        st.error(f"Error: File '{filename}' not found. Please make sure the GeoJSON file is correctly uploaded.")
        st.stop()

    # Step 2: Try opening it as JSON
    try:
        with open(filename) as f:
            data = json.load(f)
        if "features" not in data:
            st.error(f"Error: The file '{filename}' does not appear to contain valid GeoJSON 'features'.")
            st.stop()
    except json.JSONDecodeError as e:
        st.error(f"Error: File '{filename}' is not valid JSON. {e}")
        st.stop()

    # Step 3: Try loading it with geopandas
    try:
        gdf = gpd.read_file(filename)
    except Exception as e:
        st.error(f"Error: Failed to load GeoJSON file with geopandas. {e}")
        st.stop()

    return gdf

# --- STREAMLIT APP SETUP ---
st.set_page_config(page_title="Maryland Property Investment Agent", layout="wide")

st.title("🏡 Maryland Property Investment Agent")

gdf = load_data()

if gdf is not None:
    st.subheader("Loaded Data Preview")
    st.dataframe(gdf)

    geojson = gdf.__geo_interface__

    layer = pdk.Layer(
        'GeoJsonLayer',
        geojson,
        get_fill_color='[200, 30, 0, 160]',
        get_line_color=[0, 0, 0],
        pickable=True,
        stroked=True
    )

    view_state = pdk.ViewState(latitude=38.8, longitude=-77.2, zoom=8)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Grid Area"}
    )

    st.subheader("Property Tax Grid Map")
    st.pydeck_chart(deck)
else:
    st.error("GeoDataFrame not loaded. Cannot visualize.")


