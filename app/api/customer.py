from flask import Blueprint, request, jsonify
from app.tools import generate_jwt_confirm_email, generate_jwt_customer_unconfirm, password, send_confirm_email, token_required_customer_unconfirm, verify_password, generate_jwt_customer, token_required_customer, check_verify_email
from app import mysql
import MySQLdb.cursors
from app.models import Bill, Cart, Customer, Order
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

        customer_email = data["customer_email"] if "customer_email" in data else None
        customer_password = data["customer_password"] if "customer_password" in data else None

        if not customer_email:
            msg = "Customer email is missing"
        elif not customer_password:
            msg = "Customer password is missing"
        else:
        # ket noi database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_email = % s', (
                    customer_email,)
            )
            account = cursor.fetchone()
            cursor.close()

            if not account:
                msg = "Email is not exits"
            elif not verify_password(account["customer_password"], customer_password):
                msg = "Password is not correct"
            # neu dung tai khoan trong DB
            else:
                account = Customer(account)
                if  not account.confirmed:
                    msg = "Unauthenticated account, please confirm account by email"
                    access_token = generate_jwt_customer_unconfirm(account.name)
                    return jsonify(status=status, msg=msg, confirm=False, access_token=access_token)
                else:
                    status = True
                    user = {
                        "customer_id": account.id,
                        "customer_name": account.name,
                        "customer_email": account.email,
                    }
                    access_token = generate_jwt_customer(account.name)
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

        url_confirm = data["url_confirm"] if "url_confirm" in data else None

        if not customer_email:
            msg = "Customer email is missing"
        elif not customer_password:
            msg = "Customer password is missing"
        elif not url_confirm:
            msg = "Url confirm is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_email = % s', (customer_email, ))
            check_email = cursor.fetchone()

            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_phone = % s', (customer_phone, ))
            check_phone = cursor.fetchone()
            if check_email:
                msg = "Email already exists !"
            elif check_phone:
                msg = "Phone already exists !"
            else:
                cursor.execute(
                    'INSERT INTO customers_account(customer_name, customer_password, customer_emai, customer_address, customer_phone) VALUES (% s, % s, % s, % s, % s)', 
                    (customer_name, password(customer_password), customer_email, customer_address, customer_phone, )
                )
                mysql.connection.commit()
                cursor.close()

                token = generate_jwt_confirm_email(customer_email)
                send_confirm_email(url_confirm, customer_email, token)

                status = True
                msg = "You have successfully registered! Please confirm your email!"

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

#######################
# XÁC THỰC TÀI KHOẢN #
#####################

# xác thực email
# - biến truyền vào là confirm_token trong json body
#----------------------------------------------------
@customer.route("/customer/verify", methods=["POST"])
@token_required_customer
@check_verify_email
def confirm_customer(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        current_user = Customer(current_user)

        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE customers_account SET confirmed = % s WHERE customer_id = % s', (True, current_user.id, )
        )
        status = True
        msg = "Email verification is successful"
    return jsonify(status=status, msg=msg)

# gửi email xác thực dành cho trường hợp muốn gửi lại
#-----------------------------------------------------------
@customer.route("/customer/verify/resend", methods=["POST"])
@token_required_customer_unconfirm
def send_verify_mail(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        url_confirm = data["url_confirm"] if "url_confirm" in data else None
        if not url_confirm:
            msg = "Url confirm is missing"
        else:
            current_user = Customer(current_user)
            if current_user.confirmed:
                msg = "Your Email already verified"
            else:
                token = generate_jwt_confirm_email(current_user.email)
                send_confirm_email(url_confirm, current_user.email, token)
                status = True
                msg = "Confirm link has been sent to your email"
    return jsonify(status=status, msg=msg)

##########
# HỒ SƠ #
########
    
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

##############
# BÌNH LUẬN #
#############

# viết bình luận
#---------------------------------------------------
@customer.route("/comment/create", methods=["POST"])
@token_required_customer
def create_comment(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None
        content = data["content"] if "content" in data else None
    
        if not product_id:
            msg = "Product id is missing"
        elif not content or content == "":
            msg = "Content is missing"
        else:
            current_user = Customer(current_user)
            time = datetime.now()
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO comments VALUE (NULL, % s, % s, % s, % s)', 
                (current_user.id, product_id, content, time,)
            )
            mysql.connection.commit()
            cursor.close()
            status = True
            msg = "comment add success"
    return jsonify(status=status, msg=msg)

#############
# GIỎ HÀNG #
###########

# xem giỏ hàng
#----------------------------------------
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

@customer.route("/cart/total", methods=["GET"])
@token_required_customer
def caculate_total_cart(current_user):
    status = False
    msg = ""
    total = 0
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
                total += int(row.product.sale_price) * row.quantity
        status = True
    return jsonify(status=status, msg=msg, total=total)
    
#############
# MUA HÀNG #
###########
@customer.route("/buy", methods=["POST"])
@token_required_customer
def buy_create_bill_and_order(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        address = data["address"] if "address" in data else None
        phone_number = data["phone_number"] if "phone_number" in data else None

        current_user = Customer(current_user)
        time_create = datetime.now()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE customer_id = % s', (current_user.id,)
        )
        carts = cursor.fetchall()
        if carts:
            cursor.execute(
                'INSERT INTO bills(customer_id, time_create) VALUE (% s, % s)', 
                (current_user.id, time_create,)
            )
            bill_id = cursor.lastrowid
            for cart in carts:
                cursor.execute(
                    'INSERT INTO product_bill VALUE(% s, % s, % s)',
                    (bill_id, cart["product_id"], cart["quantity"],)
                )
            mysql.connection.commit()

            cursor.execute(
                'SELECT * FROM bills WHERE bill_id = % s', (bill_id,)
            )
            bill = cursor.fetchone()
            bill = Bill(bill)
            cursor.execute(
                'UPDATE bills SET total = % s WHERE bill_id = % s', (bill.total, bill.id, )
            )
            mysql.connection.commit()
            
            time = datetime.now()
            
            # Tạo đơn hàng
            if not address:
                address = current_user.address
            if not phone_number:
                phone_number = current_user.phone
            cursor.execute(
                'INSERT INTO orders(customer_id, bill_id, `address`, phone_number, last_when_update) VALUES (% s, % s, % s, % s, % s)',
                (current_user.id, bill_id, address, phone_number, time,)
            )
            mysql.connection.commit()
            status = True
            msg = "Order has been create"
        else:
            msg = "Don't have any product in cart to create bill"
    return jsonify(status=status, msg=msg)



############
# HOÁ ĐƠN #
##########

# xem một hoá đơn bằng id
#----------------------------------------
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
            data = cursor.fetchone()
            if data:
                data = Bill(data)
                bill = {
                    "bill_id": data.id,
                    "customer": data.customer,
                    "products": data.products,
                    "fee_ship": data.fee_ship,
                    "total": data.total,
                    "time_create": data.time_create
                }
                status = True
            else:
                msg = "Access database is error"
            cursor.close()
    return jsonify(status=status, msg=msg, bill=bill)

# Xem toàn bộ hoá đơn
#-----------------
@customer.route("/bill/all", methods=["GET"])
@token_required_customer
def get_bill_all(current_user):
    status = False
    msg = ""
    bills = []

    if request.method == "GET":
        current_user = Customer(current_user)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM bills WHERE customer_id = % s', 
            (current_user.id,))
        data = cursor.fetchall()
        if data:
            for row in data:
                row = Bill(row)
                bill = {
                    "bill_id": row.id,
                    "customer": row.customer,
                    "products": row.products,
                    "fee_ship": row.fee_ship,
                    "total": row.total,
                    "time_create": row.time_create
                }
                bills.append(bill)
            status = True

    return jsonify(status=status, msg=msg, bills=bills)

# Tạo hoá đơn
#------------------------------------------------
@customer.route("/bill/create", methods=["POST"])
@token_required_customer
def create_bill(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        current_user = Customer(current_user)
        time_create = datetime.now()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM carts WHERE customer_id = % s', (current_user.id,)
        )
        carts = cursor.fetchall()
        if carts:
            cursor.execute(
                'INSERT INTO bills(customer_id, time_create) VALUE (% s, % s)', 
                (current_user.id, time_create,)
            )
            bill_id = cursor.lastrowid
            for cart in carts:
                cursor.execute(
                    'INSERT INTO product_bill VALUE(% s, % s, % s)',
                    (bill_id, cart["product_id"], cart["quantity"],)
                )
            mysql.connection.commit()

            cursor.execute(
                'SELECT * FROM bills WHERE bill_id = % s', (bill_id,)
            )
            bill = cursor.fetchone()
            bill = Bill(bill)
            cursor.execute(
                'UPDATE bills SET total = % s WHERE bill_id = % s', (bill.total, bill.id, )
            )
            mysql.connection.commit()

            bill_detail = {
                "bill_id": bill.id,
                "customer": bill.customer,
                "products": bill.products,
                "fee_ship": bill.fee_ship,
                "total": bill.total,
                "time_create": bill.time_create
            }
            status = True
            msg = "Bill has been created"
        else:
            msg = "Don't have any product in cart to create bill"
    return jsonify(status=status, msg=msg, bill=bill_detail)

#############
# ĐƠN HÀNG #
###########

# xem tất cả đơn đặt hàng
@customer.route("/order/all", methods=["GET"])
@token_required_customer
def get_order_all(current_user):
    status = False
    msg = ""
    orders = []
    if request.method == "GET":
        current_user = Customer(current_user)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM orders WHERE customer_id = % s', (current_user.id, )
        )
        data = cursor.fetchall()
        if data:
            for row in data:
                row = Order(row)
                order = {
                    "bill_id": row.bill,
                    "customer": row.customer,
                    "address": row.address,
                    "phone": row.phone,
                    "status": row.status,
                }
                orders.append(order)
            status = True
        else:
            msg = "Access database error or Order empty"
    return jsonify(status=status, msg=msg, orders=orders)


# tạo đơn đặt hàng
#--------------------------
@customer.route("/order/create", methods=["POST"])
@token_required_customer
def create_order(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        bill_id = data["bill_id"] if "bill_id" in data else None
        address = data["address"] if "address" in data else None
        phone_number = data["phone_number"] if "phone_number" in data else None
        time = datetime.now()

        if not bill_id:
            msg = "Bill id is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM bills WHERE bill_id = % s', 
                (bill_id,)
            )
            check = cursor.fetchone()
            if check:
                cursor.execute(
                    'SELECT * FROM orders WHERE bill_id = % s', 
                    (bill_id,)
                )
                check = cursor.fetchone()
                if check:
                    msg = "Order already exist"
                else:
                    current_user = Customer(current_user)
                    if not address:
                        address = current_user.address
                    if not phone_number:
                        phone_number = current_user.phone
                    cursor.execute(
                        'INSERT INTO orders(customer_id, bill_id, address, phone_number, last_when_update) VALUES (% s, % s, % s, % s, % s)',
                        (current_user.id, bill_id, address, phone_number, time,)
                    )
                    mysql.connection.commit()
                    status = True
                    msg = "Order has been created"
            else:
                msg = "Bill doesn't exist"
            cursor.close()
    return jsonify(status=status, msg=msg)