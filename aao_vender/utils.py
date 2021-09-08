
from .models import *
import http.client
import json
import requests
from config import *


# user_data={'username':username,
#           'email_id':email_id,
#           'mobile_number':mobile_number,
#           'totalmonth':package_categtory,
#           'start_date':start_date,
#           'end_date':end_date,
#           'peruser_price':peruser_price,
#           'remaining_balance':remaining_balance}
#
# result_tran = transection_fun(current_user,user_aao,totalprice,user_data)
#
# class Aoo_User_Order_Details(models.Model):
#     auod_id = models.AutoField(auto_created=True, primary_key=True,)
#     auod_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_vender')
#     auod_user = models.ForeignKey(Aoo_User_Details, on_delete=models.CASCADE, related_name='%(class)s_user')
#     auod_subsc_package = models.PositiveIntegerField( default=1, null=True)
#     auod_start_date = models.DateTimeField(blank=True)
#     auod_end_date = models.DateTimeField(blank=True)
#     auod_created_at = models.DateTimeField(auto_now_add=True)
#     auod_last_modified_on = models.DateTimeField(auto_now=True)
#     auod_is_active = models.BooleanField(default=True)
#
#
# class Vender_Transection_Details(models.Model):
#     vtd_id = models.AutoField(auto_created=True, primary_key=True,)
#     vtd_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_vender')
#     vtd_debit = models.PositiveIntegerField( default=0 )
#     vtd_total_remaining = models.PositiveIntegerField( default=0 )
#     vtd_trans_for = models.ForeignKey(Aoo_User_Order_Details, on_delete=models.CASCADE, related_name='%(class)s_trans_for')
#     vtd_created_at = models.DateTimeField(auto_now_add=True)
#     vtd_last_modified_on = models.DateTimeField(auto_now=True)
#     vtd_is_active = models.BooleanField(default=True)
#
#
def creat_remote_user(mobile_number,username,plan):
    try:
        mobile_number="+91"+str(mobile_number)
        plan="kaliaa"

        conn = http.client.HTTPSConnection("0.0.0.0", 8000)
        payload = {"name":username,"mobile":mobile_number,"plan":str(plan)}
        headers = {
          'accept': 'application/json',
          'aao_token': 'yZNqkApikAsRD3pW',
          'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        conn.request("POST", "/users/outerapi", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return_data_api=data.decode("utf-8")
        print(return_data_api,'response from api aoonxt')
        return return_data_api

    except Exception as e:
        return {"fail_server":"servererror"}


def create_remote_user2(mobile_number,username,plan):
    try:
        url = conf['AAO_NXT_URL']+"users/outerapi"
        
        payload='''{"name":"'''+username +'''","mobile":"+91'''+mobile_number+'''","plan":"'''+plan+'''"}'''
        print('payload----------',payload)
        headers = {
          'accept': 'application/json',
          'aao_token': 'yZNqkApikAsRD3pW',
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data=response.text
        res = json.loads(data)
        return res
        
    except Exception as e:
        return {"fail_server":"servererror"}





def transection_fun(vender,user_aao,totalprice,user_data):

    user_aao_order = Aoo_User_Order_Details(auod_vender=vender,
                                            auod_user=user_aao,
                                            auod_subsc_package = user_data['totalmonth'],
                                            auod_start_date = user_data['start_date'],
                                            auod_end_date = user_data['end_date']
                                            )
    user_aao_order.save()

    vtd_total_remaining_calculated = user_data['remaining_balance'] - totalprice




    user_aao_order = Vender_Transection_Details(
                                        vtd_vender=vender,
                                        vtd_debit = totalprice,
                                        vtd_total_remaining = vtd_total_remaining_calculated,
                                        vtd_trans_for = user_aao_order,

                                    )
    user_aao_order.save()



    vender_details = Vender_Details.objects.get(vd_user=vender)
    vender_details.vd_aao_balance = vtd_total_remaining_calculated
    vender_details.vd_aao_user = vender_details.vd_aao_user + 1
    vender_details.save()

    return True

    # except Exception as e:
    #     print(str(e),"something error happened")
    #     return False

