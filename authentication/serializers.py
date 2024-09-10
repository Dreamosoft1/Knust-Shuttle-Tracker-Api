from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, login #noqa
from rest_framework.exceptions import AuthenticationFailed #noqa
from django.core.validators import RegexValidator 
from rest_framework.authtoken.models import Token 
from .utils import OTPUtils
from .email import send_email
class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User_Profile
        fields = ["image"]

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17, required=False)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "id"]

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate(self, attrs):
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError("Email is required")
        return attrs
    
    def create(self, validated_data):
        email = validated_data.get("email")
        try:
            user = User.objects.filter(email=email).first()
            if user:
                code, token = OTPUtils.generate_otp(user)
                subject = "Password reset"
                message = f"Your OTP code is {code}"
                send_email(subject, message, email)
            else:
                raise serializers.ValidationError("User not found")   
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return {"message": "OTP sent successfully", "token": token} 
    
class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def create(self, validated_data):
        otp = validated_data.get("otp")
        password = validated_data.get("password")
        token = validated_data.get("token")

        data = OTPUtils.decode_token(token)
        if not data or not isinstance(data, dict):
            raise serializers.ValidationError("Invalid token")
        user = User.objects.filter(id=data.get("user_id")).first()
        if not user:
            raise serializers.ValidationError("User does not exist")
        if not OTPUtils.verify_otp(otp, data["secret"]):
            raise serializers.ValidationError("Invalid OTP")
        user.set_password(password)
        user.save()
    
        
 
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","password", "email","full_name")
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
            if not validated_data.get("email").endswith("@st.knust.edu.gh"):
                raise serializers.ValidationError("Invalid email")
            else:
                email = validated_data.get("email")
                username_from_email = email.split("@")[0]
                if username_from_email == validated_data.get("username"):
                    user = User.objects.create(**validated_data)
                    user.set_password(user.password)
                    user.is_active = True
                    user.save()
                    return user
                else:
                    raise serializers.ValidationError("Invalid email or username")
                
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)               
                
class FullUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="user_profile")
    
    class Meta:
        model = User
        fields = ["id","full_name", "email", "profile", "username"]

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="user_profile")

    class Meta:
        model = User
        fields = ["full_name", "profile"]

    def update(self, instance, validated_data):
        # Update the User instance
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.save()

        # Update the UserProfile instance
        profile_data = validated_data.pop("user_profile", None)
        if profile_data:
            # Assuming "user_profile" is a OneToOneField relation to the User model
            profile = instance.user_profile
            profile_serializer = UserProfileSerializer(instance=profile, data=profile_data, partial=True)
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data