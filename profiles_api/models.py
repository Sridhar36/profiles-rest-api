# Importing necessary modules from Django
from django.db import models  # Provides database model functionality
from django.contrib.auth.models import AbstractBaseUser  # Provides a base class for custom user models
from django.contrib.auth.models import PermissionsMixin  # Adds permissions functionality to custom user model


from django.contrib.auth.models import BaseUserManager
...


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



# Custom user profile model that inherits from AbstractBaseUser and PermissionsMixin
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system."""
    
    # Defining the email field with max length 255 and ensuring it's unique (no two users can have the same email)
    email = models.EmailField(max_length=255, unique=True)

    # Defining a field for the user's name, max length of 255 characters
    name = models.CharField(max_length=255)

    # Defining the is_active field, which determines if the user is active or not (default: True)
    is_active = models.BooleanField(default=True)

    # Defining the is_staff field, which determines if the user has staff-level permissions (default: False)
    is_staff = models.BooleanField(default=False)

    # Connecting a custom manager for the UserProfile model (you need to define UserProfileManager elsewhere)
    objects = UserProfileManager()

    # Specifies the field that will be used as the username (in this case, email instead of the default username)
    USERNAME_FIELD = 'email'

    # List of fields that are required when creating a user, besides the USERNAME_FIELD (email in this case)
    REQUIRED_FIELDS = ['name']

    # Method to return the full name of the user
    def get_full_name(self):
        """Retrieve full name for user."""
        return self.name

    # Method to return a short version of the user's name (in this case, just their name)
    def get_short_name(self):
        """Retrieve short name of user."""
        return self.name

    # String representation of the user object; this is how the user will appear when printed or in the Django admin
    def __str__(self):
        """Return string representation of user."""
        return self.email
