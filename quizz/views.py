from django.http import JsonResponse
from datetime import datetime,timedelta
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz
from .serializers import QuizSerializer
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import pytz


@csrf_exempt
@api_view(['POST'])
def create_quiz(request):
    print(settings.DATABASES)
    serializer = QuizSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        print("VALIDDDDDDDDDDDDDDDDDDDDD")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@cache_page(60 * 5)
def get_active_quiz(request):
    try:
        now = datetime.now()
        quiz = Quiz.objects.filter(start_date__lte=now, end_date__gte=now).first()
        if quiz:
            serializer = QuizSerializer(quiz)
            return JsonResponse(serializer.data)
        else:
            return JsonResponse({'message': 'No active quiz found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@cache_page(60 * 5)
def get_quiz_result(request, id):
    try:
        print("IDDDDDD",id)
        quiz = Quiz.objects.get(id=id) 
        date = datetime.now()
        end_date = quiz.end_date+ timedelta(minutes=5)
        end_date = end_date.replace(tzinfo=None)
        if end_date > date.replace(tzinfo=None):
            return JsonResponse({'message': 'Quiz result not available yet'}, status=403)
        serializer = QuizSerializer(quiz)
        return JsonResponse({'rightAnswer': serializer.data['right_answer']})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@cache_page(60 * 5)
def get_all_quizzes(request):
    try:
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)