from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/optimized_f1_lap_time_model.pkl")

# Initialize FastAPI
app = FastAPI()

# Define request schema
class LapTimeInput(BaseModel):
    LapNumber: int
    TyreLife: float
    Sector1Time: float
    Sector2Time: float
    Sector3Time: float
    Compound: str  # Ensure Compound is a string

# Mapping tire compounds to numeric values
compound_mapping = {
    "Soft": 0,
    "Medium": 1,
    "Hard": 2
}

@app.get("/")
def home():
    return {"message": "F1 Lap Time Prediction API is running!"}

@app.post("/predict/")
def predict(data: LapTimeInput):
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame([data.dict()])

        # Encode "Compound" to numeric value
        if data.Compound not in compound_mapping:
            return {"error": f"Invalid Compound type: {data.Compound}. Must be one of {list(compound_mapping.keys())}"}
        
        df["Compound"] = df["Compound"].map(compound_mapping)

        # Predict lap time
        prediction = model.predict(df)

        return {"Predicted Lap Time (s)": float(prediction[0])}
    
    except Exception as e:
        return {"error": str(e)}
