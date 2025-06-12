from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Max
from django.utils import timezone
from .models import *
import json

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
    若注册成功，则后端提供：成功状态、注册成功信息和用户信息
    若失败，则依据情况抛出各种错误信息
"""
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            username = data.get('username')
            password = data.get('password')
            phone = data.get('phone')
            age = data.get('age')
            registration_code = data.get('registration_code', '')  # 注册码可以为空

            # 检查必填字段是否为空
            if not all([username, password, phone, age]):
                return JsonResponse({
                    'status': 'error',
                    'message': '所有字段都是必填的'
                }, status=400)
            
            # 检查用户是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': '用户名已存在'
                }, status=400)
            
            if registration_code == 'ZNJJ':  # 注册码匹配
                permission = 2  # 工作人员
            elif int(age) >= 18:
                permission = 1  # 成人
            else:
                permission = 0  # 儿童

            # 创建新用户
            new_user = User.objects.create(
                username=username,
                password=make_password(password),
                phone=phone,
                age = int(age),
                permission=permission
            )

            # 返回注册成功响应
            return JsonResponse({
                'status': 'success',
                'message': '注册成功',
                'user': {
                    'username': username,
                    'phone': phone,
                    'permission': permission
                }
            }, status=201)
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'注册失败：{str(e)}'
            }, status=500)
    
    # 若不是POST请求，返回空响应，前端处理页面渲染
    return JsonResponse({})



"""
    用户登录
    前端传入用户名和密码
    若无该用户则返回“该用户不存在”
    若密码错误则返回“密码错误，请重新再试”
    登录成功返回登陆成功，并跳转到管理界面（home）
"""
def login(request):
    if request.method == 'POST':
        try:
            # 获取前端传入的JSON数据
            data = json.loads(request.body) if request.body else {}
            username = data.get('username')
            password = data.get('password')

            # 验证必填字段
            if not username or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户名和密码不能为空'
                }, status=400)

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):

                    return JsonResponse({
                        'status': 'success',
                        'message': '登录成功',
                        'user': {
                            'username': username,
                            'permission': user.permission
                        }
                    })
                else:
                    print(f'{username}, {password}')
                    return JsonResponse({
                        'status': 'error',
                        'message': '密码错误'
                    }, status=400)
                    
            except User.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户不存在'
                }, status=404)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'登录失败: {str(e)}'
            }, status=500)

    # GET请求返回空响应（前端处理页面渲染）
    return JsonResponse({})

"""
    退出登录
    前端在home中设计“退出登录”按钮，点击后退出登录，然后跳转到登录界面
"""
def logout(request):
    # if request.method == 'POST':
    #     try:
    #         if request.session.get('is_authenticated'):
    #             request.session.flush()  # 清除所有会话信息
    #             return JsonResponse({
    #                 'status': 'success',
    #                 'message': '您已成功退出登录！'
    #             })
    #         else:
    #             return JsonResponse({
    #                 'status': 'error',
    #                 'message': '您尚未登录'
    #             }, status=400)
    #     except Exception as e:
    #         return JsonResponse({
    #             'status': 'error',
    #             'message': f'注销失败: {str(e)}'
    #         }, status=500)
    
    # GET请求返回空响应（前端处理页面渲染）
    return JsonResponse({})
    

"""
    修改密码
    前端从登录页面进入修改密码页面
    前端需要提供4个方框，对应用户名、密码、新密码、确认新密码，并传到后端
    后端将会依次验证用户名、旧密码和确认的新密码
    若用户名不存在，则前端在方框下提示“用户名不存在，请重新再试”
    若旧密码错误，则前端在方框下提示“旧密码错误，请重新输入”
    若新密码和确认新密码不一致，则前端在方框下提示“新密码和确认新密码不一致，请重新输入”
    若上述三步骤均验证成功，后端保存，status变为成功，抛出成功信息
    若错误，则依据不同情况抛出错误信息，status为false
"""
def change_password(request):
    if request.method == 'POST':
        try:
            # 获取前端传入的JSON数据
            data = json.loads(request.body) if request.body else {}
            username = data.get('username')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_new_password = data.get('confirm_new_password')

            # 验证必填字段
            if not all([username, old_password, new_password, confirm_new_password]):
                return JsonResponse({
                    'status': 'error',
                    'message': '所有字段都是必填的',
                    'error_field': 'all'
                }, status=400)

            # 验证用户名是否存在
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户不存在，请重新再试',
                    'error_field': 'username'
                }, status=404)

            # 验证旧密码是否正确
            if not user.check_password(old_password):
                return JsonResponse({
                    'status': 'error',
                    'message': '旧密码错误，请重新输入',
                    'error_field': 'old_password'
                }, status=400)

            # 验证新密码和确认密码是否一致
            if new_password != confirm_new_password:
                return JsonResponse({
                    'status': 'error',
                    'message': '新密码和确认新密码不一致，请重新输入',
                    'error_field': 'confirm_new_password'
                }, status=400)

            # 更新密码
            user.set_password(new_password)
            user.save()

            # 返回成功响应
            return JsonResponse({
                'status': 'success',
                'message': '密码修改成功，请重新登录'
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据',
                'error_field': 'all'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'密码修改失败: {str(e)}',
                'error_field': 'all'
            }, status=500)

    # GET请求返回空响应（前端处理页面渲染）
    return JsonResponse({})
    
"""
    主页面
    提供4个跳转和退出登录按钮，不需要具体的逻辑实现
    若为登录，则status为error，并提供重定向路径
    若成功，则status为sucess，并提供用户名、权限、跳转选择（5个选项）等信息
"""
def home(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    permission = User.objects.get(username=username).get_permission()
    
    # 返回主页所需的基本信息
    return JsonResponse({
        'status': 'success',
        'data': {
            'username': username,
            'permission': permission,
            'menu_options': [
                {'name': '设备管理', 'url': '/home/devices/'},
                {'name': '设备增删', 'url': '/home/add_delete/'},
                {'name': '日志查询', 'url': '/home/query_logs/'},
                {'name': '一键习惯', 'url': '/home/habits/'},
                {'name': '退出登录', 'url': '/logout/'}
            ]
        }
    })

"""
    从home.html跳转到该页面
    该页面提供“添加设备”和“删除设备”两个按钮，分别跳转到add_device和delete_device页面
    若未登录，则status为error，并提供重定向路径（login）
    # 若权限不足，则status为error，并提供重定向路径（home）
    若成功，则status为success，并返回页面所需数据（用户名、跳转选项等）
"""
def add_delete(request): 
    # 返回页面所需数据
    return JsonResponse({
        'status': 'success',
        'data': {
            'page_title': '设备管理',
            'options': [
                {
                    'name': '添加设备',
                    'url': '/home/add_delete/add_device/',
                    'description': '添加新设备到系统'
                },
                {
                    'name': '删除设备',
                    'url': '/home/add_delete/delete_device/',
                    'description': '从系统中移除设备'
                }
            ]
        }
    })

"""
    add_device.html
    前端传入设备名和设备类型
    若未登录，则status为error，提供重定向路径（login）
    若权限不足，则status为error，提供重定向路径（add_delete）
    若设备已存在，则status为error，抛出错误信息
    若设备类型错误（为严格按照5个类进行填写），则status为error
    添加成功则status为success
    GET请求会返回所有设备的信息
"""
def add_device(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data = json.loads(request.body)
            device_name = data.get('device_name')
            device_type = data.get('device_type')
            username = data.get('username')
            permission = User.objects.get(username=username).get_permission()

            if permission != 2:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限添加设备',
                    'redirect': '/home/add_delete/'
                }, status=403)

            # 验证必填字段
            if not all([device_name, device_type]):
                return JsonResponse({
                    'status': 'error',
                    'message': '设备名称和类型不能为空'
                }, status=400)
            
            if device_type not in ['Light', 'WashingMachine', 'Robotvacuum', 'AirConditioner', 'Curtain']:
                return JsonResponse({
                    'status': 'error',
                    'message': '设备类型错误'
                }, status=400)

            # 检查设备是否已存在
            if Device.objects.filter(Device_name=device_name).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': '设备名称已存在'
                }, status=400)

            # 根据设备类型创建具体设备
            device_models = {
                'Light': Light,
                'WashingMachine': WashingMachine,
                'Robotvacuum': Robotvacuum,
                'AirConditioner': AirConditioner,
                'Curtain': Curtain
            }

            if device_type in device_models:
                max_id = Device.objects.aggregate(max_id=Max('Device_id'))['max_id'] or 0
                new_device = device_models[device_type].objects.create(
                    Device_id=max_id + 1,
                    Device_name=device_name,
                    Device_type=device_type
                )
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': '无效的设备类型'
                }, status=400)

            # 记录日志
            Log.objects.create(
                username=username,
                devicename=device_name,
                devicetype=device_type,
                operation='add',
                timestamp=timezone.now()
            )

            # 返回成功响应
            return JsonResponse({
                'status': 'success',
                'message': '设备添加成功',
                'device': {
                    'id': new_device.Device_id,
                    'name': new_device.Device_name,
                    'type': new_device.Device_type
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'添加设备失败: {str(e)}'
            }, status=500)

    # GET请求返回设备类型选项和现有设备列表
    device_types = ['Light', 'WashingMachine', 'Robotvacuum', 'AirConditioner', 'Curtain']
    devices = list(Device.objects.values('Device_id', 'Device_name', 'Device_type'))
    
    return JsonResponse({
        'status': 'success',
        'device_types': device_types,
        'devices': devices,
        # 'username': username
    })

"""
    delete_device.html
    未登录，则status为error，抛出错误信息，提供重定向
    权限不足，则status为error，抛出错误信息，提供重定向
    未选择删除的设备，status为error，提供错误信息
    删除成功，status为success，后端分别提供被删除的设备和仍存在的设备
    GET请求返回所有设备,status为success
"""
def delete_device(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data = json.loads(request.body)
            device_name = data.get('device_name')  # 改为使用设备ID列表
            username = data.get('username')
            permission = User.objects.get(username=username).get_permission()
            print(f'username: {username}, device_name: {device_name}, permission: {permission}')

            if permission != 2:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限删除设备',
                    'redirect': '/home/add_delete/'
                }, status=403)
            
            if not device_name:
                return JsonResponse({
                    'status': 'error',
                    'message': '请选择要删除的设备'
                }, status=400)
            
            deleted_devices = []

            try:
                print('1')
                device = Device.objects.get(Device_name=device_name)
                device_name = device.Device_name
                device_type = device.Device_type

                # 删除设备
                device.delete()

                # 记录日志
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype=device_type,
                    operation='delete',
                    timestamp=timezone.now()
                )

                deleted_devices.append({
                    'name': device_name,
                    'type': device_type
                })

            except Device.DoesNotExist:
                pass

            
            # 返回成功响应
            return JsonResponse({
                'status': 'success',
                'message': f'成功删除 {len(deleted_devices)} 个设备',
                'deleted_devices': deleted_devices,
                'remaining_devices': list(Device.objects.values('Device_id', 'Device_name', 'Device_type'))
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '无效的JSON数据'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'删除设备失败: {str(e)}'
            }, status=500)
    
    # GET请求返回所有设备列表
    devices = list(Device.objects.values('Device_id', 'Device_name', 'Device_type'))
    return JsonResponse({
        'status': 'success',
        'devices': devices,
        # 'username': username
    })

"""
    查询日志query_logs
    若未登录，则status为error，提供错误信息和重定向
    若权限不足，则status为error，提供错误信息和重定向
    若查询成功，则会提供由近到远的日志信息（依据条件筛选，若条件为空则返回所有信息）
"""
def query_logs(request):
    try:
        # 初始化查询集
        logs = Log.objects.all().order_by('-timestamp')
        
        # 处理筛选条件
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            username = data.get('username')
            permission = User.objects.get(username=username).get_permission()

            if permission != 2:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限查看此信息',
                    'redirect': '/home/'
                }, status=403)
            
            # 获取筛选参数
            filters = {
                'username': data.get('check_username'),
                'devicename': data.get('devicename'),
                'start_time': data.get('start_time'),
                'end_time': data.get('end_time')
            }
            
            # 应用筛选条件
            if filters['username']:
                logs = logs.filter(username__icontains=filters['username'])
            if filters['devicename']:
                logs = logs.filter(devicename__icontains=filters['devicename'])
            if filters['start_time'] and filters['end_time']:
                logs = logs.filter(timestamp__range=[filters['start_time'], filters['end_time']])
        
        # 构建响应数据
        log_data = []
        for log in logs:
            log_data.append({
                'id': log.Log_id,
                'username': log.username,
                'device_name': log.devicename,
                'device_type': log.devicetype,
                'operation': log.operation,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'formatted_operation': f"{log.username} {log.operation} {log.devicename}({log.devicetype})"
            })
        
        # 添加分页信息
        total_count = logs.count()
        
        return JsonResponse({
            'status': 'success',
            'logs': log_data, # 日志数据
            'total_count': total_count, # 总记录数
            'filter_options': {
                'usernames': list(Log.objects.order_by().values_list('username', flat=True).distinct()),
                'devicenames': list(Log.objects.order_by().values_list('devicename', flat=True).distinct())
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'查询日志失败: {str(e)}'
        }, status=500)

'''
    devices主页面
    所有设备按照类别进行分类，并提供跳转路径、设备类别、设备图标名称
    图标名称、跳转路径可能需要修改
'''
def devices(request):    
    try:
        username = ""
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
        permission = User.objects.get(username=username).get_permission()
        
        # 查询所有设备并按类型分组
        devices = Device.objects.all()
        
        # 定义设备类型映射
        device_type_mapping = {
            'Light': {
                'name': '灯光设备',
                'icon': 'lightbulb',
                'endpoint': '/api/light/'
            },
            'AirConditioner': {
                'name': '空调设备',
                'icon': 'ac-unit',
                'endpoint': '/api/airConditioner/'
            },
            'Curtain': {
                'name': '窗帘设备',
                'icon': 'curtains',
                'endpoint': '/api/curtain/'
            },
            'WashingMachine': {
                'name': '洗衣设备',
                'icon': 'local_laundry_service',
                'endpoint': '/api/washingMachine/'
            },
            'Robotvacuum': {
                'name': '扫地机器人',
                'icon': 'cleaning_services',
                'endpoint': '/api/robotvacuum/'
            }
        }
        
        # 按类型分组设备
        grouped_devices = {}
        for device in devices:
            device_type = device.Device_type
            if device_type not in grouped_devices:
                grouped_devices[device_type] = {
                    'type_info': device_type_mapping.get(device_type, {
                        'name': device_type,
                        'icon': 'devices',
                        'endpoint': f'/api/{device_type.lower()}/'
                    }),
                    'devices': []
                }
            
            grouped_devices[device_type]['devices'].append({
                'id': device.Device_id,
                'name': device.Device_name,
                'status': device.get_status() if hasattr(device, 'get_status') else None,
                'endpoint': f"/api/{device_type.lower()}/"
            })
        
        # 转换为前端需要的数组格式
        device_categories = [
            {
                'type': device_type,
                'type_name': info['type_info']['name'],
                'icon': info['type_info']['icon'],
                'endpoint': info['type_info']['endpoint'],
                'devices': info['devices']
            } 
            for device_type, info in grouped_devices.items()
        ]
        
        return JsonResponse({
            'status': 'success',
            'device_categories': device_categories,
            'username': username,
            'permission': permission
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'获取设备列表失败: {str(e)}'
        }, status=500)


"""
    light.html对应的逻辑
    未登录，status为error，提供错误信息和重定向
    未提供设备名称时，status为error，提供错误信息
    若已登录且满足各种条件，则修改数据库信息，然后同GET请求
    GET请求时，提供设备当前的各种状态信息
"""
def light(request):
    try:
        device_name = ""
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            device_name = data.get('device_name')
            username = data.get('username')
        
        if not device_name:
            return JsonResponse({
                'status': 'error',
                'message': '缺少设备名称参数'
            }, status=400)

        # 获取设备对象
        light = Light.objects.get(Device_name=device_name)

        # 处理POST请求（设备控制）
        if request.method == 'POST':
            # 处理状态变更
            if 'new_status' in data:
                new_status = data['new_status']
                if new_status not in ['0', '1']:
                    return JsonResponse({
                        'status': 'error',
                        'message': '无效的状态值'
                    }, status=400)
                
                new_status = int(new_status)
                light.set_status(new_status)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="Light",
                    operation='turn on' if new_status == 1 else 'turn off',
                    timestamp=timezone.now()
                )

            # 处理亮度变更
            if 'new_brightness' in data:
                new_brightness = int(data['new_brightness'])
                if not 0 <= new_brightness <= 100:
                    return JsonResponse({
                        'status': 'error',
                        'message': '亮度值必须在0到100之间'
                    }, status=400)
                
                light.set_brightness(new_brightness)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="light",
                    operation=f"set brightness to {new_brightness}"
                )

            # 处理名称变更
            if 'new_name' in data:
                new_name = data['new_name'].strip()
                if not new_name:
                    return JsonResponse({
                        'status': 'error',
                        'message': '设备名称不能为空'
                    }, status=400)
                
                old_name = light.Device_name
                light.set_name(new_name)
                Log.objects.create(
                    username=username,
                    devicename=old_name,
                    devicetype="light",
                    operation=f"rename to {new_name}"
                )

        # GET请求返回设备当前状态
        return JsonResponse({
            'status': 'success',
            'device': {
                'id': light.Device_id,
                'name': light.Device_name,
                'type': light.Device_type,
                'status': light.get_status(),
                'brightness': light.get_brightness(),
            }
        })

    except Light.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '设备不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)

"""
    airConditioner.html
    逻辑与light基本一致，注意mode
    返回设备名、状态、温度、模式等等信息
    GET请求返回当前设备的各种信息
"""
def airConditioner(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            device_name = data.get('device_name')
            username = data.get('username')
            print(device_name)
            print(username)

        if not device_name:
            return JsonResponse({
                'status': 'error',
                'message': '缺少设备名称参数'
            }, status=400)

        # 获取设备对象
        ac = AirConditioner.objects.get(Device_name=device_name)
        permission = User.objects.get(username=username).get_permission()

        # 处理POST请求（设备控制）
        if request.method == 'POST':
            # 验证和设置温度（16-30度）
            if 'new_temperature' in data:
                new_temp = int(data['new_temperature'])
                if not 16 <= new_temp <= 30:
                    return JsonResponse({
                        'status': 'error',
                        'message': '温度必须介于16-30度之间'
                    }, status=400)
                
                ac.set_temperature(new_temp)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="airConditioner",
                    operation=f"set temperature to {new_temp}"
                )

            # 验证和设置模式（cool/heat/auto）
            if 'new_mode' in data:
                valid_modes = ['cool', 'heat', 'auto', 'dry', 'fan']
                new_mode = data['new_mode']
                if new_mode not in valid_modes:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'无效的模式，必须是: {", ".join(valid_modes)}'
                    }, status=400)
                
                ac.set_mode(new_mode)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="airConditioner",
                    operation=f"set mode to {new_mode}"
                )

            # 设置开关状态
            if 'new_status' in data:
                new_status = data['new_status']
                if new_status not in ['0', '1']:
                    return JsonResponse({
                        'status': 'error',
                        'message': '无效的状态值'
                    }, status=400)
                
                new_status = int(new_status)
                ac.set_status(new_status)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="airConditioner",
                    operation='turn on' if new_status == 1 else 'turn off'
                )

            # 修改设备名称（需要权限）
            if 'new_name' in data:
                if permission < 1:
                    return JsonResponse({
                        'status': 'error',
                        'message': '您没有权限修改设备名称'
                    }, status=403)
                
                new_name = data['new_name'].strip()
                if not new_name:
                    return JsonResponse({
                        'status': 'error',
                        'message': '设备名称不能为空'
                    }, status=400)
                
                old_name = ac.Device_name
                ac.set_name(new_name)
                Log.objects.create(
                    username=username,
                    devicename=old_name,
                    devicetype="airConditioner",
                    operation=f"rename to {new_name}"
                )

        # GET请求返回设备当前状态
        return JsonResponse({
            'status': 'success',
            'device': {
                'id': ac.Device_id,
                'name': ac.Device_name,
                'type': ac.Device_type,
                'status': ac.get_status(),
                'temperature': ac.get_temperature(),
                'mode': ac.get_mode(),
                'valid_modes': ['cool', 'heat', 'auto', 'dry', 'fan'],
                'min_temp': 16,
                'max_temp': 30
            }
        })

    except AirConditioner.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '空调设备不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)

"""
    curtain.html对应的逻辑
    逻辑基本与light一致，比light少了brightness
    若失败，status为error，提供各种错误信息
    若成功，status为success，返回当前窗帘的状态
"""
def curtain(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            device_name = data.get('device_name')
            username = data.get('username')

        if not device_name:
            return JsonResponse({
                'status': 'error',
                'message': '缺少设备名称参数'
            }, status=400)

        # 获取设备对象
        curtain = Curtain.objects.get(Device_name=device_name)
        permission = User.objects.get(username=username).get_permission()

        # 处理POST请求（设备控制）
        if request.method == 'POST':
            # 设置开关状态
            if 'new_status' in data:
                new_status = data['new_status']
                if new_status not in ['0', '1']:
                    return JsonResponse({
                        'status': 'error',
                        'message': '无效的状态值（0表示关闭，1表示打开）'
                    }, status=400)
                
                new_status = int(new_status)
                curtain.set_status(new_status)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="curtain",
                    operation='turn on' if new_status == 1 else 'turn off'
                )

            # 修改设备名称（需要权限）
            if 'new_name' in data:
                if permission < 1:
                    return JsonResponse({
                        'status': 'error',
                        'message': '您没有权限修改设备名称'
                    }, status=403)
                
                new_name = data['new_name'].strip()
                if not new_name:
                    return JsonResponse({
                        'status': 'error',
                        'message': '设备名称不能为空'
                    }, status=400)
                
                old_name = curtain.Device_name
                curtain.set_name(new_name)
                Log.objects.create(
                    username=username,
                    devicename=old_name,
                    devicetype="curtain",
                    operation=f"rename to {new_name}"
                )


        # GET请求返回设备当前状态
        return JsonResponse({
            'status': 'success',
            'device': {
                'id': curtain.Device_id,
                'name': curtain.Device_name,
                'type': curtain.Device_type,
                'status': curtain.get_status(),
            }
        })

    except Curtain.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '窗帘设备不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)

"""
    washingMachine.html对应的逻辑
    逻辑基本与light一致（注意mode）
    若失败则status为error，提供各种错误信息
    若成功则status为success，并提供当前设备的当前状态信息
    GET请求返回当前设备的各种状态信息
"""
def washingMachine(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            device_name = data.get('device_name')
            username = data.get('username')

        if not device_name:
            return JsonResponse({
                'status': 'error',
                'message': '缺少设备名称参数'
            }, status=400)

        # 获取设备对象
        wm = WashingMachine.objects.get(Device_name=device_name)
        permission = User.objects.get(username=username).get_permission()

        # 处理POST请求（设备控制）
        if request.method == 'POST':
            # 检查用户权限
            if permission < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限操作洗衣机设备',
                    'redirect': '/home/devices/'
                }, status=403)

            # 设置开关状态
            if 'new_status' in data:
                new_status = data['new_status']
                if new_status not in ['0', '1']:
                    return JsonResponse({
                        'status': 'error',
                        'message': '无效的状态值（0表示关闭，1表示打开）'
                    }, status=400)
                
                new_status = int(new_status)
                if new_status == 1:
                    wm.set_starttime(timezone.now())
                wm.set_status(new_status)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="washingMachine",
                    operation='turn on' if new_status == 1 else 'turn off'
                )

            # 设置洗衣模式
            if 'new_mode' in data:
                valid_modes = ['standard', 'quick', 'delicate', 'heavy', 'wool']
                new_mode = data['new_mode']
                if new_mode not in valid_modes:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'无效的洗衣模式，可选: {", ".join(valid_modes)}'
                    }, status=400)
                
                wm.set_mode(new_mode)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="washingMachine",
                    operation=f"set mode to {new_mode}"
                )

            # 修改设备名称
            if 'new_name' in data:
                new_name = data['new_name'].strip()
                if not new_name:
                    return JsonResponse({
                        'status': 'error',
                        'message': '设备名称不能为空'
                    }, status=400)
                
                old_name = wm.Device_name
                wm.set_name(new_name)
                Log.objects.create(
                    username=username,
                    devicename=old_name,
                    devicetype="washingMachine",
                    operation=f"rename to {new_name}"
                )

        # GET请求返回设备当前状态
        return JsonResponse({
            'status': 'success',
            'device': {
                'id': wm.Device_id,
                'name': wm.Device_name,
                'type': wm.Device_type,
                'status': wm.get_status(),
                'mode': wm.get_mode(),
                'valid_modes': ['standard', 'quick', 'delicate', 'heavy', 'wool'],
            }
        })

    except WashingMachine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '洗衣机设备不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)

"""
    robotvacuum.html对应的逻辑
    逻辑与light基本一致(注意mode)
    若失败，则status为error，返回各种错误信息
    成功则返回当前设备修改后的状态
    GET请求返回当前设备的状态
"""
def robotvacuum(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            device_name = data.get('device_name')
            username = data.get('username')

        if not device_name:
            return JsonResponse({
                'status': 'error',
                'message': '缺少设备名称参数'
            }, status=400)

        # 获取设备对象
        robot = Robotvacuum.objects.get(Device_name=device_name)
        permission = User.objects.get(username=username).get_permission()

        # 处理POST请求（设备控制）
        if request.method == 'POST':
            # 检查用户权限
            if permission < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限操作扫地机器人',
                    'redirect': 'home/devices/'
                }, status=403)

            # 设置开关状态
            if 'new_status' in data:
                new_status = data['new_status']
                if new_status not in ['0', '1']:
                    return JsonResponse({
                        'status': 'error',
                        'message': '无效的状态值（0表示关闭，1表示打开）'
                    }, status=400)
                
                new_status = int(new_status)
                robot.set_status(new_status)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="robotvacuum",
                    operation='turn on' if new_status == 1 else 'turn off'
                )

            # 设置清扫模式
            if 'new_mode' in data:
                valid_modes = ['auto', 'spot', 'edge', 'single_room', 'mop']
                new_mode = data['new_mode']
                if new_mode not in valid_modes:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'无效的清扫模式，可选: {", ".join(valid_modes)}'
                    }, status=400)
                
                robot.set_mode(new_mode)
                Log.objects.create(
                    username=username,
                    devicename=device_name,
                    devicetype="robotvacuum",
                    operation=f"set mode to {new_mode}"
                )

            # 修改设备名称
            if 'new_name' in data:
                new_name = data['new_name'].strip()
                if not new_name:
                    return JsonResponse({
                        'status': 'error',
                        'message': '设备名称不能为空'
                    }, status=400)
                
                old_name = robot.Device_name
                robot.set_name(new_name)
                Log.objects.create(
                    username=username,
                    devicename=old_name,
                    devicetype="robotvacuum",
                    operation=f"rename to {new_name}"
                )

            # return JsonResponse(response_data)

        # GET请求返回设备当前状态
        return JsonResponse({
            'status': 'success',
            'device': {
                'id': robot.Device_id,
                'name': robot.Device_name,
                'type': robot.Device_type,
                'status': robot.get_status(),
                'mode': robot.get_mode(),
                'valid_modes': ['auto', 'spot', 'edge', 'single_room', 'mop'],
            }
        })

    except Robotvacuum.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '扫地机器人不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)


"""
    habits.html处理逻辑
    第一次进入页面时为GET请求，返回当前用户的所有习惯（关键：devices_data）
    POST请求时，用户选择习惯名称，传入到后端并开启所有设备，最后返回设备信息列表(activated_devices)
"""
def habits(request):
    try:        
        # 处理POST请求（执行习惯）
        username = ""
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            habit_name = data.get('habit_name')
            username = data.get('username')
            
            if not habit_name:
                return JsonResponse({
                    'status': 'error',
                    'message': '请选择要执行的习惯'
                }, status=400)
            
            try:
                habit = Habits.objects.get(username=username, habit_name=habit_name)
                activated_devices = []
                
                for device in habit.favorite_devices.all():
                    # 开启设备
                    device.turn_on()
                    device_info = {
                        'name': device.Device_name,
                        'type': device.Device_type,
                        'status': device.get_status()
                    }
                    activated_devices.append(device_info)
                    
                    # 记录日志
                    Log.objects.create(
                        username=username,
                        devicename=device.Device_name,
                        devicetype=device.Device_type,
                        operation=f"通过习惯'{habit_name}'启动"
                    )
                
                return JsonResponse({
                    'status': 'success',
                    'message': f"习惯'{habit_name}'已执行",
                    'activated_devices': activated_devices
                })
                
            except Habits.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '找不到指定的习惯'
                }, status=404)

        # GET请求返回用户所有习惯
        user_habits = Habits.objects.filter(username=username)
        habits_data = []
        
        for habit in user_habits:
            devices_data = []
            for device in habit.favorite_devices.all():
                devices_data.append({
                    'id': device.Device_id,
                    'name': device.Device_name,
                    'type': device.Device_type,
                    'status': device.get_status() if hasattr(device, 'get_status') else None
                })
            
            habits_data.append({
                'id': habit.habit_id,
                'name': habit.habit_name,
                'created_at': habit.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'devices': devices_data
            })
        
        return JsonResponse({
            'status': 'success',
            'habits': habits_data,
            'username': username,
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'操作失败: {str(e)}'
        }, status=500)
        

"""
    add_habit.html逻辑
    检查各种条件是否满足，若不满足则status为error，message为错误信息
    POST请求时，前端提供各种设备名device_names（列表），之后创建一条habit记录
    GET请求时，返回所有设备的信息（关键：devices）
"""
def add_habit(request):
    try:        
        # 处理POST请求（创建新习惯）
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            selected_device_names = data.get('device_names', [])
            habit_name = data.get('habit_name', '').strip()
            username = data.get('username')
            permission = User.objects.get(username=username).get_permission()

            if permission < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限创建习惯',
                    'redirect': '/home/habits/'
                }, status=403)

            # 验证输入
            if not habit_name:
                return JsonResponse({
                    'status': 'error',
                    'message': '习惯名称不能为空'
                }, status=400)
                
            if not selected_device_names:
                return JsonResponse({
                    'status': 'error',
                    'message': '请至少选择一个设备'
                }, status=400)

            # 检查习惯是否已存在
            if Habits.objects.filter(username=username, habit_name=habit_name).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': '该习惯名称已存在'
                }, status=400)

            # 创建新习惯
            habit = Habits.objects.create(
                username=username,
                habit_name=habit_name
            )

            # 添加设备到习惯
            added_devices = []
            for device_name in selected_device_names:
                try:
                    device = Device.objects.get(Device_name=device_name)
                    habit.favorite_devices.add(device)
                    added_devices.append({
                        'id': device.Device_id,
                        'name': device.Device_name,
                        'type': device.Device_type
                    })
                    
                    Log.objects.create(
                        username=username,
                        devicename=device.Device_name,
                        devicetype=device.Device_type,
                        operation=f"添加到习惯'{habit_name}'"
                    )
                except Device.DoesNotExist:
                    continue

            return JsonResponse({
                'status': 'success',
                'message': '习惯创建成功',
                'habit': {
                    'name': habit.habit_name,
                    'device_count': len(added_devices)
                },
                'added_devices': added_devices
            })

        # GET请求返回所有可用设备
        devices = Device.objects.all()
        device_list = []
        
        for device in devices:
            device_list.append({
                'id': device.Device_id,
                'name': device.Device_name,
                'type': device.Device_type,
                'status': device.get_status() if hasattr(device, 'get_status') else None
            })
        
        return JsonResponse({
            'status': 'success',
            'devices': device_list,
            'username': username
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'创建习惯失败: {str(e)}'
        }, status=500)

"""
    delete_habit.html逻辑
    与add_habit类似
    当POST请求时，执行删除逻辑，并返回剩余的习惯记录(remaining_habits)
    当GET请求时，返回所有的习惯记录(habits_data)
"""
def delete_habit(request):
    try:
        # 处理POST请求（删除习惯）
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            habit_name = data.get('habit_name')
            username = data.get('username')
            permission = User.objects.get(username=username).get_permission()

            if permission < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': '您没有权限删除习惯',
                    'redirect': '/home/habits/'
                }, status=403)

            if not habit_name:
                return JsonResponse({
                    'status': 'error',
                    'message': '请提供要删除的习惯名称'
                }, status=400)

            try:
                habit = Habits.objects.get(username=username, habit_name=habit_name)
                
                # 记录删除日志
                for device in habit.favorite_devices.all():
                    Log.objects.create(
                        username=username,
                        devicename=device.Device_name,
                        devicetype=device.Device_type,
                        operation=f"从习惯'{habit_name}'中移除"
                    )
                
                # 删除习惯
                habit.delete()
                
                # 获取剩余习惯
                remaining_habits = list(Habits.objects.filter(username=username).values(
                    'habit_name'
                ))
                
                return JsonResponse({
                    'status': 'success',
                    'message': f"习惯'{habit_name}'已删除",
                    'remaining_habits': remaining_habits
                })
                
            except Habits.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': '找不到指定的习惯'
                }, status=404)

        # GET请求返回用户所有习惯
        habits = Habits.objects.filter(username=username)
        habits_data = []
        
        for habit in habits:
            habits_data.append({
                'id': habit.id,
                'name': habit.habit_name,
                'devices': habit.favorite_devices,
                'device_count': habit.favorite_devices.count(),
            })
        
        return JsonResponse({
            'status': 'success',
            'habits_data': habits_data,
            'username': username
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'删除习惯失败: {str(e)}'
        }, status=500)
