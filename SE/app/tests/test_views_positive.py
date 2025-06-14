# tests_views_positive.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from ..models import *
import json

class ViewsPositiveTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='admin',
            password=make_password('admin123'),
            phone='1234567890',
            age=30,
            permission=2
        )
        session = self.client.session
        session['is_authenticated'] = True
        session['username'] = self.user.username
        session['permission'] = self.user.permission
        session.save()

    # --- 用户功能相关测试 ---
    def test_register_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'phone': '1234567890',
            'age': 22
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_change_password_success(self):
        url = reverse('change_password')
        data = {
            'username': 'admin',
            'old_password': 'admin123',
            'new_password': 'newpass123',
            'confirm_new_password': 'newpass123'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    # --- 设备增删与页面 ---
    def test_add_delete_page_success(self):
        url = reverse('add_delete')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_add_device_get(self):
        url = reverse('add_device')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_add_device_post_success(self):
        url = reverse('add_device')
        payload = {'device_name': 'Light1', 'device_type': 'Light', 'username': 'admin'}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(Device.objects.filter(Device_name='Light1').exists())

    def test_delete_device_get(self):
        Light.objects.create(Device_id=10, Device_name='LightDel', Device_type='Light')
        url = reverse('delete_device')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_delete_device_post_success(self):
        d = Light.objects.create(Device_id=11, Device_name='ToDelete', Device_type='Light')
        url = reverse('delete_device')
        payload = {'device_name': 'ToDelete','username': 'admin'}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertFalse(Device.objects.filter(Device_id=d.Device_id).exists())

    # --- 控制功能 ---
    def test_light_control_success(self):
        Light.objects.create(Device_id=12, Device_name='LightCtrl', Device_type='Light', brightness=50)
        url = reverse('light')
        payload = {'device_name': 'LightCtrl', 'status': 1, 'brightness': 70}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_air_conditioner_control_success(self):
        AirConditioner.objects.create(Device_id=13, Device_name='AC1', Device_type='AirConditioner', temperature=25, mode='cool')
        url = reverse('airConditioner')
        payload = {
            'device_name': 'AC1',
            'username': 'admin',
            'new_status': '1',
            'new_temperature': 28,
            'new_mode': 'heat'
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['device']['temperature'], 28)

    # --- 日志与习惯 ---
    def test_query_logs_success(self):
        Light.objects.create(Device_id=14, Device_name='QueryLight', Device_type='Light')
        Log.objects.create(Log_id=1, username='admin', devicename='QueryLight', devicetype='Light', operation='add')
        url = reverse('query_logs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_add_habit_success(self):
        device = Light.objects.create(Device_id=100, Device_name='HabitLight', Device_type='Light')
        url = reverse('add_habit')
        payload = {
            'username': 'admin',
            'habitname': 'MorningRoutine',
            'devicename': 'HabitLight',
            'devicetype': 'Light',
            'brightness': 80
        }
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['habitname'], 'MorningRoutine')
        self.assertEqual(response.json()['devicename'], 'HabitLight')

    def test_query_habits_success(self):
        Habits.objects.create(
            username='admin',
            habitname='MyHabit',
            devicename='QueryLight',
            devicetype='Light',
            brightness=60,
            status=1
        )
        url = reverse('habits')
        payload = {'username': 'admin'}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'admin')
        self.assertTrue(any(h['habitname'] == 'MyHabit' for h in response.json()['result']))

    def test_exec_habit_success(self):
        Habits.objects.create(
            username='admin',
            habitname='EveningRoutine',
            devicename='Light',
            devicetype='Light',
            brightness=40,
            status=1
        )
        url = reverse('exec_habit')
        payload = {'username': 'admin', 'habitname': 'EveningRoutine'}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['habitname'], 'EveningRoutine')
        self.assertEqual(response.json()['devicename'], 'Light')
        self.assertTrue(any('brightness' in a for a in response.json()['actions']))

