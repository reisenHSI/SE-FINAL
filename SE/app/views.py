from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from .models import *

"""
前端需要实现的界面：
    ·登录界面
    ·注册界面
    ·主页界面:跳转到devices、add_delete、query_Log、habits，并提供logout键
    ·设备选项界面：包含灯、空调、窗帘、扫地机、洗衣机五个类别的所有设备（devices）
        ·灯：灯的名称、亮度调节（0-100选项条）、开关键、修改名称（light）
        ·空调：空调名称、参考空调遥控器？（开关、三种模式、温度调节、温度显示）、修改名称（airConditioner）
        ·窗帘：窗帘名称、开关、修改名称(curtain)
        ·扫地机：设备名称、模式选择、开关、修改名称(washingMachine)
        ·洗衣机：洗衣机名称、模式选择、开关、修改名称(robotvacuum)
    ·设备增删页面：选择增加或删除设备（add_delete）
        ·增加设备：add_device
        ·删除设备：delete_device
    ·日志查询界面：展示日志、过滤查询日志（query_Log）
    ·一键开启：列出常用的habits，点击选取（habit）
        ·添加习惯（add_habit）：添加habit
        ·删除习惯（delete_habit）：删除habit
"""
# Create your views here.

"""
    注册用户
    前端传入用户名、密码、电话、年龄
    可选择地传入“注册码”用来判断是否为工作人员(ZNJJ)(假设只有内部人员知道该注册码)
    后端将信息进行处理，并存入数据库
    前端返回“注册成功”，然后跳转回登陆界面
    若用户名重复，则抛出消息，后端重定向到注册页面，前端提示重新输入
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
    else:
        return render(request, 'register.html')
    
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
            # 判断用户是否存在
            user = User.objects.get(username=username)
            if check_password(password,user.password): # 使用哈希密码进行验证
                request.session['username'] = username  # 将用户名保存到会话中
                request.session['is_authenticated'] = True
                request.session['permission'] = user.permission
                messages.success(request, '登录成功') # 存在，登录成功
                return redirect('home')  # 重定向到 home 页面
            else:
                # 密码错误，抛出错误信息
                messages.error(request, '密码错误')
        except User.DoesNotExist:
            # 用户不存在，抛出错误信息
            messages.error(request, '用户不存在')
    return render(request, 'login.html')


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
            # 用户名不存在
            messages.error(request, '用户名不存在，请重新再试')
            return render(request, 'change_password.html', {'error_field': 'username'})
        
        # 验证旧密码是否正确
        if not user.check_password(old_password):
            # 旧密码错误
            messages.error(request, '旧密码错误，请重新输入')
            return render(request, 'change_password.html', {
                'username': username,
                'error_field': 'old_password'
            })
        
        # 验证新密码和确认密码是否一致
        if new_password != confirm_new_password:
            # 新密码和确认密码不一致
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
    主页面
    提供4个跳转和退出登录按钮，不需要具体的逻辑实现
"""
def home(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面

    return render(request, 'home.html')

"""
    从home.html跳转到该页面
    该页面提供“添加设备”和“删除设备”两个按钮，分别跳转到add_device和delete_device页面
"""
def add_delete(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面

    return render(request, 'add_delete.html')

"""
    以下两个函数是添加和删除设备逻辑
    在home页面提供一个设备管理的选项
    通过“设备管理”选项进入add_delete页面，可以选择添加或删除
    点击“添加设备”，则跳转到add_device页面，用户需要传入设备名，并通过选项框选择设备类型
    点击“删除设备”，则跳转到delete_device页面，用户通过选中设备,传入设备列表
    以上操作均在权限为2（工作人员）的用户下才能进行（后端）
"""

"""
    add_device.html
    第一次进入时，后端提供所有设备
    用户添加设备时，前端提供输入的设备名、设备类型
    后端执行添加操作，并返回所有设备
    device_type可能需要通过选择传入（而不是文本输入），便于统一
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
        # 先在Device中创建记录
        new_device = Device(
            Device_id=max_id + 1,
            Device_name=device_name,
            Device_type=device_type
        )
        # 在派生类中创建记录
        if device_type == 'Light':
            new_device = Light.objects.create(Device_id=max_id + 1, 
                                            Device_name=device_name, 
                                            Device_type=device_type)
        elif device_type == 'WashingMachine':
            new_device = WashingMachine.objects.create(Device_id=max_id + 1, 
                                            Device_name=device_name, 
                                            Device_type=device_type)
        elif  device_type == 'Robotvacuum':
            new_device = Robotvacuum.objects.create(Device_id=max_id + 1, 
                                            Device_name=device_name, 
                                            Device_type=device_type)
        elif device_type == 'AirConditioner':
            new_device = AirConditioner.objects.create(Device_id=max_id + 1, 
                                            Device_name=device_name, 
                                            Device_type=device_type)
        elif device_type == 'Curtain':
            new_device = Curtain.objects.create(Device_id=max_id + 1, 
                                            Device_name=device_name, 
                                            Device_type=device_type)
        new_device.save()
        
        current_time = timezone.now()
        Log.objects.create(
            username=username,
            devicename=device_name,
            devicetype=device_type,
            operation='add',
            timestamp = current_time
        )
        
        # 返回添加成功信息并重定向到主界面
        messages.success(request, '设备添加成功')
        return redirect('add_device')
    
    devices = Device.objects.all()
    context = {'devices': devices,
               'username': username}
    
    # 如果不是 POST 请求，返回添加设备页面
    return render(request, 'add_device.html', context)

"""
    delete_device.html
    第一次进入时，提供所有设备列表
    用户选择设备进行删除（列表，可以多个设备）
    删除成功后，返回删除成功信息，并返回所有设备列表
"""
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
            device = Device.objects.get(Device_name=device_name)
            device.delete()
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype=Device.objects.get(Device_name=device_name).Device_type,
                operation='delete'
            )
        # 返回删除成功信息并重定向到主界面
        messages.success(request, '设备删除成功')
        return redirect('delete_device')
    
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

'''
    devices主页面
    按类别显示所有设备（前端可以考虑按类别可视化为图标+设备名？）
    后端提供所有已分类的设备（一个包含5个列表的列表）
    前端点击设备的图标，需要根据设备名跳转到对应的设备类型
    （light, curtain, robotvacuum, airconditioner, washingmachine）
    后端传出的context拥有device的所有信息，前端可以据此进行跳转和后续传输请求
'''
def devices(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    # 查询所有设备
    devices = Device.objects.all()
    
    # 按设备类型分组
    devices_by_type = {}
    for device in devices:
        device_type = device.Device_type
        if device_type not in devices_by_type:
            devices_by_type[device_type] = []
        devices_by_type[device_type].append(device)
    
    # 将分组后的设备信息传递到模板
    context = {
        'devices_by_type': devices_by_type
    }
    
    # 渲染主界面模板
    return render(request, 'devices.html', context)


"""
    light.html对应的逻辑
    前端需要传入设备名称（用户在devices页面点击的设备）
    前端选择性提供设备修改的状态（new_status、new_brightness、new_name）
    设备状态包括：开关、亮度、新名称
    后端中，当用户第一次进入light.html时，会将数据库中该设备的状态提供给前端进行展示
    当用户修改设备状态时，后端处理这些请求，之后返回最新的设备状态给前端
"""
def light(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    device_name = request.POST.get('device_name')
    light = Light.objects.get(Device_name=device_name)

    if request.method == 'POST':
        # 检查亮度合法
        if 'new_brightness' in request.POST:
            new_brightness = request.POST.get('new_brightness')
            if new_brightness < 0 or new_brightness > 100:
                messages.error(request, '亮度值必须在0到100之间！')
                return redirect('light')
        
        if 'new_status' in request.POST:
            new_status = request.POST.get('new_status')
            light.set_status(new_status) # 0表示关闭，1表示打开
            messages.success(request, '操作成功！')
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="light",
                operation='turn on' if new_status == '1' else 'turn off'
            )
        if 'new_brightness' in request.POST:
            new_brightness = request.POST.get('new_brightness')
            light.set_brightness(new_brightness)
            messages.success(request, f"亮度已修改为{new_brightness}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="light",
                operation=f"set brightness to {new_brightness}"
            )
        if 'new_name' in request.POST:
            new_name = request.POST.get('new_name')
            light.set_name(new_name)
            messages.success(request, f"设备名已修改为{new_name}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="light",
                operation=f"set device_name to {new_name}"
            )
        # light.save()
        return redirect(reverse('light'))

    context = {
        'status': light.get_status(),
        'brightness': light.get_brightness(),
        'name': light.get_name()
    }
    return render(request, 'light.html', context)
        
"""
    airConditioner.html对应的逻辑:参考空调遥控器？
    前端需要传入设备名称（用户在devices页面点击的设备）
    前端选择性提供设备修改的状态（new_status、new_temperature、new_mode、new_name）
    设备状态包括：开关、温度、模式、新名称
    后端中，当用户第一次进入airCondotioner.html时，会将数据库中该设备的状态提供给前端进行展示
    当用户修改设备状态时，后端处理这些请求，之后返回最新的设备状态给前端
"""
def airConditioner(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    device_name = request.POST.get('device_name')
    airConditioner = AirConditioner.objects.get(Device_name=device_name)
    
    if request.method == 'POST':
        if 'new_status' in request.POST:
            new_status = request.POST.get('new_status')
            airConditioner.set_status(new_status) # 0表示关闭，1表示打开
            messages.success(request, '操作成功！')
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="airConditioner",
                operation='turn on' if new_status == '1' else 'turn off'
            )
        if 'new_temperature' in request.POST:
            new_temperature = request.POST.get('new_temperature')
            airConditioner.set_temperature(new_temperature)
            messages.success(request, f"亮度已修改为{new_temperature}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="airConditioner",
                operation=f"set temperature to {new_temperature}"
            )
        if 'new_mode' in request.POST:
            new_mode = request.POST.get('new_mode')
            airConditioner.set_mode(new_mode)
            messages.success(request, f"模式已修改为{new_mode}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="airConditioner",
                operation=f"set mode to {new_mode}"
            )
        if 'new_name' in request.POST:
            new_name = request.POST.get('new_name')
            airConditioner.set_name(new_name)
            messages.success(request, f"设备名已修改为{new_name}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="airConditioner",
                operation=f"change name to {new_name}"
            )
        # airConditioner.save()
        return redirect(reverse('airConditioner'))

    context = {
        'status': airConditioner.get_status(),
        'temperature': airConditioner.get_temperature(),
        'mode': airConditioner.get_mode(),
        'name': airConditioner.get_name()
    }
    return render(request, 'airConditioner.html', context)

"""
    curtain.html对应的逻辑
    前端需要传入设备名称（用户在devices页面点击的设备）
    前端选择性提供设备修改的状态（new_status、new_name）
    设备状态包括：开关、亮度、新名称
    后端中，当用户第一次进入curtain.html时，会将数据库中该设备的状态提供给前端进行展示
    当用户修改设备状态时，后端处理这些请求，之后返回最新的设备状态给前端
"""
def curtain(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    device_name = request.POST.get('device_name')
    curtain = Curtain.objects.get(Device_name=device_name)

    if request.method == 'POST':
        if 'new_status' in request.POST:
            new_status = request.POST.get('new_status')
            curtain.set_status(new_name) # 0表示关闭，1表示打开
            messages.success(request, '操作成功！')
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="curtain",
                operation='turn on' if new_status == '1' else 'turn off'
            )
        if 'new_name' in request.POST:
            new_name = request.POST.get('new_name')
            curtain.set_name(new_name)
            messages.success(request, f"设备名已修改为{new_name}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="curtain",
                operation=f"set name to {new_name}"
            )
        # curtain.save()
        return redirect(reverse('curtain'))

    context = {
        'status': curtain.get_status(),
        'name': curtain.get_name()
    }
    return render(request, 'curtain.html', context)

"""
    washingMachine.html对应的逻辑
    前端需要传入设备名称（用户在devices页面点击的设备）
    前端选择性提供设备修改的状态（new_status、new_mode、new_name）
    设备状态包括：开关、模式、新名称
    后端中，当用户第一次进入washingMachine.html时，会将数据库中该设备的状态提供给前端进行展示
    当用户修改设备状态时，后端处理这些请求，之后返回最新的设备状态给前端
"""

def washingMachine(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    device_name = request.POST.get('device_name')
    washingMachine = WashingMachine.objects.get(Device_name=device_name)
    permission = request.session.get('permission')

    if request.method == 'POST':
        # 检查用户权限
        if permission < 1:
            messages.error(request, '无权限操作！')
            return redirect('washingMachine')
        
        if 'new_status' in request.POST:
            new_status = request.POST.get('new_status')
            washingMachine.set_status(new_status) # 0表示关闭，1表示打开
            messages.success(request, '操作成功！')
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="washingMachine",
                operation='turn on' if new_status == '1' else 'turn off'
            )
        if 'new_mode' in request.POST:
            new_mode = request.POST.get('new_mode')
            washingMachine.set_mode(new_mode)
            messages.success(request, f"模式已修改为{new_mode}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="washingMachine",
                operation=f"set mode to {new_mode}"
            )
        if 'new_name' in request.POST:
            new_name = request.POST.get('new_name')
            washingMachine.set_name(new_name)
            messages.success(request, f"设备名已修改为{new_name}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="washingMachine",
                operation=f"set name to {new_name}"
            )
        # washingMachine.save()
        return redirect(reverse('washingMachine'))

    context = {
        'status': washingMachine.get_status(),
        'mode': washingMachine.get_mode(),
        'name': washingMachine.get_name()
    }
    return render(request, 'washingMachine.html', context)

"""
    robotvacuum.html对应的逻辑
    前端需要传入设备名称（用户在devices页面点击的设备）
    前端选择性提供设备修改的状态（new_status、new_mode、new_name）
    设备状态包括：开关、模式、新名称
    后端中，当用户第一次进入robotvacuum.html时，会将数据库中该设备的状态提供给前端进行展示
    当用户修改设备状态时，后端处理这些请求，之后返回最新的设备状态给前端
"""

def robotvacuum(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    device_name = request.POST.get('device_name')
    robotvacuum = Robotvacuum.objects.get(Device_name=device_name)
    permission = request.session.get('permission')

    if request.method == 'POST':
        # 检查用户权限
        if permission < 1:
            messages.error(request, '无权限操作！')
            return redirect('robotvacuum')
        
        if 'new_status' in request.POST:
            new_status = request.POST.get('new_status')
            robotvacuum.set_status(new_status) # 0表示关闭，1表示打开
            messages.success(request, '操作成功！')
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="robotvacuum",
                operation='turn on' if new_status == '1' else 'turn off'
            )
        if 'new_mode' in request.POST:
            new_mode = request.POST.get('new_mode')
            robotvacuum.set_mode(new_mode)
            messages.success(request, f"模式已修改为{new_mode}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="robotvacuum",
                operation=f"set mode to {new_mode}"
            )
        if 'new_name' in request.POST:
            new_name = request.POST.get('new_name')
            robotvacuum.set_name(new_name)
            messages.success(request, f"设备名已修改为{new_name}!")
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype="robotvacuum",
                operation=f"set name to {new_name}"
            )
        # robotvacuum.save()
        return redirect(reverse('robotvacuum'))

    context = {
        'status': robotvacuum.get_status(),
        'mode': robotvacuum.get_mode(),
        'name': robotvacuum.get_name()
    }
    return render(request, 'robotvacuum.html', context)



"""
    habits.html处理逻辑
    第一次进入页面时，后端会提供当前用户的所有habit信息，前端显示
    启动设备时，前端需要提供用户选择的haibit选项(habit_name)，后端依据选项打开设备
"""
def habits(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    user_habits = Habits.objects.filter(username=username)

    if request.method == 'POST':
        # 选择一个习惯
        selected_habit_name = request.POST.get('habit_name')
        habit = Habits.objects.get(username=username, habit_name=selected_habit_name)
        for device in habit.favorite_devices.all():
            device.turn_on()
            Log.objects.create(
                username=username,
                devicename=device.get_name(),
                devicetype=device.Device_type,
                operation='turn on'
            )

    context = {
        'user_habits': user_habits,
        'username': username,
    }
    return render(request, 'habits.html', context)
        

"""
    add_habit.html逻辑
    前端需要提供用户选择的设备名和习惯名称（提供文本框输入习惯名称）
    后端创建一条habit记录，将这些设备加入到habit中
    第一次进入页面时，后端提供所有设备（类似于devices），供用户选择
    数据格式为：
    selected_devices = request.POST.getlist('device_name')
    habit_name = request.POST.get('habit_name')
"""
def add_habit(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面

    username = request.session.get('username')
    
    if request.method == 'POST':
        # 获取用户提交的设备名称列表
        selected_devices = request.POST.getlist('device_name')
        habit_name = request.POST.get('habit_name')

        # 创建新的habit记录
        habit = Habits(username=username, habit_name=habit_name)
        habit.save()

        # 遍历选中的设备，将它们添加到habit记录中
        for device_name in selected_devices:
            device = Device.objects.get(Device_name=device_name)
            if device not in habit.favorite_devices.all():
                habit.favorite_devices.add(device)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype=Device.objects.get(Device_name=device_name).Device_type,
                    operation=f"add to habit {habit_name}"
                )
        
        messages.success(request, '习惯添加完成')
        return redirect('habits')  # 重定向到主页

    # 如果不是 POST 请求，或者用户直接访问该页面，显示添加习惯的表单
    devices = Device.objects.all()
    return render(request, 'add_habit.html', {'devices': devices, 'username': username})

"""
    delete_habit.html逻辑
    第一次登录时，后端提供所有当前用户的习惯
    之后用户选择习惯，后端进行删除，并返回新的习惯列表
    前端需要提供删除的习惯名称
"""
def delete_habit(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, '请先登录！')
        return redirect('login')  # 重定向到登录页面
    
    username = request.session.get('username')
    habits = Habits.objects.filter(username=username)

    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        habit = Habits.objects.get(habit_name=habit_name)
        for device in habit.favorite_devices.all():
            Log.objects.create(
                username=username,
                devicename=device.get_name(),
                devicetype=device.Device_type,
                operation=f"delete from habit {habit_name}"
            )
        habit.delete()
        messages.success(request, '删除成功！')
        
        return redirect('habits')
    
    context = {
        'habits': habits,
        'username': username
    }

    return render(request, 'delete_habit.html', context)







# '''
#     这个是habits的主界面，会显示所有已经添加过的habits，然后每一条habits可以的后面有一个可以勾选的方框，
#     然后最下面有一个应用和删除按钮，点击后会将勾选的记录的信息列表传给后端，后端根据method种类执行对应操作
# '''
# def habit(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面

#     username = request.session.get('username')
#     user_habits = habits.objects.filter(username=username)  # 获取当前用户的所有习惯

#     if request.method == 'POST':
#         # 获取用户勾选的习惯ID列表
#         selected_habit_ids = request.POST.getlist('habit_id')

#         # 遍历选中的习惯并应用
#         for habit_id in selected_habit_ids:
#             habit = habits.objects.get(habit_id=habit_id)
#             apply_habit(request, habit)

#         messages.success(request, '所选习惯已成功应用')
#         return redirect('habits_page')

#     if request.method == 'DELETE':
#         # 获取要删除的习惯ID
#         selected_habit_ids = request.POST.getlist('habit_id')

#         # 遍历选中的习惯并应用
#         for habit_id in selected_habit_ids:
#             habit = habits.objects.get(habit_id=habit_id)
#             habit.delete()

#         messages.success(request, '习惯已成功删除')
#         return redirect('habits_page')
    
#     return render(request, 'habits.html', {'user_habits': user_habits})


# # 用户添加一条habit记录，流程是用户不断添加设备，前端将设备名传给后端，然后添加到habits的devices，直到用户点击前端的 “完成”按键，停止添加设备
# '''
#     这个函数的功能在add_habit前端页面完成，只要前端method不为complete，就会一直传入设备，然后添加
# '''
# def add_habit(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面

#     username = request.session.get('username')
    
#     if request.method == 'POST':
#         # 获取用户提交的设备名称列表
#         selected_devices = request.POST.getlist('device_name')

#         # 创建新的habit记录
#         habit = habits(username=username)
#         habit.save()

#         # 遍历选中的设备，将它们添加到habit记录中
#         for device_name in selected_devices:
#             device = Device.objects.get(Device_name=device_name)
#             if device not in habit.favorite_devices.all():
#                 habit.favorite_devices.add(device)
        
#         messages.success(request, '习惯添加完成')
#         return redirect('habits')  # 重定向到主页

#     # 如果不是 POST 请求，或者用户直接访问该页面，显示添加习惯的表单
#     devices = Device.objects.all()
#     return render(request, 'add_habit.html', {'devices': devices, 'username': username})


# # 应用habit，用户在habits界面选择一个habit应用，然后将这个habit里面的所有设备都开启
# '''
#     这个功能放在habits页面里
#     habits页面显示目前有的所有habits，然后用户可以勾选某些habit，然后点击应用来调用apply_habit函数；
#     add_habit可以作为一个按键，点击就跳转到add_habit页面
# '''
# def apply_habit(request,habit):
#     # 获取习惯中的所有设备
#     devices = habit.favorite_devices.all()

#     # 遍历设备并调用turn_on函数开启设备
#     for device in devices:
#         turn_on_device(request, device.Device_name)

# def turn_on_device(request,device_name):
#     request.method = 'POST'  # 模拟POST请求
#     request.POST = {'device_name': device_name}  # 设置设备名称
#     return turn_on(request) # 调用turn on，会写入日志

# """
#     设备操作之后，加入日志（设备名、设备类型、操作、用户、时间）
# """
# def turn_on(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
    
#     # 根据设备ID获取设备对象
#     device_name = request.POST.get('device_name')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
    
#     # 根据设备类型调用相应的 turn_on 方法
#     if device.Device_type == 'Light':
#         # 灯不需要权限检查
#         light = Light.objects.get(Device_name=device_name)
#         light.turn_on()
#         light.save()
#     elif device.Device_type in ['AirConditioner', 'Curtain', 'WashingMachine', 'RobotVacuum']:
#         # 其他设备需要权限至少为1
#         if current_user_permission < 1:
#             messages.error(request, '您没有权限打开此设备')
#             return redirect('devices')  # 重定向到设备列表页面
        
#         if device.Device_type == 'AirConditioner':
#             air_conditioner = AirConditioner.objects.get(Device_name=device_name)
#             air_conditioner.turn_on()
#             air_conditioner.save()
#         elif device.Device_type == 'Curtain':
#             curtain = Curtain.objects.get(Device_name=device_name)
#             curtain.turn_on()
#             curtain.save()
#         elif device.Device_type == 'WashingMachine':
#             washing_machine = WashingMachine.objects.get(Device_name=device_name)
#             washing_machine.turn_on()
#             washing_machine.save()
#         elif device.Device_type == 'RobotVacuum':
#             robot_vacuum = Robotvacuum.objects.get(Device_name=device_name)
#             robot_vacuum.turn_on()
#             robot_vacuum.save()

#     current_time = timezone.now()
#     # 创建日志
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='turn on',
#         timestamp=current_time
#     )

#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已打开')
#     return redirect('devices')

# """
#     设备操作之后，加入日志（设备名、设备类型、操作、用户、时间）
# """
# def turn_off(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')

#     device_name = request.POST.get('device_name')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)

#     if device.Device_type == 'Light':
#         # 灯不需要权限检查
#         light = Light.objects.get(Device_name=device_name)
#         light.turn_off()
#         light.save()
#     elif device.Device_type in ['AirConditioner', 'Curtain', 'WashingMachine', 'RobotVacuum']:
#         # 其他设备需要权限至少为1
#         if current_user_permission < 1:
#             messages.error(request, '您没有权限关闭此设备')
#             return redirect('devices')  # 重定向到设备列表页面
        
#         if device.Device_type == 'AirConditioner':
#             air_conditioner = AirConditioner.objects.get(Device_name=device_name)
#             air_conditioner.turn_off()
#             air_conditioner.save()
#         elif device.Device_type == 'Curtain':
#             curtain = Curtain.objects.get(Device_name=device_name)
#             curtain.turn_off()
#             curtain.save()
#         elif device.Device_type == 'WashingMachine':
#             washing_machine = WashingMachine.objects.get(Device_name=device_name)
#             washing_machine.turn_off()
#             washing_machine.save()
#         elif device.Device_type == 'RobotVacuum':
#             robot_vacuum = Robotvacuum.objects.get(Device_name=device_name)
#             robot_vacuum.turn_off()
#             robot_vacuum.save()
#     current_time = timezone.now()

#     # 创建日志
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='turn off',
#         timestamp=current_time
#     )

#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已关闭')
#     return redirect('devices')

# """
#     设备操作之后，加入日志（设备名、设备类型、操作、用户、时间）
#     然后相比turnon和turnoff，需要多传入brightness
# """
# def set_brightness(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
    
#     # 根据设备ID获取设备对象
#     device_name = request.POST.get('device_name')
#     brightness = request.POST.get('brightness')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
#     light = Light.objects.get(Device_name=device_name)
#     light.set_brightness(brightness)
#     light.save()
#     current_time = timezone.now()
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='set brightness: f{brightness}',
#         timestamp=current_time
#     )
    
#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已调整亮度')
#     return redirect('devices')

# """
#     设备操作之后，加入日志（设备名、设备类型、操作、用户、时间）
#     然后相比turnon和turnoff，需要多传入mode
# """
# def aircondition_set_mode(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
#     if current_user_permission < 1:
#         messages.error(request, '您没有权限修改此设备')
#         return redirect('devices')
#     # 根据设备ID获取设备对象
#     device_name = request.POST.get('device_name')
#     mode = request.POST.get('mode')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
#     airconditioner = AirConditioner.objects.get(Device_name=device_name)
#     airconditioner.set_mode(mode)
#     airconditioner.save()
#     current_time = timezone.now()
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='set mode: f{mode}',
#         timestamp=current_time
#     )

#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已修改模式')
#     return redirect('devices')

# def aircondition_set_temperature(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
#     if current_user_permission < 1:
#         messages.error(request, '您没有权限修改此设备')
#         return redirect('devices')
#     device_name = request.POST.get('device_name')
#     temperature = request.POST.get('temperature').int()
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
#     airconditioner = AirConditioner.objects.get(Device_name=device_name)
#     airconditioner.set_temperature(temperature)
#     airconditioner.save()
#     current_time = timezone.now()
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='set temperature: f{temperature}',
#         timestamp=current_time
#     )
    
#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已修改温度')
#     return redirect('devices')

# def washing_set_mode(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
#     if current_user_permission < 1:
#         messages.error(request, '您没有权限修改此设备')
#         return redirect('devices')
#     device_name = request.POST.get('device_name')
#     mode = request.POST.get('mode')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
#     washingMachine = WashingMachine.objects.get(Device_name=device_name)
#     washingMachine.set_mode(mode)
#     washingMachine.save()
#     current_time = timezone.now()
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='set mode: f{mode}',
#         timestamp=current_time
#     )
    
#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已修改模式')
#     return redirect('devices')

# def RobotVacuum_set_mode(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面
#     current_user_permission = request.session.get('permission')
#     if current_user_permission < 1:
#         messages.error(request, '您没有权限修改此设备')
#         return redirect('devices')
#     device_name = request.POST.get('device_name')
#     mode = request.POST.get('mode')
#     username = request.session.get('username')
#     device = Device.objects.get(Device_name=device_name)
#     robotvacuum = Robotvacuum.objects(Device_name = device_name)
#     robotvacuum.set_mode(mode)
#     robotvacuum.save()
#     current_time = timezone.now()
#     Log.objects.create(
#         username=username,
#         devicename=device.Device_name,
#         devicetype=device.Device_type,
#         operation='set mode: f{mode}',
#         timestamp=current_time
#     )
    
#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device.Device_name} 已修改模式')
#     return redirect('devices')

# def change_name(request):
#     if not request.session.get('is_authenticated'):
#         messages.error(request, '请先登录！')
#         return redirect('login')  # 重定向到登录页面

#     current_user_permission = request.session.get('permission')
#     if current_user_permission < 1:
#         messages.error(request, '您没有权限重命名设备')
#         return redirect('devices')  # 重定向到设备列表页面

#     # 获取设备当前名称和新名称
#     device_name = request.POST.get('device_name')
#     new_device_name = request.POST.get('new_device_name')
#     username = request.session.get('username')

#     # 检查新名称是否为空
#     if not new_device_name:
#         messages.error(request, '新设备名称不能为空')
#         return redirect('devices')

#     # 检查新名称是否与现有设备名称冲突
#     if Device.objects.filter(Device_name=new_device_name).exists():
#         messages.error(request, '新设备名称已存在，请选择其他名称')
#         return redirect('devices')

#     # 获取设备对象
#     try:
#         device = Device.objects.get(Device_name=device_name)
#     except Device.DoesNotExist:
#         messages.error(request, '设备不存在')
#         return redirect('devices')

#     # 更新设备名称
#     device.Device_name = new_device_name
#     device.save()
#     current_time = timezone.now()

#     # 创建日志
#     Log.objects.create(
#         username=username,
#         devicename=new_device_name,
#         devicetype=device.Device_type,
#         operation='rename: f{new_device_name}',
#         timestamp=current_time
#     )

#     # 返回操作成功信息并重定向到设备列表页面
#     messages.success(request, f'{device_name} 已成功重命名为 {new_device_name}')
#     return redirect('devices')