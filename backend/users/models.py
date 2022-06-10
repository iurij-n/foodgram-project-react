from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Q


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
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+\Z',
                # message='Username must be Alphanumeric',
                # code='invalid_username'
            ),
        ]
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    @property
    def allowed_role(self):
        return self.role == UserRole.USER or self.role == UserRole.ADMIN

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    class Meta:
        ordering = ('pk',)
