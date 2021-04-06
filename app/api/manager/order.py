from flask import Blueprint, request, jsonify
from app.tools import token_required_admin, permission_required
from app.models import Action, Admin, Permission, Order
from app import mysql
import MySQLdb.cursors
from datetime import datetime

order = Blueprint("order", __name__)

#####################
# QUẢN LÝ ĐƠN HÀNG #
###################

# xem một đơn đặt hàng qua id bill
#-------------------
@order.route("/admin/order", methods=["GET"])
@token_required_admin
@permission_required(Permission.ORDER_MANAGER, Action.READ)
def get_order(current_user):
    status = False
    msg = ""
    order = {}
    if request.method == "GET":
        bill_id = request.args.get("bill_id")
        if not bill_id:
            msg = "Bill id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM orders WHERE bill_id = % s', 
                (bill_id, )
            )
            data = cursor.fetchone()
            if data:
                data = Order(data)
                order = {
                    "bill_id": data.bill,
                    "customer": data.customer,
                    "address": data.address,
                    "phone": data.phone,
                    "status": data.status,
                    "who_update": data.admin,
                    "last_update": data.last_update
                }
                status = True
            else:
                msg = "Access database error or Order empty or Bill id is wrong"
            cursor.close()
    return jsonify(status=status, msg=msg, order=order)

# xem tất cả đơn đặt hàng
# - nếu biến truyền vào là id khách hàng 
#------------------------------------------------
@order.route("/admin/order/all", methods=["GET"])
@token_required_admin
@permission_required(Permission.ORDER_MANAGER, Action.READ)
def get_order_all(current_user):
    status = False
    msg = ""
    orders = []
    if request.method == "GET":
        customer_id = request.args.get("customer_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM orders WHERE (customer_id = % s) OR (% s IS NULL)', 
            (customer_id, customer_id, )
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
                    "who_update": row.admin,
                    "last_update": row.last_update
                }
                orders.append(order)
            status = True
        else:
            msg = "Access database error or Order empty"
        cursor.close()
    return jsonify(status=status, msg=msg, orders=orders)

# sửa trạng thái đơn hàng
#-----------------------------
@order.route("/admin/order/edit", methods=["POST"])
@token_required_admin
@permission_required(Permission.ORDER_MANAGER, Action.EDIT)
def edit_order(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []
        bill_id = data["bill_id"] if "bill_id" in data else None
        order_status = data["status"] if "status" in data else None
        address = data["address"] if "address" in data else None
        phone = data["phone"] if "phone" in data else None

        if not bill_id:
            msg = "Bill id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM orders WHERE bill_id = % s', (bill_id,)
            )
            order = cursor.fetchone()
            if order:
                current_user = Admin(current_user)
                order = Order(order)
                last_update = datetime.now()
                
                if not order_status:
                    order_status = order.status
                if not address:
                    address = order.address
                if not phone:
                    phone = order.phone

                cursor.execute(
                    'UPDATE orders SET status = % s, address = % s, phone_number = % s, last_who_update = % s, last_when_update = % s WHERE bill_id = % s', 
                    (order_status, address, phone, current_user.id, last_update, bill_id,)
                )
                mysql.connection.commit()
                cursor.close()
                status = True
                msg = "Order has been updated"
            else:
                msg = "Access database error or bill id wrong"
    return jsonify(status=status, msg=msg)