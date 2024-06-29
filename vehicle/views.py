from rest_framework import generics
from .models import Vehicle, Driver
import random
from .permissions import IsDriver
from rest_framework.authtoken.models import Token
from authentication.models import User
from .serializers import VehicleSerializer, DriverSerializer, DriverCreateSerializer
from .exceptions import ExternalAPIError
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth import authenticate
class DriverCreateView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['name'] + str(random.randint(1, 1000))
        email = username + "@st.knust.edu.gh"
        user = User.objects.create_user(username=username, email=username+email, full_name=serializer.validated_data['name'], last_name="Driver", password="defaultpassword")
        driver = authenticate(username=email, password="defaultpassword")
        login(request, driver)
        token, _ = Token.objects.get_or_create(user=user)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"token":token.key}, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        vehicle_id = self.request.data['vehicle']
        vehicle = Vehicle.objects.get(id=vehicle_id)
        driver_instance = serializer.save(user=self.request.user)
        driver_instance.vehicle.add(vehicle)  # Assuming 'vehicle' is a many-to-many field in the Driver model

class DriverDetailView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        long = self.kwargs['long']
        lat = self.kwargs['lat']
        return Driver.objects.filter(longitude__range=(long-0.1, long+0.1), latitude__range=(lat-0.1, lat+0.1))

class VehicleUpdateView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticated,IsDriver,)
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.vehicle = Vehicle.objects.get(id=instance.id)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        try:
            driver = Driver.objects.get(user=self.request.user, vehicle=self.vehicle)
            serializer.save(driver=driver)
        except Driver.DoesNotExist:
            raise ExternalAPIError("You are not authorized to update this vehicle")