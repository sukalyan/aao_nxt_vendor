from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vender_Details(models.Model):
    vd_id = models.AutoField(auto_created=True, primary_key=True,)
    vd_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    vd_mob_number = models.TextField(max_length=20, default=None)
    vd_aao_user = models.PositiveIntegerField( default=0, null=True)
    #number of user creted by this vender
    vd_aao_balance = models.PositiveIntegerField( default=0, null=True)
    vd_plan_subscribe = models.TextField(max_length=200, default=None, null=True)
    vd_per_user_price = models.PositiveIntegerField( default=100, null=True)
    vd_created_at = models.DateTimeField(auto_now_add=True)
    vd_last_modified_on = models.DateTimeField(auto_now=True)
    vd_is_active = models.BooleanField(default=True)
    vd_api_key = models.TextField(max_length=255, default=None)
    vd_api_secrate = models.TextField(max_length=255, default=None)

class Aoo_User_Details(models.Model):
    aud_id = models.AutoField(auto_created=True, primary_key=True,)
    aud_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    aud_username = models.TextField(max_length=5000, default=None)
    aud_email = models.TextField(max_length=5000, default=None)
    aud_mobile_number = models.TextField(max_length=20, default=None)
    aud_subsc_package = models.PositiveIntegerField( default=1, null=True)
    aud_start_date = models.DateTimeField(blank=True)
    aud_end_date = models.DateTimeField(blank=True)
    aud_created_at = models.DateTimeField(auto_now_add=True)
    aud_last_modified_on = models.DateTimeField(auto_now=True)
    aud_is_active = models.BooleanField(default=True)


class Aoo_User_Order_Details(models.Model):
    auod_id = models.AutoField(auto_created=True, primary_key=True,)
    auod_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_vender')
    auod_user = models.ForeignKey(Aoo_User_Details, on_delete=models.CASCADE, related_name='%(class)s_user')
    auod_subsc_package = models.PositiveIntegerField( default=1, null=True)
    auod_start_date = models.DateTimeField(blank=True)
    auod_end_date = models.DateTimeField(blank=True)
    auod_created_at = models.DateTimeField(auto_now_add=True)
    auod_last_modified_on = models.DateTimeField(auto_now=True)
    auod_is_active = models.BooleanField(default=True)

class Vender_Transection_Details(models.Model):
    vtd_id = models.AutoField(auto_created=True, primary_key=True,)
    vtd_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_vender')
    vtd_debit = models.PositiveIntegerField( default=0 )
    vtd_total_remaining = models.PositiveIntegerField( default=0 )
    vtd_trans_for = models.ForeignKey(Aoo_User_Order_Details, on_delete=models.CASCADE, related_name='%(class)s_trans_for')
    vtd_created_at = models.DateTimeField(auto_now_add=True)
    vtd_last_modified_on = models.DateTimeField(auto_now=True)
    vtd_is_active = models.BooleanField(default=True)


class Admin_Ading_Credit (models.Model):
    adc_id = models.AutoField(auto_created=True, primary_key=True,)
    adc_vender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_vender')
    adc_credit_amount = models.PositiveIntegerField( default=0, null=True)
    adc_created_at = models.DateTimeField(auto_now_add=True)
    adc_last_modified_on = models.DateTimeField(auto_now=True)
    adc_is_active = models.BooleanField(default=True)
