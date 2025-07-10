import os
from pathlib import Path
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load

# Get the model path from environment variables with a default
MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

app = FastAPI()

# Define paths relative to the script's parent directory
BASE_DIR = Path(__file__).parent.parent
model_path = BASE_DIR / MODEL_PATH

# Check if model exists
if not model_path.exists():
    # This is a critical error, so we can raise an exception
    raise RuntimeError(f"Model not found at {model_path}")

# Load the model
model = load(model_path)

# Define expected number of features
NUM_FEATURES = 8

class PredictionRequest(BaseModel):
    data: list[list[float]]

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictionRequest):
    """Prediction endpoint."""
    try:
        # Validate input shape
        for sample in request.data:
            if len(sample) != NUM_FEATURES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid input data. Expected {NUM_FEATURES} features, but got {len(sample)}."
                )

        # Convert the input data to a numpy array
        X = np.array(request.data)

        # Make predictions
        predictions = model.predict(X)

        # Return the predictions
        return {"predictions": predictions.tolist()}
    except HTTPException as e:
        # Re-raise HTTPException
        raise e
    except Exception as e:
        # For any other exception, return a 500 error
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

