from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register("schedule_days", views.DayViewSet, basename="days")
router.register("schedule_times", views.TimeViewSet, basename="times")

urlpatterns = [
    path('table/', views.table)
]

urlpatterns += router.urls
