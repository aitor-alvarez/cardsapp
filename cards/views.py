from django.views.generic import ListView
from .models import *
from django.shortcuts import render, get_list_or_404
import random
from django.http import HttpResponse
from assessment.models import Question, Quiz, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'cards/topic_list.html'

@login_required
def get_cards_by_topic(request, topic_id, lang):
    cards_list=[]
    cards = get_list_or_404(Card, topic_id=topic_id, language=lang)
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
        if c.image:
            card['image'] = c.image.url
        else:
            card['image'] =''
        try:
            card['quizzes'] =[]
            for q in c.quizzes.all():
                card['quizzes'] +=get_quiz(q.pk)
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
            return HttpResponse('Your response is correct')
        elif rating ==0:
            return HttpResponse('Your answer is incorrect')


def get_quiz(quiz_id):
    questions_all=[]
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    for q in questions.all():
        answers = Answer.objects.filter(question=q)
        assessment = {}
        if q.figure:
            assessment['question'] = [q.pk, q.content, q.figure.url]
        else:
            assessment['question'] = [q.pk, q.content]
        choices=[]
        for choice in answers:
            choices.append([choice.pk, choice.content, int(choice.correct)])
        assessment['choices'] = choices
        questions_all.append(assessment)
    return questions_all

def get_user_activity(request):
    sequences = CardSequence.objects.filter(user=request.user).order_by('-created')
    seqs = []
    for seq in sequences:
        dict = {}
        dict['created'] = seq.created
        if seq.rating:
            dict['rating'] = seq.rating
        score = 0
        if len (seq.quiz_responses.all ()) > 0:
            for resp in seq.quiz_responses.all():
                score += int(resp.answer.correct)
            percent = score / len (seq.quiz_responses.all())
            dict['score'] = round(percent*100)
        else:
            dict['score'] =0
        seqs.append(dict)
    return render(request, 'cards/history.html', {'sequences': seqs})


def show_card(request, card_id):
    card = Card.objects.get(id=card_id)
    return render (request, 'cards/single_card.html', {'card': card})
