from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class MyAccountManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = MyAccountManager()

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/profile", default='static/images/profile.svg', blank=True, null=True)
    favorite_location = models.ManyToManyField(location, related_name='favorite_location', blank=True)
    def __str__(self):
        return self.user.full_name



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        User_Profile.objects.create(user=instance)