from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model for EngiRAG.

    Uses Django's built-in authentication and permissions.
    Additional user fields can be introduced later.
    """

    pass
