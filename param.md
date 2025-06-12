# 使用之前请先查看models.py文件，明确各属性信息。如：device_status是Integer，合法状态包括0、1、2


register:

## **用户注册**

- 请求方式：POST
- 请求URL：`/register`

### 请求参数（JSON Body）

| 字段名           | 类型   | 是否必填 | 描述                          |
|------------------|--------|----------|-------------------------------|
| username         | string | 是       | 用户名（唯一）                |
| password         | string | 是       | 密码（明文传输，后端加密存储）|
| phone            | string | 是       | 手机号                        |
| age              | int    | 是       | 年龄                          |
| registration_code| string | 否       | 注册码（默认空）              |

### 返回值

#### 成功响应（201 Created）
```json
{
    "status": "success",
    "message": "注册成功",
    "user": {
        "username": "john",
        "phone": "13800138000",
        "permission": 1
    }
}
```
#### 错误码：400、500



login：

## **用户登录**

- 请求方式：POST  
- 请求URL：`/login`  

### 请求参数（JSON Body）

| 字段名   | 类型   | 是否必填 | 描述               |
|----------|--------|----------|--------------------|
| username | string | 是       | 注册时的用户名     |
| password | string | 是       | 注册时的密码（明文）|

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "message": "登录成功",
    "user": {
        "username": "john",
        "permission": 1
    }
}
```
#### 错误码：400、404、500


logout：

## **用户登出**

- 请求方式：POST
- 请求URL：`/logout`

### 请求参数
无

### 返回值

- 状态码：200
- 响应体示例：
```json
{
    "status": "success",
    "message": "您已成功退出登录！"
}
```
#### 错误码：400（未登录状态）、500（服务器内部错误）


change_password：

## **修改密码**

- 请求方式：POST  
- 请求URL：`/change_password`  

### 请求参数（JSON Body）

| 参数名             | 类型   | 是否必填 | 描述                     |
|--------------------|--------|----------|--------------------------|
| username           | string | 是       | 要修改密码的用户名       |
| old_password       | string | 是       | 当前密码（明文）         |
| new_password       | string | 是       | 新密码（明文）           |
| confirm_new_password| string | 是       | 确认新密码（明文）       |

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "message": "密码修改成功，请重新登录"
}
```
#### 错误码：400、404、500


home:

## **获取主页信息**

- 请求方式：GET  
- 请求URL：`/home`  

### 请求参数
无

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "data": {
        "username": "john",
        "permission": 1,
        "menu_options": [
            {"name": "设备管理", "url": "/home/devices/"},
            {"name": "设备增删", "url": "/home/add_delete/"},
            {"name": "日志查询", "url": "/home/query_logs/"},
            {"name": "一键习惯", "url": "/home/habits/"},
            {"name": "退出登录", "url": "/logout/"}
        ]
    }
}
```
#### 错误码：401


add_delete：

## **设备增删页面**

- 请求方式：GET  
- 请求URL：`/home/add_delete`  

### 请求参数
无

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "data": {
        "page_title": "设备管理",
        "options": [
            {
                "name": "添加设备",
                "url": "/home/add_delete/add_device/",
                "description": "添加新设备到系统"
            },
            {
                "name": "删除设备",
                "url": "/home/add_delete/delete_device/",
                "description": "从系统中移除设备"
            }
        ],
        "username": "john"
    }
}
```
#### 错误码：401


add_device：

## **添加设备**

- 请求方式：POST  
- 请求URL：`/home/add_delete/add_device/`  

### 请求参数（JSON Body）

| 参数名                 | 类型   | 是否必填 | 描述      |
|---------------------|--------|----------|-----------|
| device_name         | string | 是       | 设备名称  |
| device_type         | string | 是       | 设备类型  |
| username            | string | 是       | 当前用户名 |

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "message": "设备添加成功",
    "device": {
        "id": 101,  # 设备ID
        "name": "客厅灯", # 设备名称
        "type": "Light"  # 设备类型
    }
}
```
- 请求方式：POST  
```json
{
    "status": "success",
    "device_types": ["Light", "WashingMachine", "Robotvacuum", "AirConditioner", "Curtain"],
    "devices": [
        {"Device_id": 1, "Device_name": "主卧灯", "Device_type": "Light"},
        {"Device_id": 2, "Device_name": "洗衣机", "Device_type": "WashingMachine"}
    ],
    "username": "john"
}
```
#### 错误码：400、401、403、500


delete_device：


## **删除设备**

- 请求方式：POST  
- 请求URL：`/home/add_delete/delete_device/`  

### 请求参数（JSON Body）

| 参数名         | 类型     | 是否必填 | 描述         |
|-------------|--------|----------|------------|
| device_name | string | 是       | 要删除的设备ID名字 |
| username    | string | 是       | 用户名        |

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "message": "成功删除 2 个设备",
    # 删除的设备信息
    "deleted_devices": [
        {
            "name": "客厅灯",
            "type": "Light"
        },
        {
            "name": "主卧空调",
            "type": "AirConditioner"
        }
    ],
    # 剩余的设备信息
    "remaining_devices": [
        {
            "Device_id": 103,
            "Device_name": "厨房灯",
            "Device_type": "Light"
        }
    ]
}

- 请求方式：GET 
{
    "status": "success",
    # 所有设备信息
    "devices": [
        {
            "Device_id": 101,
            "Device_name": "客厅灯",
            "Device_type": "Light"
        },
        {
            "Device_id": 102,
            "Device_name": "主卧空调",
            "Device_type": "AirConditioner"
        }
    ],
    "username": "john"
}
```
#### 错误码：400、401、403、500

query_logs：

## **查询日志**

- 请求方式：POST（筛选）/ GET（获取全部）  
- 请求URL：`/home/query_logs/`  

### 请求参数（JSON Body - POST筛选时）

| 参数名       | 类型   | 是否必填 | 描述                     |
|--------------|--------|----------|--------------------------|
| username     | string | 否       | 按用户名查询         |
| devicename   | string | 否       | 按设备名查询         |
| start_time   | string | 否       | 开始时间（YYYY-MM-DD）   |
| end_time     | string | 否       | 结束时间（YYYY-MM-DD）   |

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "logs": [
        {
            "id": 1,
            "username": "john",
            "device_name": "客厅灯",
            "device_type": "Light",
            "operation": "add",
            "timestamp": "2023-10-01 14:30:22",
            "formatted_operation": "john add 客厅灯(Light)"
        },
        {
            "id": 2,
            "username": "mary",
            "device_name": "主卧空调",
            "device_type": "Airconditioner",
            "operation": "delete",
            "timestamp": "2023-10-02 16:30:22",
            "formatted_operation": "mary delete 主卧空调(Airconditioner)"
        }
    ],
    "total_count": 15,
    "filter_options": {
        "usernames": ["john", "mary"],
        "devicenames": ["客厅灯", "主卧空调"]
    }
}
```
#### 错误码：400、401、403、500


devices:
## **获取设备列表**

- 请求方式：GET  
- 请求URL：`/home/devices/`  

### 请求参数
无

### 返回值

#### 成功响应（200 OK）
```json
{
    "status": "success",
    "device_categories": [
        {
            "type": "Light",
            "type_name": "灯光设备",
            "icon": "lightbulb",
            "endpoint": "/api/light/",
            "devices": [
                {
                    "id": 1,
                    "name": "客厅灯",
                    "status": 0,  // 0表示关闭
                    "endpoint": "/api/light/"
                }
            ]
        },
        {
            "type": "AirConditioner",
            "type_name": "空调设备",
            "icon": "ac-unit",
            "endpoint": "/api/airConditioner/",
            "devices": [
                {
                    "id": 2,
                    "name": "主卧空调",
                    "status": 1,  // 1表示打开
                    "endpoint": "/api/airConditioner/"
                }
            ]
        }
    ],
    "username": "john",
    "permission": 1
}
```
#### 错误码：401、500


# 以下五个设备GET和POST请求返回的结果一致，都是设备最新的状态信息

light：

## **灯光设备控制**

- 请求方式：GET（查询状态）/ POST（控制设备）  
- 请求URL：`/home/devices/light/`  

### 请求参数

#### GET请求
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| device_name  | string | 是       | 灯光设备名称 |

#### POST请求（JSON Body）
| 参数名          | 类型   | 是否必填 | 描述              | 有效值               |
|-----------------|--------|----------|-----------------|----------------------|
| device_name     | string | 是       | 灯光设备名称      |                     |
| new_status      | string | 否       | 设置开关状态      | 0/1                 |
| new_brightness  | int    | 否       | 设置亮度值        | 0-100之间的整数      |
| new_name        | string | 否       | 修改设备名称      | 非空字符串           |

### 返回值

#### 成功响应（200 OK）
1. GET请求响应：
```json
{
    "status": "success",
    "device": {
        "id": 1,
        "name": "客厅灯",
        "type": "Light",
        "status": 1,
        "brightness": 80,
    }
}
```
2. POST请求响应：
```json
{
    "status": "success",
    "message": "操作成功",
    "device": {
        "name": "客厅灯",
        "type": "Light"
    },
    "changes": {
        "status": 1,
        "brightness": 75
    }
}
```
#### 错误码：401、404、400、500


airConditioner：
## **空调设备控制**

- 请求方式：GET（查询状态）/ POST（控制设备）  
- 请求URL：`/home/devices/airConditioner/`  

### 请求参数

#### GET请求
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| device_name  | string | 是       | 空调设备名称 |

#### POST请求（JSON Body）
| 参数名          | 类型   | 是否必填 | 描述                     | 有效值/范围           |
|-----------------|--------|----------|--------------------------|-----------------------|
| device_name     | string | 是       | 空调设备名称             |                       |
| new_status      | string | 否       | 设置开关状态             | '0'(关)/'1'(开)       |
| new_temperature | int    | 否       | 设置温度值               | 16-30之间的整数       |
| new_mode        | string | 否       | 设置运行模式             | cool/heat/auto/dry/fan|
| new_name        | string | 否       | 修改设备名称             | 非空字符串            |

### 返回值

#### 成功响应（200 OK）
1. GET/POST请求响应：
```json
{
    "status": "success",
    "device": {
        "id": 2,
        "name": "主卧空调",
        "type": "AirConditioner",
        "status": 1,
        "temperature": 25,
        "mode": "cool",
        "valid_modes": ["cool", "heat", "dry"],
        "min_temp": 16,
        "max_temp": 30
    }
}
```
#### 错误码：400、401、403、404、500

curtain:

## **窗帘设备控制**

- 请求方式：GET（查询状态）/ POST（控制设备）  
- 请求URL：`/home/devices/curtain/`  

### 请求参数

#### GET请求
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| device_name  | string | 是       | 窗帘设备名称 |

#### POST请求（JSON Body）
| 参数名          | 类型   | 是否必填 | 描述                     | 有效值/范围           |
|-----------------|--------|----------|--------------------------|-----------------------|
| device_name     | string | 是       | 窗帘设备名称             |                       |
| new_status      | string | 否       | 设置开关状态             | 0/1                   |
| new_name        | string | 否       | 修改设备名称             | 非空字符串            |

### 返回值

#### 成功响应（200 OK）
1. GET/POST请求响应：
```json
{
    "status": "success",
    "device": {
        "id": 3, # 请使用name，不要使用id
        "name": "主卧窗帘",
        "type": "Curtain",
        "status": 1,
    }
}
```
#### 错误码：400、401、403、404、500


washingMachine:

## **洗衣机设备控制**

- 请求方式：GET（查询状态）/ POST（控制设备）  
- 请求URL：`/home/devices/washingMachine/`  

### 请求参数

#### GET请求
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| device_name  | string | 是       | 洗衣机设备名称 |

#### POST请求（JSON Body）
| 参数名          | 类型   | 是否必填 | 描述                     | 有效值/范围           |
|-----------------|--------|----------|--------------------------|-----------------------|
| device_name     | string | 是       | 洗衣机设备名称           |                       |
| new_status      | string | 否       | 设置开关状态             | '0'(停止)/'1'(启动)   |
| new_mode        | string | 否       | 设置洗衣模式             | standard/quick/delicate/heavy/wool |
| new_name        | string | 否       | 修改设备名称             | 非空字符串            |

### 返回值

#### 成功响应（200 OK）
1. GET/POST请求响应：
```json
{
    "status": "success",
    "device": {
        "id": 4,
        "name": "主卧洗衣机",
        "type": "WashingMachine",
        "status": 1,
        "mode": "standard",
        "valid_modes": ["standard", "quick", "delicate", "heavy", "wool"],
    }
}
```
#### 错误码：400、401、403、404、500


robotvacuum:

## **扫地机器人控制**

- 请求方式：GET（查询状态）/ POST（控制设备）  
- 请求URL：`/home/devices/robotvacuum/`  

### 请求参数

#### GET请求
| 参数名       | 类型   | 是否必填 | 描述           |
|--------------|--------|----------|----------------|
| device_name  | string | 是       | 扫地机器人名称 |

#### POST请求（JSON Body）
| 参数名          | 类型   | 是否必填 | 描述                     | 有效值/范围           |
|-----------------|--------|----------|--------------------------|-----------------------|
| device_name     | string | 是       | 扫地机器人设备名称           |                       |
| new_status      | string | 否       | 设置开关状态             | 0/1/2                   |
| new_mode        | string | 否       | 设置清扫模式             | standard/quick/delicate/heavy/wool |
| new_name        | string | 否       | 修改设备名称             | 非空字符串            |

### 返回值

#### 成功响应（200 OK）
1. GET/POST请求响应：
```json
{
    "status": "success",
    "device": {
        "id": 5,
        "name": "客厅扫地机器人",
        "type": "Robotvacuum",
        "status": 1,
        "mode": "sweep",
        "valid_modes": ["auto", "spot", "edge", "single_room", "mop"],
    }
}
```
#### 错误码：400、401、403、404、500

habits：

## **一键习惯功能**

- 请求方式：GET（查询习惯）/ POST（执行习惯）  
- 请求URL：`/home/habits/`  

### 请求参数

#### GET请求
无

#### POST请求（JSON Body）
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| habit_name   | string | 是       | 习惯名称   |

### 返回值

#### 成功响应（200 OK）
1. GET请求响应（获取用户所有习惯）：
```json
{
    "status": "success",
    "habits": [
        {
            "id": 1,
            "name": "回家模式",
            "created_at": "2023-10-15 08:30:00",
            "devices": [
                {
                    "id": 1,
                    "name": "客厅灯",
                    "type": "Light",
                    "status": "1"
                },
                {
                    "id": 2,
                    "name": "主卧空调",
                    "type": "AirConditioner",
                    "status": "1"
                }
            ]
        }
    ],
    "username": "john"
}
```
2. POST请求响应（执行习惯）：
```json
{
    "status": "success",
    "message": "习惯'回家模式'已执行",
    # 打开的设备
    "activated_devices": [
        {
            "name": "客厅灯",
            "type": "Light",
            "status": 1
        },
        {
            "name": "主卧空调",
            "type": "AirConditioner",
            "status": 1
        }
    ]
}
```
#### 错误码：400、401、404、500


add_habit：

## **添加新习惯**

- 请求方式：GET（获取可用设备）/ POST（创建习惯）  
- 请求URL：`/home/habits/add_habit/`  

### 请求参数

#### GET请求
无

#### POST请求（JSON Body）
| 参数名            | 类型   | 是否必填 | 描述                     |
|-------------------|--------|----------|--------------------------|
| habit_name        | string | 是       | 新习惯名称               |
| device_names      | array  | 是       | 要包含的设备名称数组      |

### 返回值

#### 成功响应（200 OK）
1. GET请求响应（获取所有设备）：
```json
{
    "status": "success",
    "devices": [
        {
            "id": 1,
            "name": "客厅灯",
            "type": "Light",
            "status": 1
        },
        {
            "id": 2,
            "name": "主卧空调",
            "type": "AirConditioner",
            "status": 1
        }
    ],
    "username": "john"
}
```
2. POST请求响应（创建新习惯）：
```json
{
    "status": "success",
    "message": "习惯创建成功",
    "habit": {
        "name": "回家模式",
        "device_count": 2
    },
    "added_devices": [
        {
            "id": 1,
            "name": "客厅灯",
            "type": "Light"
        },
        {
            "id": 2,
            "name": "主卧空调",
            "type": "AirConditioner"
        }
    ]
}
```
#### 错误码：400、401、404、500


delete_habit：

## **删除习惯**

- 请求方式：GET（获取习惯列表）/ POST（删除习惯）  
- 请求URL：`/home/habits/delete/`  

### 请求参数

#### GET请求
无

#### POST请求（JSON Body）
| 参数名       | 类型   | 是否必填 | 描述       |
|--------------|--------|----------|------------|
| habit_name   | string | 是       | 要删除的习惯名称 |

### 返回值

#### 成功响应（200 OK）
1. GET请求响应（获取所有习惯）：
```json
{
    "status": "success",
    "habits_data": [
        {
            "id": 1,
            "name": "回家模式",
            "devices": [
                {
                    "Device_id": 1,
                    "Device_name": "客厅灯",
                    "Device_type": "Light"
                },
                {
                    "Device_id": 2,
                    "Device_name": "主卧空调",
                    "Device_type": "AirConditioner"
                }
            ],
            "device_count": 2
        }
    ],
    "username": "john"
}
```
2. POST请求响应（删除习惯）：
```json
{
    "status": "success",
    "message": "习惯'回家模式'已删除",
    "remaining_habits": [
        {
            "habit_name": "睡眠模式"
        }
        {
            "habit_name": "工作模式"
        }
    ]
}
```





