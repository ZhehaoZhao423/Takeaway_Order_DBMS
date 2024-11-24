# Takeaway_Order_DBMS
Based on：https://github.com/orion-orion/Takeaways-Order-Sys 

NIS3351 数据库原理及安全大作业

组员：孔珺晓 赵哲浩 毛锐

### 项目结构
```
├── README.md                 // 项目说明文档
├── app.py                    // 主程序入口
├── config.py                 // 配置文件
├── init.sql                  // 数据库初始化脚本
├── utils.py                  // 工具函数集合
├── static                    // 静态资源文件夹
│   ├── css                   // CSS样式文件
│   ├── fonts                 // 字体文件
│   ├── images                // 图片文件
│   ├── js                    // JavaScript脚本
├── templates                 // HTML模板文件夹
├── handlers                  // 逻辑处理模块
│   ├── __init__.py          // 初始化文件
│   ├── error_handlers.py    // 错误处理模块
├── views                     // 路由视图模块
│   ├── __init__.py          // 初始化文件
│   ├── admin_views.py       // 管理员视图
│   ├── merchant_views.py    // 商家视图
│   ├── user_views.py        // 用户视图
```
### 环境依赖
Python 3.9.10         
Flask 2.1.1              
PyMySQL 1.0.2              
MySQL 8.0.28             
### 快速启动
先以MySQL的root身份执行SQL脚本初始化数据库与数据表项(会提示输入root用户的登录密码)
```
mysql -uroot -p  < init.sql
```
或者逐步执行init.sql

然后将config.py中的mysql_pwd改为本地MySQL的root用户登录密码

最后执行Web服务启动程序
```
python app.py --mysql_pwd 123456 --db_name appDB
```
注意此处mysql_pwd也是你MySQL的root用户登录密码，db_name即你用init.sql创建的数据库名称。
