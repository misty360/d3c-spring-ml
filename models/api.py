from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# Load model and encoders
model = joblib.load("xgb_model.pkl")
uni_encoder = joblib.load("uni_encoder.pkl")
country_encoder = joblib.load("country_encoder.pkl")

app = FastAPI()

class InputData(BaseModel):
    university: str
    country: str
    visa_status: int
    activism_status: int

@app.post("/predict")
def predict(data: InputData):
    try:
        print("Received input:", data.dict())

        encoded_uni = int(uni_encoder.transform(pd.DataFrame({'universities':[data.university]}))[0][0])
        encoded_country = int(country_encoder.transform(pd.DataFrame({'countries':[data.country]}))[0][0])

        df = pd.DataFrame([{
            "universities": encoded_uni,
            "countries": encoded_country,
            "visa_status": data.visa_status,
            "activism_status": data.activism_status
        }])

        prob = model.predict_proba(df)[0][1]
        return {"deportation_probability": round(float(prob), 4)}
    
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
