# SE-FINAL
app中存放各种类和函数

管理员： se 密码：123456


class User中加入get_user函数，通过用户名查询用户
class Log中， 加入operation字段（表示增加、去除、维修等）
class Log中， 修改类的表示形式，增加operation
class Log中， 修改添加日志操作，创建时初始化operation
class Device中，修改更改设备名，添加self
class Device中，增加根据设备名获取设备的操作
class AirConditioner中，修改除湿为"dry"
class washMachine中，补充turn_on操作
class robotvaccum中，补充turn_on操作
class Device中，补充获取设备状态的函数，返回设备状态（开/关）
model.py中添加habits类，维护用户使用习惯

to do:
User类中添加注册、用户身份认证？
Log的create_Log传参是否应该传入Log_id？（自动生成）
Device类中Device_user的作用？