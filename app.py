# app.py

import streamlit as st
import requests

# --- PAGE TITLE ---
st.title("🏡 Property Pal - Real Estate Research Assistant")

# --- FUNCTIONS TO QUERY PROPERTY DATA ---

def search_property_maryland(address):
    """Search Maryland property tax data."""
    endpoint = "https://data.imap.maryland.gov/arcgis/rest/services/GeocodeServices/MD_Composite_Locator/GeocodeServer/findAddressCandidates"
    params = {
        "SingleLine": address,
        "f": "json",
        "outFields": "*",
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

if response.headers['Content-Type'] == 'application/json':
        try:
            data = response.json()  # Attempt to parse as JSON
except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON. Response text:", response.text)
         return None  # Return None or handle the error as needed
else:
        print("Received non-JSON response:", response.text)
        return None  # Return None or handle the error as needed
        
        return data

# --- STREAMLIT UI ---

st.header("Search for a Property Address")

address = st.text_input("Enter Address (MD, VA, WV)")
state = st.selectbox("Select State", ["Maryland", "Virginia", "West Virginia"])

if st.button("🔎 Search"):
    if state == "Maryland":
        location = search_property_maryland(address)
        if location:
            st.success(f"✅ Found Property Coordinates: {location}")
            # Here you would call another function to pull tax data for MD using the location
            st.info("ℹ️ Property tax data retrieval coming soon...")
        else:
            st.error("❌ Property not found in Maryland database.")

    elif state == "Virginia":
        st.warning("⚠️ Virginia tax data connection not set up yet.")

    elif state == "West Virginia":
        st.warning("⚠️ West Virginia tax data connection not set up yet.")
