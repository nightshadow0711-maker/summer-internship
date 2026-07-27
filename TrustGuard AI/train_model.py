import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from ml.model_utils import save_artifacts

from config.settings import BASE_DIR


DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dataset.csv"
)


def train_model():

    print("=" * 70)

    print(
        "TRUTHGUARD AI"
    )

    print(
        "MODEL TRAINING"
    )

    print("=" * 70)


    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    if not DATA_FILE.exists():

        raise FileNotFoundError(

            "Dataset not found.\n"

            "Run:\n"

            "python -m ml.prepare_dataset"

        )


    df = pd.read_csv(

        DATA_FILE

    )


    # ---------------------------------------------------------
    # Validate
    # ---------------------------------------------------------

    required = [

        "news_text",

        "label"

    ]


    for col in required:

        if col not in df.columns:

            raise ValueError(

                f"Missing column: {col}"

            )


    df = df.dropna(

        subset=[

            "news_text",

            "label"

        ]

    )


    df["news_text"] = (

        df["news_text"]

        .astype(str)

        .str.strip()

    )


    df["label"] = (

        df["label"]

        .astype(int)

    )


    print(

        f"\nTotal records: {len(df)}"

    )


    print(

        "\nLabel distribution:"

    )


    print(

        df["label"]

        .value_counts()

    )


    # ---------------------------------------------------------
    # Split data
    # ---------------------------------------------------------

    X_train, X_test, y_train, y_test = (

        train_test_split(

            df["news_text"],

            df["label"],

            test_size=0.20,

            random_state=42,

            stratify=df["label"]

        )

    )


    # ---------------------------------------------------------
    # TF-IDF
    # ---------------------------------------------------------

    vectorizer = TfidfVectorizer(

        sublinear_tf=True,

        strip_accents="unicode",

        max_features=150000,

        ngram_range=(1, 2),

        min_df=2,

        max_df=0.95,

        stop_words="english"

    )


    X_train_tfidf = (

        vectorizer.fit_transform(

            X_train

        )

    )


    X_test_tfidf = (

        vectorizer.transform(

            X_test

        )

    )


    print(

        f"\nTF-IDF features: "
        f"{X_train_tfidf.shape[1]}"

    )


    # ---------------------------------------------------------
    # Model
    # ---------------------------------------------------------

    model = LogisticRegression(

        max_iter=2000,

        C=2.0,

        class_weight="balanced",

        solver="liblinear"

    )


    print(

        "\nTraining model..."

    )


    model.fit(

        X_train_tfidf,

        y_train

    )


    # ---------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------

    predictions = (

        model.predict(

            X_test_tfidf

        )

    )


    # ---------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------

    accuracy = (

        accuracy_score(

            y_test,

            predictions

        )

    )


    precision = (

        precision_score(

            y_test,

            predictions,

            zero_division=0

        )

    )


    recall = (

        recall_score(

            y_test,

            predictions,

            zero_division=0

        )

    )


    f1 = (

        f1_score(

            y_test,

            predictions,

            zero_division=0

        )

    )


    print(

        "\n"
        + "=" * 70

    )


    print(

        "MODEL PERFORMANCE"

    )


    print(

        "=" * 70

    )


    print(

        f"Accuracy:  "
        f"{accuracy * 100:.2f}%"

    )


    print(

        f"Precision: "
        f"{precision * 100:.2f}%"

    )


    print(

        f"Recall:    "
        f"{recall * 100:.2f}%"

    )


    print(

        f"F1 Score:  "
        f"{f1 * 100:.2f}%"

    )


    print(

        "\nClassification Report:"

    )


    print(

        classification_report(

            y_test,

            predictions

        )

    )


    # ---------------------------------------------------------
    # Save artifacts
    # ---------------------------------------------------------

    metadata = {

        "model_name":
            "TF-IDF + Logistic Regression",

        "accuracy":
            float(accuracy),

        "precision":
            float(precision),

        "recall":
            float(recall),

        "f1":
            float(f1),

        "label_mapping": {

            "0": "FAKE",

            "1": "REAL"

        },

        "training_rows":
            len(df)

    }


    save_artifacts(

        model,

        vectorizer,

        metadata

    )


    print(

        "\nModel saved successfully."

    )


if __name__ == "__main__":

    train_model()