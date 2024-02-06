from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework import generics, status
from django.contrib.auth import logout
from rest_framework.permissions import AllowAny, IsAuthenticated

@api_view(["GET"])
def get_user_token(request):
    user = request.user

    # Check if a token already exists for the user
    token, created = Token.objects.get_or_create(user=user)
    key = token.key
    user = token.user.username
    return Response({'key':key,"user":user})

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(email=request.data['email'])
            token, _ = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        return response

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            if user.is_active == False:
                raise AuthenticationFailed(detail="User is not verified")
        except User.DoesNotExist:
            raise AuthenticationFailed(detail="Invalid email")
        email = email
        username_from_email = email.split('@')[0]
        user = User.objects.get(email=email)
        if username_from_email == user.username:
            if not email.endswith('@st.knust.edu.gh'):
                raise serializers.ValidationError('Invalid email')
            user = authenticate(username=email, password=password)
            if user is None:
                raise AuthenticationFailed(detail="Invalid password")
        else:
            raise AuthenticationFailed(detail="Invalid email")
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = FullUserSerializer
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)
