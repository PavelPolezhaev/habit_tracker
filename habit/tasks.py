from celery import shared_task
from django.utils import timezone

from habit.models import Habit
from habit.services import send_message


@shared_task(name="habit.check_habits_and_send_reminders")
def check_habits_and_send_reminders():
    """Отправляет напоминания пользователям о выполнении привычек"""
    current_datetime = timezone.now()
    current_day = current_datetime.date()
    current_time = current_datetime.time()

    habbits = Habit.objects.filter(is_pleasant=False)
    # Только пользователи с указанным tg_chat_id интересуют
    habbits = habbits.filter(user__tg_chat_id__isnull=False)
    # Время выполнения больше или равно текущему
    habbits = habbits.filter(time__gte=current_time)
    for habit in habbits:
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
