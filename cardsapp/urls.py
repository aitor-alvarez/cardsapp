"""cardsapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cards.views import *
from django.conf.urls.static import static
from django.conf import settings
from assessment.views import save_quiz_response

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', TopicListView.as_view(), name='topics-list'),
    path('cards/<int:topic_id>', get_cards_by_topic, name='cards'),
    path('save_rating/<int:card_id>/<int:seq_id>/<int:rating>', save_card_rating, name='save_card_rating'),
    path('quiz/<int:quiz_id>', get_quiz, name='get_quiz'),
    path('save_quiz/<int:question_id>/<int:choice_id>', save_quiz_response, name='save_quiz'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
