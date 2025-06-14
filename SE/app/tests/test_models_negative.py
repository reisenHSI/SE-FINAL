from django.test import TestCase
from django.utils import timezone
from ..models import*

# User 模型负向测试
class UserModelNegativeTest(TestCase):
    def test_set_password_empty(self):
        user = User.objects.create(username='Bob', password='123456', phone='9876543210', age=30, User_id=2)
        with self.assertRaises(ValueError):
            user.set_password('')

    def test_check_password_wrong_format(self):
        user = User.objects.create(username='Charlie', password='123456', phone='9876543210', age=30, User_id=3)
        self.assertFalse(user.check_password('short'))

# Device 模型负向测试
class DeviceModelNegativeTest(TestCase):
    def test_turn_on_invalid_status(self):
        device = Device.objects.create(Device_id=8, Device_name="InvalidDevice", Device_type="Generic", Device_status=0)
        with self.assertRaises(ValueError):
            device.set_status(3)  # 假设设备状态应在 0 到 2 之间

    def test_change_name_empty(self):
        device = Device.objects.create(Device_id=9, Device_name="DeviceToRename", Device_type="Generic", Device_status=1)
        with self.assertRaises(ValueError):
            device.change_name('')  # 设备名称不能为空

# Light 模型负向测试
class LightModelNegativeTest(TestCase):
    def test_set_brightness_out_of_range(self):
        light = Light.objects.create(Device_id=10, Device_name="Light1", Device_type="Light", Device_status=1, brightness=50)
        with self.assertRaises(ValueError):
            light.set_brightness(110)  # 假设亮度应在 0 到 100 之间

# AirConditioner 模型负向测试
class AirConditionerModelNegativeTest(TestCase):
    def test_set_temperature_out_of_range(self):
        ac = AirConditioner.objects.create(Device_id=11, Device_name="AC1", Device_type="AirConditioner", Device_status=1, temperature=22, mode="cool")
        with self.assertRaises(ValueError):
            ac.set_temperature(50)  # 假设温度应在 16 到 30 之间

    def test_set_invalid_mode(self):
        ac = AirConditioner.objects.create(Device_id=12, Device_name="AC2", Device_type="AirConditioner", Device_status=1, temperature=22, mode="cool")
        with self.assertRaises(ValueError):
            ac.set_mode("invalid_mode")  # 模式应为 'cool', 'heat', 或 'dry'

# WashingMachine 模型负向测试
class WashingMachineModelNegativeTest(TestCase):
    def test_set_invalid_mode(self):
        wm = WashingMachine.objects.create(Device_id=13, Device_name="WM1", Device_type="WashingMachine", Device_status=1, mode="wash")
        with self.assertRaises(ValueError):
            wm.set_mode("invalid_mode")  # 模式应为 'wash', 'dry', 或 'fastwash'

# Robotvacuum 模型负向测试
class RobotvacuumModelNegativeTest(TestCase):
    def test_set_invalid_mode(self):
        robot = Robotvacuum.objects.create(Device_id=14, Device_name="Robot1", Device_type="RobotVacuum", Device_status=1, mode="sweep")
        with self.assertRaises(ValueError):
            robot.set_mode("invalid_mode")  # 模式应为 'sweep' 或 'mop'

# Curtain 模型负向测试
class CurtainModelNegativeTest(TestCase):
    def test_add_device_with_invalid_status(self):
        curtain = Curtain.objects.create(Device_id=15, Device_name="Curtain1", Device_type="Curtain", Device_status=1)
        with self.assertRaises(ValueError):
            curtain.add_device(Device_id=16, Device_name="Curtain2", Device_type="Curtain", Device_status=3)  # 假设状态应为 0, 1, 或 2

# # Log 模型负向测试
# class LogModelNegativeTest(TestCase):
#     def test_create_log_with_missing_fields(self):
#         with self.assertRaises(ValueError):
#             Log.objects.create(Log_id=20, username="Alice", devicename="Light1", operation="turn_on")  # 缺少 devicetype 字段

#     def test_query_log_by_invalid_time_range(self):
#         now = timezone.now()
#         Log.objects.create(Log_id=21, username="Bob", devicename="AC1", devicetype="AirConditioner", operation="turn_on")
#         logs = Log.query_Log_by_time_range(now.replace(hour=0), now.replace(hour=23))
#         self.assertEqual(len(logs), 1)

# Habits 模型负向测试
# class HabitsModelNegativeTest(TestCase):
#     def test_add_favorite_device_invalid_device(self):
#         habit = Habits.objects.create(habit_id=17, username="Alice", habit_name="Morning")
#         invalid_device = Device(Device_id=18, Device_name="InvalidDevice", Device_type="Generic", Device_status=0)
#         with self.assertRaises(ValueError):
#             habit.add_favorite_device(invalid_device)  # 设备未保存到数据库，无法添加

#     def test_remove_nonexistent_favorite_device(self):
#         habit = Habits.objects.create(habit_id=18, username="Alice", habit_name="Evening")
#         nonexistent_device = Device(Device_id=19, Device_name="NonexistentDevice", Device_type="Generic", Device_status=0)
#         with self.assertRaises(ValueError):
#             habit.remove_favorite_device(nonexistent_device)  # 设备未添加，无法移除
