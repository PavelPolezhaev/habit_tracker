from datetime import time, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем тестового пользователя
        self.user = User.objects.create(email="test@example.com", password="testpass123", tg_chat_id="123456789")

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые привычки
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Пить кофе",
            is_pleasant=True,
            periodicity=1,
            time_needed=timedelta(seconds=30),
            is_public=True,
        )

        self.useful_habit = Habit.objects.create(
            user=self.user,
            place="Спортзал",
            time=time(18, 0),
            action="Тренировка",
            is_pleasant=False,
            periodicity=2,
            award="Посмотреть сериал",
            time_needed=timedelta(minutes=1),
            is_public=False,
        )

        # URL для тестирования
        self.create_url = reverse("habit:habit_create")
        self.list_url = reverse("habit:my_habit_list")
        self.public_list_url = reverse("habit:public_habit_list")

    def test_habit_creation(self):
        """Тестирование создания привычки"""
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Утренняя пробежка",
            "is_pleasant": False,
            "periodicity": 1,
            "award": "Кофе",
            "time_needed": "00:02:00",
            "is_public": True,
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_habit_list(self):
        """Тестирование получения списка привычек пользователя"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_public_habit_list(self):
        """Тестирование получения списка публичных привычек"""
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Пить кофе")

    def test_habit_update(self):
        """Тестирование обновления привычки"""
        update_url = reverse("habit:habit_update", kwargs={"pk": self.useful_habit.pk})
        data = {
            "action": "Вечерняя тренировка",
            "place": "Спортзал",
            "time": "18:00:00",
            "is_pleasant": False,
            "periodicity": 2,
            "award": "Посмотреть сериал",
            "time_needed": "00:01:00",
            "is_public": False,
        }

        response = self.client.patch(update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.useful_habit.refresh_from_db()
        self.assertEqual(self.useful_habit.action, "Вечерняя тренировка")

    def test_habit_delete(self):
        """Тестирование удаления привычки"""
        delete_url = reverse("habit:habit_delete", kwargs={"pk": self.useful_habit.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)


class HabitPermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем двух пользователей
        self.user1 = User.objects.create(email="user1@example.com", password="testpass123")
        self.user2 = User.objects.create(email="user2@example.com", password="testpass123")

        # Создаем привычку для первого пользователя
        self.habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time=time(8, 0),
            action="Тестовая привычка",
            is_pleasant=False,
            periodicity=1,
            award="Тестовая награда",
            time_needed=timedelta(seconds=30),
        )

    def test_user_permissions(self):
        """Тестирование прав доступа к привычкам"""
        # Аутентифицируем второго пользователя
        self.client.force_authenticate(user=self.user2)

        # Пытаемся получить доступ к привычке первого пользователя
        retrieve_url = reverse("habit:habit_retrieve", kwargs={"pk": self.habit.pk})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Пытаемся обновить привычку первого пользователя
        update_url = reverse("habit:habit_update", kwargs={"pk": self.habit.pk})
        response = self.client.patch(update_url, {"action": "Новое действие"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Пытаемся удалить привычку первого пользователя
        delete_url = reverse("habit:habit_delete", kwargs={"pk": self.habit.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
