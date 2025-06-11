from django.contrib import admin
from .models import User, Log, Device, Light, AirConditioner, Curtain, WashingMachine, Robotvacuum, Habits

# Register your models here.


# 注册 User 模型
@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('User_id', 'username', 'phone', 'age', 'permission') # 在列表页显示这些字段
    search_fields = ('username', 'phone') # 添加搜索框，可按用户名和电话搜索
    list_filter = ('permission', 'age') # 添加筛选器，可按权限和年龄筛选
    ordering = ('User_id',) # 按用户 ID 排序

# 注册 Log 模型
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('Log_id', 'username', 'devicename', 'devicetype', 'timestamp', 'operation')
    search_fields = ('username', 'devicename', 'operation')
    list_filter = ('timestamp', 'operation')
    ordering = ('-timestamp',) # 按时间戳降序排列

# 注册 Device 模型
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_type', 'Device_status')
    search_fields = ('Device_name', 'Device_type')
    list_filter = ('Device_status',)
    ordering = ('Device_id',)

# 注册 Light 模型
@admin.register(Light)
class LightAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_status', 'brightness')
    search_fields = ('Device_name',)
    list_filter = ('Device_status',)
    rdering = ('Device_id',)

# 注册 AirConditioner 模型
@admin.register(AirConditioner)
class AirConditionerAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_status', 'temperature', 'mode')
    search_fields = ('Device_name',)
    list_filter = ('Device_status', 'mode')
    ordering = ('Device_id',)

# 注册 Curtain 模型
@admin.register(Curtain)
class CurtainAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_status')
    search_fields = ('Device_name',)
    list_filter = ('Device_status',)
    ordering = ('Device_id',)

@admin.register(WashingMachine)
class WashingMachineAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_status', 'mode')
    search_fields = ('Device_name',)
    list_filter = ('Device_status', 'mode')
    ordering = ('Device_id',)
    readonly_fields = ('Device_id',)

# 注册 Robotvacuum 模型
@admin.register(Robotvacuum)
class RobotvacuumAdmin(admin.ModelAdmin):
    list_display = ('Device_id', 'Device_name', 'Device_status', 'mode')
    search_fields = ('Device_name',)
    list_filter = ('Device_status', 'mode')
    ordering = ('Device_id',)
    readonly_fields = ('Device_id',)

# 注册 Habits 模型
@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = ('habit_id', 'username', 'habit_name')
    search_fields = ('username', 'habit_name')
    filter_horizontal = ('favorite_devices',)  # 优化多对多字段的显示
    ordering = ('habit_id',)
    readonly_fields = ('habit_id',)