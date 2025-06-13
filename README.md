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

# 配置  
后端: Django  
前端: Vue  

为了解决跨域问题, 需要下载`django-cors-headers`包:  
```bash
pip install django-cors-headers -i https://pypi.tuna.tsinghua.edu.cn/simple
```

# 运行:  

运行后端  
```bash
pip install django-cors-headers==3.7.0
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

添加`tailwind css`组件
```bash
npm install -D tailwindcss postcss autoprefixer
```
如果还不能正常运行，则继续运行下面命令
```bash
npx tailwindcss@3.4.17 init -p
```

待办：
1. 添加设备时外键出错
2. 日志查询的用户名和过滤条件的用户名冲突（√ 已修复）
3. 添加/删除设备时，返回数据的username可能存在异常（√ 已修复）
3. 注册时的用户权限初始化问题（邀请码）（前端）
4. light修改亮度等时，数据库可以修改成功，但是日志查询不到，并且给前端返回error（√ 已修复）
5. 在admin修改名字时，Device正常，但其他设备的名字也同时被更改(√ 已修复)
6. 在curtain界面，修改设备名时方框无效，需要在上方弹出的提示框中填写（前端）
7. 空调、扫地机、洗衣机前端传入username和device_name为空（前端）
8. 洗衣机设置剩余时间，后端维护开始时间，前端计算剩余时间(若为关机状态，剩余时间应该为0)
9. 扫地机设置剩余电量、已清扫面积两个参数（怎么构建？）
10. 日志查询（query_logs）前端传入username有问题，第一次进入时username为空，点击重置之后才能获取到用户名（前端）