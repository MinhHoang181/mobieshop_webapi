from flask import Blueprint, request, jsonify
from ..tools import password, verify_password, generate_jwt_customer, token_required_customer
from .. import mysql
import MySQLdb.cursors
from ..models import Customer

customer = Blueprint("customer", __name__)

#############################
# CHỨC NĂNG CỦA KHÁCH HÀNG #
###########################

# Đăng nhập
#------------------------------------------
@customer.route("/login", methods=["POST"])
def login():
    loggedin = False
    user = []
    msg = ""
    access_token = ""
    if request.method == "POST":

        data = request.json if request.json else []

        customer_name = data["customer_name"] if "customer_name" in data else ""
        customer_password = data["customer_password"] if "customer_password" in data else ""

        if customer_name == "":
            msg = "Customer name is missing"
        elif customer_password == "":
            msg = "Customer password is missing"
        else:
        # ket noi database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_name = % s', (
                    customer_name,)
            )
            account = cursor.fetchone()
            mysql.connection.commit()
            cursor.close()

            if not account:
                msg = "Username is not exits"
            elif not verify_password(account["customer_password"], customer_password):
                msg = "Password is not correct"
            # neu dung tai khoan trong DB
            else:
                loggedin = True
                user = {
                    "customer_id": account["customer_id"],
                    "customer_name": account["customer_name"],
                }
                access_token = generate_jwt_customer(account["customer_name"])
    return jsonify(loggedin=loggedin, msg=msg, access_token=access_token, user=user)

# Đăng ký
#---------------------------------------------
@customer.route("/register", methods=["POST"])
def register():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        customer_name = data["customer_name"] if "customer_name" in data else None
        customer_password = data["customer_password"] if "customer_password" in data else None
        customer_address = data["customer_address"] if "customer_address" in data else None
        customer_phone = data["customer_phone"] if "customer_phone" in data else None

        if not customer_name:
            msg = "Customer name is missing"
        elif not customer_password:
            msg = "Customer password is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_name = % s', (customer_name, ))
            account = cursor.fetchone()
            if account:
                msg = "Account already exists !"
            else:
                cursor.execute(
                    'INSERT INTO customers_account VALUES (NULL, % s, % s, % s, % s)', (customer_name, password(customer_password), customer_address, customer_phone, ))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully registered !"

    return jsonify(status=status, msg=msg)

# Xem thông tin cá nhân
#--------------------------------------------
@customer.route("/profile", methods=["GET"])
@token_required_customer
def profile(current_user):
    status = False
    msg = ""
    if request.method == "GET":
        current_user = Customer(current_user)
        user = {
            "customer_id" : current_user.id,
            "customer_name" : current_user.name,
            "customer_address" : current_user.address,
            "customer_phone" : current_user.phone
        }
        status = True
    return jsonify(status=status, msg=msg, user=user)

# sửa thông tin của khách hàng request
# - truyền json biến nào cần thay đổi
#-------------------------------------------------
@customer.route("/profile/edit", methods=["POST"])
@token_required_customer
def edit_profile_customer(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        current_user = Customer(current_user)

        data = request.json if request.json else []

        customer_address = data["customer_address"] if "customer_address" in data else None
        customer_phone = data["customer_phone"] if "customer_phone" in data else None

        if not customer_address:
            customer_address = current_user.address
        if not customer_phone:
            customer_phone = current_user.phone

        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE customers_account SET customer_address = % s, customer_phone = % s WHERE customer_id = % s', (
                customer_address, customer_phone, current_user.id,)
        )
        mysql.connection.commit()
        cursor.close()

        status = True
        msg = "Your info has been updated!"

    return jsonify(status=status, msg=msg)
