import datetime

from celery import shared_task
from django.utils import timezone

from habit.models import Habit
from habit.services import send_message


@shared_task(name='habit.check_habits_and_send_reminders')
def check_habits_and_send_reminders():
    """Отправляет напоминания пользователям о выполнении привычек"""
    current_datetime = timezone.now()
    current_day = current_datetime.date()
    current_time = current_datetime.time()

    habits = Habit.objects.filter(is_pleasant=False)
    for habit in habits:
        if not habit.last_execution or (current_day - habit.last_execution).days >= habit.periodicity:
            if habit.time >= current_time:
                reward_habit = None
                if habit.award:
                    reward_habit = habit.award
                if habit.related_habit:
                    reward_habit = habit.related_habit
                message = f"""Напоминание: {habit.action} в {habit.place}
                        Не забудьте вознагродить себя: {reward_habit}"""
                chat_id = habit.user.tg_chat_id
                send_message(message, chat_id)
                habit.last_execution = current_day
