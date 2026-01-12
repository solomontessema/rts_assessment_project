import os
import joblib
import json
import pandas as pd
import numpy as np

# Load model and preprocessor
def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "bank_classifier.joblib"))
    preprocessor = joblib.load(os.path.join(model_dir, "bank_preprocessor.joblib"))
    return {"model": model, "preprocessor": preprocessor}

# Receive data from Streamlit
def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        request_dict = json.loads(request_body)
        return pd.DataFrame([request_dict])
    elif request_content_type == 'text/csv':
        from io import StringIO
        return pd.read_csv(StringIO(request_body))
    raise ValueError(f"Unsupported content type: {request_content_type}")

# The "Brain": Pre-process -> Predict -> Probability
def predict_fn(input_data, model_dict):
    model = model_dict["model"]
    preprocessor = model_dict["preprocessor"]
    
    # 1. Transform raw input (e.g. 'married') using the trained preprocessor
    processed_data = preprocessor.transform(input_data)
    
    # 2. Get the binary prediction (0 or 1)
    prediction = model.predict(processed_data)
    
    # 3. Get the probability (Required by your PDF!)
    # probability of index 1 (the 'yes' subscription)
    probability = model.predict_proba(processed_data)[0][1]
    
    return {
        "prediction": int(prediction[0]),
        "probability_score": float(probability)
    }

def output_fn(prediction_dict, content_type):
    return json.dumps(prediction_dict)