from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    # index
    path('', views.IndexRedirectView.as_view(), name='index_redirect'),

    # question
    path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('question/update/<int:question_id>/', views.QuestionUpdateView.as_view(),
         name='question_update'),
    path('question/delete/<int:question_id>/', views.QuestionDeleteView.as_view(),
         name='question_delete'),
    path('question/list/', views.QuestionListView.as_view(), name='question_list'),

    # answer
    path('answer/<int:question_id>/create/', views.AnswerCreateView.as_view(), name='answer_create'),
    path('answer/update/<int:answer_id>/', views.AnswerUpdateView.as_view(),
         name='answer_update'),
    path('answer/delete/<int:answer_id>/', views.AnswerDeleteView.as_view(),
         name='answer_delete'),
    path('answer/<int:question_id>/list/', views.AnswerListView.as_view(), name='answer_list'),

    # game
    path('game/start/', views.GameStartTemplateView.as_view(), name='game_start'),
    path('game/list/', views.GameListView.as_view(), name='game_list'),
    path('game/get-questions/', views.GameCreateRedirectView.as_view(), name='game_get_questions'),
    path('game/playing/<int:game_id>/', views.PlayGameView.as_view(), name='game_play'),
]
