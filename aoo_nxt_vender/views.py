from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('main_login')

@csrf_exempt
def main_login(request):

    if request.user.is_authenticated:
        user = request.user
        # groupid = user.groups.values_list('id', flat=True).first()
        # groupname = user.groups.values_list('name', flat=True).first()

        #2 project site_manager
        #3 project user
        context = {"user":user,"groupid":'groupid','groupname':'groupname'}
        return render(request,'home.html', context)

    if request.method == "GET":
        context = {"data":"data"}
        return render(request, 'index.html', context)

    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        email_id_exist = User.objects.filter(email=email.lower()).exists()
        if not(email_id_exist):
            context = {"user":"wp","index_try":"Y"}
            return render(request, 'index.html', context)

        username = User.objects.get(email=email.lower()).username

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)

            # groupid = user.groups.values_list('id', flat=True).first()
            # groupname = user.groups.values_list('name', flat=True).first()
            #
            # #2 project site_manager
            # #3 project user
            context = {"user":user,"groupid":'groupid','groupname':'groupname'}
            return render(request, 'home.html', context)

        else:
            context = {"user":"wp","login_try":"Y"}
            return render(request, 'index.html', context)

@csrf_exempt
def error_page(request):
    if request.method == "GET":
        context = {"data":"data"}
        return render(request, '404.html', context)
