from django.urls import path

from . import views

urlpatterns = [
    path('api/table', views.table, name="home"),
    path('api/users', views.register, name='register'),
    path('api/users/<str:username>', views.login, name='login'),
    path('api/classes/<str:auditorium_id>', views.auditorium_info, name='auditorium'),
    path('api/classes/<str:auditorium_id>/reserve', views.reserve_auditorium, name='reserve'),
    path('api/classes/<str:auditorium_id>/unreserve', views.unreserve_auditorium, name='unreserve'),
]
