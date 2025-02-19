from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import joblib

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow frontend requests (IMPORTANT for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific frontend domains for security
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Load pre-trained lap time prediction model
try:
    model = joblib.load("models/optimized_f1_lap_time_model.pkl")
except Exception as e:
    print(f"🚨 Model Loading Error: {e}")

# Lap data validation class
class LapData(BaseModel):
    LapNumber: int = Field(..., gt=0, description="Lap number must be positive")
    TyreLife: int = Field(..., ge=0, description="Tyre life must be non-negative")
    Sector1Time: float = Field(..., gt=0, description="Sector 1 time must be positive")
    Sector2Time: float = Field(..., gt=0, description="Sector 2 time must be positive")
    Sector3Time: float = Field(..., gt=0, description="Sector 3 time must be positive")
    Compound: str

# Define categorical encoding for tyre compounds
tyre_encoding = {"Soft": 0, "Medium": 1, "Hard": 2}

@app.get("/")
async def home():
    return {"message": "F1 Lap Time Prediction API is running!"}

@app.post("/predict")
async def predict_lap_time(data: LapData):
    try:
        # Convert tyre compound to numeric value
        compound_numeric = tyre_encoding.get(data.Compound, 1)

        # Prepare features for model
        features = np.array([
            data.LapNumber,
            data.TyreLife,
            data.Sector1Time,
            data.Sector2Time,
            data.Sector3Time,
            compound_numeric
        ]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]
        return {"Predicted Lap Time (s)": round(prediction, 3)}

    except Exception as e:
        return {"error": str(e)}
