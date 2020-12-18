from django.shortcuts import render
from .models import Agency
from .serializers import AgencySerializer
from rest_framework.decorators import api_view
# class view imports
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
# authentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly



class AgencyListApiView(APIView):
    '''
    List all agencies OR create an agency 
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgencyDetailView(APIView):
    '''
    View details of individual agencies, updated and delete agencies  
    '''
    def get_object(self, pk):
        try:
            return Agency.objects.get(pk=pk)
        except Agency.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        agency = self.get_object(pk)
        serializer = AgencySerializer(agency)
        return Response(serializer.data)

    def put(self, request,pk,format=None):
        agency = self.get_object(pk)
        serializer = AgencySerializer(agency,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)