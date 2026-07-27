from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(
    __file__
).resolve().parent


ENV_FILE = BASE_DIR / ".env"


print("=" * 60)

print("TRUTHGUARD AI API CONFIGURATION TEST")

print("=" * 60)


print()

print(
    "Project Directory:"
)

print(
    BASE_DIR
)


print()

print(
    ".env Location:"
)

print(
    ENV_FILE
)


print()

print(
    ".env Exists:"
)

print(
    ENV_FILE.exists()
)


load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


fact_check_key = os.getenv(
    "FACT_CHECK_API_KEY",
    ""
).strip()


news_api_key = os.getenv(
    "NEWS_API_KEY",
    ""
).strip()


print()

print(
    "NEWS_API_KEY:"
)

if news_api_key:

    print(
        "CONFIGURED"
    )

else:

    print(
        "NOT CONFIGURED"
    )


print()

print(
    "FACT_CHECK_API_KEY:"
)

if fact_check_key:

    print(
        "CONFIGURED"
    )

    print()

    print(
        "Key length:",
        len(
            fact_check_key
        )
    )

    print()

    print(
        "Key preview:",
        fact_check_key[:8]
        + "..."
    )

else:

    print(
        "NOT CONFIGURED"
    )


print()

print("=" * 60)