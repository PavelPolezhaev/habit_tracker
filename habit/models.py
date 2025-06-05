from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создатель привычки")
    place = models.CharField(
        max_length=100, verbose_name="Место", help_text="Место в котором небходимо выполнять привычку"
    )
    time = models.TimeField(verbose_name="Время выполнения", help_text="Время когда необходимо выполнять привычку")
    action = models.CharField(
        max_length=100, verbose_name="Действие", help_text="Действие которое представляет собой привычка"
    )
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки.",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.",
        blank=True,
        null=True,
    )
    periodicity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(7)], verbose_name="Периодичность привычки", default=1
    )
    award = models.CharField(
        max_length=200,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения.",
        blank=True,
        null=True,
    )
    time_needed = models.DurationField(
        verbose_name="Время на выполнение",
        help_text="Время, которое предположительно потратит пользователь на выполнение привычки.",
    )
    is_public = models.BooleanField(
        verbose_name="Признак публичности",
        help_text="Привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.",
        default=0,
    )
    last_execution = models.DateField(verbose_name="Дата последнего выполнения", null=True, blank=True)

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
