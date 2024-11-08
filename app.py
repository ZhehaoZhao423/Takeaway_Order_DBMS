# -*- coding=utf-8 -*-
# app.py
from flask import Flask
import config
# 从 views 包导入所有视图函数
import views
# 从 handlers 包导入所有错误处理函数
import handlers
from utils import parse_args
import sys
import importlib
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER  # 你可以在此设置相关配置
app.config['DEBUG'] = True
importlib.reload(sys)

@app.errorhandler(404)
def page_not_found(e):
    return handlers.page_not_found(e)

# 注册蓝图
views.register_blueprints(app)

if __name__ == '__main__':
    args = parse_args()
    mysql_pwd = args.mysql_pwd
    db_name = args.db_name
    app.run(host='localhost', port='9090')
