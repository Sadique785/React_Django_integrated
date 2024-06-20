from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework.views import APIView




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)        
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')



        if not username or not password:
            return Response({"error": "username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        

        if user is None:
            return Response({"error": "Invalid email address or password."}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)

        return Response({'status': 'Successfully logged in.'}, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data.get('email')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return Response({'error':'Email and Password are required'}, status = status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email = email).exists():
            return Response({'error': 'USer already exists'}, status = status.HTTP_400_BAD_REQUEST)
        
        # user = User.objects.create(username = username, email = email, password =password, first_name=first_name, last_name=last_name)
        serializer = RegisterSerializer(data = data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
