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
                    "product_thumbnail": data.thumbnail,
                    "product_description": data.description,
                    "product_default_price": data.default_price,
                    "product_sale_price": data.sale_price,
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

# Manage Order
@main.route("/addorder", methods=["POST", "GET"])
def addorder():
    status = False
    msg = ""
    if request.method == "POST":

        data = request.json
        customer_id = data["customer_id"]
        order_date = datetime.now()
        order_sub_total_price = data["order_sub_total_price"]
        order_shipping = data["order_shipping"]
        coupon_code = data["coupon_code"]
        order_total_price = data["order_total_price"]
        order_status = data["order_status"]
        order_last_update_who = data["order_last_update_who"]
        order_last_update_when = datetime.now()

        if order_sub_total_price == "" or order_shipping == "" or order_total_price == "":
            msg = "Please fill out the form !"
        else:
            # ket noi database
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO orders VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s,% s)', (
                    customer_id, order_date, order_sub_total_price, order_shipping, coupon_code, order_total_price, order_status, order_last_update_who, order_last_update_when,)
            )
            mysql.connection.commit()
            cursor.close()

            status = True
            msg = "You have successfully added !"
    return jsonify(status=status, msg=msg)


@main.route("/getallorder", methods=['GET'])
def getallorder():
    status = False
    msg = ""

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM orders')
        data = cursor.fetchall()
        cursor.close()

        status = True
        msg = "Get all orders!"
    return jsonify(status=status, msg=msg, data=data)


@main.route("/editorder", methods=['GET', 'POST'])
def editorder():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        order_id = data["order_id"]
        customer_id = data["customer_id"]
        order_date = datetime.now()
        order_sub_total_price = data["order_sub_total_price"]
        order_shipping = data["order_shipping"]
        coupon_code = data["coupon_code"]
        order_total_price = data["order_total_price"]
        order_status = data["order_status"]
        order_last_update_who = data["order_last_update_who"]
        order_last_update_when = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM orders WHERE order_id = % s', (order_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'UPDATE `orders` SET `customer_id` = % s, `order_date` = % s, `order_sub_total_price` = % s, `order_shipping` = % s, `coupon_code` = % s, `order_total_price` = % s, `order_status` = % s, `order_last_update_who` = % s, `order_last_update_when` = % s WHERE `orders`.`order_id` = % s', (
                    customer_id, order_date, order_sub_total_price, order_shipping, coupon_code, order_total_price, order_status, order_last_update_who, order_last_update_when, order_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Orders info has been updated!"
        elif order_sub_total_price == "" or order_shipping == "" or order_total_price == "":
            msg = "Please fill out the form !"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)


@main.route("/deleteorder", methods=['GET', 'POST'])
def deleteorder():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        order_id = data["order_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM orders WHERE order_id = % s', (order_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'DELETE FROM `orders` WHERE `orders`.`order_id` = % s', (
                    order_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Order info has been deleted!"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Product warranty
@main.route("/addwarranty", methods=["POST", "GET"])
def addwarranty():
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json

        customer_id = data["customer_id"]
        product_name = data["product_name"]
        seri_number = data["seri_number"]
        description = data["description"]
        status_ = data["status"]
        date = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM warranty WHERE seri_number = % s', (seri_number, ))
        item = cursor.fetchone()

        if item:
            msg = "Your warranty already exist!"
        elif product_name == "" or seri_number == "":
            msg = "Please fill out the form!"
        else:
            cursor.execute(
                'INSERT INTO warranty VALUES (NULL, % s, % s, % s, % s, % s, % s)', (customer_id, product_name, seri_number, description, status_, date, ))
            mysql.connection.commit()
            cursor.close()

            status = True
            msg = "You have successfully added !"
        return jsonify(status=status, msg=msg)


@main.route("/getallwarranty", methods=['GET'])
def getallwarranty():
    status = False
    msg = ""

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM warranty')
        data = cursor.fetchall()
        cursor.close()

        status = True
        msg = "Get all warranty!"
    return jsonify(status=status, msg=msg, data=data)


@main.route("/editwarranty", methods=['GET', 'POST'])
def editwarranty():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        warranty_id = data["warranty_id"]
        customer_id = data["customer_id"]
        product_name = data["product_name"]
        seri_number = data["seri_number"]
        description = data["description"]
        status_ = data["status"]
        date = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM warranty WHERE warranty_id = % s', (warranty_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'UPDATE `warranty` SET `product_name` = % s, `seri_number` = % s, `description` = % s, `status` = % s, `date` = % s WHERE `warranty`.`warranty_id` = % s', (
                    product_name, seri_number, description, status_, date, warranty_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Warranty info has been updated!"
        elif product_name == "" or seri_number == "" or description == "" or status_ == "":
            msg = "Please fill out the form !"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)


@main.route("/deletewarranty", methods=['GET', 'POST'])
def deletewarranty():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        warranty_id = data["warranty_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM warranty WHERE warranty_id = % s', (warranty_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'DELETE FROM `warranty` WHERE `warranty`.`warranty_id` = % s', (
                    warranty_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Warranty info has been deleted!"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Manage Carts
@main.route("/addcart", methods=['GET', 'POST'])
def addcart():
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json

        order_id = ""
        customer_id = data["customer_id"]
        product_id = data["product_id"]
        quantity = data["quantity"]
        date = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO carts VALUES (NULL, % s, % s, % s, % s)', (customer_id, product_id, quantity, date,))
        mysql.connection.commit()
        cursor.close()

        status = True
        msg = "You have successfully added !"
        return jsonify(status=status, msg=msg)


@main.route("/getallcart", methods=['GET'])
def getallcart():
    status = False
    msg = ""

    if request.method == 'GET':
        data = request.json

        customer_id = data["customer_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE customer_id = % s', (customer_id,))
        data = cursor.fetchall()
        cursor.close()

        status = True
        msg = "Get all carts!"
    return jsonify(status=status, msg=msg, data=data)


@main.route("/editcart", methods=['GET', 'POST'])
def editcart():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        cart_id = data["cart_id"]
        quantity = data["quantity"]
        date = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE cart_id = % s', (cart_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'UPDATE `carts` SET `quantity` = % s, `date_time` = % s WHERE `carts`.`cart_id` = % s', (
                    quantity, date, cart_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Cart info has been updated!"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)


@main.route("/deletecart", methods=['GET', 'POST'])
def deletecart():
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json
        cart_id = data["cart_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE cart_id = % s', (cart_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                'DELETE FROM `carts` WHERE `carts`.`cart_id` = % s', (
                    cart_id,)
            )
            mysql.connection.commit()

            status = True
            msg = "Cart info has been deleted!"
        else:
            msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Count Price via Cart
@main.route("/getprice", methods=['GET', 'POST'])
def getprice():
    status = False
    msg = ""
    total = 0

    if request.method == "GET":

        data = request.json
        cart_id = data["cart_id"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE cart_id = % s', (cart_id, ))
        item = cursor.fetchone()
        if item:

            product_id = item["product_id"]
            cursor.execute(
                'SELECT quantity FROM `carts` WHERE `carts`.`cart_id` = % s', (
                    cart_id,)
            )
            cart = cursor.fetchone()
            quantity = cart["quantity"]

            cursor.execute(
                'SELECT product_sale_price FROM `products` WHERE `products`.`product_id` = % s', (
                    product_id,)
            )
            product = cursor.fetchone()
            price = product["product_sale_price"]
            cursor.close()

        total = price * quantity

        status = True
        msg = "Get Total Price has been done!"
    else:
        msg = "Fail to get price of quantity product"
    return jsonify(status=status, msg=msg, total=total)

# Count Total price
@main.route("/gettotalprice", methods=['GET', 'POST'])
def gettotalprice():
    status = False
    msg = ""
    total = 0

    if request.method == "GET":

        data = request.json
        customer_id = data["customer_id"]
        coupon_code = data["coupon_code"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE customer_id = % s', (customer_id, ))
        item = cursor.fetchall()
        if item:

            for i in range(len(item)):
                product_id = item[i]['product_id']
                quantity = item[i]['quantity']

                cursor.execute(
                    'SELECT product_sale_price FROM `products` WHERE `products`.`product_id` = % s', (
                        product_id,)
                )
                product = cursor.fetchone()
                price = product["product_sale_price"]

                total += price * quantity

            status = True
            msg = "Get Total Price has been done!"

            if coupon_code != "":
                cursor.execute(
                    'SELECT coupon_discount FROM `coupon` WHERE `coupon`.`coupon_code` = % s', (
                        coupon_code,)
                )
                coupon = cursor.fetchone()
                if coupon:
                    coupon_discount = coupon['coupon_discount']
                    total_dis = total - total*coupon_discount/100

        else:
            msg = "Fail to get total of order"
    return jsonify(status=status, msg=msg, total=total, total_dis=total_dis)


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
