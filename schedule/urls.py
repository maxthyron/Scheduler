from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="schedule-home"),
    path('table/', views.table, name="schedule-table"),
    path('table/refresh_models/', views.refresh_models, name='refresh'),
    ]