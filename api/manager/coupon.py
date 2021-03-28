from flask import Blueprint, request, jsonify
from app import mysql
import MySQLdb.cursors
from app.tools import token_required_admin, permission_required
from app.models import Permission, Action, Coupon

coupon = Blueprint("coupon", __name__)

###########################
# QUẢN LÝ PHIẾU MUA HÀNG #
#########################

# lấy thông tin một phiếu mua hàng
# - Biến truyền vào là id 
#----------------------------------------------
@coupon.route("/admin/coupon", methods=['GET'])
@token_required_admin
@permission_required(Permission.COUPON_MANAGER, Action.READ)
def get_coupon(current_user):
    status = False
    msg = ""
    coupon = {}

    if request.method == 'GET':
        coupon_id = request.args["coupon_id"] if "coupon_id" in request.args else None

        if not coupon_id:
            msg = "Coupon id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM coupon')
            data = cursor.fetchone()
            cursor.close()
            if data:
                data = Coupon(data)
                coupon = {
                    "coupon_id": data.id,
                    "coupon_name": data.name,
                    "coupon_code": data.code,
                    "coupon_discount": data.discount
                }
                status = True
            else:
                msg = "Fail access database"
    return jsonify(status=status, msg=msg, coupon=coupon)

# Lấy thông tin mọi phiếu mua hàng
#-----------------------------------------
@coupon.route("/admin/coupon/all", methods=['GET'])
@token_required_admin
@permission_required(Permission.COUPON_MANAGER, Action.READ)
def get_coupon_all(current_user):
    status = False
    msg = ""
    coupons = []

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM coupon')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                row = Coupon(row)
                coupon = {
                    "coupon_id": row.id,
                    "coupon_name": row.name,
                    "coupon_code": row.code,
                    "coupon_discount": row.discount
                }
                coupons.append(coupon)
            status = True
        else:
            msg = "Fail access database"
    return jsonify(status=status, msg=msg, coupons=coupons)

# Thêm phiếu mua hàng
#--------------------------------------------------------
@coupon.route("/admin/coupon/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.COUPON_MANAGER, Action.CREATE)
def add_coupon(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []

        coupon_name = data["coupon_name"] if "coupon_name" in data else None
        coupon_code = data["coupon_code"] if "coupon_code" in data else None
        coupon_discount = data["coupon_discount"] if "coupon_discount" in data else None

        if not coupon_name:
            msg = "Coupon name is missing"
        elif not coupon_code:
            msg = "Coupon code is missing"
        elif not coupon_discount:
            msg = "Coupon discount is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM coupon WHERE coupon_name = % s', (coupon_name, ))
            check = cursor.fetchone()
            if check:
                msg = "Coupon name already exists"
            else:
                cursor.execute(
                    'INSERT INTO coupon VALUES (NULL, % s, % s, % s)', (
                        coupon_name, coupon_code, coupon_discount, )
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully added coupon"
    return jsonify(status=status, msg=msg)

# Sửa phiếu mua hàng
# - Thuộc tính nào cần sửa thì truyền vào json
#------------------------------------------------------
@coupon.route("/admin/coupon/edit", methods=['POST'])
@token_required_admin
@permission_required(Permission.COUPON_MANAGER, Action.EDIT)
def edit_coupon(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json if request.json else []

        coupon_id = data["coupon_id"] if "coupon_id" in data else None
        coupon_name = data["coupon_name"] if "coupon_name" in data else None
        coupon_code = data["coupon_code"] if "coupon_code" in data else None
        coupon_discount = data["coupon_discount"] if "coupon_discount" in data else None

        # Nếu không có id thì báo lỗi
        if not coupon_id:
            msg = "coupon id is missing"
        # Nếu có
        else:
            # kiểm tra xem có id đó không
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM coupon WHERE coupon_id = % s', (coupon_id, ))
            coupon = cursor.fetchone()
            # nếu có
            if coupon:
                # chuyển sang dạng object cho dễ sài
                coupon = Coupon(coupon)
                # nếu có biến name và name khác với trước khi đổi
                if coupon_name and coupon_name != coupon.name:
                    # kiểm tra tên mới có bị trùng không
                    cursor.execute(
                        'SELECT * FROM coupon WHERE coupon_name = % s', (coupon_name, ))
                    check = cursor.fetchone()
                    # nếu trùng
                    if check:
                        msg = "Coupon name already exists"
                        return jsonify(status=status, msg=msg)
                # nếu không có biến name hoặc là biến name giống như cũ
                else:
                    coupon_name = coupon.name
                if coupon_code and coupon_code != coupon.code:
                    # kiểm tra tên mới có bị trùng không
                    cursor.execute(
                        'SELECT * FROM coupon WHERE coupon_code = % s', (coupon_code, ))
                    check = cursor.fetchone()
                    # nếu trùng
                    if check:
                        msg = "Coupon code already exists"
                        return jsonify(status=status, msg=msg)
                # nếu không có biến name hoặc là biến name giống như cũ
                else:
                    coupon_code = coupon.code
                # nếu không có biến nào thì lấy giá trị cũ biến đó
                if not coupon_discount:
                    coupon_discount = coupon.discount

                cursor.execute(
                    'UPDATE `coupon` SET `coupon_name` = % s, coupon_code = % s, coupon_discount = % s WHERE coupon_id = % s', (
                        coupon_name, coupon_code, coupon_discount, coupon_id, )
                )
                mysql.connection.commit()

                status = True
                msg = "Coupon info has been updated!"
            else:
                msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Xoá phiếu mua hàng
# - Biến truyền vào là id
#--------------------------------------------------------
@coupon.route("/admin/coupon/delete", methods=['POST'])
@token_required_admin
@permission_required(Permission.COUPON_MANAGER, Action.DELETE)
def delete_coupon(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []
        coupon_id = data["coupon_id"] if "coupon_id" in data else None

        if not coupon_id:
            msg = "Coupon id is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM coupon WHERE coupon_id = % s', (coupon_id, ))
            coupon = cursor.fetchone()
            if coupon:
                cursor.execute(
                    'DELETE FROM `coupon` WHERE `coupon`.`coupon_id` = % s', (
                        coupon_id,)
                )
                mysql.connection.commit()

                status = True
                msg = "Coupon has been deleted!"
            else:
                msg = "Fail to delete!"

    return jsonify(status=status, msg=msg)
