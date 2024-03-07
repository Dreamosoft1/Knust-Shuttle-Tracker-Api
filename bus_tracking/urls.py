from django.urls import path
from .views import *

urlpatterns = [
    path('buses/', BusListAPIView.as_view(), name='bus-list'),
]
