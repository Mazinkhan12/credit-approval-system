"""
Credit Approval Predictor - Backend
------------------------------------
Loads the model, scaler, and encoders trained in Colab, and exposes:
  - GET  /            -> serves the frontend (index.html)
  - POST /predict     -> accepts applicant data, returns a prediction

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# ---- Load the trained model, scaler, and encoders ONCE when the server starts ----
try:
    model = joblib.load(os.path.join(MODELS_DIR, "credit_model.joblib"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "credit_scaler.joblib"))
    encoders = joblib.load(os.path.join(MODELS_DIR, "credit_encoders.joblib"))
except FileNotFoundError as e:
    raise SystemExit(
        "\nCould not find your model files inside backend/models/.\n"
        "Make sure credit_model.joblib, credit_scaler.joblib, and "
        "credit_encoders.joblib (downloaded from Colab) are placed there.\n"
        f"Details: {e}\n"
    )

# The 15 input columns, in the exact order the model was trained on (0-14).
# Column 15 was the target (+/-) and is not an input.
FEATURE_COLUMNS = list(range(15))
CATEGORICAL_COLUMNS = [0, 3, 4, 5, 6, 8, 9, 11, 12, 13]
TARGET_COLUMN = 15


@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data received."}), 400

    warnings = []
    row = [None] * len(FEATURE_COLUMNS)  # will hold 15 plain numbers, in order

    for col in FEATURE_COLUMNS:
        key = str(col)
        if key not in data or data[key] in (None, ""):
            return jsonify({"error": f"Missing value for field A{col + 1}."}), 400

        raw_value = data[key]

        if col in CATEGORICAL_COLUMNS:
            # Turn the text category into the number the model expects,
            # using the SAME encoder fitted in Colab.
            encoder = encoders[col]
            value = str(raw_value).strip()
            if value not in encoder.classes_:
                # This exact category was never seen during training.
                # Rather than crash, fall back to the most common category
                # and tell the user, so the demo stays usable and honest.
                fallback = encoder.classes_[0]
                warnings.append(
                    f"'{value}' for field A{col + 1} wasn't seen during training; "
                    f"used '{fallback}' instead."
                )
                value = fallback
            row[col] = float(encoder.transform([value])[0])
        else:
            try:
                row[col] = float(raw_value)
            except (TypeError, ValueError):
                return jsonify({"error": f"Field A{col + 1} must be a number."}), 400

    # Same scaling used during training
    X_scaled = scaler.transform(np.array([row]))

    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0]

    target_encoder = encoders[TARGET_COLUMN]
    label = target_encoder.inverse_transform([prediction])[0]  # '+' or '-'
    result = "Approved" if label == "+" else "Rejected"

    approve_index = list(target_encoder.classes_).index("+")
    approve_probability = round(float(probability[approve_index]) * 100, 1)

    return jsonify({
        "prediction": result,
        "approve_probability": approve_probability,
        "warnings": warnings,
    })


if __name__ == "__main__":
    print("\nCredit Approval Predictor backend starting...")
    print("Open http://127.0.0.1:5000 in your browser.\n")
    app.run(debug=True, port=5000)
