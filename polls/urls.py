from django.urls import include, path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (PollViewSet,
                   QuestionViewSet,
                   AnswerViewSet,
                   QwestionsByPollViewSet,
                   AnswerByPollViewSet,
                   ActivePollsViewSet,
                   answer_question,
                   GetPollsByUserView,
)


v1_router = DefaultRouter()

v1_router.register('polls', PollViewSet, basename='polls')
v1_router.register('questions', QuestionViewSet, basename='questions')
v1_router.register('answers', AnswerViewSet, basename='questions')
v1_router.register('active_polls', ActivePollsViewSet, basename='active_polls')
v1_router.register('get_my_answers', GetPollsByUserView, basename='get_answers')

v1_router.register('polls/(?P<poll_id>.+)/questions',
                    QwestionsByPollViewSet,
                    basename='questions_by_poll')

v1_router.register('polls/(?P<poll_id>.+)/questions/(?P<question_id>.+)/answers',
                    AnswerByPollViewSet,
                    basename='questions_by_poll')

urlpatterns = [
    path('v1/token-auth/', views.obtain_auth_token), #Bearer 
    path('v1/make_answer/', answer_question),
    path('v1/', include(v1_router.urls)),    
]