from django.urls import path
from .views import *

urlpatterns = [
    path('create/', DriverCreateView.as_view(), name="create-driver"),
    path('get/<str:long>/<str:lat>/', DriverDetailView.as_view(), name="get-details"),
    path('get/', DriverdetailViewToken.as_view(), name="get-drivers"),
    path('update-vehicle/<id>/', VehicleUpdateView.as_view(), name="update-car"),
    path('update/<id>/', DriverUpdateView.as_view(), name="update-driver"),
    path('verify/', DriverOtpVerification.as_view(), name="verify-driver"),
    path('login/', DriverLoginView.as_view(), name="driver-login"),
    path('logout/', DriverLogoutView.as_view(), name="driver-logout"),
    path('get-vehicle-list/', VehicleListView.as_view(), name="get-vehicle"),
    path('check/', CheckDriverVerification.as_view(), name="check-driver"),
]