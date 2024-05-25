from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from .serializers import UserSerializer
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to OopsDanceStudio!")

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': token.user_id})
        else:
            return Response({'message': "credentials don't match"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = request.user
    logger.info(f"User: {user}")
    return Response({
        'message': 'Token is valid',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
        }
    })