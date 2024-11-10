from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# ! Fixing the migration problem if there is unknown error
# ? https://chat.openai.com/c/a2bedf2d-801d-4814-8298-9dd7fb0973c3
"""
TLDR;
Delete the migrations file, drop the tables, and do this
python manage.py flush
python manage.py makemigrations your_app_name
python manage.py migrate
"""

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_ambassador = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_ambassador = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    fullName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_ambassador = models.BooleanField(default=True)
    
    first_name = None
    last_name = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Ensures email is prompted when creating superuser
    
    objects = UserManager()