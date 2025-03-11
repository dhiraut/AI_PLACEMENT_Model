import numpy as np
import pandas as pd

def generate_dataset(num_samples=1000):
    data = []
    for _ in range(num_samples):
        room_width = np.random.randint(10, 20)  
        room_height = np.random.randint(10, 20)
        furniture_width = np.random.randint(2, 5)
        furniture_height = np.random.randint(2, 5)
        spacing = np.random.randint(1, 3)

        x = np.random.randint(0, room_width - furniture_width)
        y = np.random.randint(0, room_height - furniture_height)

        data.append([room_width, room_height, furniture_width, furniture_height, spacing, x, y])

    columns = ["room_width", "room_height", "furniture_width", "furniture_height", "spacing", "x", "y"]
    return pd.DataFrame(data, columns=columns)

# Generate and save dataset
dataset = generate_dataset()
dataset.to_csv("furniture_dataset.csv", index=False)
print("Dataset generated and saved as furniture_dataset.csv")
