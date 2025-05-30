from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    User_id = models.IntegerField(primary_key=True)
    permission = models.fields.IntegerField(default=0) #儿童为0，成人为1，工作人员为2
    def __str__(self):
        return self.username

class Log(models.Model):
    Log_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    devicename = models.CharField(max_length=20)
    devicetype = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.Log_id} : {self.username} - {self.deviceid} at {self.timestamp}"
    
    def create_Log(self, Log_id, username, devicename, devicetype):
        self.Log_id = Log_id
        self.username = username
        self.devicename = devicename
        self.devicetype = devicetype
        self.save()

    def query_Log(self, Log_id):
        return Log.objects.get(Log_id=Log_id)
    
    def query_Log_by_username(self, username):
        return Log.objects.filter(username=username)
    
    def query_Log_by_devicename(self, devicename):
        return Log.objects.filter(devicename=devicename)
    
    @classmethod
    def query_Log_by_time_range(cls, start_time, end_time):
        return cls.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)
    


class Device(models.Model):
    Device_id = models.IntegerField(primary_key=True)
    Device_name = models.CharField(max_length=20)
    Device_type = models.CharField(max_length=20)
    Device_user = models.CharField(max_length=20)
    Device_status = models.IntegerField(default=0)

    def __str__(self): 
        return self.Device_name
    
    def change_name(self, new_name):
        Device_name = new_name
        self.save()
    
class Light(Device):
    brightness = models.IntegerField(default=100)

    def __str__(self):
        return f"Light: {self.Device_name}"
    
    def turn_on(self):
        self.Device_status = 1
        self.save()

    def turn_off(self):
        self.Device_status = 0
        self.save()

    def change_brightness(self, brightness):
        self.brightness = brightness
        self.save()

class AirConditioner(Device):
    temperature = models.IntegerField(default=25)
    mode = models.CharField(max_length=20, default='cool') #cool为制冷，heat为制热，wet为除湿

    def __str__(self):
        return f"AirConditioner: {self.Device_name}"

    def turn_on(self):
        self.Device_status = 1
        self.save()

    def turn_off(self):
        self.Device_status = 0
        self.save()

    def cool(self):
        self.mode = 'cool'
        self.save()

    def heat(self):
        self.mode = 'heat'
        self.save()

    def wet(self):
        self.mode = 'wet'
        self.save()

    def change_temperature(self, temperature):
        self.temperature = temperature
        self.save()


class Curtain(Device):
    def __str__(self):
        return f"Curtain: {self.Device_name}"
    
    def turn_on(self):
        self.Device_status = 1
        self.save()

    def turn_off(self):
        self.Device_status = 0
        self.save()

class washingMachine(Device):
    mode = models.CharField(max_length=20, default='wash') #wash为洗涤，dry为烘干,fastwash为快速洗涤

    def __str__(self):
        return f"WashingMachine: {self.Device_name}"
    
    def turn_off(self):
        self.Device_status = 0
        self.save()

    def wash(self):
        self.Device_status = 1
        self.mode = 'wash'
        self.save()

    def dry(self):
        self.Device_status = 1
        self.mode = 'dry'
        self.save()

    def fastwash(self):
        self.Device_status = 1
        self.mode = 'fastwash'
        self.save()

class robotvaccum(Device):
    mode = models.CharField(max_length=20, default='clean') #sweep为清扫，mop为拖地

    def __str__(self):
        return f"RobotVaccum: {self.Device_name}"
    
    def sweep(self):
        self.Device_status = 1
        self.mode = 'sweep'
        self.save()

    def mop(self):
        self.Device_status = 1
        self.mode = 'mop'
        self.save()

    def turn_off(self):
        self.Device_status = 0
        self.save()