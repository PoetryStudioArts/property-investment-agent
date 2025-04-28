# app.py

import streamlit as st
import geopandas as gpd
import folium
import os

# --- PAGE TITLE ---
st.title("🏡 USDA Property Eligibility Map")

# --- LOAD SHAPEFILE ---
st.header("Load USDA Ineligible Areas Shapefile")

# Path to your shapefile (relative to project root)
shapefile_path = 'USDA_Data/SFH_MFH_Ineligible.shp'

# Check if file exists
if not os.path.exists(shapefile_path):
    st.error(f"❌ Shapefile not found at {shapefile_path}")
else:
    try:
        gdf = gpd.read_file(shapefile_path)
        st.success("✅ Successfully loaded USDA shapefile!")

        # Display basic info
        st.subheader("Shapefile Details")
        st.write(gdf.head())

                # --- PLOT MAP ---
        st.subheader("Map of Ineligible Areas")

        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='orange', edgecolor='black')
        ax.set_title("USDA Ineligible Areas Map")  # Add a title to the map
        ax.axis('off')  # Hide x and y axis
        st.pyplot(fig)
 
    except Exception as e: st.error(f":red[Error loading shapefile: {e}]") 
      

    except Exception as e:
        st.error(f"🚨 Error loading shapefile: {e}")
