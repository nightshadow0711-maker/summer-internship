# 🛡️ TRUTHGUARD AI

AI-Powered News Intelligence & Verification Platform built with Python and Streamlit.

## Features

- Enterprise/cyber-intelligence inspired UI
- Analyse News landing page
- Article text, URL and TXT/PDF upload
- Real-time text statistics
- TF-IDF + Logistic Regression fake-news prediction
- Online news verification via NewsAPI or GNews
- Google Fact Check API integration
- Source credibility scoring
- Unified evidence-based final assessment
- Verification Engine page
- Interactive Dashboard
- Analytics and model metrics
- Searchable analysis History
- Source Intelligence
- PDF reports
- CSV exports
- Gmail/SMTP report delivery
- SQLite persistence
- Configurable `.env`
- Graceful behavior when external APIs are not configured

## Quick Start

### 1. Create environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
--uprgrade pip
pip install -r requirements.txt
```

### 3. Prepare dataset

Place your files here:

```text
data/raw/Fake.csv
data/raw/True.csv
```

The files should contain a `text`, `title`, `news_text`, or `article` column.

Run:

```bash
python ml/prepare_dataset.py
```

### 4. Train model

```bash
python ml/train_model.py
```

This creates:

```text
models/fake_news_model.pkl
models/tfidf_vectorizer.pkl
models/model_metadata.json
```

### 5. Configure APIs

Copy:

```text
.env.example
```

to:

```text
.env
```

Add API keys as required.

Recommended:

- NewsAPI or GNews for current news search
- Google Fact Check Tools API for fact-check matches
- Gmail SMTP with an App Password for email reports

### 6. Run

```bash
streamlit run app.py
```

## Important

The system separates:

1. ML prediction
2. Online evidence
3. Fact-check results
4. Source credibility
5. Final assessment

A model prediction is not treated as proof. If external verification is unavailable, the UI states that external verification is limited.

## Project Structure

```text
truthguard_ai/
├── app.py
├── config/
├── database/
├── ml/
├── verification/
├── reports/
├── utils/
├── data/
├── models/
└── pages/
```

## Notes

This project is designed as an educational AI/ML project and decision-support tool. Results depend on model quality, article text, external API availability, and source coverage.
