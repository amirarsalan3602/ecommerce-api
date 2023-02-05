from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.manager import UserManager
import random
import string

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obg=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
        
    @classmethod
    def get_random_string(cls):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str
    
    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)

        return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }


# Create your models here.
