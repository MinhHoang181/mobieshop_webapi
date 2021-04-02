from flask import Blueprint, request, jsonify
from app.tools import token_required_admin, verify_password, generate_jwt_admin
from app import mysql
import MySQLdb.cursors
from app.models import Admin
from datetime import datetime

admin = Blueprint("admin", __name__)

#####################
# CHỨC NĂNG CƠ BẢN #
###################

# Đăng nhập admin
#---------------------------------------------
@admin.route("/admin/login", methods=["POST"])
def login():
    status = False
    user = []
    msg = ""
    access_token = ""
    if request.method == "POST":

        data = request.json if request.json else []

        admin_name = data["admin_name"] if "admin_name" in data else ""
        admin_password = data["admin_password"] if "admin_password" in data else ""

        if admin_name == "":
            msg = "Admin name is missing"
        elif admin_password == "":
            msg = "Admin password is missing"
        else:
            # ket noi database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_name = % s', (
                    admin_name,)
            )
            account = cursor.fetchone()
            cursor.close()

            if not account:
                msg = "Username is not exits"
            elif not verify_password(account["admin_password"], admin_password):
                msg = "Password is not correct"
            # neu dung tai khoan trong DB
            else:
                status = True
                user = {
                    "admin_id": account["admin_id"],
                    "admin_name": account["admin_name"],
                }
                access_token = generate_jwt_admin(account["admin_name"])
    return jsonify(status=status, msg=msg, access_token=access_token, user=user)

# Đăng xuất
#------------------------------------------
@admin.route("/admin/logout", methods=["GET"])
@token_required_admin
def logout(current_user):
    status = False
    msg = ""
    if request.method == "GET":
        admin_id = current_user["admin_id"]
        token = request.headers["x-access-token"] 
        created = datetime.now()

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO blacklist_token_admin VALUES (% s, % s, % s)', (admin_id, token, created))
        mysql.connection.commit()
        cursor.close()

        status = True
        msg = "You have logout!"
    return jsonify(status=status, msg=msg)

# Lấy thông tin tài khoản admim
#----------------------------------------------
@admin.route("/admin/profile", methods=["GET"])
@token_required_admin
def profile(current_user):
    status = False
    msg = ""
    if request.method == "GET":
        current_user = Admin(current_user)
        user = {
            "admin_id" : current_user.id,
            "admin_name" : current_user.name,
            "admin_role" : current_user.role
        }
        status = True
    return jsonify(status=status, msg=msg, user=user)

# sửa thông tin của quản trị viên request
# - truyền json biến nào cần thay đổi
#----------------------------------------------------
@admin.route("/admin/profile/edit", methods=["POST"])
@token_required_admin
def edit_profile_admin(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        current_user = Admin(current_user)

        data = request.json if request.json else []

        cursor = mysql.connection.cursor()
        # cursor.execute(
        #     'UPDATE admins_account SET admin_email = % s WHERE admin_id = % s', (
        #         admin_email, current_user.id,)
        # )
        mysql.connection.commit()
        cursor.close()

        status = True
        msg = "Your info has been updated!"

    return jsonify(status=status, msg=msg)

