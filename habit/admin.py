from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "place",
        "time",
        "is_pleasant",
        "periodicity",
    )
    list_filter = ("is_pleasant", "is_public", "user")
    search_fields = ("action", "place", "user__email")
    ordering = ("id",)
