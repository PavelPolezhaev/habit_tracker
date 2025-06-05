from datetime import timedelta

from django.core.exceptions import ValidationError

from habit.models import Habit


class AwardValidator:
    """Валидатор, проверяющий корректность заполнения полей связанной привычки и вознаграждения."""

    def __call__(self, data):
        related_habit = data.get("related_habit")
        award = data.get("award")
        is_pleasant = data.get("is_pleasant", False)

        related_habit_filled = related_habit is not None
        award_filled = bool(award)

        related_habit_obj = None
        if related_habit_filled:
            try:
                related_habit_obj = Habit.objects.get(
                    id=related_habit.id if hasattr(related_habit, "id") else related_habit
                )
            except Habit.DoesNotExist:
                raise ValidationError("Связанная привычка не найдена.")

        if not is_pleasant:
            if related_habit_filled and award_filled:
                raise ValidationError(
                    "Можно указать либо связанную привычку, либо вознаграждение, но не оба поля одновременно."
                )
            if not related_habit_filled and not award_filled:
                raise ValidationError(
                    "Для полезной привычки должно быть указано либо вознаграждение, либо связанная привычка."
                )
            if related_habit_filled and not related_habit_obj.is_pleasant:
                raise ValidationError("Связанная привычка должна быть приятной (is_pleasant=True).")

        else:
            if award_filled:
                raise ValidationError("Приятная привычка не может иметь вознаграждения.")
            if related_habit_filled:
                raise ValidationError("Приятная привычка не может иметь связанных привычек.")


class ExecutionTimeValidator:
    """Валидатор для проверки времени выполнения привычки"""

    def __call__(self, value):
        if value:
            if value > timedelta(seconds=120):
                raise ValidationError("Время выполнения привычки не должно превышать 120 секунд")
