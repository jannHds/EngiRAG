from dotenv import dotenv_values
from .settings import *

# Dedicated local PostgreSQL migration test settings.
# Never use the shared Supabase database for these tests.

_pgtest_env = BASE_DIR.parent / ".env.pgtest"

if not _pgtest_env.is_file():
    raise RuntimeError("Missing local .env.pgtest file.")

_pgtest_password = dotenv_values(_pgtest_env).get(
    "PGTEST_PASSWORD"
)

if not _pgtest_password:
    raise RuntimeError("PGTEST_PASSWORD is required.")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "engirag_test",
        "USER": "engirag_test_user",
        "PASSWORD": _pgtest_password,
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "disable",
        },
        "CONN_MAX_AGE": 0,
    }
}
