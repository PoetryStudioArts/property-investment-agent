# app.py

import streamlit as st
import requests

# --- PAGE TITLE ---
st.title("🏡 Property Pal - Real Estate Research Assistant")

# --- FUNCTIONS TO QUERY PROPERTY DATA ---

def search_property_maryland(address):
    city = address.get('city')
    state = address.get('state')
    zipcode = address.get('zipcode')

    response = requests.get(f"http://api.example.com/search?city={city}&state={state}&zipcode={zipcode}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

    if response.headers['Content-Type'] == 'application/json':
        try:
            data = response.json()  # Attempt to parse as JSON
            return data  # Ensure return is inside try
        except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON. Response text:", response.text)
            return None  # Return None or handle the error as needed
    else:
        print("Received non-JSON response:", response.text)
        return None  # Return None or handle the error as needed


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
