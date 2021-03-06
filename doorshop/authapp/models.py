from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', blank=True, default=18)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
