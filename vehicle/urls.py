from django.urls import path
from .views import *

urlpatterns = [
    path('create/', DriverCreateView.as_view(), name="create-driver"),
    path('get/<str:long>/<str:lat>/', DriverDetailView.as_view(), name="get-details"),
    path('update-vehicle/<id>/', VehicleUpdateView.as_view(), name="update-car"),
]