# views/merchant_views.py
from config import app, mysql_pwd, db_name, username, userRole  # 导入配置变量
from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename
import pymysql

from utils import allowed_file

merchant_blueprint = Blueprint('merchant', __name__)

# 商家查看菜品信息
@merchant_blueprint.route('/MerchantMenu', methods=['GET', 'POST'])
def MerchantMenu():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM DISHES WHERE restaurant = '%s'" % username

        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
    if request.method == 'POST':
        if request.form["action"] == "删除该菜品":
            dishname = request.form.get('dishname')
            rest = request.form.get('restaurant')
            print(rest)
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "DELETE FROM DISHES where dishname = '{}' and restaurant = '{}'".format(dishname, rest)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("菜品删除成功")
                dmsg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品删除失败")
                dmsg = "fail"
            return render_template('MerchantMenu.html', dishname=dishname, rest=rest, dmessages=dmsg)
        elif request.form["action"] == "按销量排序":
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY sales DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
        elif request.form["action"] == "按价格排序":
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY price DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)


# 商家修改菜品信息
@merchant_blueprint.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""

    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "修改菜品信息":
        dishname = request.form['dishname']  # 传递过去菜品名
        rest = request.form['restaurant']  # 传递过去商家名
        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = request.form.get('isSpecialty')
        # imagesrc = request.form['imagesrc']
        print(dishname)
        print(isSpecialty)
        print(type(isSpecialty))

        return render_template('MenuModify.html', dishname=dishname, rest=rest, dishinfo=dishinfo,
                               nutriention=nutriention, price=price, username=username, messages=msg,
                               isSpecialty=isSpecialty)
    elif request.form["action"] == "提交修改":

        dishname = request.form.get('dishname')
        rest = request.form.get('rest')

        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        filename = ''

        if f != '' and allowed_file(f.filename):
            filename = secure_filename(f.filename)

        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename

        print(isSpecialty)
        print(type(isSpecialty))
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        if filename == '':
            sql = "Update DISHES SET dishinfo = '{}', nutriention = '{}', price = {} , isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(
                dishinfo, nutriention, price, isSpecialty, dishname, rest)
        else:
            sql = "Update DISHES SET dishinfo = '{}', nutriention = '{}', price = {} ,imgsrc = '{}', isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(
                dishinfo, nutriention, price, imgsrc, isSpecialty, dishname, rest)
        print(sql)

        try:
            cursor.execute(sql)
            db.commit()
            print("菜品信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("菜品信息修改失败失败")
            msg = "fail"
        return render_template('MenuModify.html', dishname=dishname, rest=rest, username=username, messages=msg)


@merchant_blueprint.route('/MenuAdd', methods=['GET', 'POST'])
def MenuAdd():
    msg = ""
    rest = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "增加菜品":
        rest = request.form['restaurant']  # 传递过去商家名
        return render_template('MenuAdd.html', rest=rest)
    elif request.form["action"] == "确认增加":
        dishname = request.form.get('dishname')
        rest = request.form.get('rest')
        dishinfo = request.form.get('dishinfo')
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        f = request.files['imagesrc']
        print(f)
        isSpecialty = int(request.form.get('isSpecialty'))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')

        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from DISHES where dishname = '{}' ".format(dishname)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # 如果已经存在该商家
        if num == 1:
            print("失败！该菜品已经添加过！")
            msg = "fail1"
        else:
            sql2 = "insert into DISHES  values ('{}', '{}','{}', '{}',{}, {},'{}', {}) ".format(dishname, rest,
                                                                                                dishinfo, nutriention,
                                                                                                price, 0, imgsrc,
                                                                                                isSpecialty)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("菜品添加成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品添加失败")
                msg = "fail"
        return render_template('MenuAdd.html', messages=msg, username=username)


@merchant_blueprint.route('/MerchantIndex')
def Merchantindexpage():
    return render_template('MerchantIndex.html')


# 个人中心页面
@merchant_blueprint.route('/MerchantPersonal')
def MpersonalPage():
    return render_template('MerchantPersonal.html')


# 修改个人信息页面
@merchant_blueprint.route('/MerchantModifyPerInfo', methods=['GET', 'POST'])
def MerchantModifyPerInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPerInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']

        f = request.files['imagesrc']
        filename = ''

        if f != '' and allowed_file(f.filename):
            filename = secure_filename(f.filename)

        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename

        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        if filename == '':
            sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                            username)
        else:
            sql = "Update {} SET address = '{}', phone = '{}',img_res = '{}' where username = '{}'".format(userRole,
                                                                                                           address,
                                                                                                           phonenum,
                                                                                                           imgsrc,
                                                                                                           username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)


# 修改密码页面
@merchant_blueprint.route('/MerchantModifyPwd', methods=['GET', 'POST'])
def MerModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPwd.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库用户名root，密码空
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)


# 商家查看订单
@merchant_blueprint.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
