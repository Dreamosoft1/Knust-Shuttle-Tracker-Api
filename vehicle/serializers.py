from rest_framework import serializers
from .models import Vehicle, Driver, Stop

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    stop = StopSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'