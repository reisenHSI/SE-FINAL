# SE-FINAL
后端：

app中存放各种类和函数

管理员： se 密码：123456
尝试登录前端界面，账号：user1，密码：se123456

model.py大致框架已实现

完善了“页面跳转逻辑.png”

后端：

views.py中每一个函数对应页面跳转的一个方框

所有视图函数（views.py）传入和返回格式均为Json格式

后端返回的Json数据中绑定了status状态码，表示错误类型

完成urls的配置，与页面跳转相对应


前端：

建立了对应的vue文件

实现了主页，登录和注册

其他逻辑功能待完善

to do:

！！！页面渲染未成功待解决（6.9）

请参考views.py和urls.py中添加/删除/修改前端的文件

Devices陈列所有设备信息

DevicesDetail实现跳转到具体设备的逻辑

Light等具体设备的逻辑

添加/删除设备的逻辑

# 运行:  

运行后端  
```bash
cd SE
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
cd ..
```

运行前端  
```bash
cd frontend-project
npm install
npm run dev
```
