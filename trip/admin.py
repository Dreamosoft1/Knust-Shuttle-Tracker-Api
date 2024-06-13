from django.contrib import admin
from .models import Trip_Request
# Register your models here.
class Trip_Request_Admin(admin.ModelAdmin):
    list_display = ['start_point', 'end_point', 'date', 'time', 'status']
    list_filter = ['date', 'status']
    search_fields = ['start_point', 'end_point']
    list_editable = ['status']
admin.site.register(Trip_Request, Trip_Request_Admin)