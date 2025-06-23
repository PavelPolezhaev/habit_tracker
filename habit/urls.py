from django.urls import path

from habit.apps import TrackerConfig
from habit.views import (
    HabitCreateAPIView,
    HabitDestroyView,
    HabitListView,
    HabitRetrieveView,
    HabitUpdateView,
    PublicHabitListView,
)

app_name = TrackerConfig.name

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("<int:pk>/update/", HabitUpdateView.as_view(), name="habit_update"),
    path("my_habits/", HabitListView.as_view(), name="my_habit_list"),
    path("public_habit/", PublicHabitListView.as_view(), name="public_habit_list"),
    path("<int:pk>/retrieve/", HabitRetrieveView.as_view(), name="habit_retrieve"),
    path("<int:pk>/delete/", HabitDestroyView.as_view(), name="habit_delete"),
]
