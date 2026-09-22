# MailGuard

## AI-Based Spam & Email Analyzer

MailGuard is a Python-based email analysis project that uses Natural Language Processing (NLP) and Machine Learning to classify emails as spam or legitimate.

## Current Features

- Raw email dataset processing
- Email text extraction
- NLP-based text processing using TF-IDF
- Machine Learning classification using Logistic Regression
- Spam / legitimate email classification
- Prediction confidence
- Flask-based web interface
- Model evaluation using accuracy, precision, recall, and F1-score

## Machine Learning

The current model was trained using:

- TF-IDF Vectorization
- Logistic Regression
- Train/Test Split

### Dataset

The current dataset contains:

- 1,399 legitimate emails
- 746 spam emails
- 2,145 total emails

### Model Performance

Test-set accuracy:

**97.90%**

Classification performance is evaluated using precision, recall, F1-score, and accuracy.

## Project Structure

```text
MAILGUARD/
│
├── app.py
├── predict.py
├── prepare_dataset.py
├── train_model.py
├── test_model.py
├── README.md
│
├── data/
│   └── spam.csv
│
├── models/
│   └── spam_classifier.pkl
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css