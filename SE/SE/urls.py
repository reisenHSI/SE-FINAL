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
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/devices/', views.devices, name='devices'),
    path('home/add_delete/', views.add_delete, name='add_delete'),
    path('home/habits/', views.habits, name='habits'),
    path('home/query_logs/', views.query_Log, name='query_Log'),
    path('home/add_delete/add_device/', views.add_device, name='add_device'),
    path('home/add_delete/delete_device/', views.add_device, name='delete_device'),
    path('home/devices/light', views.light, name='light'),
    path('home/devices/curtain', views.curtain, name='curtain'),
    path('home/devices/washingMachine', views.washingMachine, name='washingMachine'),
    path('home/devices/robotvacuum', views.robotvacuum, name='robotvacuum'),
    path('home/devices/airConditioner', views.airConditioner, name='airConditioner'),
    path('home/habits/add_habit/', views.add_habit, name='add_habit'),
    path('home/habits/delete_habit/', views.delete_habit, name='delete_habit'),
]
