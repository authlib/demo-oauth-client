from django.urls import path
from project import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('auth/', views.auth, name='auth'),
]
