from django.contrib import admin
from .models import Feedback
# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'date']
    search_fields = ['name', 'email', 'message']
    list_filter = ['date']

admin.site.register(Feedback, FeedbackAdmin)