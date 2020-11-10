from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_list, name='devices'),
    path('create/', views.create, name='devices'),
    path('<int:pk>/delete', views.delete, name='devices'),
    path('<int:pk>/update', views.update, name='devices')
]
