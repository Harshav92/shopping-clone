from flask import Blueprint
from flask import request
import json
import jwt
import datetime
from ..services.userservices import *


user = Blueprint("users", __name__)

@user.route("/register", methods=["POST"])

def register():
    """
    user registration
    """
    dct = request.json
    resp = register_user(dct)
    return json.dumps({"msg":resp})

@user.route("/login", methods=['GET'])
def login():
    """
    user login
    """
    dct = request.json
    resp = login_user(dct)
    return json.dumps({"msg":resp})

@user.route("/delete", methods=["DELETE"])
def delete():
    """
    delete user
    """
    resp = delete_user(dct)
    return json.dumps({"msg":resp})


@user.route("/address/add", methods=['POST'])
def add_adress():
    """
    adress add
    """
    auth_code = request.headers['auth_code']
    data = request.json
    resp = address_add(data,auth_code)
    return json.dumps({"msg":resp})

@user.route("/address/edit", methods=['POST'])
def edit_adress():
    """
    adress edit
    """
    auth_code = request.headers['auth_code']
    data = request.json
    resp = address_edit(data,auth_code)
    return json.dumps({"msg":resp})

@user.route("/address/show", methods=['GET'])
def show_adress():
    """
    adress show
    """
    auth_code = request.headers['auth_code']
    resp = address_show(auth_code)
    return json.dumps({"msg":resp})

