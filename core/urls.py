from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/',include('authentication.urls')),
    #path("trip/", include("trip.urls")),
    path("driver/", include("vehicle.urls")),
    #path("lostfound/", include("lostfound.urls")),
    path('bus_tracking/', include('bus_tracking.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)