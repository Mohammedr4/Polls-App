# urls.py
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create_question, name='create_question'),
    path('<int:question_id>/comment/', views.comment_on_poll, name='add_comment'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]