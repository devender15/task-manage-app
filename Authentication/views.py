from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

from .serializers import *
from .renderers import *


# Create your views here.

User = get_user_model()

# generate token manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):

    serializer_class = LoginSerializer
    renderer_classes = [UserJsonRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = authenticate(email=email, password=password)

        if(user is not None):
            token = get_tokens_for_user(user)
            return Response({'token': token,'success': 'Login Successfull !'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_field_errors': 'Email or password is not valid !'}}, status=status.HTTP_404_NOT_FOUND)
            

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    renderer_classes = [UserJsonRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": serializer.data,
            "token": token,
            "message": "Account successfully created !"
        }, status=status.HTTP_201_CREATED)

class UserDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserJsonRenderer]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)