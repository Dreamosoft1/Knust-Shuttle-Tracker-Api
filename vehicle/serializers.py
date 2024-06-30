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
        fields = ['id','name', 'image', 'number', 'driver_id', 'date_of_birth','gender','vehicle']

class DriverCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Driver
        fields = ['id','name', 'driver_id', 'password']

class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['number', 'image', 'gender', 'date_of_birth','vehicle']

class DriverOtpVerificationSerializer(serializers.Serializer):
    code = serializers.CharField()
    user_id = serializers.CharField()

class DriverLoginSerializer(serializers.Serializer):
    driver_id = serializers.CharField()
    password = serializers.CharField(write_only=True)