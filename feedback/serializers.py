from rest_framework import serializers
from .models import Trip_Request

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip_Request
        fields = '__all__'
