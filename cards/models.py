# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from assessment.models import Quiz
from django.utils import timezone

type_choices = (
    ('C', 'Content'),
    ('F', 'Feedback')
)

learning_choices = (
    ('A', 'Assess'),
    ('D', 'Discover'),
    ('F', 'Familiarize'),
    ('U', 'Use')
)

lang_choices = (
    ('C', 'Chinese'),
    ('R', 'Russian')
)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username+' Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Card(models.Model):
    reference_id = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=250, blank=False)
    title = models.CharField(max_length=150, blank=False)
    topic = models.ForeignKey('Topic', blank=True, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=1, choices=type_choices, blank=True)
    subtopic = models.ForeignKey('Subtopic', blank=True, null=True, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    prompt = models.CharField(max_length=250, blank=True)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='uploads', blank=True)
    video = models.URLField(blank=True)
    duration = models.FloatField(blank=True)
    learning_phase = models.CharField(max_length=1, choices=learning_choices, blank=True)
    language = models.CharField(max_length=1, choices=lang_choices, blank=False)
    assessment = models.ForeignKey(Quiz, blank=True, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CardRating(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.card.title


class Linkage(models.Model):
    name = models.CharField(max_length=150, blank=False)
    group_cards = models.ManyToManyField('Card')

    def __str__(self):
        return self.name


class TopicManager(models.Manager):
    def get_by_natural_key(self, name, chinese_name, russian_name ):
        return self.get(name=name, chinese_name=chinese_name, russian_name=russian_name)


class Topic(models.Model):
    objects = TopicManager()
    name = models.CharField(max_length=150, blank=False)
    chinese_name = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    russian_name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='uploads', blank=True)

    class Meta:
        unique_together = (('name', 'chinese_name', 'russian_name'),)

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class CardSequence(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    card_sequence = models.CharField(max_length=250)
    rating = models.ManyToManyField('CardRating', blank=True)
    created = models.DateTimeField(default=timezone.now)