from flask import request, jsonify, Blueprint
from app.models import Brand, Comment, Customer, Product
import MySQLdb.cursors
from app import mysql
import math

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
        product_id = request.args["product_id"] if "product_id" in request.args else None

        if not product_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM products WHERE product_id= %s', (product_id, ))
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
# - biến truyền vào có thể là page, low_price, high_price, brand
#-------------------------------------------
@main.route("/product/all", methods=['GET'])
def get_product_all():
    status = False
    msg = ""
    products = []

    if request.method == 'GET':
        product_name = request.args.get("product_name")
        page = request.args.get("page", type=int)
        low_price = request.args.get("low_price", type=int)
        high_price = request.args.get("high_price", type=int)
        brand_id = request.args.get("brand_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM products WHERE (brand_id = % s OR % s IS NULL) AND (product_sale_price >= % s OR  % s IS NULL) AND (product_sale_price <= % s OR % s IS NULL) AND (product_name like % s OR % s IS NULL)',
            (brand_id, brand_id, low_price, low_price, high_price, high_price, str(product_name) + "%", product_name,))
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

# lấy tổng số trang
#---------------------
@main.route("/product/all/count", methods=["GET"])
def count_page():
    status = False
    msg = ""
    num_page = 0
    if request.method == "GET":
        product_name = request.args.get("product_name")
        low_price = request.args.get("low_price", type=int)
        high_price = request.args.get("high_price", type=int)
        brand_id = request.args.get("brand_id")

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM products WHERE (brand_id = % s OR % s IS NULL) AND (product_sale_price >= % s OR  % s IS NULL) AND (product_sale_price <= % s OR % s IS NULL) AND (product_name like % s OR % s IS NULL)',
            (brand_id, brand_id, low_price, low_price, high_price, high_price, str(product_name) + "%", product_name, )
        )
        count = cursor.fetchone()
        count = int(count[0])
        if count != 0:
            num_page = math.ceil(count / Product.NUM_PER_PAGE)
        status = True
        
    return jsonify(status=status, msg=msg, num_page=num_page, num_product=count)

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

##############
# BÌNH LUẬN #
############

# lấy tất cả bình luận của một sản phẩm
# biến truyền vào là id sản phẩm, nếu không có đồng nghĩa lấy hết
#-------------------------------------------
@main.route("/comment/all", methods=["GET"])
def get_comment_all():
    status = False
    msg = ""
    comments = []
    if request.method == "GET":
        product_id = request.args.get("product_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM comments WHERE (product_id = % s) OR (% s IS NULL) ORDER BY time DESC',
            (product_id, product_id,)
        )
        data = cursor.fetchall()
        if data:
            for row in data:
                row = Comment(row)
                comment = {
                    "comment_id": row.id,
                    "customer": row.customer,
                    "product_id": row.product,
                    "content": row.content,
                    "time": row.time
                }
                comments.append(comment)
            status = True
        else:
            msg = "Access database is error or comments is empty or product_id is wrong"
        return jsonify(status=status, msg=msg, comments=comments)

##################################
# CÁC API CHƯA XỬ LÝ, PHÂN LOẠI #
################################

#############
# API TEST #
###########

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

from app.tools import send_confirm_email, generate_jwt_confirm_email
@main.route("/send", methods=["POST"])
def send_mail():
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        customer_email = data["customer_email"] if "customer_email" in data else None
        url_confirm = data["url_confirm"] if "url_confirm" in data else None
        if not customer_email:
            msg = "Customer email is missing"
        elif not url_confirm:
            msg = "Url confirm is missing"
        else:
            token = generate_jwt_confirm_email(customer_email)
            send_confirm_email(url_confirm, "phamminhhoang181@gmail.com", token)
            status = True
    return jsonify(status=status, msg=msg)
    
#########################################


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