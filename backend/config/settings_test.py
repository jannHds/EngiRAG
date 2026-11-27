
from .settings import *

# Isolated local database for migration testing.
# Does not connect to shared Supabase.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "migration_test.sqlite3",
    }
}
