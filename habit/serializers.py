from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habit.models import Habit
from habit.validators import AwardValidator, ExecutionTimeValidator


class HabitSerializer(ModelSerializer):
    time_needed = serializers.DurationField(
        validators=[ExecutionTimeValidator()],
        required=False,
        help_text="Длительность выполнения в формате HH:MM:SS (макс. 2 минуты)",
    )

    class Meta:
        model = Habit
        fields = (
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "award",
            "time_needed",
            "is_public",
        )
        validators = [AwardValidator()]
