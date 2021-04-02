from flask import Blueprint, request, jsonify
from app import mysql
from app.tools import token_required_admin, permission_required, password
from app.models import Admin, Customer, Permission, Action, Role
import MySQLdb.cursors

account = Blueprint("account", __name__)

#################################
# QUẢN LÝ TÀI KHOẢN KHÁCH HÀNG #
###############################

# Xem thông tin tài khoản một khách hàng thông qua id hoặc name
#---------------------------------------------------------
@account.route("/admin/account/customer", methods=['GET'])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.READ)
def get_customer(current_user):
    msg = ""
    customer = {}
    status = False

    if request.method == "GET":
        customer_id = request.args["customer_id"] if "customer_id" in request.args else None
        customer_name = request.args["customer_name"] if "customer_name" in request.args else None

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # nếu có id thì dùng
        if customer_id:
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_id = % s', (customer_id, ))
            data = cursor.fetchone()
            cursor.close()
        # hoặc nếu có name
        elif customer_name:
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_name = % s', (customer_name, ))
            data = cursor.fetchone()
            cursor.close()
        if data:
            user = Customer(data)
            customer = {
                "customer_id" : user.id,
                "customer_name" : user.name,
                "customer_email" : user.email,
                "customer_address" : user.address,
                "customer_phone" : user.phone
            }
            status = True
        else:
            msg = "Error access database"
    return jsonify(status=status, msg=msg, customer=customer)

# Lấy danh sách mọi khách hàng
#-------------------------------------------------------------
@account.route("/admin/account/customer/all", methods=["GET"])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.READ)
def get_customers_all(current_user):
    msg = ""
    customers = []
    status = False

    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM customers_account')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                user = Customer(row)
                customer = {
                    "customer_id" : user.id,
                    "customer_name" : user.name,
                    "customer_email" : user.email,
                    "customer_address" : user.address,
                    "customer_phone" : user.phone
                }
                customers.append(customer)
            status = True
        else:
            msg = "Error access database"
    return jsonify(status=status, msg=msg, customers=customer)

# Sửa thông tin của một khách hàng
# - Biến truyền vào là những thuộc tính nào cần sửa
#---------------------------------------------------------------
@account.route("/admin/account/customer/edit", methods=["POST"])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.EDIT)
def edit_customer(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        customer_id = data["customer_id"] if "customer_id" in data else None
        customer_name = data["customer_name"] if "customer_name" in data else None
        customer_password = data["customer_password"] if "customer_password" in data else None
        customer_address = data["customer_address"] if "customer_address" in data else None
        customer_phone = data["customer_phone"] if "customer_phone" in data else None

        # nếu không có id báo lỗi
        if not customer_id:
            msg = "Customer id is missing"
        # nếu có
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # kiểm tra xem có id trong dữ liệu không
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_id = % s', (customer_id, ))
            account = cursor.fetchone()
            # nếu có
            if account:
                customer = Customer(account)
                # nếu có biến name và name khác name cũ
                if customer_name and customer_name != customer.name:
                    # kiểm tra xem name mới có bị trùng không
                    cursor.execute(
                        'SELECT * FROM customers_account WHERE customer_name = % s', (customer_name, ))
                    check = cursor.fetchone()
                    # nếu có báo lỗi
                    if check:
                        msg = "Customer name already exsist"
                        return jsonify(status=status, msg=msg)
                # nếu không có biến nào thì đặt mặc định như cũ
                else:
                    customer_name = customer.name
                if not customer_password:
                    customer_password = customer.password_hash
                # riêng nếu có password thì băm rồi lưu
                else:
                    customer_password = password(customer_password)
                if not customer_address:
                    customer_address = customer.address
                if not customer_phone:
                    customer_phone = customer.phone
                cursor.execute(
                    'UPDATE customers_account SET customer_name = % s, customer_password = % s, customer_address = % s, customer_phone = % s WHERE customer_id = % s', (
                        customer_name, customer_password, customer_address, customer_phone, customer_id,)
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Customer info has been updated!"
            else:
                msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# xoá một khách hàng
# - Dùng id hoặc name đều được
#-----------------------------------------------------------------
@account.route("/admin/account/customer/delete", methods=["POST"])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.DELETE)
def delete_customer(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        customer_id = data["customer_id"] if "customer_id" in data else None
        customer_name = data["customer_name"] if "customer_name" in data else None

        if not customer_id and not customer_name:
            msg = "Customer id or name is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if customer_name:
                cursor.execute(
                    'SELECT * FROM customers_account WHERE customer_name = % s', (customer_name, ))
                account = cursor.fetchone()
            else:
                cursor.execute(
                    'SELECT * FROM customers_account WHERE customer_id = % s', (customer_id, ))
                account = cursor.fetchone()

            if account:
                if customer_name:
                    cursor.execute(
                        'DELETE FROM customers_account WHERE customer_name = % s', (customer_name,  ))
                else:
                    cursor.execute(
                        'DELETE FROM customers_account WHERE customer_id = % s', (customer_id,  ))

                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Customer has been deleted!"
            else:
                msg = "Fail to delete"

    return jsonify(status=status, msg=msg)

####################################
# QUẢN LÝ TÀI KHOẢN QUẢN TRỊ VIÊN #
##################################

# Xem thông tin tài khoản một khách hàng
# - Dùng id hoặc name
#------------------------------------------------------
@account.route("/admin/account/admin", methods=['GET'])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.READ)
def get_admin(current_user):
    msg = ""
    admin = {}
    status = False

    if request.method == "GET":
        admin_id = request.args["admin_id"] if "admin_id" in request.args else None
        admin_name = request.args["admin_name"] if "admin_name" in request.args else None

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # nếu có id thì dùng
        if admin_id:
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_id = % s', (admin_id, ))
            data = cursor.fetchone()
            cursor.close()
        # nếu có name
        elif admin_name:
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_name = % s', (admin_name, ))
            data = cursor.fetchone()
            cursor.close()
        if data:
            user = Admin(data)
            admin = {
                "admin_id" : user.id,
                "admin_name" : user.name,
                "admin_role" : user.role
            }
            status = True
        else:
            msg = "Error access database"
    return jsonify(status=status, msg=msg, admin=admin)

# Lấy danh sách mọi quản trị viên
#----------------------------------------------------------
@account.route("/admin/account/admin/all", methods=["GET"])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.READ)
def get_admins_all(current_user):
    msg = ""
    admins = []
    status = False

    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM admins_account')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                user = Admin(row)
                admin = {
                    "admin_id" : user.id,
                    "admin_name" : user.name,
                    "admin_role" : user.role
                }
                admins.append(admin)
            status = True
        else:
            msg = "Error access database"
    return jsonify(status=status, msg=msg, admins=admins)

# Thêm admin
#--------------------------------------------------------------
@account.route("/admin/account/admin/create", methods=['POST'])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.CREATE)
def create_admin(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        admin_name = data["admin_name"] if "admin_name" in data else None
        admin_password = data["admin_password"] if "admin_name" in data else None
        admin_role = data["admin_role"] if "admin_role" in data else None

        if not admin_name:
            msg = "Admin name is missing"
        elif not admin_password:
            msg = "Admin password is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_name = % s', (admin_name, ))
            account = cursor.fetchone()
            if account:
                msg = "Account already exists !"
            else:
                cursor.execute(
                    'INSERT INTO admins_account VALUES (NULL, % s, % s, % s)', (admin_name, password(admin_password), admin_role, ))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully registered !"

    return jsonify(status=status, msg=msg)

# Sửa thông tin của một admin
# - Biến truyền vào là những thuộc tính nào cần sửa
#------------------------------------------------------------
@account.route("/admin/account/admin/edit", methods=["POST"])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.EDIT)
def edit_admin(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        admin_id = data["admin_id"] if "admin_id" in data else None
        admin_name = data["admin_name"] if "admin_name" in data else None
        admin_password = data["admin_password"] if "admin_password" in data else None
        admin_role = data["admin_role"] if "admin_role" in data else None

        # nếu thiếu id
        if not admin_id:
            msg = "Admin id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # kiểm tra xem id có tồn tại trong dữ liệu không
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_id = % s', (admin_id, ))
            account = cursor.fetchone()
            # nếu có
            if account:
                admin = Admin(account)
                # nếu có biến name và name khác với trước khi đổi
                if admin_name and admin_name != admin.name:
                    # kiểm tra tên mới có bị trùng không
                    cursor.execute(
                        'SELECT * FROM admins_account WHERE admin_name = % s', (admin_name, ))
                    check = cursor.fetchone()
                    # nếu trùng
                    if check:
                        msg = "Admin name already exists"
                        return jsonify(status=status, msg=msg)
                # nếu không có biến name hoặc là biến name giống như cũ
                else:
                    admin_name = admin.name
                # nếu không có các biến sau thì cho giá trị cũ
                if not admin_password:
                    admin_password = admin.password_hash
                # riêng thằng password thì băm ra mới lưu
                else:
                    admin_password = password(admin_password)
                if not admin_role:
                    admin_role = admin.role
                cursor.execute(
                    'UPDATE admins_account SET admin_name = % s, admin_password = % s, admin_role = % s WHERE admin_id = % s', (
                        admin_name, admin_password, admin_role, admin_id,)
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Admin info has been updated!"
            else:
                msg = "Fail to update info!"

    return jsonify(status=status, msg=msg)

# Xoá admin
#--------------------------------------------------------------
@account.route("/admin/account/admin/delete", methods=['POST'])
@token_required_admin
@permission_required(Permission.ACCOUNT_MANAGER, Action.DELETE)
def delete_admin(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        admin_id = data["admin_id"] if "admin_id" in data else None
        admin_name = data["admin_name"] if "admin_name" in data else None

        if not admin_id and not admin_name:
            msg = "Customer id or name is missing"
        else:
            cursor = mysql.connection.cursor()
            if admin_name:
                cursor.execute(
                    'SELECT * FROM admins_account WHERE admin_name = % s', (admin_name, ))
                account = cursor.fetchone()
            else:
                cursor.execute(
                    'SELECT * FROM admins_account WHERE admin_id = % s', (admin_id, ))
                account = cursor.fetchone()

            if account:
                if admin_name:
                    cursor.execute(
                        'DELETE FROM admins_account WHERE admin_name = % s', (admin_name,  ))
                else:
                    cursor.execute(
                        'DELETE FROM admins_account WHERE admin_id = % s', (admin_id,  ))

                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Admin has been deleted!"
            else:
                msg = "Fail to delete"

    return jsonify(status=status, msg=msg)