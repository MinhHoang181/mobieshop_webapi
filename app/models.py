from app import mysql
import MySQLdb.cursors

# Khách hàng
class Customer():
    def __init__(self, current_user):
        self.id = current_user["customer_id"] if current_user else None
        self.name = current_user["customer_name"] if current_user else None
        self.password_hash = current_user["customer_password"] if current_user else None
        self.address = current_user["customer_address"] if current_user else None
        self.phone = current_user["customer_phone"] if current_user else None

# Quản trị viên
class Admin():
    def __init__(self, current_user):
        self.id = current_user["admin_id"] if current_user else None
        self.name = current_user["admin_name"] if current_user else None
        self.password_hash = current_user["admin_password"] if current_user else None
        self.email = current_user["admin_email"] if current_user else None
        self.role = current_user["admin_role"] if current_user else None

# chức vụ
class Role():

    def __init__(self, role):
        self.id = role[0]
        self.name = role[1]
        self.permissions = []

        # lưu danh sách quyền hạn
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT permission_name, action_name FROM permission_role WHERE role_name = % s', (
                self.name,)
        )
        data = cursor.fetchall()
        term = []
        for x in data:
            # lấy dữ liệu quyền dưới dạng object
            if x[0] not in term:
                # tạo object Permission
                term.append(x[0])
                cursor.execute(
                    'SELECT * FROM permissions WHERE permission_name = % s', (x[0],)
                )
                self.permissions.append(Permission(cursor.fetchone()))
            # lưu các hành động
            if x[1] not in self.permissions[term.index(x[0])].actions:
                self.permissions[term.index(x[0])].actions.append(x[1])
            
        cursor.close()

    def get_all_permission(self):
        perm_list = []
        for perm in self.permissions:
            data = {
                "name" : perm.name,
                "detail" : perm.detail,
                "actions": perm.actions
            }
            perm_list.append(data)
        return perm_list

# Quyền hạn
class Permission():
    ROLE_MANAGER = "RoleManager"
    ACCOUNT_MANAGER = "AccountManager"
    PRODUCT_MANAGER = "ProductManager"
    BRAND_MANAGER = "BrandManager"
    COUPON_MANAGER = "CouponManager"

    def __init__(self, permission):
        self.id = permission[0]
        self.name = permission[1]
        self.detail = permission[2]
        self.actions = []

# Loaị hành động
class Action():
    READ = "read"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"

# Sản phẩm
class Product():
    def __init__(self, product):
        self.id = product["product_id"] if product else None
        self.name = product["product_name"] if product else None
        self.thumbnail = product["product_thumbnail"] if product else None
        self.description = product["product_description"] if product else None
        self.default_price = product["product_default_price"] if product else None
        self.sale_price = product["product_sale_price"] if product else None
        self.last_update_when = product["product_last_update_when"] if product else None

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Lấy thông tin nhãn hiệu
        cursor.execute(
            'SELECT * FROM brands WHERE brand_id = % s', (product["brand_id"], )
        )
        self.brand = Brand(cursor.fetchone())
        # Lấy thông tin quản trị viên cập nhật cuối
        cursor.execute(
            'SELECT * FROM admins_account WHERE admin_id = % s', (product["product_last_update_who"], )
        )
        self.last_update_who = Admin(cursor.fetchone())

# nhãn hiệu
class Brand():
    def __init__(self, brand):
        self.id = brand["brand_id"] if brand else None
        self.name = brand["brand_name"] if brand else None

# Phiếu giảm giá
class Coupon():
    def __init__(self, coupon):
        self.id = coupon["coupon_id"] if coupon else None
        self.name = coupon["coupon_name"] if coupon else None
        self.code = coupon["coupon_code"] if coupon else None
        self.discount = coupon["coupon_discount"] if coupon else None