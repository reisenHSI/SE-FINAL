"""SE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
import app.views as views

urlpatterns = [
    # 确保空路径跳转login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # 管理员入口
    path('admin/', admin.site.urls),
    
    # 认证入口（流程图起点）
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    
    # 主控制台（login指向的唯一入口）
    path('home/', views.home, name='home'),
    
    # 设备控制分支（devices下级）
    path('home/devices/', views.devices, name='devices'),
    path('home/devices/light/', views.light, name='light'),
    path('home/devices/curtain/', views.curtain, name='curtain'),
    path('home/devices/airConditioner/', views.airConditioner, name='airConditioner'),
    path('home/devices/washingMachine/', views.washingMachine, name='washingMachine'),
    path('home/devices/robotvacuum/', views.robotvacuum, name='robotvacuum'),
    
    # 设备管理分支（add_delete下级）
    path('home/add_delete/', views.add_delete, name='add_delete'),
    path('home/add_delete/add_device/', views.add_device, name='add_device'),
    path('home/add_delete/delete_device/', views.delete_device, name='delete_device'),  # 修正了视图函数
    
    # 日志查询（直接来自home）
    path('home/query_logs/', views.query_logs, name='query_logs'),  # 统一使用小写
    
    # 习惯管理分支（habits下级）
    path('home/habits/', views.habits, name='habits'),
    path('home/habits/add_habit/', views.add_habit, name='add_habit'),
    path('home/habits/delete_habit/', views.delete_habit, name='delete_habit'),
]
