from django.shortcuts import render

# Create your views here.
def register():
    pass
    
def login():
    pass

def logout():
    pass

def change_password():
    pass

# def add_device():
#     pass

# def delete_device():
#     pass
# 这两个要判断权限级是否达到2（工作人员）

def query_Log_by_username():
    pass

def query_Log_by_devicename():
    pass

def query_Log_by_time_range():
    pass
# 这三个函数需要先判定用户的权限是否够

def turn_on():
    pass

def turn_off():
    pass

def change_brightness():
    pass

def cool():
    pass

def heat():
    pass

def wet():
    pass

def change_temperature():
    pass

def wash():
    pass

def dry():
    pass

def fastwash():
    pass

def sweep():
    pass

def mop():
    pass

def open():
    pass

def close():
    pass
# 这些函数也需要判断用户权限级，儿童只能开关灯和窗帘，其他都没有权限

def change_name():
    pass
# 需要判断权限大于等于1（起码是成人）

