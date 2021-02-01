from django.shortcuts import render
from .models import User
import jwt
from rest_framework import generics,status
from .serializers import RegisterSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from .utils import Util



from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from .renderers import UserRenderer
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True )
        serializer.save()
        user_data = serializer.data
        
        user=User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain     
        relativeLink = reverse('verify-email' )
        absurl='http://' + current_site+relativeLink+"?token="+ str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email address ' + absurl
        data = {
            'email_body': email_body,
            'email_receipient': user.email,
            'email_subject':'Verify your email'
        }
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):

    def post(self, request):
        serializer_class=LoginSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


