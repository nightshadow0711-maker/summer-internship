# ============================================================
# TRUTHGUARD AI
# ml/predictor.py
#
# ML prediction engine
# ============================================================

from pathlib import Path
import pickle
import json
import re

import numpy as np


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODELS_DIR / "fake_news_model.pkl"

VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"

METADATA_PATH = MODELS_DIR / "model_metadata.json"


# ============================================================
# GLOBAL MODEL CACHE
# ============================================================

_MODEL = None

_VECTORIZER = None

_METADATA = None


# ============================================================
# LOAD PICKLE
# ============================================================

def load_pickle(path):

    with open(

        path,

        "rb"

    ) as file:

        return pickle.load(

            file

        )


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    global _MODEL

    global _VECTORIZER

    global _METADATA


    if _MODEL is not None:

        return (

            _MODEL,

            _VECTORIZER,

            _METADATA

        )


    if not MODEL_PATH.exists():

        raise FileNotFoundError(

            f"ML model not found:\n{MODEL_PATH}"

        )


    if not VECTORIZER_PATH.exists():

        raise FileNotFoundError(

            f"TF-IDF vectorizer not found:\n"
            f"{VECTORIZER_PATH}"

        )


    _MODEL = load_pickle(

        MODEL_PATH

    )


    _VECTORIZER = load_pickle(

        VECTORIZER_PATH

    )


    if METADATA_PATH.exists():

        try:

            with open(

                METADATA_PATH,

                "r",

                encoding="utf-8"

            ) as file:

                _METADATA = json.load(

                    file

                )

        except Exception:

            _METADATA = {}


    else:

        _METADATA = {}


    return (

        _MODEL,

        _VECTORIZER,

        _METADATA

    )


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if text is None:

        return ""


    text = str(

        text

    )


    text = re.sub(

        r"\s+",

        " ",

        text

    )


    return text.strip()


# ============================================================
# DETECT LABEL MEANING
# ============================================================

def label_to_type(

    label,

    metadata=None

):

    # --------------------------------------------------------
    # Metadata mapping
    # --------------------------------------------------------

    if metadata:

        label_mapping = metadata.get(

            "label_mapping",

            {}

        )


        if str(label) in label_mapping:

            mapped = str(

                label_mapping[str(label)]

            ).upper()


            if "REAL" in mapped:

                return "REAL"


            if "FAKE" in mapped:

                return "FAKE"


    # --------------------------------------------------------
    # String labels
    # --------------------------------------------------------

    label_string = str(

        label

    ).upper().strip()


    if any(

        value in label_string

        for value in [

            "REAL",

            "TRUE",

            "GENUINE",

            "AUTHENTIC",

            "RELIABLE"

        ]

    ):

        return "REAL"


    if any(

        value in label_string

        for value in [

            "FAKE",

            "FALSE",

            "FALSEHOOD",

            "MISLEADING",

            "UNTRUE"

        ]

    ):

        return "FAKE"


    # --------------------------------------------------------
    # Numeric labels
    #
    # IMPORTANT:
    # This assumes the common training format:
    #
    # 0 = Fake
    # 1 = Real
    #
    # If your training script uses the opposite mapping,
    # model_metadata.json should define it.
    # --------------------------------------------------------

    try:

        numeric = int(

            float(

                label

            )

        )


        if numeric == 1:

            return "REAL"


        if numeric == 0:

            return "FAKE"


    except Exception:

        pass


    return "UNCERTAIN"


# ============================================================
# GET PROBABILITY
# ============================================================

def get_probability_for_class(

    model,

    probabilities,

    class_name,

    metadata=None

):

    classes = getattr(

        model,

        "classes_",

        []

    )


    for index, label in enumerate(

        classes

    ):

        detected_type = label_to_type(

            label,

            metadata

        )


        if detected_type == class_name:

            return float(

                probabilities[index]

            )


    return None


# ============================================================
# PREDICT NEWS
# ============================================================

def predict_news(

    text,

    save_to_database=False

):

    text = clean_text(

        text

    )


    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not text:

        return {

            "prediction":

                "UNCERTAIN",

            "real_probability":

                50.0,

            "fake_probability":

                50.0,

            "confidence":

                0.0,

            "model_ready":

                False,

            "message":

                "No article text provided."

        }


    try:

        model, vectorizer, metadata = load_model()


        # ----------------------------------------------------
        # Transform text
        # ----------------------------------------------------

        X = vectorizer.transform(

            [text]

        )


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        raw_prediction = model.predict(

            X

        )[0]


        prediction = label_to_type(

            raw_prediction,

            metadata

        )


        # ----------------------------------------------------
        # Probability
        # ----------------------------------------------------

        real_probability = 50.0

        fake_probability = 50.0


        if hasattr(

            model,

            "predict_proba"

        ):

            probabilities = model.predict_proba(

                X

            )[0]


            real_value = get_probability_for_class(

                model,

                probabilities,

                "REAL",

                metadata

            )


            fake_value = get_probability_for_class(

                model,

                probabilities,

                "FAKE",

                metadata

            )


            if real_value is not None:

                real_probability = (

                    real_value * 100

                )


            if fake_value is not None:

                fake_probability = (

                    fake_value * 100

                )


        else:

            # ------------------------------------------------
            # Models without probability support
            # ------------------------------------------------

            if prediction == "REAL":

                real_probability = 75.0

                fake_probability = 25.0


            elif prediction == "FAKE":

                real_probability = 25.0

                fake_probability = 75.0


        # ----------------------------------------------------
        # Normalize
        # ----------------------------------------------------

        total = (

            real_probability

            +

            fake_probability

        )


        if total > 0:

            real_probability = (

                real_probability

                /

                total

                *

                100

            )


            fake_probability = (

                fake_probability

                /

                total

                *

                100

            )


        # ----------------------------------------------------
        # Determine prediction from probability
        # ----------------------------------------------------

        if prediction == "UNCERTAIN":

            if real_probability >= 50:

                prediction = "REAL"

            else:

                prediction = "FAKE"


        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = max(

            real_probability,

            fake_probability

        )


        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

        result = {

            "prediction":

                prediction,

            "real_probability":

                round(

                    real_probability,

                    2

                ),

            "fake_probability":

                round(

                    fake_probability,

                    2

                ),

            "confidence":

                round(

                    confidence,

                    2

                ),

            "model_ready":

                True,

            "raw_prediction":

                str(

                    raw_prediction

                ),

            "message":

                "ML model prediction completed successfully."

        }


        return result


    except Exception as e:

        return {

            "prediction":

                "UNCERTAIN",

            "real_probability":

                50.0,

            "fake_probability":

                50.0,

            "confidence":

                0.0,

            "model_ready":

                False,

            "message":

                f"ML prediction error: {e}"

        }