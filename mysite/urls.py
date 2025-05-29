from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls', namespace='polls')),
    path('', RedirectView.as_view(url='/polls/', permanent=False)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include('polls.api_urls', namespace='polls_api')),
]
