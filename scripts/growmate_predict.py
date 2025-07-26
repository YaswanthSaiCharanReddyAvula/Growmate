import pandas as pd
import joblib
import lightgbm as lgb
from datetime import datetime


# ------------------------ Load Model and Encoders ------------------------ #
model = joblib.load("D:/Internship/Venkat/growmate/models/lgbm_model.pkl")
print("✅ Model loaded successfully!")

# Load all encoders (used to encode categorical string features to numeric labels)
plant_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/plant_encoder.pkl"
)


plant_type_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/plant_type_encoder.pkl"
)


soil_type_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/soil_type_encoder.pkl"
)


season_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/season_encoder.pkl"
)


sunlight_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/sunlight_encoder.pkl"
)


pot_ground_encoder = joblib.load(
    "D:/Internship/Venkat/growmate/models/pot_ground_encoder.pkl"
)

# ------------------------ Plant-type Mapping Logic ------------------------ #
# 📌 This is used to auto-determine plant_type based on plant_name
plant_type_map = {
    "rose": "flowering",
    "basil": "herb",
    "mint": "herb",
    "cactus": "succulent",
    "aloe_vera": "succulent",
    "spider_plant": "foliage",
    "money_plant": "foliage",
    "peace_lily": "flowering",
    "tomato": "fruiting",
    "snake_plant": "succulent",
}


# ------------------------ Safe Encoding Helper ------------------------ #
# 📌 This handles unseen values safely by mapping them to 'unknown' if necessary
def safe_transform(encoder, value, label_name):
    try:
        return encoder.transform(value)
    except ValueError:
        print(
            f"⚠️ Unseen label '{value[0]}' in '{label_name}'. Replacing with 'unknown'"
        )
        return encoder.transform(["unknown"]) if "unknown" in encoder.classes_ else [0]


# ------------------------ Generate Input ------------------------ #

# 📌 Replace these with real-time input or frontend form input later

plant_name = "rose"  # 📌 Allowed: ['rose', 'basil', 'mint', 'cactus', 'aloe_vera', 'spider_plant', 'money_plant', 'peace_lily', 'tomato', 'snake_plant']


plant_type = plant_type_map.get(
    plant_name, "unknown"
)  # 📌 Allowed: ['herb', 'flowering', 'succulent', 'fruiting', 'foliage']

# 📌 Auto-calculated from timestamp (use real database value for last_watered_date)
today = datetime.today()

last_watered_date = datetime(2025, 1, 7)  # <-- 📌 Replace with last watered timestamp
days_since_watered = (today - last_watered_date).days

sample_input = {
    "plant_name": [plant_name],  # 📌 Trained list above
    "plant_type": [
        plant_type
    ],  # 📌 ['herb', 'flowering', 'succulent', 'fruiting', 'foliage']
    "soil_type": [
        "sandy"
    ],  # 📌 ['sandy', 'loamy', 'clayey'] → you can expand this and retrain
    "soil_ph": [6.5],  # 📌 Accepts float value; normal range = 5.5 to 7.5
    "soil_nitrogen": [20],  # 📌 Accepts numeric (ppm) → adjust based on IOT soil sensor
    "soil_phosphorus": [15],  # 📌 Accepts numeric (ppm)
    "soil_potassium": [25],  # 📌 Accepts numeric (ppm)
    "plant_age_weeks": [10],  # 📌 Integer number of weeks since planting
    "last_watered_days": [
        days_since_watered
    ],  # 📌 Computed above from last watering timestamp
    "temperature": [25],  # 📌 Degrees Celsius (auto from weather API or sensor)
    "humidity": [0],  # 📌 Percentage (auto from weather API or sensor)
    "rainfall": [
        0
    ],  # 📌 Millimeters of rainfall (daily) — can be fetched or set manually
    "season": ["summer"],  # 📌 ['summer', 'winter', 'rainy']
    "sunlight_exposure": [
        "full_sun"
    ],  # 📌 ['low_light', 'indirect_light', 'partial_sun', 'full_sun']
    "pot_or_ground": ["pot"],  # 📌 ['pot', 'ground'] — user-defined when plant is added
}

sample_df = pd.DataFrame(sample_input)

# ------------------------ Encode Categoricals ------------------------ #
sample_df["plant_name"] = safe_transform(
    plant_encoder, sample_df["plant_name"], "plant_name"
)
sample_df["plant_type"] = safe_transform(
    plant_type_encoder, sample_df["plant_type"], "plant_type"
)
sample_df["soil_type"] = safe_transform(
    soil_type_encoder, sample_df["soil_type"], "soil_type"
)
sample_df["season"] = safe_transform(season_encoder, sample_df["season"], "season")
sample_df["sunlight_exposure"] = safe_transform(
    sunlight_encoder, sample_df["sunlight_exposure"], "sunlight_exposure"
)
sample_df["pot_or_ground"] = safe_transform(
    pot_ground_encoder, sample_df["pot_or_ground"], "pot_or_ground"
)

# ------------------------ Predict ------------------------ #
prediction = model.predict(sample_df)[0]  # 📌 Output: 0, 1, or 2
label_map = {
    0: "Needs Watering",
    1: "Moderate",
    2: "Well Watered",
}  # 📌 Human-readable mapping

print(
    f"\n🪴 Predicted Watering Status: {prediction} → {label_map.get(prediction, 'Unknown')}"
)