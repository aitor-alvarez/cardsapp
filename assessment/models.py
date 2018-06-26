# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Quiz (models.Model):
    name = models.CharField(max_length=150, blank=False)
    question = models.ManyToManyField('Question')

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.CharField (max_length=150, blank=False)
    option = models.ManyToManyField ('Choice')

    def __str__(self):
        return self.question


class Choice (models.Model):
    choice = models.CharField (max_length=150, blank=False)
    correct = models.BooleanField()

    def __str__(self):
        return self.choice


class QuestionRating(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    response = models.ForeignKey('Choice', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)