from django.contrib import admin
from django.urls import path,include
from . import views
from django.urls import path
from .views import home, auth_page, career_guide, quiz_page, recommend_view, get_chat_history, list_chats,chat_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.auth_page, name='auth_page'),
    path('auth/', include('django.contrib.auth.urls')),
    path('career-guide/', views.career_guide, name='career_guide'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('api/recommend/', views.recommend_view, name='recommend'),
    path('api/chats/', list_chats, name='list_chats'),
    path('api/chats/<int:session_id>/', get_chat_history, name='chat_history'),
    path('api/chat/', chat_api, name='chat_api'),
    path("api/chats/new/", views.new_chat, name="new_chat"),
    path("api/chats/<int:session_id>/delete/", views.delete_chat, name="delete_chat"),
    path("quiz/", views.quiz_page, name="quiz"),
    path("submit-quiz/<int:user_id>/", views.submit_quiz, name="submit_quiz"),
    path("api/ask-gpt/", views.ask_gpt, name="ask_gpt"),
    path('profile/', views.user_profile, name='user_profile'),
]

