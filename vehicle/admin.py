from django.contrib import admin
from .models import *

admin.site.register([Stop, Driver, Vehicle, Driver_ID])
