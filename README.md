# MailGuard — AI Email Security Analyzer

MailGuard is an AI-assisted email security analysis tool that combines Natural Language Processing (NLP), machine learning, URL analysis, phishing detection, and email header analysis to identify potentially suspicious emails.

The project started as a simple spam-classification MVP and is being gradually developed into a broader email-security analysis system.

## Features

### 1. NLP + Machine Learning

MailGuard analyzes email content using:

* TF-IDF vectorization
* Logistic Regression
* Natural language processing
* Spam classification
* Prediction confidence

The current model was trained using email data from the SpamAssassin public corpus.

**Current held-out test accuracy: 97.90%**

### 2. Suspicious URL Analysis

MailGuard extracts URLs from email content and checks for characteristics commonly associated with suspicious links, including:

* URL shortening services
* IP addresses used instead of domain names
* Excessive subdomains
* Unusually long URLs
* Security-related keywords
* Suspicious URL structures

### 3. Phishing Indicator Detection

The analyzer checks email content for common phishing-related patterns such as:

* Urgent language
* Account suspension threats
* Credential requests
* Password requests
* Financial information requests
* Verification requests
* Requests for sensitive information

### 4. Email Header Analysis

MailGuard can analyze raw email headers and identify observable characteristics including:

* From address
* Reply-To address
* Return-Path
* Message-ID
* Received headers
* SPF results
* DKIM results
* DMARC results
* From / Reply-To domain mismatches
* From / Return-Path domain mismatches
* Authentication failures

### 5. Explainable Risk Scoring

MailGuard combines multiple analysis layers into a single risk score from 0–100.

The score currently considers:

* Machine-learning spam confidence
* Suspicious URLs
* Phishing indicators
* Email header findings

The system categorizes the resulting score as:

|  Score | Risk Level |
| -----: | ---------- |
|   0–29 | LOW        |
|  30–59 | MEDIUM     |
|  60–79 | HIGH       |
| 80–100 | CRITICAL   |

These thresholds and weights are application-defined heuristics and are not intended to represent a universal security standard.

### 6. Web Interface

MailGuard provides a Flask-based web interface where users can:

* Paste email content
* Optionally provide raw email headers
* Analyze the email
* View ML classification and confidence
* Review suspicious URLs
* Review phishing indicators
* Inspect email header findings
* View authentication results
* View the overall risk score and risk level

## Architecture

```text
                         EMAIL
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          ML MODEL     URL ANALYSIS   PHISHING
              │            │         DETECTION
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                    HEADER ANALYSIS
                           │
                  SPF / DKIM / DMARC
                  Domain Mismatches
                           │
                           ▼
                      RISK ENGINE
                           │
                           ▼
                   SCORE + RISK LEVEL
                           │
                           ▼
                    WEB INTERFACE
```

## Technology Stack

* Python
* Flask
* Pandas
* Scikit-learn
* Joblib
* TF-IDF
* Logistic Regression
* HTML
* CSS

## Project Structure

```text
MAILGUARD/
│
├── analysis/
│   ├── header_analyzer.py
│   ├── phishing_detector.py
│   ├── risk_engine.py
│   └── url_analyzer.py
│
├── data/
│   ├── spam.csv
│   └── SpamAssassin corpus archives
│
├── models/
│   └── spam_classifier.pkl
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── predict.py
├── prepare_dataset.py
├── train_model.py
├── test_model.py
├── test_header_analyzer.py
└── README.md
```

## Dataset

MailGuard currently uses email data from the **Apache SpamAssassin Public Corpus**.

The dataset preparation script extracts plain-text email content from the downloaded corpus archives and creates:

```text
data/spam.csv
```

Current dataset:

```text
Ham emails  : 1399
Spam emails : 746
Total       : 2145
```

The dataset is divided into training and testing data using an 80/20 split with stratification.

## Machine Learning Model

The current classification pipeline is:

```text
Email Text
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression
    ↓
SPAM / HAM Classification
    ↓
Prediction Confidence
```

The model achieved:

```text
Accuracy: 97.90%
```

on the held-out test set.

Model evaluation:

```text
              precision    recall  f1-score

ham              0.98       0.99      0.98
spam             0.99       0.95      0.97

accuracy                              0.98
```

## Risk Analysis

The ML classifier and security risk engine serve different purposes.

The ML classifier answers:

> Does the email content resemble spam based on the trained model?

The risk engine answers:

> What observable security characteristics were detected across the email?

This allows MailGuard to identify cases where an email may be classified as legitimate by the ML model while still containing suspicious security characteristics in its URLs, content, or headers.

## Example Analysis

A suspicious email containing:

```text
https://bit.ly/account-verification
```

may trigger findings such as:

```text
URL shortening service detected
Security-related keywords found
```

Combined with phishing indicators and suspicious email headers, these findings can increase the overall risk score.

## Running MailGuard

### 1. Install dependencies

```bash
python -m pip install flask pandas scikit-learn joblib
```

### 2. Prepare the dataset

```bash
python prepare_dataset.py
```

### 3. Train the model

```bash
python train_model.py
```

This creates:

```text
models/spam_classifier.pkl
```

### 4. Run the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Testing

The project includes tests for:

* Machine-learning predictions
* URL and phishing analysis
* Email header analysis
* Combined risk analysis

Run the model test with:

```bash
python test_model.py
```

Run the header analyzer test with:

```bash
python test_header_analyzer.py
```

## Development Roadmap

MailGuard is being developed incrementally.

### Current

* [x] NLP-based email classification
* [x] Spam detection
* [x] Prediction confidence
* [x] Suspicious URL analysis
* [x] Phishing indicator detection
* [x] Explainable risk scoring
* [x] Email header analysis
* [x] SPF / DKIM / DMARC result analysis
* [x] Flask web interface

### Planned

* [ ] Threat intelligence integration
* [ ] Reputation checks for URLs and domains
* [ ] More advanced phishing analysis
* [ ] Improved header and authentication analysis
* [ ] Attachment analysis
* [ ] Expanded model evaluation
* [ ] Additional security-focused detection features

## Disclaimer

MailGuard is an educational and experimental cybersecurity project.

Its classifications, heuristics, and risk scores should not be treated as definitive proof that an email is malicious or safe. Security findings should be interpreted alongside other security controls and investigation techniques.

## Author

**Devidas Vitthal Zende**

GitHub: https://github.com/devcyan

LinkedIn: https://www.linkedin.com/in/devidas-zende-00133028b/
