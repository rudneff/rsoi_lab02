from django.conf.urls import url

from ask_api.views import QuestionListView, QuestionDetailView, AnswerListView, AnswerDetailView, \
    CustomUserCreateView, status, CustomUserAuthenticationView, some_client_page, token

urlpatterns = [
    url(r'questions/$', QuestionListView.as_view(), name='questions-list'),
    url(r'questions/(?P<pk>[0-9]+)/$', QuestionDetailView.as_view(), name='questions-detail'),
    url(r'answers/', AnswerListView.as_view(), name='answers-list'),
    url(r'answers/(?P<pk>[0-9]+)/$', AnswerDetailView.as_view(), name='answers-detail'),
    url(r'signup/$', CustomUserCreateView.as_view(), name="signup"),
    url(r'status/$', status, name='api-status'),
    url(r'authorize/$', CustomUserAuthenticationView.as_view(), name='signin'),
    url(r'some_client_page/$', some_client_page, name='redirect-page'),
    url(r'token/$', token, name='get-token'),
]
