from flask import Blueprint, request, jsonify
from app.tools import token_required_admin, permission_required
from app.models import Action, Bill, Permission
from app import mysql
import MySQLdb.cursors

bill = Blueprint("bill", __name__)

####################
# QUẢN LÝ HOÁ ĐƠN #
##################

# xem một hoá đơn qua id hoá đơn
@bill.route("/admin/bill", methods=["GET"])
@token_required_admin
@permission_required(Permission.BILL_MANAGER, Action.READ)
def get_bill(current_user):
    status = False
    msg = ""
    bill = {}

    if request.method == "GET":
        bill_id = request.args.get("bill_id")

        if not bill_id:
            msg = "Bill id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM bills WHERE bill_id = % s', 
                (bill_id,))
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
                msg = "Access database is error or bill id wrong"
            cursor.close()
    return jsonify(status=status, msg=msg, bill=bill)

# xem mọi hoá đơn của một khách hàng qua id khách hàng
# - Nếu có id khách hàng thì xem một còn không là xem hết
#----------------------------------------------
@bill.route("/admin/bill/all", methods=["GET"])
@token_required_admin
@permission_required(Permission.BILL_MANAGER, Action.READ)
def get_bill_all(current_user):
    status = False
    msg = ""
    bills = []

    if request.method == "GET":
        customer_id = request.args.get("customer_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM bills WHERE (customer_id = % s) OR (% s IS NULL)', 
            (customer_id, customer_id))
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
        else:
            msg = "Access database is error or bills empty"
        cursor.close()
    return jsonify(status=status, msg=msg, bills=bills)
