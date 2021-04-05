from flask import request, jsonify, Blueprint
from app.models import Brand, Product
import MySQLdb.cursors
from datetime import datetime
from app import mysql

main = Blueprint("main", __name__)

#########################
# CÁC API CHUNG CƠ BẢN #
#######################

@main.route("/")
def index():
    return "Index page for web api"

#############
# SẢN PHẨM #
###########

# lấy thông tin một sản phẩm
# - Biến truyền vào là id 
#------------------------------------------------
@main.route("/product", methods=['GET'])
def get_product():
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
                    "product_thumbnail": {
                        "image_name": data.thumbnail.name,
                        "image_base64": data.thumbnail.base64
                    },
                    "product_description": data.description,
                    "product_default_price": data.default_price,
                    "product_sale_price": data.sale_price,
                    "time_warranty": data.time_warranty
                }
                status = True
            else:
                msg = "Fail access database"
    return jsonify(status=status, msg=msg, product=product)

# Lấy thông tin của tất cả sản phẩm
#----------------------------------------------------
@main.route("/product/all", methods=['GET'])
def get_product_all():
    status = False
    msg = ""
    products = []

    if request.method == 'GET':
        page = request.args.get("page", type=int)
        low_price = request.args.get("low_price", type=int)
        high_price = request.args.get("high_price", type=int)
        brand_id = request.args.get("brand_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not brand_id:
            cursor.execute(
                'SELECT * FROM products WHERE (product_sale_price >= % s OR  % s IS NULL) AND (product_sale_price <= % s OR % s IS NULL)',
                (low_price, low_price, high_price, high_price, ))
            
        else:
            cursor.execute(
                'SELECT * FROM products WHERE brand_id = % s', 
                (brand_id, ))
        data = cursor.fetchall()
        cursor.close()
        if data:
            if page:
                first_index = (page - 1) * Product.NUM_PER_PAGE
                last_index = first_index + Product.NUM_PER_PAGE
                data = data[first_index:last_index]
            for row in data:
                row = Product(row)
                product = {
                    "product_id": row.id,
                    "product_name": row.name,
                    "brand": {
                        "brand_id": row.brand.id,
                        "brand_name": row.brand.name
                    },
                    "product_thumbnail": {
                        "image_name": row.thumbnail.name,
                        "image_base64": row.thumbnail.base64
                    },
                    "product_description": row.description,
                    "product_default_price": row.default_price,
                    "product_sale_price": row.sale_price,
                    "time_warranty": row.time_warranty
                }
                products.append(product)
            status = True
        else:
            msg = "Fail access database"
    return jsonify(status=status, msg=msg, products=products)

##############
# NHÃN HIỆU #
############

# Lấy thông tin một nhãn hiệu
# - Biến truyền vào là id 
#-------------------------------------
@main.route("/brand", methods=['GET'])
def get_brand():
    status = False
    msg = ""
    brand = {}

    if request.method == 'GET':
        brand_id = request.args["brand_id"] if "brand_id" in request.args else None

        if not brand_id:
            msg = "Brand id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM brands WHERE brand_id = % s', (brand_id, ))
            data = cursor.fetchone()
            cursor.close()
            if data:
                data = Brand(data)
                brand = {
                    "brand_id": data.id,
                    "brand_name": data.name
                }
                status = True
            else:
                msg = "Fail access database"
    return jsonify(status=status, msg=msg, brand=brand)

# Lấy thông tin mọi nhãn hiệu
#------------------------------------------------
@main.route("/brand/all", methods=['GET'])
def get_brand_all():
    status = False
    msg = ""
    brands = []

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM brands')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                row = Brand(row)
                brand = {
                    "brand_id": row.id,
                    "brand_name": row.name
                }
                brands.append(brand)
            status = True
        else:
            msg = "Fail access database"
    return jsonify(status=status, msg=msg, brands=brands)

##################################
# CÁC API CHƯA XỬ LÝ, PHÂN LOẠI #
################################

from app.tools import allowed_file, upload_image

@main.route("/upload", methods=["POST"])
def upload():
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        img_b64 = data["image_base64"] if "image_base64" in data else None
        img_name = data["image_name"] if "image_name" in data else None
        
        if not img_b64 or img_b64 == "":
            msg = "Image base64 is missing"
        elif not img_name or img_name == "":
            msg = "Image name is missing"
        elif not allowed_file(img_name):
            msg = "Image format is not allow"
        else:
            upload = upload_image(img_name, img_b64)
            if upload:
                status = True
                msg = "Image has been uploaded"
            else:
                msg = "Image upload fail"
    return jsonify(status=status, msg=msg)     

# Search Product by Name
@main.route("/searchproduct", methods=['GET', 'POST'])
def searchproduct():
    status = False
    msg = ""

    if request.method == "GET":

        data = request.json

        product_name = data["product_name"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT product_name FROM products WHERE product_name LIKE '{}%' order by product_name".format(
            product_name)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        status = True
        msg = "List of product"
    else:
        msg = "False to searched"

    return jsonify(status=status, msg=msg, result=result)

# Search Customer by Name
@main.route("/searchcustomer", methods=['GET', 'POST'])
def searchcustomer():
    status = False
    msg = ""

    if request.method == "GET":

        data = request.json

        customer_name = data["customer_name"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT customer_name FROM customers_account WHERE customer_name LIKE '{}%' order by customer_name".format(
            customer_name)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        status = True
        msg = "List of customer"
    else:
        msg = "False to searched"

    return jsonify(status=status, msg=msg, result=result)


# Search User by Name
@main.route("/searchuser", methods=['GET', 'POST'])
def searchuser():
    status = False
    msg = ""

    if request.method == "GET":

        data = request.json

        admin_name = data["admin_name"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT admin_name FROM admins_account WHERE admin_name LIKE '{}%' order by admin_name".format(
            admin_name)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        status = True
        msg = "List of admin"
    else:
        msg = "False to searched"

    return jsonify(status=status, msg=msg, result=result)


# Get Products by Brand
@main.route("/getproductbrand", methods=['GET', 'POST'])
def getproductbrand():
    status = False
    msg = ""

    if request.method == "GET":

        data = request.json

        brand_id = data["brand_id"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM products WHERE brand_id = % s', (brand_id, ))
        products = cursor.fetchall()
        cursor.close()

        status = True
        msg = "List of product via brand"
    else:
        msg = "False to get products via brand"

    return jsonify(status=status, msg=msg, products=products)
