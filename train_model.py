import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("data/spam.csv")

# Remove missing values
data = data.dropna(subset=["text", "label"])

# Input and target
X = data["text"]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# NLP + Machine Learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=10000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])

# Train
print("Training MailGuard model...")
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print(f"Accuracy: {accuracy:.2%}")
print()
print("Classification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "models/spam_classifier.pkl")

print()
print("Model saved to:")
print("models/spam_classifier.pkl")