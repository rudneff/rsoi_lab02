from django.conf.urls import patterns, url

from ask_api import views
from ask_api.views import QuestionListView, QuestionDetailView, AnswerListView, AnswerDetailView, signup

urlpatterns = patterns(
    '',
    url(r'questions/$', QuestionListView.as_view(), name='questions-list'),
    url(r'questions/(?P<pk>[0-9]+)/$', QuestionDetailView.as_view(), name='questions-detail'),
    url(r'answers/', AnswerListView.as_view(), name='answers-list'),
    url(r'answers/(?P<pk>[0-9]+)/$', AnswerDetailView.as_view(), name='answers-detail'),
    url(r'signup/$', signup, name="signup")
)
