# handlers/error_handlers.py
from config import app  # 导入配置变量
from flask import render_template

#404跳转
def page_not_found(error):
    return render_template("404.html"), 404