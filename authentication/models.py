from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password=password, **extra_fields)


class User(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

<<<<<<< HEAD
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, password=password, **extra_fields)

class location(models.Model):
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        return self.latitude + " " + self.longitude

class User(AbstractUser):
    email = models.EmailField(("email address"), unique=True)
    full_name = models.CharField(max_length=150, default="Default Name")
    latitude = models.CharField(max_length=50, default="0")
    longitude = models.CharField(max_length=50, default="0")
=======
    
    
    
class User(AbstractUser):
    email = models.EmailField(("email address"), unique=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
>>>>>>> 98af928bb2d038c90054482f1e354ee363899ce6
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']
    objects = MyAccountManager()
    

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/profile", default='static/images/profile.svg', blank=True, null=True)
<<<<<<< HEAD
    favorite_location = models.ManyToManyField(location, related_name='favorite_location', blank=True)
=======
   
>>>>>>> 98af928bb2d038c90054482f1e354ee363899ce6
    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
<<<<<<< HEAD
    if created and not hasattr(instance, 'userprofile'):
        User_Profile.objects.create(user=instance)
=======
    if created and not hasattr(instance, 'UserProfile'):
        User_Profile.objects.create(user=instance)
>>>>>>> 98af928bb2d038c90054482f1e354ee363899ce6
