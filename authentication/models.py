from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(("email address"), unique=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    student_number = models.CharField(max_length=19, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']
    

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/profile", default='static/images/profile.svg', blank=True, null=True)
   
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'UserProfile'):
        User_Profile.objects.create(user=instance)