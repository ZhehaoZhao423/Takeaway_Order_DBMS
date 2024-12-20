# views/admin_views.py
from config import app, mysql_pwd, db_name, username  # 导入配置变量
import config
from flask import render_template, request, Blueprint
import pymysql

admin_blueprint = Blueprint('admin', __name__)

# 管理员的店铺列表页面
@admin_blueprint.route('/adminRestList', methods=['GET', 'POST'])
def adminRestListPage():
    msg = ""
    username = config.username
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM RESTAURANT"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminRestList.html', username=username, messages=msg)
    elif request.form["action"] == "移除":
        RESTName = request.form.get('RESTName')
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # TODO: 点击移除后显示移除成功，但数据库里没有删掉
        # 删除DISHES的
        sql1 = "DELETE FROM DISHES WHERE restaurant = '{}'".format(RESTName)
        cursor.execute(sql1)
        db.commit()
        # 删除订单表里的
        sql2 = "DELETE FROM ORDER_COMMENT WHERE restaurant = '{}'".format(RESTName)
        cursor.execute(sql2)
        db.commit()
        # # 删除shoppingCart的
        # sql3 = "DELETE FROM WHERE restaurant = '{}'".format(RESTName)
        # cursor.execute(sql3)
        db.commit()
        # 删除restaurant的
        sql4 = "DELETE FROM RESTAURANT WHERE username = '{}'".format(RESTName)
        cursor.execute(sql4)
        db.commit()
        print(sql4)

        msg = "delete"
        print(msg)

        return render_template('adminRestList.html', username=username, messages=msg)


# 管理员查看评论列表
@admin_blueprint.route('/adminCommentList', methods=['GET', 'POST'])
def adminCommentPage():
    msg = ""
    username = config.username
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 and text <> ''"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminCommentList.html', username=username, messages=msg)
    elif request.form["action"] == "按评分升序排列":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 AND text is not null Order BY c_rank"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('adminCommentList.html', username=username, messages=msg)

# 用户登录后显示商家列表
@admin_blueprint.route('/UserRestList',methods=['GET', 'POST'])
def UserRestListPage():
    msg = ""
    username = config.username
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM RESTAURANT"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('UserRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('UserRestList.html', username=username, messages=msg)
