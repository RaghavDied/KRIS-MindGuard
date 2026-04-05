import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

with open("backend./data/toxicity_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels = [item["toxicity"] for item in data]


X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


joblib.dump(model, "backend/trained_models/toxicity_model.pkl")
joblib.dump(vectorizer, "backend/trained_models/toxicity_vectorizer.pkl")

print("\nToxicity model trained & saved!")