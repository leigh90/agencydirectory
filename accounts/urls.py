from django.urls import path,include
from .views import RegisterAPIView, LoginAPIView, VerifyEmail


from .import views

urlpatterns = [
   
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', RegisterAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email')


] 