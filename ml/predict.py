import os
import joblib
import pandas as pd


# ==============================
# LOAD TRAINED MODEL
# ==============================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "interview_model.pkl"
)


model = joblib.load(MODEL_PATH)


# ==============================
# PREDICT INTERVIEW SCORE
# ==============================

def predict_interview_score(
    answer_quality,
    eye_contact,
    posture,
    speech_score
):

    data = pd.DataFrame(
        [[
            answer_quality,
            eye_contact,
            posture,
            speech_score
        ]],
        columns=[
            "answer_quality",
            "eye_contact",
            "posture",
            "speech_score"
        ]
    )

    prediction = model.predict(data)[0]

    # Keep score between 0 and 100
    prediction = max(
        0,
        min(100, prediction)
    )

    return round(
        float(prediction),
        1
    )