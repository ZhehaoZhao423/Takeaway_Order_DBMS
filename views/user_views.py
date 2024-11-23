# views/user_views.py
from flask import render_template, request, Blueprint
import pymysql
from config import mysql_pwd, db_name, username

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
@user_blueprint.route('/index')
# 首页
def indexpage():
    return render_template('index.html')


# 注册
@user_blueprint.route('/register', methods=['GET', 'POST'])
def registerPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('Register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        addr = request.form.get('addr')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')

        if userRole == 'RESTAURANT':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from RESTAURANT where username = '{}' ".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已经存在该商家
            if num == 1:
                print("失败！商家已注册！")
                msg = "fail1"
            else:
                sql2 = "insert into RESTAURANT (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("商家注册成功")
                    msg = "done1"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail1"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from CUSTOMER where username = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已存在该用户
            if num == 1:
                print("用户已注册！请直接登录。")
                msg = "fail2"
            else:
                sql2 = "insert into CUSTOMER (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("商家注册成功")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail2"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)


# 登录
@user_blueprint.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('logIn.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')

        if userRole == 'ADMIN':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from ADMIN where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该管理员且密码正确
            if num == 1:
                print("登录成功！欢迎管理员！")
                msg = "done1"
            else:
                print("您没有管理员权限或登录信息出错。")
                msg = "fail1"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'RESTAURANT':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from RESTAURANT where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该商家且密码正确
            if num == 1:
                print("登录成功！欢迎商家用户！")
                msg = "done2"
            else:
                print("您没有商家用户权限或登录信息出错。")
                msg = "fail2"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from CUSTOMER where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该用户且密码正确
            if num == 1:
                print("登录成功！欢迎用户！")
                # print("login user: ",username)
                msg = "done3"
            else:
                print("您没有用户权限，未注册或登录信息出错。")
                msg = "fail3"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)


#选择商家进入菜单列表
@user_blueprint.route('/Menu',methods=['GET', 'POST'])
def menu():
    msg = ""
    global restaurant
    if request.form["action"] == "进入本店":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM DISHES WHERE restaurant = '%s'" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "特色菜":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' AND isSpecialty = 1" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "按销量排序":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY sales DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "按价格排序":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY price DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)

#查看商家评论
@user_blueprint.route('/ResComment',methods=['GET','POST'])
def resComment():
    msg = ""
    global restaurant
    if request.form["action"] == "查看评价":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 1 AND text <> '' "% restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('ResComment.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('ResComment.html', username=username, RESTAURANT=restaurant, messages=msg)


# 购物车
@user_blueprint.route('/myOrder',methods=['GET', 'POST'])
def shoppingCartPage():
    global username
    print("global user:",username)
    if request.method == 'GET':
        print("myOrder-->GET")
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('myOrder.html', username=username, messages=msg)
    elif request.method == 'POST':
        print("Received POST data:", request.form)
        if request.form["action"] == "加入购物车":
            print("myOrder-->加入购物车")
            restaurant = request.form['restaurant']
            dishname = request.form['dishname']
            price = (float)(request.form['price'])
            img_res = request.form['img_res']
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            print("shopping user: ",username)
            sql1 = "insert into  SHOPPINGCART (username,restaurant,dishname,price,img_res) values ('{}','{}','{}',{},'{}') ".format(username,restaurant,dishname,price,img_res)
            cursor.execute(sql1)
            sql = "SELECT * FROM SHOPPINGCART"
            cursor.execute(sql)
            res = cursor.fetchall()
            if len(res) != 0:
                msg = "done"
                print(msg)
                print(len(res))
                return render_template('myOrder.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('myOrder.html', username=username, messages=msg)

        elif request.form["action"] == "结算":
            print("结算啦")
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            '''
            这下面
            '''
            restaurant = request.form['restaurant']
            print(restaurant)
            dishname = request.form['dishname']
            price = request.form['price']
            img_res = request.form['img_res']
            mode = request.form['mode']
            print("************************************************")
            print("==*==")
            print(mode)

            if mode == 1:
                print("堂食")

            else:
                print("外送")
            return render_template('index.html')
        else:
            print("咋回事")
            return render_template('index.html')


# 个人中心页面
@user_blueprint.route('/personal')
def personalPage():
    return render_template('personal.html')


# 修改个人信息页面
@user_blueprint.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
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
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username)


# 修改密码页面
@user_blueprint.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    global username
    print("username:",username)
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username)
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
            return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username)


@user_blueprint.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
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
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username, messages=msg)
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
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg)
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
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
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
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print("用户要确认收货啦")
        orderID = request.form['orderID']
        print(orderID)
        sql1 = "Update ORDER_COMMENT SET isFinished = 1, text = '' WHERE orderID = '%s' " % orderID
        print(sql1)
        cursor.execute(sql1)
        db.commit()

        sql2 = "select * from ORDER_COMMENT WHERE orderID = '%s' " % orderID
        cursor.execute(sql2)
        res1 = cursor.fetchone()
        restaurant = res1[1]
        dishname = res1[2]
        print("{} {} 销量+1".format(dishname, restaurant))

        sql = "Update DISHES SET sales = sales+1 WHERE dishname = '{}' AND restaurant = '{}'" .format(dishname, restaurant)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        msg = "UpdateSucceed"
        return render_template('OrderPage.html', username=username, messages=msg)

    else:
        return render_template('OrderPage.html', username=username, messages=msg)


@user_blueprint.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
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
        # 查询未完成及未评论订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' and isFinished = 1 and text <> '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "待评价订单":
        # 未评价订单跳转到写评论中
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print("MyCommentsPage - 未评价订单: {}".format(len(res)))
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("MyCommentsPage - 待评价订单 - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=len(res))

    else:
        return render_template('MyComments.html', username=username, messages=msg)


@user_blueprint.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    msg=""
    if request.method == 'GET':
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        # presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        # cursor.execute(presql)
        # res1 = cursor.fetchall()
        # notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - GET - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按交易时间排序":
        # TODO: 排序之后显示的是空的，不显示的问题没有解决
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print(username)
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - 按交易时间排序 -NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("WriteCommentsPage - 按价格排序 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("WriteCommentsPage - 未完成订单 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('WriteComments.html', username=username, messages=msg)


@user_blueprint.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "写评论":
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "提交评论":
        print("提交评论!")
        orderID = request.form.get('orderID')
        c_rank = request.form.get('rank')
        text = request.form.get('text')
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update ORDER_COMMENT SET text = '{}', c_rank = {} where orderID = '{}'".format(text, c_rank, orderID)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("用户评论成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("用户评论失败")
            msg = "fail"
        return render_template('CommentForm.html', messages = msg, username=username)
