from flask import current_app, request, jsonify, render_template
from flask_mail import Message
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import mysql, mail, ALLOWED_EXTENSIONS
import MySQLdb.cursors
import base64
from PIL import Image
import io
import os

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

###############
# XỬ LÝ MAIL #
#############

# gửi mail xác thực tài khoản
def send_confirm_email(url, to, token):
    msg = Message("Xác thực tài khoản", recipients=[to], sender="SOA Mobile Shop")
    url = url + "?confirm=" + token
    msg.body = render_template("confirm_email.txt", customer_email = to,  url=url)
    mail.send(msg)

##############
# XỬ LÝ ẢNH #
############

# kiểm tra loại dữ liệu cho phép
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# tải ảnh lên server
def upload_image(img_name, img_b64, size=None):
    try:
        img_binary = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_binary))
        img_name = secure_filename(img_name)
        if size:
            img = img.resize(size)
        img.save(os.path.join(current_app.config["UPLOAD_FOLDER"], img_name))
        return True
    except:
        return False

# xoá ảnh trên server
def delete_image(image_name):
    try:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
    except:
        return False

# lấy ảnh dạng base64 từ server
def get_base64_image(image_name):
    image_base64 = None
    try:
        with open(os.path.join(current_app.config["UPLOAD_FOLDER"], image_name), 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        return image_base64
    except:
        return image_base64


#######################
# TẠO JSON WEB TOKEN #
#####################

# tạo json web token cho customer
#---------------------------------------------------------
def generate_jwt_customer(customer_name, expiration=3600):
    s = Serializer(current_app.config["SECRET_KEY"] + "customer", expiration)
    return s.dumps({"customer_name": customer_name}).decode("utf-8")

# tạo json web token tạm cho customer chưa confirm
#---------------------------------------------------------
def generate_jwt_customer_unconfirm(customer_name, expiration=300):
    s = Serializer(current_app.config["SECRET_KEY"] + "customer unconfirm", expiration)
    return s.dumps({"customer_name": customer_name}).decode("utf-8")

# tạo json web token cho admin
#---------------------------------------------------
def generate_jwt_admin(admin_name, expiration=3600):
    s = Serializer(current_app.config["SECRET_KEY"] + "admin", expiration)
    return s.dumps({"admin_name": admin_name}).decode("utf-8")

# tạo json web token cho xác thực email
#---------------------------------------------------------------
def generate_jwt_confirm_email(customer_email, expiration=3600):
    s = Serializer(current_app.config["SECRET_KEY"] + "confirm email", expiration)
    return s.dumps({"customer_email": customer_email}).decode("utf-8")

#####################
# KIỂM TRA BẢO MẬT #
###################

# kiểm tra xem confirm-token và access-token có cùng định danh một người không
#-------------------
def check_verify_email(f):
    @wraps(f)
    def decorated(current_user ,*args, **kwargs):
        status = False
        msg = ""
        s = Serializer(current_app.config["SECRET_KEY"] + "confirm email")
        data = request.json if request.json else []
        confirm_token = data["confirm_token"] if "confirm_token" in data else None
        if not confirm_token:
            msg = "Confirm token is missing"
            return jsonify(status=status, msg=msg), 401
        try:
            # giải mã token lấy dữ liệu
            data = s.loads(confirm_token.encode("utf-8"))

            # nếu email trong confirm-token khác email trong user hiện tại request thì báo lỗi
            if current_user["customer_email"] != data["customer_email"]:
                msg = "Confirm token is invalid"
                return jsonify(status=status, msg=msg), 401
        # nếu các bước trên lỗi thì báo lỗi
        except:
            msg = "Confirm token is invalid"
            return jsonify(status=status, msg=msg), 401
        return f(current_user ,*args, **kwargs)
    # đúng hết thì đi tiếp
    return decorated

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
            return jsonify(msg = "Token is missing !", status = False), 401
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
            if not current_user:
                return jsonify(msg = "Token is invalid !", status = False), 401
            # kiểm tra xem token có trong blacklist không
            cursor.execute(
                'SELECT * FROM blacklist_token_customer WHERE customer_id = % s AND token = % s', 
                    (current_user["customer_id"], token))
            check = cursor.fetchone()
            if check:
                return jsonify(msg = "Token is invalid !", status = False), 401

            # đóng kết nối databases
            cursor.close()
        # nếu các bước trên bị lỗi thì coi như token không hợp lệ
        except: 
            return jsonify(msg = "Token is invalid !", status = False), 401
        # trả về người dùng hiện tại
        return  f(current_user, *args, **kwargs) 
    return decorated

# yêu cầu kiểm tra token trước khi thực hiện API phía customer chưa xác thực
#------------------------------
def token_required_customer_unconfirm(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        s = Serializer(current_app.config["SECRET_KEY"] + "customer unconfirm")
        token = None

        # kiểm tra xem token có trong header không
        if "x-access-token" in request.headers: 
            token = request.headers["x-access-token"] 
        # trả về 401 nếu không có token
        if not token: 
            return jsonify(msg = "Token is missing !", status = False), 401
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
            if not current_user:
                return jsonify(msg = "Token is invalid !", status = False), 401
            # đóng kết nối databases
            cursor.close()
        # nếu các bước trên bị lỗi thì coi như token không hợp lệ
        except: 
            return jsonify(msg = "Token is invalid !", status = False), 401
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

            if not current_user:
                return jsonify({"msg" : "Token is invalid !", "status" : False}), 401

            # kiểm tra xem token có trong blacklist không
            cursor.execute(
                'SELECT * FROM blacklist_token_admin WHERE admin_id = % s AND token = % s', 
                    (current_user["admin_id"], token))
            check = cursor.fetchone()
            if check:
                return jsonify(msg = "Token is invalid !", status = False), 401

            # đóng kết nối database
            cursor.close()
        # nếu các bước trên bị lỗi thì coi như token không hợp lệ
        except: 
            return jsonify(msg = "Token is invalid !", status = False), 401
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
            cursor.close()

            # nếu không có quyền đó thì trả về tin nhắn và báo lỗi 401
            if not check:
                return jsonify(msg= "You don't have permission !", status = False), 401 
            
            # nếu có thì tiếp tục thực hiện API
            return f(*args, **kwargs)
        return decorated_function
    return decorator
