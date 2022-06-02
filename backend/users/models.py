from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole():
    USER = 'user'
    ADMIN = 'admin'
    GUEST = 'guest'
    CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (GUEST, 'Гость'),
    ]


class User(AbstractUser):

    role = models.CharField(
        max_length=5,
        choices=UserRole.CHOICES,
        default=UserRole.USER,
        verbose_name='Уровень доступа'
    )

    @property
    def allowed_role(self):
        return self.role == UserRole.USER or self.role == UserRole.ADMIN

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    class Meta:
        ordering = ('username',)