from django.db import models

class Stop(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50, unique=True)
    max_power = models.CharField(max_length=50, blank=True, null=True)
    fuel_type = models.CharField(max_length=50, blank=True, null=True)
    max_speed = models.CharField(max_length=50, blank=True, null=True)
    zero_to_sixty = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50,blank=True,null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    gear_type = models.CharField(max_length=50, blank=True, null=True)
    fuel_consumption = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    start = models.ManyToManyField(Stop, related_name='start',blank=True)
    stop = models.ManyToManyField(Stop, related_name='stops',blank=True)
    def __str__(self):
        return self.vehicle_number

class Driver(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='driver')
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    vehicle = models.ManyToManyField(Vehicle, related_name='vehicle',blank=True)
    image = models.ImageField(upload_to='driver_images', blank=True, null=True)
    latitude = models.CharField(max_length=50, default="0")
    number = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, default="0")
    driver_id = models.CharField(max_length=50,unique=True, blank=True, null=True)
    def __str__(self):
        return self.name

class Driver_ID(models.Model):
    driver_id = models.CharField(max_length=50)
    def __str__(self):
        return self.driver_id