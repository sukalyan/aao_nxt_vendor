"""aoo_nxt_vender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from . import views
import  aao_vender.restviews  as restviews

router = routers.DefaultRouter()
router.register(r'users', restviews.UserViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('aao_vender/', include('aao_vender.urls')),
    path('', views.main_login, name='main_login_index'),
    path('login/', views.main_login, name='main_login'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('error_page/', views.error_page, name='error_page'),
    path('api/', include(router.urls)),
    path('api/user_renew', restviews.UserRenewViewSet.as_view()),
    path('api/user_renew/', restviews.UserRenewViewSet.as_view()),
    path('api/userstatus', restviews.UserStatusViewSet.as_view()),
    path('api/userstatus/', restviews.UserStatusViewSet.as_view()),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
