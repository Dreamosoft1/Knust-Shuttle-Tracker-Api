from django.db import models
from authentication.models import User
from vehicle.models import Driver

# Create your models here.
class Trip_Request(models.Model):
    status_choices = (1, 'Pending'), (2, 'Accepted'), (3, 'Rejected')
    users = models.ManyToManyField(User)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver')
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.IntegerField(default=1, choices=status_choices)

    def __str__(self):
        return self.start_point + ' to ' + self.end_point + ' on ' + str(self.date) + ' at ' + str(self.time)