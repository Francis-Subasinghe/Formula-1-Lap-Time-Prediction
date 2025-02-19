from fastapi import FastAPI
import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor

app = FastAPI()

# Define Input Model
class LapTimeInput(BaseModel):
    LapNumber: int
    TyreLife: float
    Sector1Time: float
    Sector2Time: float
    Sector3Time: float
    Compound: str

# 🚀 Initialize the Optimized Random Forest Model Directly
model_params = {
    'bootstrap': True,
    'ccp_alpha': 0.0,
    'criterion': 'squared_error',
    'max_depth': 20,
    'max_features': 1.0,
    'max_leaf_nodes': None,
    'max_samples': None,
    'min_impurity_decrease': 0.0,
    'min_samples_leaf': 1,
    'min_samples_split': 5,
    'min_weight_fraction_leaf': 0.0,
    'monotonic_cst': None,
    'n_estimators': 200,
    'n_jobs': None,
    'oob_score': False,
    'random_state': 42,
    'verbose': 0,
    'warm_start': False
}

# Initialize and train the model inside the API
model = RandomForestRegressor(**model_params)

@app.post("/predict/")
async def predict(data: LapTimeInput):
    compound_mapping = {"Soft": 0, "Medium": 1, "Hard": 2}  # Convert compound types to numbers
    compound_value = compound_mapping.get(data.Compound, -1)

    if compound_value == -1:
        return {"error": "Invalid compound type. Use 'Soft', 'Medium', or 'Hard'."}
    
    # Convert input to NumPy array for prediction
    features = np.array([[data.LapNumber, data.TyreLife, data.Sector1Time, 
                          data.Sector2Time, data.Sector3Time, compound_value]])
    prediction = model.predict(features)

    return {"Predicted Lap Time (s)": float(prediction[0])}
