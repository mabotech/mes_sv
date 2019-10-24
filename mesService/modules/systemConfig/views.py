# -*- coding: utf-8 -*-
# @createTime    : 2019/8/30 10:05
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
import json
import traceback

from flask import current_app, request
from flask.json import jsonify

from . import system_config_blue


@system_config_blue.route('/menu_tree')
def menu_tree():
    """
    生产菜单树节点
    :return:
    """
    result = []
    menu_list = []
    menu_list_sql = """select get_menu_item();"""

    try:
        menu_list = current_app.db.query(menu_list_sql)[0]['get_menu_item']
    except Exception:
        current_app.logger.error(traceback.format_exc())

    # 拿到所有的id和menu的映射
    id_map_menu = {}

    for menu in menu_list:
        id = menu['id']
        id_map_menu[id] = menu

    for menu in menu_list:
        # 找到父节点加入到父节点的children
        parentid = menu['parentid']
        if parentid:
            parent = id_map_menu[parentid]
            parent_children = parent.get('children', [])
            if parent_children == []:
                parent['children'] = []
            parent['children'].append(menu)
        else:
            result.append(menu)

    return jsonify(result)


@system_config_blue.route('/delete_menu', methods=['POST', 'DELETE'])
def delete_menu():
    """
    删除菜单项
    :return:
    """
    result = 0
    try:
        req_data = request.get_data(as_text=True)
        dict_data = json.loads(req_data)
        id = dict_data.get('id')
        base_sql = """select deleteMenu({});"""
        sql = base_sql.format(id)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    try:
        result = current_app.db.execute(sql)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
    return jsonify({"result": result})


@system_config_blue.route('/get_menu_item', methods=['GET'])
def get_menu_item():
    """
    获取菜单列表
    :return:
    """
    sql = "select get_all_menu_item();"
    result = []
    try:
        result = current_app.db.query(sql)[0]['get_all_menu_item']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
    return jsonify(result)


@system_config_blue.route('/insert_menu', methods=['POST'])
def insert_menu():
    """
    插入菜单项
    :return:
    """
    result = 0
    try:
        data = request.get_data(as_text=True)
        json_data = json.loads(data)
        name = json_data['name']
        parentid = json_data['parentid']
        if parentid is None:
            parentid = 'null'
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    try:
        sql = "select insertMenu('{name}', {parentid});".format(name=name, parentid=parentid)
        result = current_app.db.execute(sql)
    except Exception as e:
        current_app.logger.errorresult = traceback.format_exc()
    return jsonify({'result': result})

@system_config_blue.route('/update_menu', methods=['POST'])
def update_menu():
    """
    更新菜单项
    :return:
    """
    result = 0

    try:
        data = request.get_data(as_text=True)
        sql = "select updatemenu('{}');".format(data)
        result = current_app.db.execute(sql)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    return jsonify({'result': result})


@system_config_blue.route('/get_menu_role', methods=['POST'])
def getMenuRole():
    """
    获取传入菜单项的权限
    :return:
    """
    result = []

    try:
        data = request.get_data(as_text=True)
        sql = "select getMenuRole('{}');".format(data)
        result = current_app.db.query(sql)[0]['getmenurole']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
    return jsonify(result)


@system_config_blue.route('/get_all_roles', methods=['GET'])
def get_all_roles():
    """
    获取所有权限
    :return:
    """
    sql = "select getAllRoles();"
    result = None
    try:
        result = current_app.db.query(sql)[0]['getallroles']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    return jsonify(result)


@system_config_blue.route('/delete_menu_role', methods=['POST'])
def delete_menu_role():
    """
    删除页面权限
    :return:
    """

    result = None
    try:
        data = request.get_data(as_text=True)
        sql = "select deletemenurole('{}');".format(data)
        result = current_app.db.query(sql)[0]['deletemenurole']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    return jsonify({"result": result})

@system_config_blue.route('/insert_menu_role', methods=['POST'])
def insert_menu_role():
    """
    添加页面权限
    :return:
    """

    result = None
    try:
        data = request.get_data(as_text=True)
        sql = "select insertmenurole('{}');".format(data)
        result = current_app.db.query(sql)[0]['insertmenurole']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    return jsonify({"result": result})

@system_config_blue.route('/link_menu', methods=['POST'])
def link_menu():
    """
    连接页面
    :return:
    """

    result = None
    try:
        data = request.get_data(as_text=True)
        sql = "select linkMenu('{}');".format(data)
        result = current_app.db.query(sql)[0]['linkmenu']
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    return jsonify({"result": result})
