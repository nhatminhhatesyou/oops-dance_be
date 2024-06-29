from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.generics import ListAPIView
from django.http import HttpResponse
from .serializers import UserSerializer, ChangePasswordSerializer
import logging

from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    permission_classes
)

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request): 
    return HttpResponse("Welcome to OopsDanceStudio!")

@permission_classes([AllowAny])   
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
  
@permission_classes([AllowAny])   
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@permission_classes([AllowAny])   
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role,
                    'date_of_birth': user.date_of_birth,
                    'avatar_url': user.avatar.url if user.avatar else None
                        }
                })
        else:
            return Response({'message': "credentials don't match"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.check_password(data.get('old_password')):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        if data.get('new_password') != data.get('confirm_password'):
            return Response({"detail": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(data.get('new_password'))
        user.save()

        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = request.user
    return Response({
        'message': 'Token is valid',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
            'date_of_birth': user.date_of_birth,
            'avatar_url': user.avatar.url if user.avatar else None
        }
    })
    
@permission_classes([AllowAny])
class InstructorListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(role='instructor')
        instructor_id = self.request.query_params.get('id', None)
        if instructor_id is not None:
            queryset = queryset.filter(id=instructor_id)
        return queryset