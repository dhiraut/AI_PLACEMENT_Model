'''from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import joblib
import os

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Initialize Flask app
app = Flask(__name__)

# Load trained model and scaler
try:
    model = tf.keras.models.load_model("furniture_placement_model.keras", safe_mode=False)
    scaler = joblib.load("scaler.pkl")  # Load StandardScaler object
    print("✅ Model and scaler loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or scaler: {e}")
    model, scaler = None, None

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the AI Furniture Placement API"}), 200

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if model is None or scaler is None:
        return jsonify({"error": "Model or scaler not loaded properly"}), 500

    try:
        data = request.get_json()
        required_fields = ["room_width", "room_height", "furniture_width", "furniture_height", "spacing"]

        # Validate input data
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields", "expected_fields": required_fields}), 400

        # Convert inputs to float
        try:
            input_data = np.array([[float(data[field]) for field in required_fields]])
        except ValueError:
            return jsonify({"error": "Invalid data format. All fields must be numeric."}), 400

        # Normalize input using the scaler
        input_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_data)
        x, y = map(float, prediction[0])  # Ensure proper JSON serialization

        return jsonify({"x": x, "y": y}), 200

    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)'''
from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import os

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Load trained model safely
try:
    model = tf.keras.models.load_model("furniture_placement_model.keras", safe_mode=False)
    mean = np.load("scaler.npy")
    std = np.load("scaler_std.npy")
    print("✅ Model and scaler loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or scaler: {e}")
    model, mean, std = None, None, None

# Home route (renders frontend)
@app.route("/")
def home():
    return render_template("index.html")

# Prediction route (API)
@app.route("/predict", methods=["POST"])
def predict():
    if model is None or mean is None or std is None:
        return jsonify({"error": "Model or scaler not loaded properly"}), 500

    try:
        data = request.get_json()
        required_fields = ["room_width", "room_height", "furniture_width", "furniture_height", "spacing"]

        # Validate input data
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert inputs to float
        try:
            room_width = float(data["room_width"])
            room_height = float(data["room_height"])
            furniture_width = float(data["furniture_width"])
            furniture_height = float(data["furniture_height"])
            spacing = float(data["spacing"])
        except ValueError:
            return jsonify({"error": "Invalid data format"}), 400

        # Prepare and normalize input
        input_data = np.array([[room_width, room_height, furniture_width, furniture_height, spacing]])
        input_data = (input_data - mean) / std

        # Make prediction
        prediction = model.predict(input_data)
        x, y = prediction[0]

        return jsonify({"x": float(x), "y": float(y)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

