# your_app/tests/test_views_negative.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from ..models import *
import json

class UserViewsNegativeTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='existinguser',
            password=make_password('correct_password'),
            phone='12345678901', age=30, User_id=1, permission=1
        )

    def test_register_missing_fields(self):
        url = reverse('register')
        data = {'username': '', 'password': 'pass', 'phone': '12345678901', 'age': 20}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('所有字段都是必填的', response.json()['message'])

    def test_register_duplicate_username(self):
        url = reverse('register')
        data = {'username': 'existinguser', 'password': 'pass', 'phone': '12345678901', 'age': 30}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('用户名已存在', response.json()['message'])

    def test_login_wrong_password(self):
        url = reverse('login')
        data = {'username': 'existinguser', 'password': 'wrong_password'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('密码错误', response.json()['message'])

    def test_login_user_not_exist(self):
        url = reverse('login')
        data = {'username': 'nouser', 'password': 'any'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('用户不存在', response.json()['message'])

    def test_login_missing_fields(self):
        url = reverse('login')
        data = {'username': '', 'password': ''}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('用户名和密码不能为空', response.json()['message'])

    def test_change_password_user_not_exist(self):
        url = reverse('change_password')
        data = {'username': 'nouser', 'old_password': 'any', 'new_password': 'a', 'confirm_new_password': 'a'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('用户不存在', response.json()['message'])

    def test_change_password_old_password_wrong(self):
        url = reverse('change_password')
        data = {'username': 'existinguser', 'old_password': 'wrong', 'new_password': 'a', 'confirm_new_password': 'a'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('旧密码错误', response.json()['message'])

    def test_change_password_new_mismatch(self):
        url = reverse('change_password')
        data = {'username': 'existinguser', 'old_password': 'correct_password', 'new_password': 'a', 'confirm_new_password': 'b'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('新密码和确认新密码不一致', response.json()['message'])

    def test_change_password_missing_fields(self):
        url = reverse('change_password')
        data = {'username': '', 'old_password': '', 'new_password': '', 'confirm_new_password': ''}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('所有字段都是必填的', response.json()['message'])

    def test_add_device_bad_json(self):
        session = self.client.session
        session['is_authenticated'] = True
        session['username'] = 'staff'
        session['permission'] = 2
        session.save()
        resp = self.client.post(reverse('add_device'), "not-json", content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('无效的JSON数据', resp.json()['message'])
