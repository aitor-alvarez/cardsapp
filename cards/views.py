from django.views.generic import ListView
from .models import *
from django.shortcuts import render, get_list_or_404
import random
from django.http import HttpResponse


class TopicListView(ListView):
    model = Topic
    template_name = 'cards/topic_list.html'


def get_cards_by_topic(request, topic_id):
    cards_list=[]
    cards = get_list_or_404(Card, topic_id=topic_id)
    cards = sorted(cards, key=lambda x: random.random())
    sequence = []
    for c in cards:
        card={}
        sequence.append(c.pk)
        card['id'] = c.pk
        card['title'] = c.title
        card['content'] = c.content
        card['description'] = c.description
        card['video'] = c.video
        card['image'] = c.image.url
        try:
            card['quizzes']=get_quiz(c.assessment.pk)
        except:
            card['quizzes']=''
        cards_list.append(card)

    card_sequence = CardSequence(user=request.user, card_sequence=sequence)
    card_sequence.save()
    return render(request, 'cards/card.html', {'cards': cards_list, 'sequence':card_sequence.pk})


def save_card_rating(request, card_id, seq_id, rating=0):
    if request.is_ajax() and request.method=='POST':
        card_rating = CardRating(card=Card.objects.get(pk=card_id), user=request.user, rating=rating)
        card_rating.save()
        card_sequence = CardSequence.objects.get(pk=seq_id)
        card_sequence.rating.add(card_rating)
        card_sequence.save()
        if rating==1:
            return HttpResponse('Glad you liked the card! :)')
        elif rating ==0:
            return HttpResponse('Sorry to hear that :(')


def get_quiz(quiz_id):
    quizzes=[]
    quiz = Quiz.objects.get(pk=quiz_id)
    for q in quiz.question.all ():
        assessment = {}
        assessment['question'] = [q.pk, q.question]
        choices=[]
        for choice in q.option.all ():
            choices.append([choice.pk, choice.choice, int(choice.correct)])
        assessment['choices'] = choices
        quizzes.append(assessment)
    return quizzes