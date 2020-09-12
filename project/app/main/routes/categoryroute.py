from flask import Blueprint
from flask import request
from ..services.categoryservices import *
import json

category = Blueprint("categories" , __name__)

@category.route("/add", methods = ['POST'])
def add_category():
    auth_code = request.headers['auth_code']
    resp = add(request.json,auth_code)
    return json.dumps({"msg":resp})


@category.route("/show", methods = ["GET"])
def show():
    auth_code = request.headers['auth_code']
    resp = category_show(auth_code)
    return json.dumps({"categories":resp})

@category.route("/show/<category>", methods = ['GET'])
def show_category(category):
    auth_code = request.headers['auth_code']
    resp = category_sub(auth_code,category)
    return json.dumps({"categories": resp})