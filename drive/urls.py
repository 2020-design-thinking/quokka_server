from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:pk>/update', views.update, name='drive'),
    path('<int:pk>/end', views.end, name='drive')
]
