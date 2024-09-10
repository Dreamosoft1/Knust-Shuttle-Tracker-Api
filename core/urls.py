from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view( # new
    openapi.Info(
        title="Shuttle Hub API",
        default_version="v1",
        description="API for the Shuttle Hub",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    #permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/',include('authentication.urls')),
    path("driver/", include("vehicle.urls")),
    path("feedback/", include("feedback.urls")),
    path('swagger/', schema_view.with_ui( # new
    'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui( # new
    'redoc', cache_timeout=0), name='schema-redoc'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)