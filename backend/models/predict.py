import joblib

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

tox_model = joblib.load(os.path.join(BASE_DIR, "trained_models/toxicity_model.pkl"))
tox_vectorizer = joblib.load(os.path.join(BASE_DIR, "trained_models/toxicity_vectorizer.pkl"))

mental_model = joblib.load(os.path.join(BASE_DIR, "trained_models/mental_model.pkl"))
mental_vectorizer = joblib.load(os.path.join(BASE_DIR, "trained_models/mental_vectorizer.pkl"))

def predict(text):

    tox_vec = tox_vectorizer.transform([text])
    mental_vec = mental_vectorizer.transform([text])

    toxicity = tox_model.predict(tox_vec)[0]
    mental = str(mental_model.predict(mental_vec)[0])

    tox_prob = tox_model.predict_proba(tox_vec).max()
    mental_prob = mental_model.predict_proba(mental_vec).max()

    risk = "LOW"

    if mental == "Suicidal" and mental_prob > 0.6:
        risk = "CRITICAL"

    elif mental in ["Depression", "Anxiety"] and mental_prob > 0.6:
        risk = "HIGH"

    elif toxicity == 1 and tox_prob > 0.7:
        risk = "TOXIC"

    else:
        risk = "MODERATE"

    return {
        "text": text,
        "toxicity": int(toxicity),
        "toxicity_confidence": float(tox_prob),
        "mental_state": mental,
        "mental_confidence": float(mental_prob),
        "risk_level": risk
    }



if __name__ == "__main__":
    tests = [
        "I want to suicide and kill myself",
        "I want to end my life",
        "You are useless and stupid",
        "I had a great day today",
        "goooooodd gurlll",
        "i'll kill everyone "
    ]

    for t in tests:
        print("\nInput:", t)
        print("Output:", predict(t))