import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Web App
st.title("🏎️ F1 Lap Time Prediction")

# Sidebar - App Information
st.sidebar.title("ℹ️ About This App")
st.sidebar.markdown("""
Welcome to the **F1 Lap Time Predictor**!  
This tool uses **AI-powered machine learning models** to estimate **lap times** based on **sector times**, **tyre wear**, and **race strategies**.
""")

st.sidebar.subheader("📌 How It Works")
st.sidebar.markdown("""
1️⃣ Enter your **sector times**, **tyre life**, and **compound**.  
2️⃣ Click **Predict** to estimate lap time.  
3️⃣ Analyze graphs to **improve your racing strategy**!  
""")

st.sidebar.subheader("📊 Why Use This?")
st.sidebar.markdown("""
✔️ **Optimize Race Strategy**  
✔️ **Analyze Tyre Performance**  
✔️ **Predict Faster Lap Times**  
✔️ **Understand Race Dynamics**  
""")

# Sidebar Inputs
st.sidebar.header("🔹 Enter Lap Data")
lap_number = st.sidebar.number_input("Lap Number", min_value=1, step=1, value=5)
tyre_life = st.sidebar.number_input("Tyre Life (laps used)", min_value=0, step=1, value=10)
sector1_time = st.sidebar.number_input("Sector 1 Time (s)", min_value=0.0, step=0.1, value=31.4)
sector2_time = st.sidebar.number_input("Sector 2 Time (s)", min_value=0.0, step=0.1, value=42.1)
sector3_time = st.sidebar.number_input("Sector 3 Time (s)", min_value=0.0, step=0.1, value=25.8)
compound = st.sidebar.selectbox("Tyre Compound", ["Soft", "Medium", "Hard"])

# FastAPI Endpoint
API_URL = "https://formula-1-lap-time-prediction-1.onrender.com/predict"

# Predict Button
if st.sidebar.button("🚀 Predict Lap Time"):
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
        st.success(f"🏁 **Predicted Lap Time: {prediction:.3f} seconds**")

        # Simulate Lap Time Trends for Visualization
        st.markdown("### 📊 Lap Time Trends Over Laps")
        lap_numbers = np.arange(1, 51)
        simulated_times = np.random.uniform(85, 100, size=50) - lap_numbers * 0.2  # Decreasing trend

        plt.figure(figsize=(10, 5))
        plt.plot(lap_numbers, simulated_times, marker='o', linestyle='-', color='red', label="Lap Time Trend")
        plt.scatter([lap_number], [prediction], color="blue", s=100, label="Your Predicted Lap")
        plt.xlabel("Lap Number")
        plt.ylabel("Lap Time (seconds)")
        plt.title("Lap Time Performance Over Laps")
        plt.legend()
        st.pyplot(plt)

        # Simulate Tyre Compound vs Lap Time
        st.markdown("### 📉 Tyre Compound vs Lap Time Analysis")
        compounds = ["Soft", "Medium", "Hard"]
        avg_lap_times = [prediction + np.random.uniform(-1, 1) for _ in range(3)]

        plt.figure(figsize=(6, 4))
        sns.barplot(x=compounds, y=avg_lap_times, palette="coolwarm")
        plt.xlabel("Tyre Compound")
        plt.ylabel("Average Lap Time (s)")
        plt.title("Tyre Compound vs Lap Time")
        st.pyplot(plt)

    else:
        st.error("❌ Error: Unable to get prediction. Please try again.")
        st.write("Raw Response:", response.text)  # Show full response for debugging

# Fun Facts & Insights
st.markdown("---")
st.markdown("### 📌 F1 Insights & Stats")
st.info("""
- **Did you know?** Tyre degradation can add up to **1.5 seconds per lap** after a few laps!  
- **F1 Data Science Fact:** AI can predict **optimal pit stop strategies** based on lap trends.  
- **Soft vs Hard Tyres:** Soft tyres provide **better grip but degrade faster**, while **hard tyres last longer but are slower**.  
""")

# Footer
st.markdown("---")
st.markdown("#### 🚀 Developed for F1 fans, data scientists, and racing enthusiasts!")
st.markdown("Built with ❤️ using **Streamlit & FastAPI**")
