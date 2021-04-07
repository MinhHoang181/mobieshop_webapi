from flask import Blueprint, request, jsonify
from app.tools import token_required_admin, permission_required
from app import mysql
from app.models import Admin, Permission, Action, Role
import MySQLdb.cursors

role = Blueprint("role", __name__)

##################################
# QUẢN LÝ CHỨC VỤ QUẢN TRỊ VIÊN #
################################

# Xem một chức vụ phụ thuôc biến truyền vào
# - Nếu có biến role_id/role_name là xem 1 chức vụ
# - Nếu không có gì thì xem chức vụ của admin request
#------------------------------------------
@role.route("/admin/role", methods=["GET"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.READ)
def get_role(current_user):
    msg = ""
    role = {}
    status = False

    if request.method == "GET":
        role_id = request.args["role_id"] if "role_id" in request.args else None
        role_name = request.args["role_name"] if "role_name" in request.args else None

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # nếu có biến role_id thì dùng
        if role_id:
            cursor.execute(
                'SELECT * FROM roles WHERE role_id = % s', (role_id, ))
            data = cursor.fetchone()
            cursor.close()
        # nếu có biến role_name
        elif role_name:
            cursor.execute(
                'SELECT * FROM roles WHERE role_name = % s', (role_name, ))
            data = cursor.fetchone()
            cursor.close()
        # không có cả 2 là xem chức vụ của admin request
        else:
            cursor.execute(
                'SELECT * FROM roles WHERE role_name = % s', (current_user["admin_role"], ))
            data = cursor.fetchone()
            cursor.close()
        if data:
            role = {
                "role_id" : data["role_id"],
                "role_name" : data["role_name"]
            }
            status = True
        else:
            msg = "Error access database or roles is empty"
    return jsonify(status=status, msg=msg, role=role)

# xem danh sách chức vụ
#----------------------------------------------
@role.route("/admin/role/all", methods=["GET"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.READ)
def get_roles_all(current_user):
    msg = ""
    roles = []
    status = False

    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM roles')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                role = {
                    "role_id" : row["role_id"],
                    "role_name" : row["role_name"]
                }
                roles.append(role)
            status = True
        else:
            msg = "Error access database or roles is empty"
    return jsonify(status=status, msg=msg, roles=roles)

# thêm chức vụ
#--------------------------------------------------
@role.route("/admin/role/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.CREATE)
def create_role(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        role_name = data["role_name"] if "role_name" in data else None

        if not role_name:
            msg = "Role name is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM roles WHERE role_name = % s', (role_name, ))
            role = cursor.fetchone()
            if role:
                msg = "Role name already exists !"
            else:
                cursor.execute(
                    'INSERT INTO roles VALUES (NULL, % s)', (role_name, ))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "You have successfully added!"

    return jsonify(status=status, msg=msg)

# Sửa chức vụ
#------------------------------------------------
@role.route("/admin/role/edit", methods=["POST"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.EDIT)
def edit_role(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        role_id = data["role_id"] if "role_id" in data else None
        role_name = data["role_name"] if "role_name" in data else None

        if not role_id:
            msg = "Role id is missing !"
        # nếu tên rỗng
        elif not role_name:
            msg = "Role name is missing !"
        else:
            # kiểm tra xem có role đó chưa qua id
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM roles WHERE role_id = % s', (role_id, ))
            role = cursor.fetchone()
            # kiểm tra xem tên mới có tồn tại rồi chưa
            cursor.execute(
                'SELECT * FROM roles WHERE role_name = % s', (role_name, ))
            new_name = cursor.fetchone()
            # nếu tên bị trùng
            if new_name:
                msg = "Role name already exists !"
            # nếu tên hợp lệ và có role đó thì cập nhật
            elif role:
                cursor.execute(
                    'UPDATE `roles` SET `role_name` = % s WHERE `roles`.`role_id` = % s', (
                        role_name, role_id,)
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Role name has been updated!"
            else:
                msg = "Fail to update role!"

    return jsonify(status=status, msg=msg)

# Xoá chức vụ thông qua biến role_id hoặc role_name đều được
#--------------------------------------------------
@role.route("/admin/role/delete", methods=["POST"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.DELETE)
def delete_role(current_user):
    status = False
    msg = ""

    if request.method == "POST":
        
        data = request.json if request.json else []

        role_id = data["role_id"] if "role_id" in data else None
        role_name = data["role_name"] if "role_name" in data else None

        if not role_id and not role_name:
            msg = "Role id or name is missing"
        else:
            cursor = mysql.connection.cursor()
            
            if role_id:
                cursor.execute(
                    'SELECT * FROM roles WHERE role_id = % s', (role_id, ))
                role = cursor.fetchone()
            elif role_name:
                cursor.execute(
                    'SELECT * FROM roles WHERE role_name = % s', (role_name, ))
                role = cursor.fetchone()
            if role:
                if role_id:
                    cursor.execute(
                        'DELETE FROM roles WHERE role_id = % s', (role_id,  ))
                elif role_name:
                    cursor.execute(
                        'DELETE FROM roles WHERE role_name = % s', (role_name,    ))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Role has been deleted!"
            else:
                msg = "Fail to delete !"

    return jsonify(status=status, msg=msg)


##############################
# QUẢN LÝ QUYỀN CỦA CHỨC VỤ # 
############################

# Xem mọi quyền của chức vụ hoặc của user hiện tại
# - Nếu có biến role_id hoặc role_name là xem quyền hạn của chức vụ đó (Khuyên dùng role_name)
# - Nếu không có gì mặc định là xem chức vụ của admin request api này
#-----------------------------------------------------
@role.route("/admin/role/permission", methods=["GET"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.READ)
def get_role_permission(current_user):
    msg = ""
    status = False

    if request.method == "GET":
        role_id = request.args["role_id"] if "role_id" in request.args else None
        role_name = request.args["role_name"] if "role_name" in request.args else None

        cursor = mysql.connection.cursor()

        # nếu không có biến role_name
        if not role_name:
            # nếu có biến role_id thì tìm kiếm database để lấy biến role_name
            if role_id:
                cursor.execute(
                    'SELECT role_name FROM roles WHERE role_id = % s', (role_id, ))
                role_name = cursor.fetchone()[0]
            # ko có cả 2 biến mặc định là xem của admin hiện tại
            else:
                role_name = Admin(current_user).role

        # lấy hết giá trị role để tạo object Role cho dễ sài
        cursor.execute(
            'SELECT * FROM roles WHERE role_name = % s', (role_name, ))
        role = cursor.fetchone()
        if role:
            role = Role(role)
            permissions = role.get_all_permission()
            status = True
        else:
            msg = "role name or id is missing or wrong"
        cursor.close
    return jsonify(status=status, msg=msg, permissions=permissions)

# xem danh sách quyền
#----------------------------------------------------------
@role.route("/admin/role/permission/list", methods=["GET"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.READ)
def get_permissions_list(current_user):
    msg = ""
    permissions = []
    status = False

    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM permissions')
        data = cursor.fetchall()
        cursor.close()
        if data:
            for row in data:
                perm = Permission(row)
                permission = {
                    "permission_id" : perm.id,
                    "permission_name" : perm.name,
                    "permission_detail" : perm.detail
                }
                permissions.append(permission)
            status = True
        else:
            msg = "Error access database or roles is empty"
    return jsonify(status=status, msg=msg, permissions=permissions)

# Thêm quyền cho chức vụ
#-------------------------------------------------------------
@role.route("/admin/role/permission/create", methods=["POST"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.CREATE)
def add_permissions(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        role_name = data["role_name"] if "role_name" in data else None
        permission_name = data["permission_name"] if "permission_name" in data else None
        action_name = data["action_name"] if "action_name" in data else None

        if not role_name:
            msg = "Role name is missing"
        elif not permission_name:
            msg = "Permission name is missing"
        elif not action_name:
            msg = "Action name is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM permission_role WHERE role_name = % s AND permission_name = % s AND action_name = % s', 
                    (role_name, permission_name, action_name))
            permission = cursor.fetchone()
            if permission:
                msg = "Role already have this permission"
            else:
                cursor.execute(
                    'INSERT INTO permission_role VALUES (NULL, % s, % s, % s)', (role_name, permission_name, action_name))
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Permission have successfully added!"

    return jsonify(status=status, msg=msg)

# Xoá quyền cho chức vụ
#-------------------------------------------------------------
@role.route("/admin/role/permission/delete", methods=["POST"])
@token_required_admin
@permission_required(Permission.ROLE_MANAGER, Action.DELETE)
def delete_permissions(current_user):
    status = False
    msg = ""

    if request.method == "POST":

        data = request.json if request.json else []

        role_name = data["role_name"] if "role_name" in data else None
        permission_name = data["permission_name"] if "permission_name" in data else None
        action_name = data["action_name"] if "action_name" in data else None

        if role_name:
            msg = "Role name is missing"
        elif permission_name:
            msg = "Permission name is missing"
        elif action_name:
            msg = "Action name is missing"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM permission_role WHERE role_name = % s AND permission_name = % s AND action_name = % s', 
                    (role_name, permission_name, action_name))
            permission = cursor.fetchone()
            if permission:
                cursor.execute(
                    'DELETE FROM permission_role WHERE role_name = % s AND permission_name = % s AND action_name = % s', 
                        (role_name, permission_name, action_name)
                )
                mysql.connection.commit()
                cursor.close()

                status = True
                msg = "Permission has been deleted!"
            else:
                msg = "Fail to delete !"

    return jsonify(status=status, msg=msg)