from django.test import TestCase
from ..models import *
# Create your tests here.
from django.utils import timezone

class UserModelTest(TestCase):
    def test_user_password(self):
        user = User.objects.create(username='Alice', password='123456', phone='1234567890', age=25, User_id=1)
        user.set_password('newpass')
        self.assertTrue(user.check_password('newpass'))

class DeviceModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(Device_id=1, Device_name="TestDevice", Device_type="Generic", Device_status=0)

    def test_turn_on_off(self):
        self.device.turn_on()
        self.assertEqual(self.device.Device_status, 1)
        self.device.turn_off()
        self.assertEqual(self.device.Device_status, 0)

    def test_change_name(self):
        self.device.change_name("NewName")
        self.assertEqual(self.device.Device_name, "NewName")

class LightModelTest(TestCase):
    def test_light_creation(self):
        light = Light.objects.create(Device_id=2, Device_name="L1", Device_type="Light", Device_status=0, brightness=70)
        light.set_brightness(90)
        self.assertEqual(light.get_brightness(), 90)

class AirConditionerModelTest(TestCase):
    def test_air_conditioner(self):
        ac = AirConditioner.objects.create(Device_id=3, Device_name="AC1", Device_type="AirConditioner", Device_status=1, temperature=22, mode="cool")
        ac.set_temperature(26)
        ac.set_mode("heat")
        self.assertEqual(ac.get_temperature(), 26)
        self.assertEqual(ac.get_mode(), "heat")

class WashingMachineModelTest(TestCase):
    def test_washing_machine(self):
        wm = WashingMachine.objects.create(Device_id=4, Device_name="WM1", Device_type="WashingMachine", Device_status=0, mode="wash")
        wm.set_mode("standard")
        self.assertEqual(wm.get_mode(), "standard")

class RobotvacuumModelTest(TestCase):
    def test_robot_vacuum(self):
        robot = Robotvacuum.objects.create(Device_id=5, Device_name="R1", Device_type="RobotVacuum", Device_status=1, mode="sweep")
        robot.set_mode("mop")
        self.assertEqual(robot.get_mode(), "mop")

class CurtainModelTest(TestCase):
    def test_curtain_add(self):
        curtain = Curtain.objects.create(Device_id=6, Device_name="C1", Device_type="Curtain", Device_status=1)
        self.assertEqual(curtain.Device_name, "C1")

class LogModelTest(TestCase):
    def test_create_and_query_log(self):
        log = Log.objects.create(Log_id=1, username="Alice", devicename="Light1", devicetype="Light", operation="turn_on")
        queried = Log.objects.get(Log_id=1)
        self.assertEqual(queried.username, "Alice")

    def test_query_by_username(self):
        Log.objects.create(Log_id=2, username="Bob", devicename="AC", devicetype="AirConditioner", operation="turn_on")
        Log.objects.create(Log_id=3, username="Bob", devicename="Light", devicetype="Light", operation="turn_off")
        logs = Log().query_Log_by_username("Bob")
        self.assertEqual(len(logs), 2)

    def test_query_by_time_range(self):
        now = timezone.now()
        log1 = Log.objects.create(Log_id=10, username="X", devicename="D1", devicetype="Light", operation="on")
        logs = Log.query_Log_by_time_range(now.replace(hour=0), now.replace(hour=23))
        self.assertTrue(log1 in logs)

class HabitsModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(Device_id=7, Device_name="HabitDevice", Device_type="Light", Device_status=1)
        self.habit = Habits.objects.create(habit_id=1, username="Alice", habit_name="Morning",favorite_devices=models.ManyToManyField(self.device))

    # def test_add_remove_favorite_device(self):
    #     self.habit
    #     # self.habit.add_favorite_device(self.device)
    #     # self.assertIn(self.device, self.habit.get_habits())
    #     # self.habit.remove_favorite_device(self.device)
    #     # self.assertNotIn(self.device, self.habit.get_habits())``