from rest_framework import serializers
from .models import Quiz
from django.contrib.postgres.fields import ArrayField

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
