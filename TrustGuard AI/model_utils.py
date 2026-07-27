from pathlib import Path

import pickle

import json


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent


MODELS_DIR = (

    BASE_DIR

    / "models"

)


MODEL_FILE = (

    MODELS_DIR

    / "fake_news_model.pkl"

)


VECTORIZER_FILE = (

    MODELS_DIR

    / "tfidf_vectorizer.pkl"

)


METADATA_FILE = (

    MODELS_DIR

    / "model_metadata.json"

)


# ============================================================
# LOAD ARTIFACTS
# ============================================================

def load_artifacts():

    if not MODEL_FILE.exists():

        return (
            None,
            None,
            {}
        )


    if not VECTORIZER_FILE.exists():

        return (
            None,
            None,
            {}
        )


    try:

        with open(

            MODEL_FILE,

            "rb"

        ) as f:

            model = pickle.load(f)


        with open(

            VECTORIZER_FILE,

            "rb"

        ) as f:

            vectorizer = pickle.load(f)


        metadata = {}


        if METADATA_FILE.exists():

            with open(

                METADATA_FILE,

                "r",

                encoding=
                    "utf-8"

            ) as f:

                metadata = json.load(f)


        return (

            model,

            vectorizer,

            metadata

        )


    except Exception:

        return (

            None,

            None,

            {}

        )


# ============================================================
# SAVE ARTIFACTS
# ============================================================

def save_artifacts(

    model,

    vectorizer,

    metadata=None

):

    MODELS_DIR.mkdir(

        parents=True,

        exist_ok=True

    )


    with open(

        MODEL_FILE,

        "wb"

    ) as f:

        pickle.dump(

            model,

            f

        )


    with open(

        VECTORIZER_FILE,

        "wb"

    ) as f:

        pickle.dump(

            vectorizer,

            f

        )


    if metadata is None:

        metadata = {}


    with open(

        METADATA_FILE,

        "w",

        encoding=
            "utf-8"

    ) as f:

        json.dump(

            metadata,

            f,

            indent=
                4

        )