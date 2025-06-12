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


1. 添加设备时外键出错
2. 注册时的用户权限初始化问题（邀请码）
3. light修改亮度等时，数据库可以修改成功，但是日志查询不到，并且给前端返回error
