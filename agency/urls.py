from django.urls import path,include
from .views import AgencyListApiView, AgencyDetailView


from .import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('',  AgencyListApiView.as_view()),
    path('agencydetails/<int:pk>', AgencyDetailView.as_view()),
    

]