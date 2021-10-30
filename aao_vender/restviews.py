from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import UserSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed


class ApiAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        API_KEY = request.META.get('HTTP_API_KEY')
        
        API_SECRET = request.META.get('HTTP_API_SECRET')
        
        if not API_KEY or not API_SECRET:
            raise exceptions.AuthenticationFailed('Missing API_SECRATE/API_SECRET')

        try:
            vendor = Vender_Details.objects.get(vd_api_key=API_KEY,vd_api_secrate=API_SECRET)
            user=vendor.vd_user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Authentication Failed')
        except Vender_Details.DoesNotExist:
            raise exceptions.AuthenticationFailed('Authentication Failed')

        return (user, None)

class UserStatusViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, ApiAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserStatusSerializer
    queryset=Aoo_User_Details.objects.all().order_by('-aud_id')
    renderer_classes = (JSONRenderer, XMLRenderer)
    
    def handle_exception(self, exc):
        
        if isinstance(exc, Http404):
            return Response({'status': 'Failed',"data":"No Record Found"},status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exc, AuthenticationFailed):
            return Response({'status': 'Error',"data":exc.detail},status=status.HTTP_403_FORBIDDEN)
            
        elif isinstance(exc, ValidationError):
            return Response({'status': 'Failed',"data":exc.detail},status=status.HTTP_400_BAD_REQUEST)
            
    def retrieve(self, request, *args, **kwargs):
        response_data=super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return Response({"status": "Success","data":response_data.data})  # Your overrid  
        
    def get_queryset(self):       
        return Aoo_User_Details.objects.filter(aud_vender= self.request.user).order_by('-aud_id')
        

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [SessionAuthentication, ApiAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=Aoo_User_Details.objects.all().order_by('-aud_id')
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, XMLRenderer)
    
    def handle_exception(self, exc):
        
        if isinstance(exc, Http404):
            return Response({'status': 'Failed',"data":"No Record Found"},status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exc, AuthenticationFailed):
            return Response({'status': 'Error',"data":exc.detail},status=status.HTTP_403_FORBIDDEN)
            
        elif isinstance(exc, ValidationError):
            return Response({'status': 'Failed',"data":exc.detail},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        
        response_data=super(UserViewSet, self).create(request, *args, **kwargs)
        return Response({"status": "Success","data": response_data.data})   # Your overrid
        
        
    def list(self, request, *args, **kwargs):
        response_data=super(UserViewSet, self).list(request, *args, **kwargs)
        return Response({"status": "Success","data":response_data.data})  # Your overrid
    
    def retrieve(self, request, *args, **kwargs):
        response_data=super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return Response({"status": "Success","data":response_data.data})  # Your overrid
    
    def get_queryset(self):
       
        return Aoo_User_Details.objects.filter(aud_vender= self.request.user).order_by('-aud_id')