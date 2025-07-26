import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define configuration
num_samples_per_class = 200  # 200 for each watering_status (0, 1, 2)
watering_classes = [0, 1, 2]
plant_names = [
    "aloe_vera", "basil", "cactus", "mint", "money_plant",
    "peace_lily", "rose", "snake_plant", "spider_plant", "tomato"
]
soil_types = ["clayey", "loamy", "sandy"]
sunlight_exposures = ["full_sun", "partial_sun", "low_light", "indirect_light"]
seasons = ["summer", "winter", "monsoon", "spring"]
pot_or_ground_options = ["pot", "ground"]
plant_types = ["flowering", "foliage"]

# Helper function to generate realistic values
def generate_row(watering_status):
    plant_name = random.choice(plant_names)
    return {
        "plant_name": plant_name,
        "plant_type": random.choice(plant_types),
        "soil_type": random.choice(soil_types),
        "soil_ph": round(np.random.uniform(5.5, 7.5), 2),
        "soil_nitrogen": round(np.random.uniform(50, 300), 1),
        "soil_phosphorus": round(np.random.uniform(20, 100), 1),
        "soil_potassium": round(np.random.uniform(100, 400), 1),
        "plant_age_weeks": np.random.randint(2, 104),
        "last_watered_days": np.random.randint(0, 15),
        "temperature": round(np.random.uniform(15, 40), 1),
        "humidity": round(np.random.uniform(20, 90), 1),
        "rainfall": round(np.random.uniform(0, 200), 1),
        "season": random.choice(seasons),
        "sunlight_exposure": random.choice(sunlight_exposures),
        "pot_or_ground": random.choice(pot_or_ground_options),
        "watering_status": watering_status
    }

# Generate the full dataset
data = []
for status in watering_classes:
    for _ in range(num_samples_per_class):
        data.append(generate_row(status))

# Create DataFrame and shuffle
df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.head()

# Save your DataFrame as a CSV file
df.to_csv("growmate_super_dataset.csv", index=False)