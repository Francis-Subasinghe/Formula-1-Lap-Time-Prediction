import streamlit as st
import requests

# Title of the Web App
st.title("🏎️ F1 Lap Time Prediction")

# Sidebar Inputs
st.sidebar.header("Enter Lap Data")
lap_number = st.sidebar.number_input("Lap Number", min_value=1, step=1, value=5)
tyre_life = st.sidebar.number_input("Tyre Life (laps used)", min_value=0, step=1, value=10)
sector1_time = st.sidebar.number_input("Sector 1 Time (s)", min_value=0.0, step=0.1, value=31.4)
sector2_time = st.sidebar.number_input("Sector 2 Time (s)", min_value=0.0, step=0.1, value=42.1)
sector3_time = st.sidebar.number_input("Sector 3 Time (s)", min_value=0.0, step=0.1, value=25.8)
compound = st.sidebar.selectbox("Tyre Compound", ["Soft", "Medium", "Hard"])

# FastAPI Endpoint
API_URL = "https://formula-1-lap-time-prediction.onrender.com"


# Predict Button
if st.sidebar.button("Predict Lap Time"):
    # Prepare data for API
    data = {
        "LapNumber": lap_number,
        "TyreLife": tyre_life,
        "Sector1Time": sector1_time,
        "Sector2Time": sector2_time,
        "Sector3Time": sector3_time,
        "Compound": compound
    }

    # Send request to FastAPI
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        prediction = response.json()["Predicted Lap Time (s)"]
        st.success(f"🏁 Predicted Lap Time: {prediction:.3f} seconds")
    else:
        st.write("Raw Response:", response.text)  # Show full response for debugging


# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & FastAPI")
