from flask import current_app, request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import mysql
import MySQLdb.cursors

###################
# XỬ LÝ MẬT KHẨU #
#################

# mã hoá password
#----------------------
def password(password):
    return generate_password_hash(password)

# kiểm tra password sau khi mã hoá
#--------------------------------------------
def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

#######################
# TẠO JSON WEB TOKEN #
#####################

# tạo json web token cho customer
#---------------------------------------------------------
def generate_jwt_customer(customer_name, expiration=3600):
    s = Serializer(current_app.config["SECRET_KEY"] + "customer", expiration)
    return s.dumps({"customer_name": customer_name}).decode("utf-8")

# tạo json web token cho admin
#---------------------------------------------------
def generate_jwt_admin(admin_name, expiration=3600):
    s = Serializer(current_app.config["SECRET_KEY"] + "admin", expiration)
    return s.dumps({"admin_name": admin_name}).decode("utf-8")

#####################
# KIỂM TRA BẢO MẬT #
###################

# yêu cầu kiểm tra token trước khi thực hiện API phía customer
#------------------------------
def token_required_customer(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        s = Serializer(current_app.config["SECRET_KEY"] + "customer")
        token = None

        # kiểm tra xem token có trong header không
        if "x-access-token" in request.headers: 
            token = request.headers["x-access-token"] 
        # trả về 401 nếu không có token
        if not token: 
            return jsonify({"msg" : "Token is missing !", "status" : False}), 401
        try: 
            # giải mã token lấy dữ liệu
            data = s.loads(token.encode("utf-8"))

            # kết nối database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # lấy dữ liệu người dùng định danh trong token
            cursor.execute(
                'SELECT * FROM customers_account WHERE customer_name = % s', (
                    data["customer_name"],)
            )
            current_user = cursor.fetchone()
            # đóng kết nối database
            mysql.connection.commit()
            cursor.close()

            if not current_user:
                return jsonify({"msg" : "Token is invalid !", "status" : False}), 401
        # nếu các bước trên bị lỗi thì coi như token không hợp lệ
        except: 
            return jsonify({"msg" : "Token is invalid !", "status" : False}), 401
        # trả về người dùng hiện tại
        return  f(current_user, *args, **kwargs) 
    return decorated

# yêu cầu kiểm tra token trước khi thực hiện API phía admin
#---------------------------
def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        s = Serializer(current_app.config["SECRET_KEY"] + "admin")
        token = None

        # kiểm tra xem token có trong header không
        if "x-access-token" in request.headers: 
            token = request.headers["x-access-token"] 
        # trả về 401 nếu không có token
        if not token: 
            return jsonify({"msg" : "Token is missing !", "status" : False}), 401
        try: 
            # giải mã token lấy dữ liệu
            data = s.loads(token.encode("utf-8"))

            # kết nối database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # lấy dữ liệu người dùng định danh trong token
            cursor.execute(
                'SELECT * FROM admins_account WHERE admin_name = % s', (
                    data["admin_name"],)
            )
            current_user = cursor.fetchone()
            # đóng kết nối database
            cursor.close()

            if not current_user:
                return jsonify({"msg" : "Token is invalid !", "status" : False}), 401
        # nếu các bước trên bị lỗi thì coi như token không hợp lệ
        except: 
            return jsonify({"msg" : "Token is invalid !", "status" : False}), 401
        # trả về người dùng hiện tại
        return  f(current_user, *args, **kwargs) 
    return decorated 

# Yêu cầu kiểm tra quyền thực hiện API phía admin
#-------------------------------------------
def permission_required(permission, action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # lấy tên quyền từ current_user được truyền vào trong args[0]
            admin_role = args[0]["admin_role"]

            # kết nối database
            cursor = mysql.connection.cursor()
            # Kiểm tra xem chức vụ quyền đó có chức năng và hành động đó không
            # Vd: Chức vụ (admin) -> chức năng (quản lý quyền) -> hành động (xem)
            cursor.execute(
                'SELECT * FROM permission_role WHERE role_name = % s AND permission_name = % s AND action_name = % s', (
                    admin_role, permission, action)
            )

            check = cursor.fetchone()
    
            # đóng kết nối database
            mysql.connection.commit()
            cursor.close()

            # nếu không có quyền đó thì trả về tin nhắn và báo lỗi 401
            if not check:
                return jsonify({"msg" : "You don't have permission !", "status" : False}), 401 
            
            # nếu có thì tiếp tục thực hiện API
            return f(*args, **kwargs)
        return decorated_function
    return decorator
