from datetime import datetime
from .models import Quiz

def update_quiz_status():
    current_time = datetime.now()
    active_quizzes = Quiz.objects.filter(startDate__lte=current_time, endDate__gte=current_time)
    inactive_quizzes = Quiz.objects.filter(startDate__gt=current_time)
    finished_quizzes = Quiz.objects.filter(endDate__lt=current_time)

    active_quizzes.update(status='active')
    inactive_quizzes.update(status='inactive')
    finished_quizzes.update(status='finished')