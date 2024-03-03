from django.db import models

class Stop(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50)
    stop = models.ManyToManyField(Stop, related_name='stops',blank=True)
    def __str__(self):
        return self.vehicle_number

class Driver(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='driver')
    name = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='drivers')
    image = models.ImageField(upload_to='driver_images', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.name