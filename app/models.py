from app import mysql
import MySQLdb.cursors

# Khách hàng
class Customer():
    def __init__(self, current_user):
        self.id = current_user["customer_id"] if current_user else None
        self.name = current_user["customer_name"] if current_user else None
        self.password_hash = current_user["customer_password"] if current_user else None
        self.email = current_user["customer_email"] if current_user else None
        self.address = current_user["customer_address"] if current_user else None
        self.phone = current_user["customer_phone"] if current_user else None

# Quản trị viên
class Admin():
    def __init__(self, current_user):
        self.id = current_user["admin_id"] if current_user else None
        self.name = current_user["admin_name"] if current_user else None
        self.password_hash = current_user["admin_password"] if current_user else None
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
    NUM_PER_PAGE = 12

    def __init__(self, product):
        self.id = product["product_id"] if product else None
        self.name = product["product_name"] if product else None
        self.thumbnail = product["product_thumbnail"] if product else None
        self.description = product["product_description"] if product else None
        self.default_price = product["product_default_price"] if product else None
        self.sale_price = product["product_sale_price"] if product else None
        self.time_warranty = product["time_warranty"] if product else None
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

# giỏ hàng
class Cart():
    def __init__(self, cart):
        self.customer = cart['customer_id'] if cart else None
        self.quantity = int(cart["quantity"]) if cart else None

        # Lấy thông tin sản phẩm
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM products WHERE product_id = % s', (cart["product_id"], )
        )
        self.product = Product(cursor.fetchone())

# hoá đơn
class Bill():
    def __init__(self, bill):
        self.id = bill["bill_id"] if bill else None
        self.fee_ship = int(bill["fee_ship"]) if bill else 0
        self.time_create = bill["time_create"] if bill else None

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # lấy thông tin khách hàng
        self.customer = {}
        cursor.execute(
            'SELECT * FROM customers_account WHERE customer_id = % s', (bill["customer_id"], ) 
        )
        data = cursor.fetchone()
        if data:
            self.customer = {
                "customer_id": data["customer_id"],
                "customer_name": data["customer_name"]
            }

        # Lấy thông tin sản phẩm
        self.products = []
        cursor.execute(
            'SELECT product_id, quantity FROM product_bill WHERE bill_id = % s', (self.id, )
        )
        data = cursor.fetchall()
        if data:
            for row in data:
                cursor.execute(
                    'SELECT * FROM products WHERE product_id = % s', (row["product_id"], )
                )
                x = cursor.fetchone()
                product = {
                    "product_id": x["product_id"],
                    "product_name": x["product_name"],
                    "product_price": int(x["product_sale_price"]),
                    "quantity": int(row["quantity"]),
                    "product_total": int(x["product_sale_price"]) * int(row["quantity"])
                }
                self.products.append(product)

        # lấy tổng tiền
        self.total = 0
        for product in self.products:
            self.total += product["product_total"]
        self.total -= self.fee_ship

class Order():
    def __init__(self, order):
        self.bill = order["bill_id"]
        self.status = order["status"]
        self.last_update = order["last_when_update"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # lấy thông tin khách hàng
        self.customer = {}
        cursor.execute(
            'SELECT * FROM customers_account WHERE customer_id = % s', (order["customer_id"], ) 
        )
        data = cursor.fetchone()
        if data:
            self.customer = {
                "customer_id": data["customer_id"],
                "customer_name": data["customer_name"]
            }
        # lấy thông tin quản trị viên cập nhật
        self.admin = {}
        cursor.execute(
            'SELECT * FROM admins_account WHERE admin_id = % s', (order["last_who_update"], ) 
        )
        data = cursor.fetchone()
        if data:
            self.admin = {
                "admin_id": data["admin_id"],
                "admin_name": data["admin_name"]
            }
        