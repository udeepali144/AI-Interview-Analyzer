import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os


# ==============================
# SAMPLE INTERVIEW DATA
# ==============================

data = {
    "answer_quality": [
        40, 50, 60, 70, 80,
        85, 90, 95, 55, 75
    ],

    "eye_contact": [
        40, 50, 60, 70, 80,
        85, 90, 95, 55, 75
    ],

    "posture": [
        50, 55, 65, 70, 80,
        85, 90, 95, 60, 75
    ],

    "speech_score": [
        45, 55, 65, 72, 80,
        88, 92, 96, 60, 78
    ],

    "final_score": [
        43, 52, 62, 71, 80,
        87, 91, 96, 58, 76
    ]
}


df = pd.DataFrame(data)


# ==============================
# FEATURES & TARGET
# ==============================

X = df[
    [
        "answer_quality",
        "eye_contact",
        "posture",
        "speech_score"
    ]
]

y = df["final_score"]


# ==============================
# TRAIN MODEL
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


# ==============================
# SAVE MODEL
# ==============================

model_path = os.path.join(
    os.path.dirname(__file__),
    "interview_model.pkl"
)


joblib.dump(
    model,
    model_path
)


print("✅ ML model trained successfully!")

print(
    f"✅ Model saved at: {model_path}"
)