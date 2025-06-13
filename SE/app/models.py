from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
"""
    用户表
    维护用户注册、登录、身份验证和权限管理
"""
class User(models.Model):
    username = models.CharField(max_length=20) # 用户名
    password = models.CharField(max_length=200) # 密码
    phone = models.CharField(max_length=20) # 电话号码
    age = models.IntegerField() # 年龄
    User_id = models.IntegerField(primary_key=True) # 用户id——主键
    permission = models.fields.IntegerField(default=0) # 权限——儿童为0，成人为1，工作人员为2

    def __str__(self):
        return self.username
    
    def get_permission(self):
        return self.permission
    
    # 修改密码
    def set_password(self, new_password):
        if not new_password: # 如果密码为空，则返回错误信息
            raise ValueError('密码不能为空！')
        self.password = make_password(new_password)

    def check_password(self, new_password):
        return check_password(new_password, self.password)

# 日志表，存储操作日志
class Log(models.Model):
    Log_id = models.IntegerField(primary_key=True) # 日志id——主键
    username = models.CharField(max_length=20) # 用户名
    devicename = models.CharField(max_length=50) # 设备名
    devicetype = models.CharField(max_length=20) # 设备类型
    timestamp = models.DateTimeField(auto_now_add=True) # 时间戳
    operation = models.CharField(max_length=200) # 操作类型
    
    # 日志号： 用户名 - 操作 - 设备名 at 时间
    def __str__(self):
        return f"{self.Log_id} : {self.username} {self.operation} {self.devicename} at {self.timestamp}"
    
    # 创建日志
    def create_Log(self, Log_id, username, devicename, devicetype, operation):
        self.Log_id = Log_id
        self.username = username
        self.devicename = devicename
        self.devicetype = devicetype
        self.operation = operation
        self.save()

    # 通过日志id查询日志
    def query_Log(self, Log_id):
        return Log.objects.get(Log_id=Log_id)
    
    # 通过用户名查询日志
    # 确保降序排序，即日志由近到远
    def query_Log_by_username(self, username):
        return Log.objects.filter(username=username).order_by('-timestamp')
    
    # 通过设备名查询日志
    def query_Log_by_devicename(self, devicename):
        return Log.objects.filter(devicename=devicename).order_by('-timestamp')
    
     # 通过时间戳查询日志
    @classmethod
    def query_Log_by_time_range(cls, start_time, end_time):
        return cls.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-timestamp')
    
class Device(models.Model):
    Device_id = models.IntegerField(primary_key=True) # 设备id——主键
    Device_name = models.CharField(max_length=20, unique=True) # 设备名
    Device_type = models.CharField(max_length=20)  # 设备类型
    Device_status = models.IntegerField(default=0) # 设备状态,0——关闭，1——打开、2——维护

    def __str__(self): 
        return self.Device_name
    
    # 打开设备
    def turn_on(self):
        self.Device_status = 1
        self.save()

    # 关闭设备
    def turn_off(self):
        self.Device_status = 0
        self.save()

    def set_status(self,status):
        if status not in [0, 1, 2]:
            raise ValueError('无效的状态值')
        self.Device_status = status
        self.save()

    # 设置名字
    def set_name(self, name):
        if not name: # 如果名字为空，则返回错误信息
            raise ValueError('设备名不能为空！')
        self.Device_name = name
        self.save()

    # 获取名字
    def get_name(self):
        return self.Device_name
    # 获取设备状态
    def get_status(self):
        return self.Device_status
    
    #  修改设备名
    def change_name(self, new_name):
        if not new_name: # 如果名字为空，则返回错误信息
            raise ValueError('设备名不能为空！')
        self.Device_name = new_name
        self.save()

    # 添加设备，接口
    def add_device(self, Device_id, Device_name, Device_type, Device_status=0):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_type not in ['Light', 'AirConditioner', 'Curtain', 'WashingMachine', 'RobotVacuum']:
            raise ValueError('设备类型无效！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        self.Device_id = Device_id
        self.Device_name = Device_name
        self.Device_type = Device_type
        self.Device_status = Device_status
        self.save()
        
    # 根据设备名获取设备
    def get_device(self, Device_name):
        return Device.objects.get(Device_name=Device_name)
    
    
# 灯
class Light(Device):
    # 亮度
    brightness = models.IntegerField(default=100)

    def __str__(self):
        return f"Light: {self.Device_name}"

    # 获取亮度
    def get_brightness(self):
        return self.brightness
    
    # 修改亮度
    def set_brightness(self, brightness):
        if brightness < 0 or brightness > 100: # 亮度只能是0-100
            raise ValueError('亮度只能是0-100')
        self.brightness = brightness
        self.save()

    # 添加设备
    def add_light(self, Device_id, Device_name, Device_status=0, brightness=50):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        if brightness < 0 or brightness > 100: # 亮度只能是0-100
            raise ValueError('亮度只能是0-100')
        self.add_device(Device_id, Device_name, 'Light', Device_status)
        self.brightness = brightness
        self.save()

# 空调
class AirConditioner(Device):
    temperature = models.IntegerField(default=25)
    mode = models.CharField(max_length=20, default='cool') #cool为制冷，heat为制热，dry为除湿

    def __str__(self):
        return f"AirConditioner: {self.Device_name}"
    
    # 获取亮度
    def get_temperature(self):
        return self.temperature
    
    # 获取模式
    def get_mode(self):
        return self.mode

    # 设置模式：cool,heat,dry
    def set_mode(self, new_mode):
        if new_mode not in ['cool', 'heat', 'auto', 'dry', 'fan']:
            raise ValueError('无效的模式！')
        self.mode = new_mode
        self.save()

    # 修改温度
    def set_temperature(self, temperature):
        if temperature < 16 or temperature > 30: # 温度只能是16-30
            raise ValueError('温度只能是16-30')
        self.temperature = temperature
        self.save()

    # 添加设备
    def add_airconditioner(self, Device_id, Device_name, Device_status, temperature=25, mode='cool'):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        if temperature < 16 or temperature > 30:
            raise ValueError('温度只能是16-30')
        self.add_device(Device_id, Device_name, 'AirConditioner', Device_status)
        self.temperature = temperature
        self.mode = mode
        self.save()

# 窗帘
class Curtain(Device):
    def __str__(self):
        return f"Curtain: {self.Device_name}"

    #  添加窗帘
    def add_curtain(self, Device_id, Device_name, Device_status):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        self.add_device(Device_id, Device_name, 'Curtain', Device_status)
        self.save()

# 洗衣机
class WashingMachine(Device):
    starttime = models.DateTimeField(auto_now_add=True, null=True) # 时间戳
    mode = models.CharField(max_length=20, default='wash') #wash为洗涤，dry为烘干,fastwash为快速洗涤

    def __str__(self):
        return f"WashingMachine: {self.Device_name}"
    
    # 获取模式
    def get_mode(self):
        return self.mode
    
    # 获取开始时间
    def get_starttime(self):
        return self.starttime
    
    # 设置开始时间
    def set_starttime(self, starttime):
        self.starttime = starttime
        self.save()

    # 设置模式：wash，dry,fastwash
    def set_mode(self, mode):
        if mode not in ['standard', 'quick', 'delicate', 'heavy', 'wool']:
            raise ValueError('无效的洗衣模式！')
        self.mode = mode
        self.save()
    
    # 添加设备
    def add_washingmachine(self, Device_id, Device_name, Device_status, mode='wash'):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        if mode not in ['standard', 'quick', 'delicate', 'heavy', 'wool']:
            raise ValueError('无效的洗衣模式！')
        self.add_device(Device_id, Device_name, 'WashingMachine', Device_status)
        self.mode = mode
        self.save()

# 扫地机器人
class Robotvacuum(Device):
    mode = models.CharField(max_length=20, default='clean') # sweep为清扫，mop为拖地
    starttime = models.DateTimeField(auto_now_add=True, null=True)
    sweeparea = models.IntegerField(default=0) # 扫过的区域
    electricity = models.IntegerField(default=100) # 剩余电量

    def __str__(self):
        return f"RobotVacuum: {self.Device_name}"
    
    # 获取模式
    def get_mode(self):
        return self.mode
    
    # 设置模式：sweep，mop
    def set_mode(self, mode):
        if mode not in ['auto', 'spot', 'edge', 'single_room', 'mop']:
            raise ValueError('无效的清扫模式！')
        self.mode = mode
        self.save()

    #  获取扫地时间
    def get_starttime(self):
        return self.starttime
    
    def set_starttime(self, starttime):
        self.starttime = starttime
        self.save()

    def get_sweeparea(self):
        return self.sweeparea
    
    def set_sweeparea(self, sweeparea):
        self.sweeparea = sweeparea

    def get_electricity(self):
        return self.electricity
    
    def set_electricity(self, electricity):
        self.electricity = electricity

    # 添加设备
    def add_robotvacuum(self, Device_id, Device_name, Device_status, mode='clean'):
        if not Device_name:
            raise ValueError('设备名不能为空！')
        if Device_status not in [0, 1, 2]: # 状态只能是0,1,2
            raise ValueError('设备状态无效！')
        if mode not in ['auto', 'spot', 'edge', 'single_room', 'mop']:
            raise ValueError('无效的清扫模式！')
        self.add_device(Device_id, Device_name, 'RobotVacuum', Device_status)
        self.mode = mode
        self.save()

"""
一名用户可以对应多条记录
一条记录维护该用户的常用设备
在view.py中实现一键开启和一键关闭逻辑
"""
class Habits(models.Model):
    habit_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    habitname = models.CharField(max_length=20, unique=True)
    devicename = models.CharField(max_length=20)
    devicetype = models.CharField(max_length=20)
    status = models.IntegerField(default=1)
    brightness = models.IntegerField(default=100, null=True)
    temperature = models.IntegerField(default=25, null=True)
    mode = models.CharField(max_length=20, default='cool', null=True) # 洗衣机、空调、扫地机

    def __str__(self):
        return self.habitname
    