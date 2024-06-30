from rest_framework import generics
from .models import Vehicle, Driver
import random
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
import os
import requests
from .permissions import IsDriver
from rest_framework.authtoken.models import Token
from authentication.models import User
from .serializers import VehicleSerializer, DriverSerializer, DriverCreateSerializer, DriverOtpVerificationSerializer, DriverUpdateSerializer, DriverLoginSerializer
from .exceptions import ExternalAPIError
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .utils import send_otp
class DriverCreateView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['name'] + str(random.randint(1, 1000)).replace(" ", "")
        email = username + "@st.knust.edu.gh"
        password = serializer.validated_data['password']
        full_name = serializer.validated_data['name']
        # Create a new user for the driver
        user = User.objects.create_user(username=username, email=email, password=password, full_name=full_name)
        user.last_name = "Driver"
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        
        # Pass the newly created user to perform_create
        self.perform_create(serializer, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({"data": serializer.data, "token": token.key}, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, user):
        # Save the driver instance with the correct user
        serializer.save(user=user)

class DriverUpdateView(generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,IsDriver,)
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.driver = Driver.objects.get(id=instance.id)
        # Check and send OTP if 'number' field is present and not empty
        if 'number' in request.data and request.data['number']:
            message = send_otp(instance.name, request.data['number'])
       
        
        # Handle the many-to-many relationship for the 'vehicle' field
        if 'vehicle' in request.data:
            vehicle_ids = request.data.get('vehicle')
            vehicles = Vehicle.objects.filter(id__in=vehicle_ids)
            instance.vehicle.set(vehicles)
    
        self.perform_update(serializer)
        return Response({"data": serializer.data, "message": message})
    
    def perform_update(self, serializer):
        try:
            driver = Driver.objects.get(user=self.request.user, id=self.kwargs['id'])
            serializer.save(driver=driver)
        except Driver.DoesNotExist:
            raise ExternalAPIError("You are not authorized to update this driver")

class DriverDetailView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        long = self.kwargs['long']
        lat = self.kwargs['lat']
        return Driver.objects.filter(longitude__range=(long-0.1, long+0.1), latitude__range=(lat-0.1, lat+0.1))

class DriverOtpVerification(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverOtpVerificationSerializer
    permission_classes = (permissions.AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data.get('code')
        user_id = serializer.validated_data.get('driver_id')
        phone = Driver.objects.get(pk=user_id).number
        data = {
            "code": code,
            "number": phone,
        }

        headers = {
        'api-key': os.environ.get('ARK_API_KEY'),
        }

        url = 'https://sms.arkesel.com/api/otp/verify'

        response = requests.post(url, json=data, headers=headers)
       
        if response.status_code == 200 and response.json().get("message") == "Successful":
            return Response({"message": "verified"}, status=200)
        elif response.status_code == 200 and response.json().get("message") == "Code has expired":
            return Response({"message": "Code expired"}, status=400)
        elif response.status_code == 200 and response.json().get("message") == "Invalid code":
            return Response({"message": "Code incorrect"}, status=400)
        else:
            print(f"Error: {response.status_code} and {response.json()}")
            return Response({"message": "Code incorrect"}, status=400)

class DriverLoginView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            driver = Driver.objects.get(driver_id=serializer.validated_data['driver_id'])
            user = driver.user
            ur = authenticate(username=user.email, password=serializer.validated_data['password'])
            if ur is None:
                return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            login(request, ur)
            token, _ = Token.objects.get_or_create(user=driver.user)
            return Response({"data":serializer.data,"token":token.key,"id":driver.pk}, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({"message":"Driver not found"}, status=status.HTTP_404_NOT_FOUND)

class DriverLogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class VehicleListView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticated,IsDriver,)
    
    def get_queryset(self):
        return Vehicle.objects.all()
    
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