from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name