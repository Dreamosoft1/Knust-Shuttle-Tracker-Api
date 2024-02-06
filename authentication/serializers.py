from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User_Profile
        fields = ['image']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password', 'email', 'phone_number','first_name', 'last_name', 'student_number')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
            if not validated_data.get('email').endswith('@st.knust.edu.gh'):
                raise serializers.ValidationError('Invalid email')
            else:
                email = validated_data.get('email')
                username_from_email = email.split('@')[0]
                if username_from_email == validated_data.get('username'):
                    user = User.objects.create(**validated_data)
                    user.set_password(user.password)
                    user.is_active = True
                    user.save()
                    return user
                else:
                    raise serializers.ValidationError('Invalid email or username')
                
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)               
                
class FullUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='user_profile')
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone_number', 'profile', 'username']
