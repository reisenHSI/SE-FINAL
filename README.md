# SE-FINAL

该文档将介绍项目逻辑、运行命令及注意事项。在进行项目之前，请先阅读该文档！！！

加入仓库后，第一次执行之前，请使用以下命令将项目克隆到本地。
```bash
git clone https://github.com/reisenHSI/SE-FINAL.git
```

## 项目结构
采用前后端分离进行开发，前端采用vue3框架，后端采用Django框架。运行时请使用两个终端分别运行。

vue3框架：frontend-project

Django框架：SE

## 前端

在运行vue之前，请先下载并安装node.js，官网下载即可。

运行前端项目：
```bash
cd frontend-project
npm install
npm install -D tailwindcss postcss autoprefixer
npm run dev
```
第一次运行时，请运行上面的所有命令构建项目。之后的运行，可以只执行下面的命令：
```bash
cd frontend-project
npm run dev
```

### 注意事项
如果`tailwind css`组件还不能正常运行，则继续运行下面命令
```bash
npx tailwindcss@3.4.17 init -p
```

## 后端

为了解决跨域问题,首先需要下载`django-cors-headers`包, 终端运行: 
```bash
pip install django-cors-headers -i https://pypi.tuna.tsinghua.edu.cn/simple
```

运行后端项目：
```bash
cd SE
python manage.py migrate
python manage.py runserver
```

在第一次运行时，请运行上面的完整命令。后续运行可以只执行：
```bash
cd SE
python manage.py runserver
```

### 注意事项
为避免各主机之间的数据库db.sqlite3文件冲突，在项目中设置了git不追踪该文件，已经提供了migrations文件夹。在第一次拉取项目时，请按上面的命令执行，如果失败（未找到SE/db.sqlite3文件），请尝试下面的命令：
```bash
cd SE
python manage.py makemigrations app
python manage.py migrate
python manage.py runserver
```
运行成功之后，将创建数据库db.sqlite3文件，并启动服务器。

虽然设置了不追踪文件提交，但如果遇到意外情况（pull的时候提示dbsqlite3文件冲突），请勿上传本地文件到仓库中！！！

如果希望创建超级用户，请运行下面的命令：
```bash
python manage.py createsuperuser
```
并按照提示创建用户，之后可以进入到127.0.0.1:8000/admin访问后台。




## 待办：
1. 添加设备时外键出错 （√ 已修复）
2. 日志查询的用户名和过滤条件的用户名冲突（√ 已修复）
3. 添加/删除设备时，返回数据的username可能存在异常（√ 已修复）
3. 注册时的用户权限初始化问题（邀请码）（前端） （√ 已修复）
4. light修改亮度等时，数据库可以修改成功，但是日志查询不到，并且给前端返回error（√ 已修复）
5. 在admin修改名字时，Device正常，但其他设备的名字也同时被更改(√ 已修复)
6. 在curtain界面，修改设备名时方框无效，需要在上方弹出的提示框中填写（前端）（√ 已修复）
7. 空调、扫地机、洗衣机前端传入username和device_name为空（前端）（√ 已修复）
8. 洗衣机设置剩余时间，后端维护开始时间，前端计算剩余时间(若为关机状态，剩余时间应该为0)
9. 扫地机设置剩余电量、已清扫面积两个参数（怎么构建？）（√ 已修复）
10. 日志查询（query_logs）前端传入username有问题，第一次进入时username为空，点击重置之后才能获取到用户名（前端） （√ 已修复）
11. 修改密码功能异常 （√ 已修复）
12. 日志查询中设备名的过滤条件有误 （√ 已修复）
13. 修改habit和robotvacuum字段，并重建数据库（后端） （√ 已修复）
14. 修改habit函数 （√ 已修复）