# Takeaway_Order_DBMS
Based on：https://github.com/orion-orion/Takeaways-Order-Sys 

NIS3351 数据库原理及安全大作业

组员：孔珺晓 赵哲浩 毛锐

### 项目结构
```
├── static             //网页静态资源
│ ├── css             //css样式配置
│ ├── fonts            //字体配置
│ ├── images           //图片文件
│ ├── js              //javascript脚本文件
├── templates           //基于jinja2编写的HTML模板文件
├── app.py             //Web服务启动程序
├── config.py           //配置文件
└── README.md           //help
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
