from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', blank=True, default=18)
    email = models.EmailField(_('e-mail'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # @staticmethod
    # def get_email(self):
    #     return f'{self.email}'
    #
    # username = get_email

    def __str__(self):
        return f'{self.first_name}'

# class GuestUser(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     is_guest = models.BooleanField(default=True)
