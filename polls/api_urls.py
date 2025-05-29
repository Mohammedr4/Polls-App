from django.urls import path
from . import api_views

app_name = 'polls_api'

urlpatterns = [
    path('', api_views.api_root, name='api-root'),
    path('questions/', api_views.QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', api_views.QuestionDetail.as_view(), name='question-detail'),
    path('comments/', api_views.PollCommentList.as_view(), name='comment-list'),
    path('choices/', api_views.ChoiceList.as_view(), name='choice-list'),

]
