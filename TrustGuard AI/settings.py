# ============================================================
# TRUTHGUARD AI
# config/settings.py
#
# Central configuration file for the entire project.
#
# IMPORTANT:
# This version does NOT apply global CSS.
# Your original UI styling remains unchanged.
# ============================================================

from pathlib import Path
import os

from dotenv import load_dotenv


# ============================================================
# PROJECT ROOT
# ============================================================

# Current file:
#
# truthguard_ai/
# └── config/
#     └── settings.py
#
# BASE_DIR becomes:
#
# truthguard_ai/
#
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT FILE
# ============================================================

ENV_FILE = BASE_DIR / ".env"

# Load environment variables from .env
#
# override=True ensures the latest .env values
# are used when Streamlit is restarted.
#
load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


# ============================================================
# APPLICATION INFORMATION
# ============================================================

APP_NAME = "TruthGuard AI"

APP_ICON = "🛡️"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "AI-Powered Fake News Detection "
    "and Verification System"
)


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = (
    BASE_DIR / "data"
)

RAW_DATA_DIR = (
    DATA_DIR / "raw"
)

PROCESSED_DATA_DIR = (
    DATA_DIR / "processed"
)


# ============================================================
# DATASET FILES
# ============================================================

TRUE_DATASET_PATH = (
    RAW_DATA_DIR / "True.csv"
)

FAKE_DATASET_PATH = (
    RAW_DATA_DIR / "Fake.csv"
)

DATASET_PATH = (
    PROCESSED_DATA_DIR / "dataset.csv"
)


# ============================================================
# MODEL DIRECTORY
# ============================================================

MODELS_DIR = (
    BASE_DIR / "models"
)


# ============================================================
# MODEL FILES
# ============================================================

MODEL_PATH = (
    MODELS_DIR / "fake_news_model.pkl"
)

VECTORIZER_PATH = (
    MODELS_DIR / "tfidf_vectorizer.pkl"
)

METADATA_PATH = (
    MODELS_DIR / "model_metadata.json"
)


# ============================================================
# DATABASE
# ============================================================

DATABASE_DIR = (
    BASE_DIR / "database"
)

DATABASE_PATH = (
    DATABASE_DIR / "truthguard.db"
)


# ============================================================
# LOGGING
# ============================================================

LOGS_DIR = (
    BASE_DIR / "logs"
)

LOG_FILE = (
    LOGS_DIR / "truthguard.log"
)


# ============================================================
# API KEYS
# ============================================================

# ------------------------------------------------------------
# NewsAPI
# ------------------------------------------------------------

NEWS_API_KEY = os.getenv(
    "NEWS_API_KEY",
    ""
).strip()


# ------------------------------------------------------------
# GNews API
#
# This variable is kept for compatibility with your
# existing Settings page.
#
# Note:
# Google News RSS does NOT require this API key.
# ------------------------------------------------------------

GNEWS_API_KEY = os.getenv(
    "GNEWS_API_KEY",
    ""
).strip()


# ------------------------------------------------------------
# Google Fact Check API
#
# Supports both:
#
# GOOGLE_FACT_CHECK_API_KEY
# FACT_CHECK_API_KEY
#
# This prevents import/configuration errors if different
# files in your project use different variable names.
# ------------------------------------------------------------

GOOGLE_FACT_CHECK_API_KEY = os.getenv(
    "GOOGLE_FACT_CHECK_API_KEY",
    ""
).strip()


FACT_CHECK_API_KEY = os.getenv(
    "FACT_CHECK_API_KEY",
    ""
).strip()


# ------------------------------------------------------------
# Synchronize Fact Check API keys
# ------------------------------------------------------------

if not GOOGLE_FACT_CHECK_API_KEY:

    GOOGLE_FACT_CHECK_API_KEY = (
        FACT_CHECK_API_KEY
    )


FACT_CHECK_API_KEY = (
    GOOGLE_FACT_CHECK_API_KEY
)


# ============================================================
# SMTP / EMAIL CONFIGURATION
# ============================================================

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME",
    ""
).strip()


SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD",
    ""
).strip()

SMTP_HOST = os.getenv(
    "SMTP_HOST",
    ""
).strip()


SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
).strip()


SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)


GMAIL_SENDER = os.getenv(
    "GMAIL_SENDER",
    SMTP_USERNAME
).strip()


# --> ADDED TO FIX IMPORT ERROR IN reports/email_report.py
SMTP_FROM = os.getenv(
    "SMTP_FROM",
    GMAIL_SENDER
).strip()


# ============================================================
# FEATURE STATUS
# ============================================================

# ------------------------------------------------------------
# Google News RSS
#
# Works without an API key.
# ------------------------------------------------------------

GOOGLE_NEWS_ENABLED = True


# ------------------------------------------------------------
# NewsAPI
# ------------------------------------------------------------

NEWS_API_ENABLED = bool(
    NEWS_API_KEY
)


# ------------------------------------------------------------
# GNews API
# ------------------------------------------------------------

GNEWS_API_ENABLED = bool(
    GNEWS_API_KEY
)


# ------------------------------------------------------------
# Google Fact Check API
# ------------------------------------------------------------

FACT_CHECK_ENABLED = bool(
    GOOGLE_FACT_CHECK_API_KEY
)


# ------------------------------------------------------------
# SMTP
# ------------------------------------------------------------

SMTP_ENABLED = bool(
    SMTP_USERNAME
    and SMTP_PASSWORD
)


# ============================================================
# NETWORK SETTINGS
# ============================================================

REQUEST_TIMEOUT = 15


USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


# ============================================================
# MACHINE LEARNING SETTINGS
# ============================================================

MODEL_CONFIDENCE_THRESHOLD = 60.0


# ============================================================
# ONLINE VERIFICATION SETTINGS
# ============================================================

MAX_ONLINE_RESULTS = 10

MAX_FACT_CHECK_RESULTS = 10


# ============================================================
# FINAL ASSESSMENT SETTINGS
# ============================================================

# Score >= 60
#     -> LIKELY REAL
#
# Score <= 40
#     -> LIKELY FAKE
#
# Score 41-59
#     -> UNCERTAIN

FINAL_REAL_THRESHOLD = 60.0

FINAL_FAKE_THRESHOLD = 40.0


# ============================================================
# SOURCE CREDIBILITY
# ============================================================

HIGH_CREDIBILITY_SOURCE_SCORE = 90.0

GOOD_CREDIBILITY_SOURCE_SCORE = 75.0

UNKNOWN_SOURCE_SCORE = 50.0


# ============================================================
# STREAMLIT SETTINGS
# ============================================================

STREAMLIT_PAGE_TITLE = APP_NAME

STREAMLIT_PAGE_ICON = APP_ICON

STREAMLIT_LAYOUT = "wide"


# ============================================================
# GLOBAL CSS FUNCTION
# ============================================================

def inject_global_css():

    """
    Compatibility function.

    Your existing app.py and pages may call:

        inject_global_css()

    This function intentionally does NOTHING.

    The reason is that the original TruthGuard AI UI
    should not be overwritten by new global CSS.

    Existing page-specific CSS and UI styling remain
    untouched.
    """

    return None


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

REQUIRED_DIRECTORIES = [

    DATA_DIR,

    RAW_DATA_DIR,

    PROCESSED_DATA_DIR,

    MODELS_DIR,

    DATABASE_DIR,

    LOGS_DIR

]


for directory in REQUIRED_DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# CONFIGURATION SUMMARY
# ============================================================

def get_config_summary():

    """
    Return the current TruthGuard AI configuration
    as a dictionary.

    API keys themselves are NOT returned for security.
    """

    return {

        # ----------------------------------------------------
        # Application
        # ----------------------------------------------------

        "app_name":
            APP_NAME,

        "app_icon":
            APP_ICON,

        "app_version":
            APP_VERSION,


        # ----------------------------------------------------
        # Project paths
        # ----------------------------------------------------

        "base_dir":
            str(BASE_DIR),

        "env_file":
            str(ENV_FILE),

        "env_exists":
            ENV_FILE.exists(),


        # ----------------------------------------------------
        # Data
        # ----------------------------------------------------

        "data_dir":
            str(DATA_DIR),

        "raw_data_dir":
            str(RAW_DATA_DIR),

        "processed_data_dir":
            str(PROCESSED_DATA_DIR),


        # ----------------------------------------------------
        # Models
        # ----------------------------------------------------

        "models_dir":
            str(MODELS_DIR),

        "model_path":
            str(MODEL_PATH),

        "vectorizer_path":
            str(VECTORIZER_PATH),

        "metadata_path":
            str(METADATA_PATH),


        # ----------------------------------------------------
        # Database
        # ----------------------------------------------------

        "database_path":
            str(DATABASE_PATH),


        # ----------------------------------------------------
        # API Status
        # ----------------------------------------------------

        "google_news_enabled":
            GOOGLE_NEWS_ENABLED,

        "news_api_enabled":
            NEWS_API_ENABLED,

        "gnews_api_enabled":
            GNEWS_API_ENABLED,

        "fact_check_enabled":
            FACT_CHECK_ENABLED,

        "SMTP_enabled":
            SMTP_ENABLED

    }


# ============================================================
# API STATUS HELPERS
# ============================================================

def is_news_api_configured():

    """
    Check whether NewsAPI is configured.
    """

    return bool(
        NEWS_API_KEY
    )


def is_gnews_api_configured():

    """
    Check whether GNews API is configured.
    """

    return bool(
        GNEWS_API_KEY
    )


def is_fact_check_api_configured():

    """
    Check whether Google Fact Check API is configured.
    """

    return bool(
        GOOGLE_FACT_CHECK_API_KEY
    )


def is_smtp_configured():

    """
    Check whether SMTP email is configured.
    """

    return bool(
        SMTP_USERNAME
        and SMTP_PASSWORD
    )


# ============================================================
# MODEL FILE STATUS
# ============================================================

def is_model_ready():

    """
    Check whether all required ML model files exist.
    """

    return (

        MODEL_PATH.exists()

        and

        VECTORIZER_PATH.exists()

    )


# ============================================================
# DATABASE STATUS
# ============================================================

def is_database_ready():

    """
    Check whether the TruthGuard database exists.
    """

    return DATABASE_PATH.exists()


# ============================================================
# FULL SYSTEM STATUS
# ============================================================

def get_system_status():

    """
    Return the current status of all major
    TruthGuard AI components.
    """

    return {

        "application":
            APP_NAME,

        "model_ready":
            is_model_ready(),

        "database_ready":
            is_database_ready(),

        "google_news":
            GOOGLE_NEWS_ENABLED,

        "news_api":
            is_news_api_configured(),

        "gnews_api":
            is_gnews_api_configured(),

        "fact_check_api":
            is_fact_check_api_configured(),

        "smtp":
            is_smtp_configured()

    }


# ============================================================
# COMMAND-LINE CONFIGURATION TEST
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 65)

    print(
        "TRUTHGUARD AI - CONFIGURATION STATUS"
    )

    print("=" * 65)

    print()


    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    print(
        "Application:",
        APP_NAME
    )

    print(
        "Icon:",
        APP_ICON
    )

    print(
        "Version:",
        APP_VERSION
    )

    print()


    # --------------------------------------------------------
    # Project
    # --------------------------------------------------------

    print(
        "Project Directory:"
    )

    print(
        BASE_DIR
    )

    print()


    print(
        ".env File:"
    )

    print(
        ENV_FILE
    )

    print()


    print(
        ".env Exists:",
        ENV_FILE.exists()
    )

    print()


    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    print(
        "ML Model:",
        (
            "READY"
            if MODEL_PATH.exists()
            else "NOT FOUND"
        )
    )

    print(
        "Vectorizer:",
        (
            "READY"
            if VECTORIZER_PATH.exists()
            else "NOT FOUND"
        )
    )

    print()


    # --------------------------------------------------------
    # Online Verification
    # --------------------------------------------------------

    print(
        "Google News RSS:",
        (
            "ENABLED"
            if GOOGLE_NEWS_ENABLED
            else "DISABLED"
        )
    )


    print(
        "NewsAPI:",
        (
            "CONFIGURED"
            if NEWS_API_ENABLED
            else "NOT CONFIGURED"
        )
    )


    print(
        "GNews API:",
        (
            "CONFIGURED"
            if GNEWS_API_ENABLED
            else "NOT CONFIGURED"
        )
    )


    print(
        "Google Fact Check API:",
        (
            "CONFIGURED"
            if FACT_CHECK_ENABLED
            else "NOT CONFIGURED"
        )
    )

    print()


    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    print(
        "SMTP:",
        (
            "CONFIGURED"
            if SMTP_ENABLED
            else "NOT CONFIGURED"
        )
    )

    print()


    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    print(
        "Database:",
        (
            "READY"
            if DATABASE_PATH.exists()
            else "NOT CREATED YET"
        )
    )

    print()


    print("=" * 65)

    print(
        "Configuration check completed."
    )

    print("=" * 65)

    print()