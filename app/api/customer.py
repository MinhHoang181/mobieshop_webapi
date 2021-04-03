from flask import Blueprint, request, jsonify
from app.tools import password, verify_password, generate_jwt_customer, token_required_customer
from app import mysql
import MySQLdb.cursors
from app.models import Cart, Customer
from datetime import datetime

customer = Blueprint("customer", __name__)

#############################
# CHỨC NĂNG CỦA KHÁCH HÀNG #
###########################

# Đăng nhập
#------------------------------------------
@customer.route("/login", methods=["POST"])
def login():
    status = False
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
                status = True
                user = {
                    "customer_id": account["customer_id"],
                    "customer_name": account["customer_name"],
                }
                access_token = generate_jwt_customer(account["customer_name"])
    return jsonify(status=status, msg=msg, access_token=access_token, user=user)

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
        customer_email = data["customer_email"] if "customer_email" in data else None
        customer_address = data["customer_address"] if "customer_address" in data else None
        customer_phone = data["customer_phone"] if "customer_phone" in data else None

        if not customer_name:
            msg = "Customer name is missing"
        elif not customer_password:
            msg = "Customer password is missing"
        elif not customer_email:
            msg = "Customer email is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_name = % s', (customer_name, ))
            account = cursor.fetchone()
            if account:
                msg = "Account already exists !"
            else:
                cursor.execute(
                    'INSERT INTO customers_account VALUES (NULL, % s, % s, % s, % s, % s)', (customer_name, password(customer_password), customer_email, customer_address, customer_phone, ))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully registered !"

    return jsonify(status=status, msg=msg)

# Đăng xuất
#------------------------------------------
@customer.route("/logout", methods=["GET"])
@token_required_customer
def logout(current_user):
    status = False
    msg = ""
    if request.method == "GET":
        customer_id = current_user["customer_id"]
        token = request.headers["x-access-token"] 
        created = datetime.now()

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO blacklist_token_customer VALUES (% s, % s, % s)', (customer_id, token, created))
        mysql.connection.commit()
        cursor.close()

        status = True
        msg = "You have logout!"
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
            "customer_email" : current_user.email,
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

#############
# GIỎ HÀNG #
###########

# xem giỏ hàng
#-----------------------
@customer.route("/cart", methods=["GET"])
@token_required_customer
def get_cart(current_user):
    status = False
    msg = ""
    cart = []
    if request.method == "GET":
        current_user = Customer(current_user)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE customer_id = % s', (current_user.id,))
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                row = Cart(row)
                product = {
                    "product_id": row.product.id,
                    "product_name": row.product.name,
                    "product_price": row.product.sale_price,
                    "quantity": row.quantity
                }
                cart.append(product)
        status = True
    return jsonify(status=status, msg=msg, cart=cart)

# tạo giỏ hàng
#------------------------------------------------
@customer.route("/cart/create", methods=["POST"])
@token_required_customer
def create_cart(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None
        quantity = data["quantity"] if "quantity" in data else 1

        # nếu thiếu product id
        if not product_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # kiểm tra xem id sản phẩm có tồn tại không
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (product_id,))
            check = cursor.fetchone()
            # nếu không báo lỗi
            if not check:
                msg = "Product doesn't exist"
            # nếu có
            else:
                current_user = Customer(current_user)
                # kiểm tra xem trong giỏ hàng có sản phẩm này chưa
                cursor.execute(
                    'SELECT * FROM carts WHERE customer_id = % s AND product_id = % s',
                    (current_user.id, product_id,))
                cart = cursor.fetchone()
                # nếu có thì cập nhật lại số lượng
                if cart:
                    cart = Cart(cart)
                    cursor.execute(
                        'UPDATE carts SET quantity = % s WHERE customer_id = % s AND product_id = % s',
                        (quantity + cart.quantity, cart.customer, cart.product.id,))
                # nếu không thì tạo mới giỏ hàng
                else:
                    cursor.execute(
                        'INSERT INTO carts VALUE (% s, % s, % s)',
                        (current_user.id, product_id, quantity)
                    )
                status = True
                msg = "Product added to cart"

                mysql.connection.commit()
                cursor.close()
    return jsonify(status=status, msg=msg)

# sửa giỏ hàng
#----------------------------------------------
@customer.route("/cart/edit", methods=["POST"])
@token_required_customer
def edit_cart(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None
        quantity = data["quantity"] if "quantity" in data else None

        if not product_id:
            msg = "Product id is missing"
        elif not quantity:
            msg = "Quantity is missing"
        else:
            current_user = Customer(current_user)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM carts WHERE customer_id = % s AND product_id = % s', 
                (current_user.id, product_id, ))
            cart = cursor.fetchone()
            if cart:
                cursor.execute(
                    'UPDATE carts SET quantity = % s WHERE customer_id = % s AND product_id = % s', 
                    (quantity, current_user.id, product_id))
                status = True
                msg = "Cart has been updated"
            else:
                msg = "Product doesn't exist in cart"
            mysql.connection.commit()
            cursor.close()

    return jsonify(status=status, msg=msg)



# xoá giỏ hàng
# - biến truyền vào là id, nếu không có id nghĩa là xoá hết
#------------------------------------------------
@customer.route("/cart/delete", methods=["POST"])
@token_required_customer
def delete_cart(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None
        cursor = mysql.connection.cursor()
        if product_id:
            cursor.execute(
                'SELECT * FROM carts WHERE product_id = % s', (product_id,))
            check = cursor.fetchone()
            if not check:
                msg = "Product doesn't exist in cart"
                return jsonify(status=status, msg=msg)

        current_user = Customer(current_user)
        
        cursor.execute(
            'DELETE FROM carts WHERE customer_id = % s AND (product_id = % s OR % s IS NULL)', 
            (current_user.id ,product_id, product_id,))
        status = True
        if product_id:
            msg = "Product has been deleted from cart"
        else:
            msg = "All product has been deleted from cart"
        mysql.connection.commit()
        cursor.close()
    return jsonify(status=status, msg=msg)

############
# HOÁ ĐƠN #
##########

# xem một hoá đơn bằng id
#-----------------
@customer.route("/bill", methods=["GET"])
@token_required_customer
def get_bill(current_user):
    status = False
    msg = ""
    bill = {}
    if request.method == "GET":
        bill_id = request.args.get("bill_id")
        if not bill_id:
            msg = "Bill id is missing"
        else:
            current_user = Customer(current_user)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM bills WHERE bill_id = % s AND customer_id = % s', 
                (bill_id, current_user.id))
            bill = cursor.fetchone()
            if bill:
                status = True
            else:
                msg = "Access database is error"
            cursor.close()
    return jsonify(status=status, msg=msg, bill=bill)
