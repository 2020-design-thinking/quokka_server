from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='users'),
    path('register/', views.register, name='users'),
    path('<int:pk>/', views.get_details, name='users')
]
