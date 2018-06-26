from .models import *
from django.shortcuts import render, get_list_or_404
import random
from django.http import HttpResponse

def save_quiz_response(request, question_id, choice_id):
    if request.is_ajax() and request.method=='POST':
        question = Question.objects.get(pk=question_id)
        choice = Choice.objects.get(pk=choice_id)
        QuestionRating.objects.create(question=question, response=choice, user=request.user)
        return HttpResponse('OK')



