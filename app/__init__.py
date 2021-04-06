from flask import Flask, current_app
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_mail import Mail
import os

mysql = MySQL()
cors = CORS()
mail = Mail()

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SIZE_THUMNAIL = (256, 256)
NO_IMAGE = "no_image.png"

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "mobileshop_soa"

    # thiết lập kết nối MySQL
    app.config['MYSQL_Host'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'mobileshop'

    # thư mục upload
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # thiết lập kết nối mail
    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config['MAIL_USERNAME'] = "soa.mobileshop@gmail.com"
    app.config['MAIL_PASSWORD'] = "soa123456"

    # thiết lập Celery
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    mysql.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    # API cơ bản hoặc chung
    from .api.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API của khách hàng
    from .api.customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)

    # API của quản trị viên
    from .api.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # API của quản lý chức vụ
    from .api.manager.role import role as role_blueprint
    app.register_blueprint(role_blueprint)

    # API của quản lý tài khoản
    from .api.manager.account import account as account_blueprint
    app.register_blueprint(account_blueprint)

    # API của quản lý sản phẩm
    from .api.manager.product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    # API của quản lý nhãn hiệu
    from .api.manager.brand import brand as brand_blueprint
    app.register_blueprint(brand_blueprint)

    # API của quản lý hoá đơn
    from .api.manager.bill import bill as bill_blueprint
    app.register_blueprint(bill_blueprint)

    # API của quản lý đơn hàng
    from .api.manager.order import order as order_blueprint
    app.register_blueprint(order_blueprint)

    return app