# app.py

import streamlit as st
import requests

# --- PAGE TITLE ---
st.title("🏡 Property Pal - Real Estate Research Assistant")

# --- FUNCTIONS TO QUERY PROPERTY DATA ---

def search_property_maryland(address):
    response = requests.get(f"http://api.example.com/search?address={address}")

    if response.status_code == 200:
        try:
            data = response.json()  # Attempt to parse as JSON
            return data
        except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON. Response text:", response.text)
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# --- STREAMLIT UI ---

st.header("Search for a Property Address")

address = st.text_input("Enter Address (e.g., '123 Main St, Baltimore, MD')")
state = st.selectbox("Select State", ["Maryland", "Virginia", "West Virginia"])

if st.button("🔎 Search"):
    if state == "Maryland":
        location = search_property_maryland(address)
        if location:
            st.success(f"✅ Found Property Coordinates: {location}")
            st.info("ℹ️ Property tax data retrieval coming soon...")
        else:
            st.error("❌ Property not found in Maryland database.")

    elif state == "Virginia":
        st.warning("⚠️ Virginia tax data connection not set up yet.")

    elif state == "West Virginia":
        st.warning("⚠️ West Virginia tax data connection not set up yet.")
