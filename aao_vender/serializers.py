from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from .utils import transection_fun,creat_remote_user,create_remote_user2
from django.utils import timezone
from rest_framework.response import Response


    
   
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    aud_username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=Aoo_User_Details.objects.all(),message="Username Already Exist In System")]
            )
    aud_email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Aoo_User_Details.objects.all(),message="Email Id Already Exist In System")]
            )
    aud_mobile_number = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=Aoo_User_Details.objects.all(),message="Mobile Number Already Exist In System")]
            )
    class Meta:
        model = Aoo_User_Details
        fields = ['aud_id','aud_username', 'aud_email', 'aud_mobile_number']
    
    
    
    def create(self,validated_data):
        username = validated_data['aud_username']
        email = validated_data['aud_email']
        mobile = validated_data['aud_mobile_number']
        
        user = None   
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        vendor = Vender_Details.objects.get(vd_user=user)
        
        month=30
        input_month=1
        peruser_price = vendor.vd_per_user_price
        remaining_balance = vendor.vd_aao_balance
        vender_plan = vendor.vd_plan_subscribe

        totalprice = peruser_price * input_month
        
        duration_in_days= month * input_month
        if (remaining_balance - totalprice) <  0:
            raise serializers.ValidationError({"detail":"Insufficiant Credit Balance"})
        if (vender_plan is None) or (vender_plan==""):
            raise serializers.ValidationError({"detail":"Member Plan is not assigned yet, contact admin"})
        
        remotestatus = create_remote_user2(mobile,username,vender_plan)
        print(remotestatus)
        if "success" in remotestatus:
            pass
        else:
            if "fail_server" in remotestatus:
                raise serializers.ValidationError({"detail":"Error From Aoonxt Server or Plan Missmatche"})
            else:
                raise serializers.ValidationError(remotestatus)
        start_date = str(timezone.now())
        end_date = str(timezone.now() + timezone.timedelta(days = duration_in_days))
        
        user_aao = Aoo_User_Details(
                        aud_vender=user,
                        aud_username=username,
                        aud_email = email,
                        aud_mobile_number = mobile,
                        aud_subsc_package = input_month,
                        aud_start_date= start_date,
                        aud_end_date= end_date

                    )
        user_aao.save()
        
        
        user_data={'username':username,
                      'email_id':email,
                      'mobile_number':mobile,
                      'totalmonth':input_month,
                      'start_date':start_date,
                      'end_date':end_date,
                      'peruser_price':peruser_price,
                      'remaining_balance':remaining_balance}
        
        result_tran = transection_fun(user,user_aao,totalprice,user_data,vender_plan)
        
        return validated_data
