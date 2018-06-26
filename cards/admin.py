from __future__ import unicode_literals
from .models import *
from django.contrib import admin





class TextMedia:
    js = [
         '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Card, Media=TextMedia)
admin.site.register(Profile)
admin.site.register(Subtopic)
admin.site.register(Topic)
admin.site.register(Linkage)
admin.site.register(CardRating)
admin.site.register(CardSequence)