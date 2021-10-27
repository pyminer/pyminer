# -*- coding: utf-8 -*-
"""
@Time ： 2020/12/12 16:24
@Author ： 别着急慢慢来
@File ：qt_vditor.py
@Software ：PyCharm
"""

from flask import Blueprint
from flask import Flask, request, jsonify, json, Response
from flask import render_template
import os
import re
from PySide2 import QtWidgets

qt_vditor = Blueprint('qt_vditor',
                      __name__,
                      url_prefix='/qt_vditor',
                      template_folder='templates')


def from_local_md_image(md_content):
    pattern = re.compile(r'(?:!\[(.*?)\]\((.*?)\))')
    new_content = pattern.sub(from_localpics, md_content)
    return new_content


def from_localpics(m):
    result = m.group(2)
    if result.startswith('file:///'):
        result.lstrip('file:///')
    return "![{}](".format(m.group(1)) + result + ")"


@qt_vditor.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        data = {
            'md_content': json_data['md_content'],
            'url': json_data['url'],
            'md_path': json_data['md_path'],
        }
        return render_template("index.html", data=data)


@qt_vditor.route('/insert_picture', methods=['GET'])
def insert_picture():
    if request.method == 'GET':
        dialog = QtWidgets.QDialog()
        name, ok = QtWidgets.QFileDialog.getOpenFileName(dialog, 'Open figure object', os.path.expanduser('~'),
                                                         filter='Image files (*.jpg *.gif *.jpeg *.png)')
        if os.path.exists(name):
            return {
                'filepath': '![](file:///' + name.replace('\\', '/') + ')',
                'code': 0
            }
        else:
            return {
                'filepath': '',
                'code': 1
            }


@qt_vditor.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        content = json_data['md_content']
        file_path = json_data['filepath']
        content = from_local_md_image(content)
        if os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return 'ok'


@qt_vditor.route('/upload_file/<path>', methods=['POST'])
def upload_file(path):
    if request.method == 'POST':
        url = json.loads(request.get_data())
        print(path)
        # hex = path.encode('utf-8')
        # str_bin = binascii.unhexlify(hex)
        # md_path = str_bin.decode('utf-8')
        # print(md_path)
        data = {
            "msg": "ok",
            "code": 0,
            "data": {
                "succMap": {
                    "": url,
                }
            }
        }
        return data, 200
