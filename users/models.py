from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Пароль")

    avatar = models.ImageField(
        upload_to="users/avatar",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите ваш аватар",
    )
    phone = models.CharField(max_length=30, verbose_name="Телефон", help_text="Введите ваш номер телефона")
    country = models.CharField(verbose_name="Страна", help_text="Введите вашу страну")
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="telegram chat id",
        help_text="Введите свой идентификатор чата в telegram (не ваше имя пользователя, которое начинается с @)",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
