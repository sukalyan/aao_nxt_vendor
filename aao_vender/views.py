from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import transection_fun,creat_remote_user,create_remote_user2

from datetime import date, timedelta

from django.utils import timezone
import pytz





@login_required(login_url='/login/')
def create_vender(request):


    if request.method == "GET":
        print("hello")
        form={'first_name': '','last_name':'','username':'','email':''}
        return render(request, 'vender/vender_form.html')

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        username = request.POST.get("username")
        email = request.POST.get("email")

        mobile_no = request.POST.get("mobile_no")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "confirm password missmatch")
            form={'first_name': first_name,'last_name': last_name,'username': username,'email':email,'mobile_no':mobile_no}

            return render(request, 'vender/vender_form.html',form )


        if User.objects.filter(email=email.lower()).exists():
            messages.error(request, "email alredy exist use another email")
            form={'first_name': first_name,'last_name': last_name,'username': username,'email':email,'mobile_no':mobile_no}

            return render(request, 'vender/vender_form.html',form )

        if User.objects.filter(username=username).exists():
            messages.error(request, "username alredy exist use another username")
            form={'first_name': first_name,'last_name': last_name,'username': username,'email':email,'mobile_no':mobile_no}

            return render(request, 'vender/vender_form.html',form )

        else:
            user = User.objects.create_user(
                                                first_name=first_name,
                                                last_name=last_name,
                                                username = username,
                                                password = password,
                                                email = email,
                                                is_active = True
                                            )
            user.save()

            vender = Vender_Details(vd_user=user,
                                    vd_mob_number=str(mobile_no),
                                    vd_is_active = True
                                )
            vender.save()


        profile_user = User.objects.get(username=username)
        print(profile_user.id)

        my_group = Group.objects.get(name='vender')

        profile_user.groups.add(my_group)

        messages.success(request, "vender created successfully.")

        return redirect('view_vender')




@login_required(login_url='/login/')
def view_vender(request):
    if request.method =='GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = users = User.objects.filter(
            groups__name='vender').count()

        query_results = User.objects.filter(
            groups__name='vender').order_by('date_joined')[:pagedata_ending]
        showingdata = query_results.count()


        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/vender_view.html', context)

@login_required(login_url='/login/')
def view_vender_pagination(request,page_number):
    if request.method =='GET':

        #query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20




        next_page_number = curent_page + 1

        totaldata = User.objects.filter(
            groups__name='vender').count()

        query_results = User.objects.filter(groups__name='vender').order_by(
            'date_joined')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()



        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/vender_view.html', context)



@login_required(login_url='/login/')
def vender_details(request, used_id):
    if request.method == 'GET':

        userexists = User.objects.filter(pk=used_id).exists()
        if userexists:
            user = User.objects.get(pk=used_id)
            vender_details = Vender_Details.objects.filter(vd_user=user)
            context = {"vender_details": vender_details
                       }
            #print(context)
            return render(request, 'vender/vender_dashboard.html', context)
        else:
            messages.error(request, "user not found.")
            return redirect('view_vender')

@login_required(login_url='/login/')
def vender_add_credit (request, used_id):
    if request.method == 'POST':

        userexists = User.objects.filter(pk=used_id).exists()
        if userexists:
            user = User.objects.get(pk=used_id)
            vender_details = Vender_Details.objects.get(vd_user=user)

            credit_amount = request.POST.get("credit_amount")

            credit_amount = request.POST.get("credit_amount")
            credit_amount = int(credit_amount)
            vender_details.vd_aao_balance = vender_details.vd_aao_balance + credit_amount
            vender_details.save()

            vender_details = Vender_Details.objects.filter(vd_user=user)
            context = {"vender_details": vender_details
                       }


            #print(context)
            return render(request, 'vender/vender_dashboard.html', context)
        else:
            messages.error(request, "user not found.")
            return redirect('view_vender')
    else:
        messages.error(request, "method not allowed")
        return redirect('view_vender')



@login_required(login_url='/login/')
def vender_add_plan (request, used_id):
    if request.method == 'POST':

        userexists = User.objects.filter(pk=used_id).exists()
        if userexists:
            user = User.objects.get(pk=used_id)
            vender_details = Vender_Details.objects.get(vd_user=user)

            vender_plan = request.POST.get("vender_plan")

            vender_details.vd_plan_subscribe = vender_plan
            vender_details.save()

            vender_details = Vender_Details.objects.filter(vd_user=user)
            context = {"vender_details": vender_details
                       }


            #print(context)
            return render(request, 'vender/vender_dashboard.html', context)
        else:
            messages.error(request, "user not found.")
            return redirect('view_vender')
    else:
        messages.error(request, "method not allowed")
        return redirect('view_vender')


@login_required(login_url='/login/')
def vender_add_per_user_price (request, used_id):
    if request.method == 'POST':

        userexists = User.objects.filter(pk=used_id).exists()
        if userexists:
            user = User.objects.get(pk=used_id)
            vender_details = Vender_Details.objects.get(vd_user=user)

            per_user_price = request.POST.get("per_user_price")
            per_user_price = int(per_user_price)
            vender_details.vd_per_user_price = per_user_price
            vender_details.save()


            vender_details = Vender_Details.objects.filter(vd_user=user)
            context = {"vender_details": vender_details
                       }

            #print(context)
            return render(request, 'vender/vender_dashboard.html', context)
        else:
            messages.error(request, "user not found.")
            return redirect('view_vender')
    else:
        messages.error(request, "method not allowed")
        return redirect('view_vender')





@login_required(login_url='/login/')
def create_aao_user(request):
    if request.method == "GET":
        current_user = request.user

        vender_details = Vender_Details.objects.filter(vd_user=current_user)

        context = {"vender_details":vender_details

                   }

        print("hello,create_aao_user")
        return render(request, 'vender/create_user_form.html',context)

    else:
        month=30
        current_user = request.user

        username = request.POST.get("username")
        email_id = request.POST.get("email_id")

        mobile_number = request.POST.get("mobile_number")
        package_categtory = request.POST.get("package_categtory")
        input_month = int(package_categtory)


        if Aoo_User_Details.objects.filter(aud_email=email_id.lower()).exists():
            messages.error(request, "email alredy exist use another email")
            form={'package_categtory': input_month,'username': username,'email_id':email_id,'mobile_number':mobile_number}

            return render(request, 'vender/create_user_form.html',form )

        if Aoo_User_Details.objects.filter(aud_mobile_number=mobile_number).exists():
            messages.error(request, "mobile number alredy exist use another mobile number")
            form={'package_categtory': input_month,'username': username,'email_id':email_id,'mobile_number':mobile_number}

            return render(request, 'vender/create_user_form.html',form )

        else:

            vender_details = Vender_Details.objects.get(vd_user=current_user)

            peruser_price = vender_details.vd_per_user_price
            remaining_balance = vender_details.vd_aao_balance
            vender_plan = vender_details.vd_plan_subscribe

            totalprice = peruser_price * input_month

            duration_in_days= month * input_month

            if  (remaining_balance - totalprice) <  0:
                messages.error(request, "you dont have enough credit ")
                form={'package_categtory': input_month,'username': username,'email_id':email_id,'mobile_number':mobile_number}
                return render(request, 'vender/create_user_form.html',form )




            #return_status = creat_remote_user(mobile_number,username,plan)
            return_status = create_remote_user2(mobile_number,username,vender_plan)

            if "success" in return_status:
                pass
            else:
                if "fail_server" in return_status:
                    messages.error(request, "error from aoonxt server or plan miss match ")
                    form={'package_categtory': input_month,'username': username,'email_id':email_id,'mobile_number':mobile_number}
                    return render(request, 'vender/create_user_form.html',form )
                else:
                    message_aao = "message from aoonxt server"+str(return_status)

                    messages.error(request,message_aao)
                    form={'package_categtory': input_month,'username': username,'email_id':email_id,'mobile_number':mobile_number}
                    return render(request, 'vender/create_user_form.html',form )



            start_date = str(timezone.now())
            end_date = str(timezone.now() + timezone.timedelta(days = duration_in_days))

            user_aao = Aoo_User_Details(
                                                aud_vender=current_user,
                                                aud_username=username,
                                                aud_email = email_id,
                                                aud_mobile_number = mobile_number,
                                                aud_subsc_package = input_month,
                                                aud_start_date= start_date,
                                                aud_end_date= end_date

                                            )
            user_aao.save()

            user_data={'username':username,
                      'email_id':email_id,
                      'mobile_number':mobile_number,
                      'totalmonth':input_month,
                      'start_date':start_date,
                      'end_date':end_date,
                      'peruser_price':peruser_price,
                      'remaining_balance':remaining_balance}

            result_tran = transection_fun(current_user,user_aao,totalprice,user_data)

            if result_tran:
                messages.success(request, "user subscription  created successfully.")
            else:

                messages.error(request, "something went wrong")


            return redirect('create_aao_user')


@login_required(login_url='/login/')
def view_aao_user(request):
    if request.method =='GET':
        current_user = request.user
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = Aoo_User_Details.objects.filter(
            aud_vender=current_user).count()

        query_results = Aoo_User_Details.objects.filter(
            aud_vender=current_user).order_by('aud_created_at')[:pagedata_ending]
        showingdata = query_results.count()


        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/aoo_user_view.html', context)


@login_required(login_url='/login/')
def view_aao_user_pagination(request,page_number):
    if request.method =='GET':
        current_user = request.user

        #query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20




        next_page_number = curent_page + 1

        totaldata = Aoo_User_Details.objects.filter(
            aud_vender=current_user).count()

        query_results = Aoo_User_Details.objects.filter(
            aud_vender=current_user).order_by('aud_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()



        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/aoo_user_view.html', context)



@login_required(login_url='/login/')
def vender_transection_view(request):
    if request.method =='GET':
        current_user = request.user
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = Vender_Transection_Details.objects.filter(
            vtd_vender=current_user).count()

        query_results = Vender_Transection_Details.objects.filter(
            vtd_vender=current_user).order_by('vtd_created_at')[:pagedata_ending]
        showingdata = query_results.count()


        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/vender_transection_view.html', context)


@login_required(login_url='/login/')
def vender_transection_view_pagination(request,page_number):
    if request.method =='GET':
        current_user = request.user

        #query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20


        next_page_number = curent_page + 1

        totaldata = Vender_Transection_Details.objects.filter(
            vtd_vender=current_user).count()

        query_results = Vender_Transection_Details.objects.filter(
            vtd_vender=current_user).order_by('vtd_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'vender/vender_transection_view.html', context)
