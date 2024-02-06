from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/',include('authentication.urls')),
    #path("trip/", include("trip.urls")),
    #path("vehicle/", include("vehicle.urls")),
    #path("lostfound/", include("lostfound.urls")),
]
