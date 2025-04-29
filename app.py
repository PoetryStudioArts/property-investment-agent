# --- IMPORTS ---
import os
import geopandas as gpd
import streamlit as st
import pydeck as pdk

# --- DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    filename = 'Maryland_Property_Data_-_Tax_Map_Grids (1).geojson'

    if not os.path.exists(filename):
        st.error(f"Error: File '{filename}' not found. Please upload it.")
        st.stop()

    try:
        gdf = gpd.read_file(filename)
    except Exception as e:
        st.error(f"Error: Failed to read GeoJSON file. {e}")
        st.stop()

    return gdf

# --- STREAMLIT APP CONFIG ---
st.set_page_config(page_title="Maryland Property Investment Agent", layout="wide")

st.title("🏡 Maryland Property Investment Agent")

# --- LOAD DATA ---
gdf = load_data()

if gdf is not None:
    st.subheader("Loaded Property Grid Data")
    st.dataframe(gdf)

    geojson = gdf.__geo_interface__

    # --- PYDECK LAYER ---
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        get_fill_color="[200, 30, 0, 160]",
        get_line_color=[0, 0, 0],
        pickable=True,
        stroked=True
    )

    view_state = pdk.ViewState(
        latitude=38.8, longitude=-77.2, zoom=8
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Grid Area"}
    )

    st.subheader("Property Tax Grid Map")
    st.pydeck_chart(deck)
else:
    st.error("GeoDataFrame not loaded. Cannot visualize.")





