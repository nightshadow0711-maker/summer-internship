import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from config.settings import BASE_DIR


RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "dataset.csv"


def load_news_file(file_path, label):

    if not file_path.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{file_path}"
        )

    print(f"\nLoading: {file_path}")

    df = pd.read_csv(file_path)

    # Normalize column names
    df.columns = [
        str(col).strip().lower()
        for col in df.columns
    ]

    print("Columns found:", list(df.columns))

    # ---------------------------------------------------------
    # Build text
    # ---------------------------------------------------------

    if "text" in df.columns:

        text = df["text"].fillna("").astype(str)

    elif "news_text" in df.columns:

        text = df["news_text"].fillna("").astype(str)

    elif "article" in df.columns:

        text = df["article"].fillna("").astype(str)

    else:

        raise ValueError(
            f"No article text column found in {file_path.name}"
        )

    # ---------------------------------------------------------
    # Add title if available
    # ---------------------------------------------------------

    if "title" in df.columns:

        title = (
            df["title"]
            .fillna("")
            .astype(str)
        )

        text = title + " " + text

    result = pd.DataFrame({

        "news_text": text,

        "label": label

    })

    return result


def prepare_dataset():

    print("\n" + "=" * 70)

    print(
        "TRUTHGUARD AI"
    )

    print(
        "DATASET PREPARATION"
    )

    print("=" * 70)


    fake_path = (
        RAW_DIR /
        "Fake.csv"
    )

    true_path = (
        RAW_DIR /
        "True.csv"
    )


    # ---------------------------------------------------------
    # Load datasets
    # ---------------------------------------------------------

    fake_df = load_news_file(

        fake_path,

        label=0

    )


    true_df = load_news_file(

        true_path,

        label=1

    )


    print(
        f"\nFake articles: {len(fake_df)}"
    )

    print(
        f"Real articles: {len(true_df)}"
    )


    # ---------------------------------------------------------
    # Remove empty records
    # ---------------------------------------------------------

    fake_df = fake_df[
        fake_df["news_text"].str.len() > 50
    ]

    true_df = true_df[
        true_df["news_text"].str.len() > 50
    ]


    # ---------------------------------------------------------
    # Balance dataset
    # ---------------------------------------------------------

    min_count = min(

        len(fake_df),

        len(true_df)

    )


    if min_count == 0:

        raise ValueError(
            "One of the datasets is empty."
        )


    fake_df = fake_df.sample(

        n=min_count,

        random_state=42

    )


    true_df = true_df.sample(

        n=min_count,

        random_state=42

    )


    # ---------------------------------------------------------
    # Combine
    # ---------------------------------------------------------

    dataset = pd.concat(

        [

            fake_df,

            true_df

        ],

        ignore_index=True

    )


    # ---------------------------------------------------------
    # Remove duplicates
    # ---------------------------------------------------------

    dataset = dataset.drop_duplicates(

        subset=[
            "news_text"
        ]

    )


    # ---------------------------------------------------------
    # Shuffle
    # ---------------------------------------------------------

    dataset = dataset.sample(

        frac=1,

        random_state=42

    ).reset_index(

        drop=True

    )


    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    PROCESSED_DIR.mkdir(

        parents=True,

        exist_ok=True

    )


    dataset.to_csv(

        OUTPUT_FILE,

        index=False

    )


    print("\n" + "=" * 70)

    print(
        "DATASET READY"
    )

    print("=" * 70)


    print(
        f"\nTotal articles: "
        f"{len(dataset)}"
    )


    print(
        f"Fake: "
        f"{len(dataset[dataset.label == 0])}"
    )


    print(
        f"Real: "
        f"{len(dataset[dataset.label == 1])}"
    )


    print(
        f"\nSaved to:"
    )

    print(
        OUTPUT_FILE
    )


if __name__ == "__main__":

    prepare_dataset()