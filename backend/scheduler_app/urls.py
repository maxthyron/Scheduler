from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path('table/', views.table)
]