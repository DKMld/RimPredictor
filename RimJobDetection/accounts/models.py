from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class Users(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=128, null=True, blank=True)

    USERNAME_FIELD = 'username'  # Set the field to be used for authentication
    REQUIRED_FIELDS = []

    objects = UserManager()


def authenticate(username=None, password=None):
    try:
        user = Users.objects.get(username=username)
        if check_password(password, user.password):
            return user
        return None
    except Users.DoesNotExist:
        return None

# class RemainingRimIdentificationAttempts(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
#     number_of_attempts = models.FloatField(default=0.0, null=False)
