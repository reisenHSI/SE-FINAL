from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Max
from .models import *

"""
前端需要实现的界面：
·登录界面
·注册界面
·主页界面（可以包含四部分——跳转到设备选项界面、设备增删页面、跳转到日志查询界面、跳转到一键开启界面）
·设备选项界面：包含灯、空调、窗帘、扫地机、洗衣机五个选项，点击选项跳转到对应设备
·灯：灯的名称（选项？）、亮度调节（0-100选项条）、开关键、添加设备、修改名称
·空调：空调名称（选项？）、参考空调遥控器？（开关、三种模式、温度调节、温度显示）、添加设备、修改名称
·窗帘：窗帘名称（选项？）、开关、添加设备、修改名称
·扫地机：设备名称（选项？）、模式选择、开关、添加设备、修改名称
·洗衣机：洗衣机名称（选项？）、模式选择、开关、添加设备、修改名称
·设备增删页面：选择增加或删除设备，进一步跳转到add_device和delete_device
·日志查询界面：展示日志、过滤查询日志
·一键开启：列出常用的habits，点击选取
"""
# Create your views here.

"""
    注册用户
    前端传入用户名、密码、电话、年龄
    可选择地传入“注册码”用来判断是否为工作人员(ZNJJ)(假设只有内部人员知道该注册码)
    后端将信息进行处理，并存入数据库
    前端返回“注册成功”，然后跳转回登陆界面
    若用户名重复，则后端重定向到注册页面，前端提示重新输入
"""
def register(request):
    if request.method == 'POST':
        # 获取前端传入的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        registration_code = request.POST.get('registration_code', '')  # 注册码可以为空

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, "用户名已存在")
            return HttpResponseRedirect(reverse('register'))  # 重定向到注册页面

        if registration_code == 'ZNJJ':  # 注册码匹配
            permission = 2  # 工作人员
        elif int(age) >= 18:
            permission = 1  # 成人
        else:
            permission = 0  # 儿童

        # 创建新用户
        new_user = User(
            username=username,
            password=make_password(password),  # 对密码进行哈希加密，数据库中存储加密的密码
            phone=phone,
            User_id=User.objects.count() + 1,  # 简单地根据当前用户数量生成 User_id
            permission=permission
        )
        new_user.save()

        # 返回注册成功信息并重定向到登录页面
        messages.success(request, "注册成功")
        return HttpResponseRedirect(reverse('login'))  # 重定向到登录页面

    # 如果不是 POST 请求，返回注册页面
    return HttpResponseRedirect(reverse('register'))
    
"""
    用户登录
    前端传入用户名和密码
    若无该用户则返回“该用户不存在”
    若密码错误则返回“密码错误，请重新再试”
    登录成功返回登陆成功，并跳转到管理界面（home）
"""
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if check_password(password,user.password): # 使用哈希密码进行验证
                request.session['username'] = username  # 将用户名保存到会话中
                request.session['is_authenticated'] = True
                messages.success(request, '登录成功')
                return redirect('home')  # 重定向到 home 页面
            else:
                messages.error(request, '密码错误')
        except User.DoesNotExist:
            messages.error(request, '用户不存在')
    return render(request, 'login.html')


#每个前端网页要用到的函数，最好加上这个，防止未登录就可以跳转
'''
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
'''

"""
    退出登录
    前端在home中设计“退出登录”按钮，点击后退出登录，然后跳转到登录界面
"""
def logout(request):
    # 注销登陆，然后返回首页
    if request.session.get('is_authenticated'):
        request.session.flush()  # 清除所有会话信息
        messages.success(request, '您已成功注销！')
    return redirect('login')  # 重定向到登录页面

"""
    修改密码
    前端从登录页面进入修改密码页面
    前端需要提供4个方框，对应用户名、密码、新密码、确认新密码，并传到后端
    后端将会依次验证用户名、旧密码和确认的新密码
    若用户名不存在，则前端在方框下提示“用户名不存在，请重新再试”
    若旧密码错误，则前端在方框下提示“旧密码错误，请重新输入”
    若新密码和确认新密码不一致，则前端在方框下提示“新密码和确认新密码不一致，请重新输入”
    若上述三步骤均验证成功，后端保存，并跳转到登录页
    error_filed表示错误的字段
"""
def change_password(request):
    if request.method == 'POST':
        # 从前端获取所有必要信息
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        # 验证用户名是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, '用户名不存在，请重新再试')
            return render(request, 'change_password.html', {'error_field': 'username'})
        
        # 验证旧密码是否正确
        if not user.check_password(old_password):
            messages.error(request, '旧密码错误，请重新输入')
            return render(request, 'change_password.html', {
                'username': username,
                'error_field': 'old_password'
            })
        
        # 验证新密码和确认密码是否一致
        if new_password != confirm_new_password:
            messages.error(request, '新密码和确认新密码不一致，请重新输入')
            return render(request, 'change_password.html', {
                'username': username,
                'error_field': 'confirm_new_password'
            })
        
        # set_password会自动进行哈希处理
        user.set_password(new_password)
        user.save()
        
        # 密码修改成功，跳转到登录页面
        messages.success(request, '密码修改成功，请重新登录')
        return redirect('login')
    
    # GET请求时返回修改密码页面
    return render(request, 'change_password.html')
    
"""
    前端需要提供4个跳转和退出登录按钮
    4个跳转分别为：设备使用、设备管理(add_delete)、日志查询和一键启动
    to do
    后端待修改
"""
def home(request):
    # 登陆进去之后的主界面，显示所有的设备
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    # # 查询所有设备
    # devices = Device.objects.all()
    
    # # 按设备类型分组
    # devices_by_type = {}
    # for device in devices:
    #     device_type = device.Device_type
    #     if device_type not in devices_by_type:
    #         devices_by_type[device_type] = []
    #     devices_by_type[device_type].append(device)
    
    # # 将分组后的设备信息传递到模板
    # context = {
    #     'devices_by_type': devices_by_type
    # }
    
    # # 渲染主界面模板
    # return render(request, 'home.html', context)
    
    # home 包含几个功能的跳转——设备、设备增删、日志查询、一键开启（共4个）
    # 设备增删已完成（add_delete）
    pass

"""
    以下两个函数是添加和删除设备逻辑
    在home页面提供一个设备管理的选项
    通过“设备管理”选项进入add_delete页面，可以选择添加或删除
    点击“添加设备”，则跳转到add_device页面，用户需要传入设备名，并通过选项框选择设备类型
    点击“删除设备”，则跳转到delete_device页面，用户通过选中设备,传入设备列表
    以上操作均在权限为2（工作人员）的用户下才能进行（后端）
"""
def add_device(request):
    # 添加设备界面，需要输入下方2个信息，然后device_type可以写成一个可选择的列表，
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    current_user_permission = request.session.get('permission')
    # 检查当前用户的权限级别是否为2（工作人员）
    if current_user_permission != 2:
        messages.error(request, '您没有权限删除设备')
        return redirect('add_delete')
    
    if request.method == 'POST':
        # 获取前端传入的设备信息
        username = request.session.get('username')
        device_name = request.POST.get('device_name')
        device_type = request.POST.get('device_type')
        
        # 创建新设备
        # 获取最大ID，不能直接使用count+1.否则删除时可能会发生竞争
        max_id = Device.objects.aggregate(max_id=Max('Device_id'))['max_id'] or 0
        new_device = Device(
            Device_id=max_id + 1,
            Device_name=device_name,
            Device_type=device_type
        )
        new_device.save()

        Log.objects.create(
            username=username,
            devicename=device_name,
            devicetype=device_type,
            operation='add'
        )
        
        # 返回添加成功信息并重定向到主界面
        messages.success(request, '设备添加成功')
        return redirect('add_delete')
    
    # 如果不是 POST 请求，返回添加设备页面
    return render(request, 'add_device.html')

def delete_device(request):
    # 点击这个删除设备的按钮，会显示出所有的设备，然后勾选这个设备，点击确认，然后就可以把这个设备删除
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    current_user_permission = request.session.get('permission')
    # 检查当前用户的权限级别是否为2（工作人员）
    if current_user_permission != 2:
        messages.error(request, '您没有权限删除设备')
        return redirect('add_delete')
    
    if request.method == 'POST':
        # 获取前端传入的设备名列表
        username = request.session.get('username')
        device_names = request.POST.getlist('device_name')
        
        # 删除选中的设备
        for device_name in device_names:
            device = Device.objects.get(Device_id=device_name)
            device.delete()
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype=Device.objects.get(Device_id=device_name).Device_type,
                operation='add'
            )
        # 返回删除成功信息并重定向到主界面
        messages.success(request, '设备删除成功')
        return redirect('add_delete')
    
    # 如果不是 POST 请求，显示所有设备供用户选择
    # device包含设备id、设备名、设备类型、设备状态
    devices = Device.objects.all()
    context = {
        'devices': devices
    }
    return render(request, 'delete_device.html', context)

"""
    查询日志
    默认提供所有日志信息，在前端页面展示最新的几条日志（已按时间由近到远排序）
    提供过滤器，可以根据[用户名、设备名、时间戳]进行筛选
    前端需要传入username\devicename\start_time\end_time(POST)
    可以动态筛选，前端传入的条件默认为None，用户操作后传入对应条件
    使用AJAX 请求 + JSON 响应，前端实现无页面跳转
    后端返回JSON数据，表示所有日志信息（筛选则返回部分）
"""
def query_Log(request):
    # 验证是否登录
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    # 获取用户信息
    username = request.session.get('username')
    user = User.objects.get(username=username)
    current_user_permission = user.permission
    
    # 无权限查看，返回空页面，抛出错误信息
    if current_user_permission < 1:
        messages.error(request, "您没有权限查看此信息")
        log_data = []
        return JsonResponse({'log_data': log_data}) # 返回空列表
    
    # 获取筛选条件
    if request.method == 'POST':
        target_username = request.POST.get('username')
        target_devicename = request.POST.get('devicename')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

    logs = Log.objects.all().order_by('-timestamp')

    # 根据传入参数进行过滤
    if target_username:
        logs = logs.filter(username=target_username)
    if target_devicename:
        logs = logs.filter(devicename=target_devicename)
    if start_time and end_time:
        logs = logs.filter(timestamp__range=[start_time, end_time])

    log_data = []
    for log in logs:
        log_data.append({
            'device_name': log.devicename, # 设备名称
            'device_type': log.devicetype, # 设备类型
            'operation': log.operation, # 操作
            'username': log.username, # 使用者
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S') # 时间戳
        })
    
    # 返回JSON响应
    return JsonResponse({'logs': log_data})

# 下面这几个函数对应的前端都大概做成一个类似按钮之类的东西
# 获取设备ID和类别，然后根据设备的类别，执行相应的操作，都可以调用models函数
"""
    设备操作之后，加入日志（设备名、设备类型、操作、用户、时间）
"""
def turn_on(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    current_user_permission = request.session.get('permission')
    
    # 根据设备ID获取设备对象
    device_name = request.POST.get('device_name')
    username = request.session.get('username')
    device = Device.objects.get(Device_name=device_name)
    
    # 根据设备类型调用相应的 turn_on 方法
    if device.Device_type == 'Light':
        # 灯不需要权限检查
        light = Light.objects.get(Device_name=device_name)
        light.turn_on()
        light.save()
    elif device.Device_type in ['AirConditioner', 'Curtain', 'WashingMachine', 'RobotVacuum']:
        # 其他设备需要权限至少为1
        if current_user_permission < 1:
            messages.error(request, '您没有权限打开此设备')
            return redirect('devices')  # 重定向到设备列表页面
        
        if device.Device_type == 'AirConditioner':
            air_conditioner = AirConditioner.objects.get(Device_name=device_name)
            air_conditioner.turn_on()
            air_conditioner.save()
        elif device.Device_type == 'Curtain':
            curtain = Curtain.objects.get(Device_name=device_name)
            curtain.turn_on()
            curtain.save()
        elif device.Device_type == 'WashingMachine':
            washing_machine = washingMachine.objects.get(Device_name=device_name)
            washing_machine.turn_on()
            washing_machine.save()
        elif device.Device_type == 'RobotVacuum':
            robot_vacuum = robotvacuum.objects.get(Device_name=device_name)
            robot_vacuum.turn_on()
            robot_vacuum.save()
    
    # 创建日志
    Log.objects.create(
        username=username,
        devicename=device.Device_name,
        devicetype=device.Device_type,
        operation='turn on'
    )

    # 返回操作成功信息并重定向到设备列表页面
    messages.success(request, f'{device.Device_name} 已打开')
    return redirect('devices')

def turn_off():
    pass

def set_brightness():
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

# 根据当前用户名，获取用户的所有habit（可能有多条记录），用户选择其中之一并打开
def habit():
    pass

