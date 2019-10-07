from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.table, name="home"),
    path('refresh_models/', views.refresh_models, name='refresh'),
    path('current/', views.current, name='current'),
    path('cancel_reserved/', views.cancel_reserved, name='cancel_reserved'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='schedule/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='schedule/logout.html'),
         name='logout'),
    path('occupy_auditorium/', views.occupy_auditorium, name='occupy_auditorium'),
    path('subject/<str:day_name>/<int:time_id>/<str:aud_id>/', views.subject, name='subject')
    ]
