from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views

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
from rest_framework.exceptions import MethodNotAllowed
import http.client
import json
import requests
from config import *
from .utils import transection_fun,creat_remote_user,create_remote_user2
from django.utils import timezone


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

class UserRenewViewSet(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication,ApiAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer, XMLRenderer)
    
    def handle_exception(self, exc):
       
        if isinstance(exc, MethodNotAllowed):
            return Response({'status': 'Error',"data":"Method Not Allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({'status': 'Error',"data":"Authentication Failed"},status=status.HTTP_403_FORBIDDEN)
            
    
    def post(self, request, *args, **kwargs):
        aud_mobile_number = request.POST.get('aud_mobile_number',None)
        if aud_mobile_number is None:
            return Response({'status': 'Failed',"data":{"aud_mobile_number":{"This field is required."}}},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        try:
            user_details = Aoo_User_Details.objects.get(aud_vender= self.request.user,aud_mobile_number=aud_mobile_number)
            
        except Aoo_User_Details.DoesNotExist:
            return Response({'status': 'Failed',"data":{"aud_mobile_number":{aud_mobile_number+" User not found"}}},status=status.HTTP_400_BAD_REQUEST)
            
        vendor = Vender_Details.objects.get(vd_user=self.request.user)
        
       
        month=30
        input_month=1
        peruser_price = vendor.vd_per_user_price
        remaining_balance = vendor.vd_aao_balance
        vender_plan = vendor.vd_plan_subscribe
        totalprice = peruser_price * input_month        
        duration_in_days= month * input_month
        
        if (remaining_balance - totalprice) <  0:
            return Response({'status': 'Failed',"data":"Insufficiant Credit Balance"},status=status.HTTP_400_BAD_REQUEST)
        if (vender_plan is None) or (vender_plan==""):
            return Response({'status': 'Failed',"data":"Member Plan is not assigned yet, contact admin"})
        
        
        remotestatus = create_remote_user2(aud_mobile_number,user_details.aud_email,vender_plan)
        
        if "success" in remotestatus:
            
            if(remotestatus['success']==False):
                return Response({'status': 'Failed',"data":remotestatus['message']},status=status.HTTP_400_BAD_REQUEST)
            
        else:
            if "fail_server" in remotestatus:
                return Response({'status': 'Failed',"data":"Error From Aoonxt Server or Plan Missmatche"},status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError(remotestatus)
                
       
        
        last_order = Aoo_User_Order_Details.objects.filter(auod_user=user_details).order_by('-auod_created_at')[0]
        last_order_end_date = last_order.auod_end_date
       

        if last_order_end_date >= timezone.now():
            start_date = last_order_end_date + timezone.timedelta(days = 1)
        else:
            start_date = timezone.now()

        end_date = str(start_date + timezone.timedelta(days = duration_in_days))

        

        user_details.aud_subsc_package = input_month
        user_details.aud_start_date = start_date
        user_details.aud_end_date = end_date

        user_details.save()

        user_data={'username':user_details.aud_username,
                  'email_id':user_details.aud_email,
                  'mobile_number':aud_mobile_number,
                  'totalmonth':input_month,
                  'start_date':start_date,
                  'end_date':end_date,
                  'peruser_price':peruser_price,
                  'remaining_balance':remaining_balance}
        
        result_tran = transection_fun(self.request.user,user_details,totalprice,user_data,vender_plan)
        
        return Response({"status": "Success","data": remotestatus})

  
    
class UserStatusViewSet(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, ApiAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer, XMLRenderer)
    def handle_exception(self, exc):
        if isinstance(exc, MethodNotAllowed):
            return Response({'status': 'Error',"data":"Method Not Allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({'status': 'Error',"data":"Authentication Failed"},status=status.HTTP_403_FORBIDDEN)

    def post(self, request,format=None):
        aud_mobile_number = request.POST.get('aud_mobile_number',None)
        subscription = request.POST.get('subscription','')
        if aud_mobile_number is None:
            return Response({'status': 'Failed',"data":{"aud_mobile_number":{"This field is required."}}},status=status.HTTP_400_BAD_REQUEST)
        try:
            aao_user=Aoo_User_Details.objects.get(aud_vender= self.request.user,aud_mobile_number=aud_mobile_number)
        except Aoo_User_Details.DoesNotExist:
            return Response({'status': 'Failed',"data":{"aud_mobile_number":{aud_mobile_number+" User not found"}}},status=status.HTTP_400_BAD_REQUEST)
        try:
            url = conf['AAO_NXT_URL']+"users/outer_user"
           
            payload=json.dumps({
              "mobile": "+91"+aud_mobile_number,
              "subscription":subscription
            })
            
            headers = {              
              'auth_token': 'yZNqkApddadikAsRD3pW',
              'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            data=response.text
            res = json.loads(data)
            print(res)
            if(res.get('Status')):
                return Response({"status": "Success","data":res})  # Your overrid
            else:
                return Response({"status": "Failed","data":res})
        except Exception as e:
            return Response({"status": "Error","data":str(e)})
        
        
          
   
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
    
        if isinstance(exc, MethodNotAllowed):
            return Response({'status': 'Error',"data":"Method Not Allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        elif isinstance(exc, Http404):
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