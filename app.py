# --- IMPORTS ---
import os
import json
import geopandas as gpd
import streamlit as st
import pydeck as pdk

# --- SMART GEOJSON LOADER ---
def smart_load_geojson(filename):
    """
    Loads a GeoJSON or JSON-like file, trying to correct common issues
    like missing 'features' wrapping, service exports, or ArcGIS quirks.
    Returns a GeoJSON dictionary ready for use with geopandas or pydeck.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # --- Normal case: valid FeatureCollection
    if data.get("type") == "FeatureCollection" and "features" in data:
        return data

    # --- ArcGIS case: wrapped inside 'layers' or 'featureSet'
    if "layers" in data:
        features = []
        for layer in data["layers"]:
            if "featureSet" in layer and "features" in layer["featureSet"]:
                features.extend(layer["featureSet"]["features"])
        return {
            "type": "FeatureCollection",
            "features": features
        }

    # --- ArcGIS serviceDefinition case (common)
    if "serviceDefinition" in data:
        if "layers" in data["serviceDefinition"]:
            features = []
            for layer in data["serviceDefinition"]["layers"]:
                if "featureSet" in layer and "features" in layer["featureSet"]:
                    features.extend(layer["featureSet"]["features"])
            return {
                "type": "FeatureCollection",
                "features": features
            }

    # --- Unknown structure
    raise ValueError("Unsupported file format: could not find 'features' or recognized structure.")

# --- DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    filename = 'Maryland_Property_Data_-_Tax_Map_Grids (1).geojson'

    # Step 1: Check if the file exists
    if not os.path.exists(filename):
        st.error(f"Error: File '{filename}' not found. Please make sure the GeoJSON file is correctly uploaded.")
        st.stop()

    # Step 2: Use the smart loader to handle odd structures
    try:
        data = smart_load_geojson(filename)
    except Exception as e:
        st.error(f"Error: Could not load the file as GeoJSON. {e}")
        st.stop()

    # Step 3: Create a GeoDataFrame from smart-loaded data
    try:
        gdf = gpd.GeoDataFrame.from_features(data["features"])
    except Exception as e:
        st.error(f"Error: Failed to convert features into a GeoDataFrame. {e}")
        st.stop()

    return gdf, data  # return both for visualization

# --- STREAMLIT APP ---
st.set_page_config(page_title="Maryland Property Investment Agent", layout="wide")

st.title("🏡 Maryland Property Investment Agent")

gdf, geojson = load_data()

if gdf is not None:
    st.subheader("Loaded Data Preview")
    st.dataframe(gdf)

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



