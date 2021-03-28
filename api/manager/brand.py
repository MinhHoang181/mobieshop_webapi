from flask import Blueprint, request, jsonify
from app import mysql
import MySQLdb.cursors
from app.tools import token_required_admin, permission_required
from app.models import Permission, Action, Brand

brand = Blueprint("brand", __name__)

######################
# QUẢN LÝ NHÃN HIỆU #
####################

# Thêm nhãn hiệu
#--------------------------------------------------------
@brand.route("/admin/brand/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.BRAND_MANAGER, Action.CREATE)
def add_brand(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []

        brand_name = data["brand_name"] if "brand_name" in data else None

        if not brand_name:
            msg = "Brand name is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM brands WHERE brand_name = % s', (brand_name, ))
            check = cursor.fetchone()
            if check:
                msg = "Brand name already exists"
            else:
                cursor.execute(
                    'INSERT INTO brands VALUES (NULL, % s)', (
                        brand_name, )
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully added brand"
    return jsonify(status=status, msg=msg)

# Sửa nhãn hiệu
# - Thuộc tính nào cần sửa thì truyền vào json
#------------------------------------------------------
@brand.route("/admin/brand/edit", methods=['POST'])
@token_required_admin
@permission_required(Permission.BRAND_MANAGER, Action.EDIT)
def edit_brand(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json if request.json else []

        brand_id = data["brand_id"] if "brand_id" in data else None
        brand_name = data["brand_name"] if "brand_name" in data else None

        # Nếu không có id thì báo lỗi
        if not brand_id:
            msg = "Brand id is missing"
        # Nếu có
        else:
            # kiểm tra xem có id nhãn hiệu đó không
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM brands WHERE brand_id = % s', (brand_id, ))
            brand = cursor.fetchone()
            # nếu có
            if brand:
                # chuyển sang dạng object cho dễ sài
                brand = Brand(brand)
                # nếu có biến name và name khác với trước khi đổi
                if brand_name and brand_name != brand.name:
                    # kiểm tra tên mới có bị trùng không
                    cursor.execute(
                        'SELECT * FROM brands WHERE brand_name = % s', (brand_name, ))
                    check = cursor.fetchone()
                    # nếu trùng
                    if check:
                        msg = "Brand name already exists"
                        return jsonify(status=status, msg=msg)
                # nếu không có biến name hoặc là biến name giống như cũ
                else:
                    brand_name = brand.name
                # nếu không có biến nào thì lấy giá trị cũ biến đó
                # dành cho phần nếu có thêm thuộc tính khác

                cursor.execute(
                    'UPDATE `brands` SET `brand_name` = % s WHERE brand_id = % s', (
                        brand_name, brand_id, )
                )
                mysql.connection.commit()

                status = True
                msg = "Brand info has been updated!"
            else:
                msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Xoá nhãn hiệu
# - Biến truyền vào là id
#--------------------------------------------------------
@brand.route("/admin/brand/delete", methods=['POST'])
@token_required_admin
@permission_required(Permission.BRAND_MANAGER, Action.DELETE)
def delete_brand(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []
        brand_id = data["brand_id"] if "brand_id" in data else None

        if not brand_id:
            msg = "Brand id is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM brands WHERE brand_id = % s', (brand_id, ))
            brand = cursor.fetchone()
            if brand:
                cursor.execute(
                    'DELETE FROM `brands` WHERE `brands`.`brand_id` = % s', (
                        brand_id,)
                )
                mysql.connection.commit()

                status = True
                msg = "Brand has been deleted!"
            else:
                msg = "Fail to delete!"

    return jsonify(status=status, msg=msg)