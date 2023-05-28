from django.db import models
import json
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres import fields
class Quiz(models.Model):
    question = models.CharField(max_length=255)
    options = models.JSONField()
    right_answer = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, default='inactive',null=True)

    def __str__(self):
        # Convert the JSON string back to a list
        return self.question
    