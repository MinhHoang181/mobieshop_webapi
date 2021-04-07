from app.models import Permission
from flask import Blueprint, request, jsonify
from app import NO_IMAGE, SIZE_THUMNAIL, mysql
import MySQLdb.cursors
from app.tools import token_required_admin, permission_required, allowed_file, upload_image
from app.models import Permission, Action, Product, Admin
from datetime import datetime

product = Blueprint("product", __name__)

#####################
# QUẢN LÝ SẢN PHẨM #
###################

# lấy thông tin một sản phẩm
# - Biến truyền vào là id 
#------------------------------------------------
@product.route("/admin/product", methods=['GET'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.READ)
def get_product(current_user):
    status = False
    msg = ""
    product = {}

    if request.method == 'GET':
        prodcut_id = request.args["product_id"] if "product_id" in request.args else None

        if not prodcut_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (prodcut_id,))
            data = cursor.fetchone()
            cursor.close()
            if data:
                data = Product(data)
                product = {
                    "product_id": data.id,
                    "product_name": data.name,
                    "brand": {
                        "brand_id": data.brand.id,
                        "brand_name": data.brand.name
                    },
                    "product_thumbnail": {
                        "image_name": data.thumbnail.name,
                        "image_base64": data.thumbnail.base64
                    },
                    "product_description": data.description,
                    "product_default_price": data.default_price,
                    "product_sale_price": data.sale_price,
                    "time_warranty": data.time_warranty,
                    "product_last_update_who": {
                        "admin_id": data.last_update_who.id,
                        "admin_name": data.last_update_who.name
                    },
                    "product_last_update_when": data.last_update_when
                }
                status = True
            else:
                msg = "Fail access database"
    return jsonify(status=status, msg=msg, product=product)

# Lấy thông tin của tất cả sản phẩm
#----------------------------------------------------
@product.route("/admin/product/all", methods=['GET'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.READ)
def get_product_all(current_user):
    status = False
    msg = ""
    products = []

    if request.method == 'GET':
        page = request.args.get("page", type=int)
        low_price = request.args.get("low_price", type=int)
        high_price = request.args.get("high_price", type=int)
        brand_id = request.args.get("brand_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not brand_id:
            cursor.execute(
                'SELECT * FROM products WHERE (product_sale_price >= % s OR  % s IS NULL) AND (product_sale_price <= % s OR % s IS NULL)',
                (low_price, low_price, high_price, high_price, ))
            
        else:
            cursor.execute(
                'SELECT * FROM products WHERE brand_id = % s', 
                (brand_id, ))
        data = cursor.fetchall()
        cursor.close()
        if data:
            if page:
                first_index = (page - 1) * Product.NUM_PER_PAGE
                last_index = first_index + Product.NUM_PER_PAGE - 1
                data = data[first_index:last_index]
            for row in data:
                row = Product(row)
                product = {
                    "product_id": row.id,
                    "product_name": row.name,
                    "brand": {
                        "brand_id": row.brand.id,
                        "brand_name": row.brand.name
                    },
                    "product_thumbnail": {
                        "image_name": row.thumbnail.name,
                        "image_base64": row.thumbnail.base64
                    },
                    "product_images": row.images,
                    "product_description": row.description,
                    "product_default_price": row.default_price,
                    "product_sale_price": row.sale_price,
                    "time_warranty": row.time_warranty,
                    "product_last_update_who": {
                        "admin_id": row.last_update_who.id,
                        "admin_name": row.last_update_who.name
                    },
                    "product_last_update_when": row.last_update_when
                }
                products.append(product)
            status = True
        else:
            msg = "Fail access database"
    return jsonify(status=status, msg=msg, products=products)

# Thêm sản phẩm
#--------------------------------------------------------
@product.route("/admin/product/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.CREATE)
def add_product(current_user):
    status = False
    msg = ""
    if request.method == "POST":
        data = request.json if request.json else []

        product_name = data["product_name"] if "product_name" in data else None
        brand_id = data["brand_id"] if "brand_id" in data else None
        product_thumbnail = data["product_thumbnail"] if "product_thumbnail" in data else None
        product_images = data["product_images"] if "product_images" in data else None
        product_description = data["product_description"] if "product_description" in data else None
        product_default_price = data["product_default_price"] if "product_default_price" in data else 0
        product_sale_price = data["product_sale_price"] if "product_sale_price" in data else 0
        time_warranty = data["time_warranty"] if "time_warranty" in data else 0
        product_last_update_when = datetime.now()

        if not product_name:
            msg = "Product name is missing"
        else:
            # kiểm tra xem có ảnh không
            # nếu có
            if product_thumbnail:
                # lấy 2 biến name và base64
                image_name = product_thumbnail["image_name"] if "image_name" in product_thumbnail else None
                image_base64 = product_thumbnail["image_base64"] if "image_base64" in product_thumbnail else None
                # nếu không có 2 biến này hoặc rỗng thì báo lỗi
                if not image_base64 or image_base64 == "":
                    msg = "Image base64 is missing"
                    return jsonify(status=status, msg=msg)
                elif not image_name or image_name == "":
                    msg = "Image name is missing"
                    return jsonify(status=status, msg=msg)
                # nếu định dạng ảnh không cho phép báo lỗi
                elif not allowed_file(image_name):
                    msg = "Image format is not allow"
                    return jsonify(status=status, msg=msg)
                # nếu thoả hết thì upload ảnh lên server
                else:
                    # upload lấy dạng ảnh đại diện 256x256 (TTHUMBNAIL)
                    upload = upload_image(image_name, image_base64, size=SIZE_THUMNAIL)
                    # nếu không upload thành công thì báo lỗi
                    if not upload:
                        msg = "Image upload fail"
                        return jsonify(status=status, msg=msg)
                    # upload thành công lấy file name lưu lên SQL
                    product_thumbnail = image_name
            else:
                # nếu không có ảnh thì cho ảnh mặc định
                product_thumbnail = NO_IMAGE

            # lưu tất cả ảnh của sản phẩm
            images = []
            if product_images:
                count = 0
                for image in product_images:
                    count += 1
                    # lấy 2 biến name và base64
                    image_name = image["image_name"] if "image_name" in image else None
                    image_base64 = image["image_base64"] if "image_base64" in image else None
                    # nếu không có 2 biến này hoặc rỗng thì báo lỗi
                    if not image_base64 or image_base64 == "":
                        msg += "\n Image " + str(count) + " base64 is missing"
                    elif not image_name or image_name == "":
                        msg += "\n Image " + str(count) + " name is missing"
                    # nếu định dạng ảnh không cho phép báo lỗi
                    elif not allowed_file(image_name):
                        msg += "\n Image " + str(count) + " format is not allow"
                    # nếu thoả hết thì upload ảnh lên server
                    else:
                        # upload lấy dạng ảnh thường
                        upload = upload_image(image_name, image_base64)
                        # nếu không upload thành công thì báo lỗi
                        if not upload:
                            msg += "\n Image " + str(count) +  " upload fail"
                        # upload thành công lấy file name lưu lên SQL
                        else:
                            images.append(image_name)


            # lấy danh tính admin đang request
            current_user = Admin(current_user)

            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO products VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (
                    product_name, brand_id, product_thumbnail, product_description, product_default_price, product_sale_price, time_warranty, current_user.id, product_last_update_when)
            )
            product_id = cursor.lastrowid
            mysql.connection.commit()
            

            # Lưu danh sách tên ảnh của sản phẩm đã upload thành công vào SQL
            for image in images:
                cursor.execute(
                    'INSERT INTO product_image(product_id, image) VALUES (% s, % s)',
                    (product_id, image,)
                )
                mysql.connection.commit()

            cursor.close()
            status = True
            msg = "You have successfully added product"
    return jsonify(status=status, msg=msg, product_id=product_id)

# Sửa sản phẩm
# - Thuộc tính nào cần sửa thì truyền vào json
#------------------------------------------------------
@product.route("/admin/product/edit", methods=['POST'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.EDIT)
def edit_product(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        data = request.json if request.json else []

        product_id = data["product_id"] if "product_id" in data else None
        product_name = data["product_name"] if "product_name" in data else None
        brand_id = data["brand_id"] if "brand_id" in data else None
        product_thumbnail = data["product_thumbnail"] if "product_thumbnail" in data else None
        product_images = data["product_images"] if "product_images" in data else None
        product_description = data["product_description"] if "product_description" in data else None
        product_default_price = data["product_default_price"] if "product_default_price" in data else None
        product_sale_price = data["product_sale_price"] if "product_sale_price" in data else None
        time_warranty = data["time_warranty"] if "time_warranty" in data else None
        product_last_update_when = datetime.now()

        # Nếu không có id thì báo lỗi
        if not product_id:
            msg = "Product id is missing"
        # Nếu có
        else:
            # kiểm tra xem có id sản phẩm đó không
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (product_id, ))
            product = cursor.fetchone()
            # nếu có
            if product:
                # lấy danh tính của admin đang request sửa sản phẩm
                current_user = Admin(current_user)
                # chuyển sang dạng object cho dễ sài
                product = Product(product)
                
                # kiểm tra xem có ảnh không
                # nếu có
                if product_thumbnail:
                    # lấy 2 biến name và base64
                    image_name = product_thumbnail["image_name"] if "image_name" in product_thumbnail else None
                    image_base64 = product_thumbnail["image_base64"] if "image_base64" in product_thumbnail else None
                    # nếu không có 2 biến này hoặc rỗng thì báo lỗi
                    if not image_base64 or image_base64 == "":
                        msg = "Image base64 is missing"
                        return jsonify(status=status, msg=msg)
                    elif not image_name or image_name == "":
                        msg = "Image name is missing"
                        return jsonify(status=status, msg=msg)
                    # nếu định dạng ảnh không cho phép báo lỗi
                    elif not allowed_file(image_name):
                        msg = "Image format is not allow"
                        return jsonify(status=status, msg=msg)
                    # nếu thoả hết thì upload ảnh lên server
                    else:
                        # upload lấy dạng ảnh đại diện 256x256 (TTHUMBNAIL)
                        upload = upload_image(image_name, image_base64, size=SIZE_THUMNAIL)
                        # nếu không upload thành công thì báo lỗi
                        if not upload:
                            msg = "Image upload fail"
                            return jsonify(status=status, msg=msg)
                        else:
                            # upload thành công lấy file name lưu lên SQL
                            product_thumbnail = image_name

                # lưu tất cả ảnh của sản phẩm
                images = []
                if product_images:
                    count = 0
                    for image in product_images:
                        count += 1
                        # lấy 3 biến name và base64 và id
                        image_id = image["image_id"] if "image_id" in image else None
                        image_name = image["image_name"] if "image_name" in image else None
                        image_base64 = image["image_base64"] if "image_base64" in image else None
                        # nếu không có 3 biến này hoặc rỗng thì báo lỗi
                        if not image_base64 or image_base64 == "":
                            msg += "\n Image " + str(count) + " base64 is missing"
                        elif not image_name or image_name == "":
                            msg += "\n Image " + str(count) + " name is missing"
                        elif not image_id:
                            msg += "\n Image " + str(count) + " id is missing"
                        # nếu định dạng ảnh không cho phép báo lỗi
                        elif not allowed_file(image_name):
                            msg += "\n Image " + str(count) + " format is not allow"
                        # nếu thoả hết thì upload ảnh lên server
                        else:
                            # upload lấy dạng ảnh thường
                            upload = upload_image(image_name, image_base64)
                            # nếu không upload thành công thì báo lỗi
                            if not upload:
                                msg += "\n Image " + str(count) +  " upload fail"
                            # upload thành công lấy file name lưu lên SQL
                            else:
                                images.append(
                                    {
                                        "image_id": image_id,
                                        "image_name": image_name
                                    }
                                )

                # nếu không có biến nào thì lấy giá trị cũ biến đó
                if not product_name:
                    product_name = product.name
                if not brand_id:
                    brand_id = product.brand.id
                if not product_thumbnail:
                    product_thumbnail = product.thumbnail.name
                if not product_description:
                    product_description = product.description
                if not product_default_price:
                    product_default_price = product.default_price
                if not product_sale_price:
                    product_sale_price = product.sale_price
                if not time_warranty:
                    time_warranty = product.time_warranty

                cursor.execute(
                    'UPDATE `products` SET `product_name` = % s, `brand_id` = % s, `product_thumbnail` = % s, `product_description` = % s, `product_default_price` = % s, `product_sale_price` = % s, `time_warranty` = % s, `product_last_update_who` = % s, `product_last_update_when` = % s WHERE `products`.`product_id` = % s', (
                        product_name, brand_id, product_thumbnail, product_description, product_default_price, product_sale_price, time_warranty, current_user.id, product_last_update_when, product_id)
                )
                mysql.connection.commit()

                # Lưu danh sách tên ảnh của sản phẩm đã upload thành công vào SQL
                for image in images:
                    cursor.execute(
                        'UPDATE product_image SET image = % s WHERE product_image_id = % s',
                        (image["image_name"], image["image_id"], )
                    )
                    mysql.connection.commit()
                msg = "Product info has been updated!"
            else:
                msg = "Fail to update info!"
            cursor.close()
    return jsonify(status=status, msg=msg)

# Xoá sản phẩm
# - Biến truyền vào là id
#--------------------------------------------------------
@product.route("/admin/product/delete", methods=['POST'])
@token_required_admin
@permission_required(Permission.PRODUCT_MANAGER, Action.DELETE)
def delete_product(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []
        product_id = data["product_id"] if "product_id" in data else None

        if not product_id:
            msg = "Product id is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE product_id = % s', (product_id, ))
            product = cursor.fetchone()
            if product:
                cursor.execute(
                    'DELETE FROM `products` WHERE `products`.`product_id` = % s', (
                        product_id,)
                )
                mysql.connection.commit()

                status = True
                msg = "Product has been deleted!"
            else:
                msg = "Fail to delete!"

    return jsonify(status=status, msg=msg)