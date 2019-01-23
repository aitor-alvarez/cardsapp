from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib import admin
from .models import *

class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Questions',
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz

class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', )
    list_filter = ('content',)
    fields = ('content', 'figure', 'quiz', 'answer_order', 'feedback_correct', 'feedback_incorrect',)

    search_fields = ('content', )
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('name', )



admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, MCQuestionAdmin)
admin.site.register(QuestionRating)