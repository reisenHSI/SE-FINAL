from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
"""
    用户表
    维护用户注册、登录、身份验证和权限管理
"""
class User(models.Model):
    username = models.CharField(max_length=20) # 用户名
    password = models.CharField(max_length=20) # 密码
    phone = models.CharField(max_length=20) # 电话号码
    age = models.IntegerField(max_length=3) # 年龄
    User_id = models.IntegerField(primary_key=True) # 用户id——主键
    permission = models.fields.IntegerField(default=0) # 权限——儿童为0，成人为1，工作人员为2

    def __str__(self):
        return self.username
    
    # 修改密码
    def set_password(self, new_password):
        self.password = new_password

    def check_password(self, new_password):
        return check_password(new_password, self.password)

# 日志表，存储操作日志
class Log(models.Model):
    Log_id = models.IntegerField(primary_key=True) # 日志id——主键
    username = models.CharField(max_length=20) # 用户名
    devicename = models.CharField(max_length=20) # 设备名
    devicetype = models.CharField(max_length=20) # 设备类型
    timestamp = models.DateTimeField(auto_now_add=True) # 时间戳
    operation = models.CharField(max_length=20) # 操作类型
    
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
        self.Device_status = status
        self.save()

    # 设置名字
    def set_name(self, name):
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
        self.Device_name = new_name
        self.save()

    # 添加设备，接口
    def add_device(self, Device_id, Device_name, Device_type, Device_status=0):
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
        self.brightness = brightness
        self.save()

    # 添加设备
    def add_light(self, Device_id, Device_name, Device_status=0, brightness=50):
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
        self.mode = new_mode
        self.save()

    # 修改温度
    def set_temperature(self, temperature):
        self.temperature = temperature
        self.save()

    # 添加设备
    def add_airconditioner(self, Device_id, Device_name, Device_status, temperature=25, mode='cool'):
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
        self.add_device(Device_id, Device_name, 'Curtain', Device_status)
        self.save()

# 洗衣机
class WashingMachine(Device):
    mode = models.CharField(max_length=20, default='wash') #wash为洗涤，dry为烘干,fastwash为快速洗涤

    def __str__(self):
        return f"WashingMachine: {self.Device_name}"
    
    # 获取模式
    def get_mode(self):
        return self.mode

    # 设置模式：wash，dry,fastwash
    def set_mode(self, mode):
        self.mode = mode
        self.save()
    
    # 添加设备
    def add_washingmachine(self, Device_id, Device_name, Device_status, mode='wash'):
        self.add_device(Device_id, Device_name, 'WashingMachine', Device_status)
        self.mode = mode
        self.save()

# 扫地机器人
class Robotvacuum(Device):
    mode = models.CharField(max_length=20, default='clean') #sweep为清扫，mop为拖地

    def __str__(self):
        return f"RobotVacuum: {self.Device_name}"
    
    # 获取模式
    def get_mode(self):
        return self.mode
    
    # 设置模式：sweep，mop
    def set_mode(self, mode):
        self.mode = mode
        self.save()

    # 添加设备
    def add_robotvacuum(self, Device_id, Device_name, Device_status, mode='clean'):
        self.add_device(Device_id, Device_name, 'RobotVacuum', Device_status)
        self.mode = mode
        self.save()

"""
一名用户可以对应多条记录
一条记录维护该用户的常用设备
在view.py中实现一键开启和一键关闭逻辑
"""
class Habits(models.Model):
    habit_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    habit_name = models.CharField(max_length=20)
    favorite_devices = models.ManyToManyField(Device) # 常用设备列表

    def __str__(self):
        return self.habit_name
    
    #  用户添加习惯
    def add_favorite_device(self, device):
        if device not in self.favorite_devices.all():
            self.favorite_devices.add(device)

    # 用户删除习惯
    def remove_favorite_device(self, device):
        if device in self.favorite_devices.all():
            self.favorite_devices.remove(device)

    # 获取当前habit的所有常用设备
    def get_habits(self):
        return self.favorite_devices.all()
    
