from django.contrib import admin
from .models import User, User_Profile
# Register your models here.
class User_ProfileInline(admin.StackedInline):
    model = User_Profile
    extra = 1  # Number of empty forms

class UserAdmin(admin.ModelAdmin):
    inlines = [User_ProfileInline]

admin.site.register(User, UserAdmin)