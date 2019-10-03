from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.table, name="home"),
    path('sign/', views.sign_up, name='user_sign'),
    path('login', views.sign_in, name='login_user'),
    path('table/', views.table, name="table"),
    path('table/refresh_models/', views.refresh_models, name='refresh'),
    path('subject/<str:day_name>/<int:time_id>/<str:aud>/', views.subject, name='subject')
    ]
