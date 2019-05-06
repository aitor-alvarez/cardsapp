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
from assessment.views import save_quiz_response, get_quizscore_sequence
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', include(('social_django.urls', 'social_django'), namespace='social')),
    path('', include(('django.contrib.auth.urls','django.contrib.auth'), namespace='auth')),
    path('', login_required(TemplateView.as_view(template_name="cards/home.html")), name="home"),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('lang/<str:lang>/', TopicListView.as_view(), name='topics-list'),
    path('cards/<int:topic_id>/<str:lang>/', get_cards_by_topic, name='cards'),
    path('card/<int:card_id>/', show_card, name='card'),
    path('history/', get_user_activity, name='history'),
    path('save_rating/<int:card_id>/<int:seq_id>/<int:rating>', save_card_rating, name='save_card_rating'),
    path('quiz/<int:quiz_id>', get_quiz, name='get_quiz'),
    path('save_quiz/<int:choice_id>/<int:sequence_id>', save_quiz_response, name='save_quiz'),
    path('quiz_score/<int:sequence_id>', get_quizscore_sequence, name='quiz_score'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
