from django.db import models

# Create your models here.
"""
    用户表
    维护用户注册、登录、身份验证和权限管理
"""
class User(models.Model):
    username = models.CharField(max_length=20) # 用户名
    password = models.CharField(max_length=20) # 密码
    phone = models.CharField(max_length=20) # 电话号码
    User_id = models.IntegerField(primary_key=True) # 用户id——主键
    permission = models.fields.IntegerField(default=0) # 权限——儿童为0，成人为1，工作人员为2

    def __str__(self):
        return self.username
    
    # 根据传入的用户名，返回用户
    def get_user(self, username):
        user = User.objects.get(username=username)
        return user

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
    def query_Log_by_username(self, username):
        return Log.objects.filter(username=username)
    
    # 通过设备名查询日志
    def query_Log_by_devicename(self, devicename):
        return Log.objects.filter(devicename=devicename)
    
     # 通过时间戳查询日志
    @classmethod
    def query_Log_by_time_range(cls, start_time, end_time):
        return cls.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)
    
class Device(models.Model):
    Device_id = models.IntegerField(primary_key=True) # 设备id——主键
    Device_name = models.CharField(max_length=20) # 设备名
    Device_type = models.CharField(max_length=20)  # 设备类型
    Device_user = models.CharField(max_length=20) # 设备使用者
    Device_status = models.IntegerField(default=0) # 设备状态

    def __str__(self): 
        return self.Device_name
    
    #  修改设备名
    def change_name(self, new_name):
        self.Device_name = new_name
        self.save()

    # 添加设备，接口
    def add_device(self, Device_id, Device_name, Device_type, Device_user, Device_status):
        self.Device_id = Device_id
        self.Device_name = Device_name
        self.Device_type = Device_type
        self.Device_user = Device_user
        self.Device_status = Device_status
        self.save()
        
    # 根据设备名获取设备
    def get_device(self, Device_name):
        return Device.objects.get(Device_name=Device_name)
    
    # 获取设备状态
    def get_status(self):
        return self.Device_status
    
# 灯
class Light(Device):
    # 亮度
    brightness = models.IntegerField(default=100)

    def __str__(self):
        return f"Light: {self.Device_name}"
    
    # 开灯
    def turn_on(self):
        self.Device_status = 1
        self.save()

    # 关灯
    def turn_off(self):
        self.Device_status = 0
        self.save()

    # 修改亮度
    def change_brightness(self, brightness):
        self.brightness = brightness
        self.save()

    # 添加设备
    def add_light(self, Device_id, Device_name, Device_user, Device_status, brightness=50):
        self.add_device(Device_id, Device_name, 'Light', Device_user, Device_status)
        self.brightness = brightness
        self.save()

# 空调
class AirConditioner(Device):
    temperature = models.IntegerField(default=25)
    mode = models.CharField(max_length=20, default='cool') #cool为制冷，heat为制热，dry为除湿

    def __str__(self):
        return f"AirConditioner: {self.Device_name}"

    # 开空调
    def turn_on(self):
        self.Device_status = 1
        self.save()

    # 关空调
    def turn_off(self):
        self.Device_status = 0
        self.save()

    # 制冷
    def cool(self):
        self.mode = 'cool'
        self.save()

    # 制热
    def heat(self):
        self.mode = 'heat'
        self.save()

    # 除湿
    def dry(self):
        self.mode = 'dry'
        self.save()

    # 修改温度
    def change_temperature(self, temperature):
        self.temperature = temperature
        self.save()

    # 添加设备
    def add_airconditioner(self, Device_id, Device_name, Device_user, Device_status, temperature=25, mode='cool'):
        self.add_device(Device_id, Device_name, 'AirConditioner', Device_user, Device_status)
        self.temperature = temperature
        self.mode = mode
        self.save()

# 窗帘
class Curtain(Device):
    def __str__(self):
        return f"Curtain: {self.Device_name}"

    # 拉开窗帘 
    def turn_on(self):
        self.Device_status = 1
        self.save()

    # 关闭窗帘
    def turn_off(self):
        self.Device_status = 0
        self.save()

    #  添加窗帘
    def add_curtain(self, Device_id, Device_name, Device_user, Device_status):
        self.add_device(Device_id, Device_name, 'Curtain', Device_user, Device_status)
        self.save()

# 洗衣机
class washingMachine(Device):
    mode = models.CharField(max_length=20, default='wash') #wash为洗涤，dry为烘干,fastwash为快速洗涤

    def __str__(self):
        return f"WashingMachine: {self.Device_name}"
    
    # 开启
    def turn_on(self):
        self.Device_status = 1
        self.save()

    #  关闭
    def turn_off(self):
        self.Device_status = 0
        self.save()

    # 洗涤
    def wash(self):
        self.Device_status = 1
        self.mode = 'wash'
        self.save()

    # 烘干
    def dry(self):
        self.Device_status = 1
        self.mode = 'dry'
        self.save()

    # 快洗
    def fastwash(self):
        self.Device_status = 1
        self.mode = 'fastwash'
        self.save()
    
    # 添加设备
    def add_washingmachine(self, Device_id, Device_name, Device_user, Device_status, mode='wash'):
        self.add_device(Device_id, Device_name, 'WashingMachine', Device_user, Device_status)
        self.mode = mode
        self.save()

# 扫地机器人
class robotvaccum(Device):
    mode = models.CharField(max_length=20, default='clean') #sweep为清扫，mop为拖地

    def __str__(self):
        return f"RobotVaccum: {self.Device_name}"
    
    # 清扫
    def sweep(self):
        self.Device_status = 1
        self.mode = 'sweep'
        self.save()

    #  拖地
    def mop(self):
        self.Device_status = 1
        self.mode = 'mop'
        self.save()

    # 开机
    def turn_on(self):
        self.Device_status = 1
        self.save()

    # 关机
    def turn_off(self):
        self.Device_status = 0
        self.save()

    # 添加设备
    def add_robotvaccum(self, Device_id, Device_name, Device_user, Device_status, mode='clean'):
        self.add_device(Device_id, Device_name, 'RobotVaccum', Device_user, Device_status)
        self.mode = mode
        self.save()


"""
    一名用户对应一条记录
    一条记录维护该用户的常用设备
    在view.py中实现一键开启和一键关闭逻辑
"""
class habits(models.Model):
    username = models.CharField(max_length=20)
    habit = models.ManyToManyField(Device) # 常用设备列表

    def __str__(self):
        return f"{self.username}'s habit"
    
    #  用户添加习惯
    def add_favorite_device(self, device):
        if device.Device_user not in self.habit.all():
            self.habit.add(device)

    # 用户删除习惯
    def remove_favorite_device(self, device):
        if device in self.habit.all():
            self.habit.remove(device)

    # 获取所有常用设备
    def get_habit(self):
        return self.habit.all()

