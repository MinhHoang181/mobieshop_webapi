from app.models import Permission
from flask import Blueprint, request, jsonify
from app import mysql
import MySQLdb.cursors
from app.tools import token_required_admin, permission_required
from app.models import Permission, Action, Product, Admin
from datetime import datetime

product = Blueprint("product", __name__)

#####################
# QUẢN LÝ SẢN PHẨM #
###################

# lấy thông tin một sản phẩm
# - Biến truyền vào là id 
#------------------------------------------------
@product.route("/admin/product", methods=['GET'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.READ)
def get_product(current_user):
    status = False
    msg = ""
    product = {}

    if request.method == 'GET':
        prodcut_id = request.args["product_id"] if "product_id" in request.args else None

        if not prodcut_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM products')
            data = cursor.fetchone()
            cursor.close()
            if data:
                data = Product(data)
                product = {
                    "product_id": data.id,
                    "product_name": data.name,
                    "brand": {
                        "brand_id": data.brand.id,
                        "brand_name": data.brand.name
                    },
                    "product_thumbnail": data.thumbnail,
                    "product_description": data.description,
                    "product_default_price": data.default_price,
                    "product_sale_price": data.sale_price,
                    "product_last_update_who": {
                        "admin_id": data.last_update_who.id,
                        "admin_name": data.last_update_who.name
                    },
                    "product_last_update_when": data.last_update_when
                }
                status = True
            else:
                msg = "Fail access database"
    return jsonify(status=status, msg=msg, product=product)

# Lấy thông tin của tất cả sản phẩm
#----------------------------------------------------
@product.route("/admin/product/all", methods=['GET'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.READ)
def get_product_all(current_user):
    status = False
    msg = ""
    products = []

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM products')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                row = Product(row)
                product = {
                    "product_id": row.id,
                    "product_name": row.name,
                    "brand": {
                        "brand_id": row.brand.id,
                        "brand_name": row.brand.name
                    },
                    "product_thumbnail": row.thumbnail,
                    "product_description": row.description,
                    "product_default_price": row.default_price,
                    "product_sale_price": row.sale_price,
                    "product_last_update_who": {
                        "admin_id": row.last_update_who.id,
                        "admin_name": row.last_update_who.name
                    },
                    "product_last_update_when": row.last_update_when
                }
                products.append(product)
            status = True
        else:
            msg = "Fail access database"
    return jsonify(status=status, msg=msg, products=products)

# Thêm sản phẩm
#--------------------------------------------------------
@product.route("/admin/product/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.CREATE)
def add_product(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []

        product_name = data["product_name"] if "product_name" in data else None
        brand_id = data["brand_id"] if "brand_id" in data else None
        product_thumbnail = data["product_thumbnail"] if "producct_thumbnail" in data else None
        product_description = data["product_description"] if "product_description" in data else None
        product_default_price = data["product_default_price"] if "product_default_price" in data else None
        product_sale_price = data["product_sale_price"] if "product_sale_price" in data else None
        product_last_update_when = datetime.now()

        if not product_name:
            msg = "Product name is missing"
        else:
            # lấy danh tính admin đang request
            current_user = Admin(current_user)

            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO products VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s)', (
                    product_name, brand_id, product_thumbnail, product_description, product_default_price, product_sale_price, current_user.id, product_last_update_when)
            )
            mysql.connection.commit()
            cursor.close()

            status = True
            msg = "You have successfully added product"
    return jsonify(status=status, msg=msg)

# Sửa sản phẩm
# - Thuộc tính nào cần sửa thì truyền vào json
#------------------------------------------------------
@product.route("/admin/product/edit", methods=['POST'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.EDIT)
def edit_product(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json if request.json else []

        product_id = data["product_id"] if "product_id" in data else None
        product_name = data["product_name"] if "product_name" in data else None
        brand_id = data["brand_id"] if "brand_id" in data else None
        product_thumbnail = data["product_thumbnail"] if "producct_thumbnail" in data else None
        product_description = data["product_description"] if "product_description" in data else None
        product_default_price = data["product_default_price"] if "product_default_price" in data else None
        product_sale_price = data["product_sale_price"] if "product_sale_price" in data else None
        product_last_update_when = datetime.now()

        # Nếu không có id thì báo lỗi
        if not product_id:
            msg = "Product id is missing"
        # Nếu có
        else:
            # kiểm tra xem có id sản phẩm đó không
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (product_id, ))
            product = cursor.fetchone()
            # nếu có
            if product:
                # lấy danh tính của admin đang request sửa sản phẩm
                current_user = Admin(current_user)
                # chuyển sang dạng object cho dễ sài
                product = Product(product)
                # nếu không có biến nào thì lấy giá trị cũ biến đó
                if not product_name:
                    product_name = product.name
                if not brand_id:
                    brand_id = product.brand.id
                if not product_thumbnail:
                    product_thumbnail = product.thumbnail
                if not product_description:
                    product_description = product.description
                if not product_default_price:
                    product_default_price = product.default_price
                if not product_sale_price:
                    product_sale_price = product.sale_price

                cursor.execute(
                    'UPDATE `products` SET `product_name` = % s, `brand_id` = % s, `product_thumbnail` = % s, `product_description` = % s, `product_default_price` = % s, `product_sale_price` = % s, `product_last_update_who` = % s, `product_last_update_when` = % s WHERE `products`.`product_id` = % s', (
                        product_name, brand_id, product_thumbnail, product_description, product_default_price, product_sale_price, current_user.id, product_last_update_when, product_id)
                )
                mysql.connection.commit()

                status = True
                msg = "Product info has been updated!"
            else:
                msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Xoá sản phẩm
# - Biến truyền vào là id
#--------------------------------------------------------
@product.route("/admin/product/delete", methods=['POST'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.DELETE)
def delete_product(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None

        if not product_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (product_id, ))
            product = cursor.fetchone()
            if product:
                cursor.execute(
                    'DELETE FROM `products` WHERE `products`.`product_id` = % s', (
                        product_id,)
                )
                mysql.connection.commit()

                status = True
                msg = "Product has been deleted!"
            else:
                msg = "Fail to delete!"

    return jsonify(status=status, msg=msg)