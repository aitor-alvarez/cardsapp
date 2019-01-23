# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.utils import timezone


ANSWER_ORDER_OPTIONS = (
    ('content', _('Answers')),
    ('random', _('Random'))
)


@python_2_unicode_compatible
class Quiz (models.Model):
    name = models.CharField(max_length=150, blank=False)

    class Meta:
        verbose_name = _ ("Quiz")
        verbose_name_plural = _ ("Quizzes")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Question(models.Model):

    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)

    figure = models.ImageField(upload_to='uploads',
                               blank=True,
                               null=True,
                               verbose_name=_("Image"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the question text that "
                                           "you want displayed"),
                               verbose_name=_('Question'))

    feedback_correct = models.TextField(max_length=2000,
                                   blank=True,
                                   help_text=_("Explanation to be shown "
                                               "after the question has "
                                               "been answered correctly"),
                                   verbose_name=_('Feedback for Correct Answers'))

    feedback_incorrect = models.TextField (max_length=2000,
                                         blank=True,
                                         help_text=_ ("Explanation to be shown "
                                                      "after the question has "
                                                      "been answered incorrectly"),
                                         verbose_name=_ ('Feedback for Incorrect Answers'))

    answer_order = models.CharField (
        max_length=30, null=True, blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_ ("The order in which multichoice "
                     "answer options are displayed "
                     "to the user"),
        verbose_name=_ ("Answer Order"))


    def check_if_correct(self, guess):
        answer = Answer.objects.get (id=guess)

        if answer.correct is True:
            return True
        else:
            return False

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by ('content')
        if self.answer_order == 'random':
            return queryset.order_by ('?')
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter (question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers (Answer.objects.filter (question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.content


@python_2_unicode_compatible
class Answer(models.Model):

    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class QuestionRating(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField (default=timezone.now)