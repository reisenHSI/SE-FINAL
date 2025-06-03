from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import *

"""
前端需要实现的界面：
·登录界面
·注册界面
·主页界面（可以包含四部分——跳转到设备选项界面、跳转到日志查询界面、跳转到一键开启界面）
·设备选项界面：包含灯、空调、窗帘、扫地机、洗衣机五个选项，点击选项跳转到对应设备
·灯：灯的名称（选项？）、亮度调节（0-100选项条）、开关键、添加设备、修改名称
·空调：空调名称（选项？）、参考空调遥控器？（开关、三种模式、温度调节、温度显示）、添加设备、修改名称
·窗帘：窗帘名称（选项？）、开关、添加设备、修改名称
·扫地机：设备名称（选项？）、模式选择、开关、添加设备、修改名称
·洗衣机：洗衣机名称（选项？）、模式选择、开关、添加设备、修改名称
·日志查询界面：展示日志、过滤查询日志
·一键开启：列出常用的habits，点击选取
"""
# Create your views here.
def register():
    # 注册用户，前端输入用户名、密码、电话，选择权限级别，然后后端确定UserId，存入数据库，返回“注册成功”，然后跳转回登陆界面
    # 需要判断是否注册过重复用户
    pass
    
def login(request):
    # 前端输入用户名和密码，如果无该用户，返回“该用户不存在”，如果密码不匹配，返回“密码错误”，如果注册成功则跳转到管理界面
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                request.session['username'] = username  # 将用户名保存到会话中
                request.session['is_authenticated'] = True
                return redirect('book')  # 重定向到 book 页面
            else:
                messages.error(request, '密码错误')
        except User.DoesNotExist:
            messages.error(request, '用户不存在')
    return render(request, 'login.html')
    pass

#每个前端网页要用到的函数，最好加上这个，防止未登录就可以跳转
'''
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
'''

def logout(request):
    # 注销登陆，然后返回首页
    if request.session.get('is_authenticated'):
        request.session.flush()  # 清除所有会话信息
        messages.success(request, '您已成功注销！')
    return redirect('login')  # 重定向到登录页面
    pass

def change_password():
    # 前端输入用户名和密码，如果无该用户，返回“该用户不存在”，如果密码不匹配，返回“密码错误”，如果修改成功则返回“密码修改成功”，然后跳转到首页
    pass

# def add_device():
#     pass

# def delete_device():
#     pass
# 这两个要判断权限级是否达到2（工作人员）

def query_Log_by_username(request):
    # 前端输入用户名，然后返回该用户的所有操作记录，包括设备名、设备类型、操作时间
    # 需要判断权限级是否达到1（成人）
    username = request.session.get('username')
    user = User.objects.get(username=username)
    current_user_permission = user.permission
    
    # 检查当前用户的权限级别是否达到1（成人）
    if current_user_permission < 1:
        messages.error(request, "您没有权限查看此信息")

    if request.method == 'POST':
        target_username = request.POST.get('username')

    logs = Log.query_Log_by_username(target_username)
    
    # 构造返回的数据
    log_data = []
    for log in logs:
        log_data.append({
            'device_name': log.devicename,
            'device_type': log.devicetype,
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 返回JSON响应
    return JsonResponse({'logs': log_data})



def query_Log_by_devicename(request):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    current_user_permission = user.permission
    
    # 检查当前用户的权限级别是否达到1（成人）
    if current_user_permission < 1:
        messages.error(request, "您没有权限查看此信息")
        
    if request.method == 'POST':
        target_device = request.POST.get('device')

    logs = Log.query_Log_by_devicename(target_device)
    
    # 构造返回的数据
    log_data = []
    for log in logs:
        log_data.append({
            'device_name': log.devicename,
            'device_type': log.devicetype,
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 返回JSON响应
    return JsonResponse({'logs': log_data})

def query_Log_by_time_range(request):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    current_user_permission = user.permission
    
    # 检查当前用户的权限级别是否达到1（成人）
    if current_user_permission < 1:
        messages.error(request, "您没有权限查看此信息")
        
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    logs = Log.query_Log_by_time_range(start_time,end_time)
    
    # 构造返回的数据
    log_data = []
    for log in logs:
        log_data.append({
            'device_name': log.devicename,
            'device_type': log.devicetype,
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 返回JSON响应
    return JsonResponse({'logs': log_data})
    pass
# 这三个函数需要先判定用户的权限是否够

# 下面这几个函数对应的前端都大概做成一个类似按钮之类的东西
# 获取设备ID和类别，然后根据设备的类别，执行相应的操作，都可以调用models函数
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

