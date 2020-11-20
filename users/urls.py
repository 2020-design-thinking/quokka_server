from django.urls import path, include
from . import views
from .views import UserViewSet

urlpatterns = [
    path('login/', UserViewSet.as_view({'post': 'login'}), name='users'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='users'),
    path('<int:pk>/', UserViewSet.as_view({'get': 'get_details'}), name='users'),
    path('cancel_reserve/', UserViewSet.as_view({'post': 'cancel_reserve'}), name='users')
]
