import tensorflow as tf
import pandas as pd
import numpy as np
import joblib  # For saving scaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
dataset = pd.read_csv("furniture_dataset.csv")

# Split into features (X) and labels (y)
X = dataset[["room_width", "room_height", "furniture_width", "furniture_height", "spacing"]].values
y = dataset[["x", "y"]].values  # Convert to NumPy array

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(2)  # Output: x, y coordinates
])

# Compile model
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Train model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Save the model in both H5 and Keras format
model.save("furniture_placement_model.h5")
model.save("furniture_placement_model.keras", save_format="keras")

# Save the scaler
joblib.dump(scaler, "scaler.pkl")

print("Model and scaler saved successfully!")
