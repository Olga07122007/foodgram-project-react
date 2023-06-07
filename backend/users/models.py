from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import EmailValidator

from .validators import (
    validate_username,
    UsernameValidator
)


USER = 'user'
ADMIN = 'admin'


ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
]


class User(AbstractUser):
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    email = models.CharField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        validators=[
            EmailValidator(
                message='Введите действительный адрес электронной почты!'
            )
        ]
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username, UsernameValidator())
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )

    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
