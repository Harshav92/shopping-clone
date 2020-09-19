from flask import Blueprint
from flask import request
from ..services.productservice import *
import json


product = Blueprint("products", __name__)

@product.route("/add", methods= ['POST'])
def add():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = add_product(auth_code,data)
    return json.dumps({"msg":resp})


@product.route("/edit", methods= ['POST'])
def edit():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = edit_product(auth_code, data)
    return json.dumps({"msg":resp})


@product.route("/show", methods= ["GET"])
def show():
    page = request.args.get('page', default=1, type=int)
    items_page = 3
    resp = product_show(request.headers["auth_code"], page, items_page)
    return json.dumps({"msg":resp})

@product.route("/addmeta/product", methods= ["POST"])
def add_meta():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = add_product_meta(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/editmeta/product", methods = ['POST'])
def delete_meta():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = add_product_meta(auth_code, data)
    return json.dumps({"msg": resp})


@product.route("/assign/category", methods= ["POST"])
def assign_category():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = prod_cat(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/search/<category>", methods= ['GET'])
def search(category):
    page = request.args.get("page", default=1, type=int)
    auth_code = request.headers['auth_code']
    #category = request.json["category"]
    resp = prod_search(auth_code, category, page)
    return json.dumps({"msg": resp})


@product.route("/wishlist/add", methods=['POST'])
def add_wish():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = wish_add(auth_code, data)
    return json.dumps({"msg":resp})


@product.route("/wishlist/delete", methods=['POST','DELETE'])
def delete_wish():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = wish_delete(auth_code, data)
    return json.dumps({"msg": resp})
    

@product.route("/cart/add", methods=['POST'])
def add_cart():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = cart_add(auth_code, data)
    return json.dumps({"msg": resp})


@product.route("/cart/delete", methods=['POST','DELETE'])
def delete_cart():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = cart_delete(auth_code, data)
    return json.dumps({"msg": resp})


@product.route("/buy", methods=['POST'])
def buy():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = buy_product(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/show/wishlist", methods=['GET'])
def show_wish():
    auth_code = request.headers['auth_code']
    resp = wish_show(auth_code)
    return json.dumps({"msg": resp})

@product.route("/show/cart", methods=['GET'])
def show_cart():
    auth_code = request.headers['auth_code']
    resp = cart_show(auth_code)
    return json.dumps({"msg": resp})

@product.route("/checkout/cart", methods=['POST'])
def checkout_cart():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = cart_checkout(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/comment", methods=['POST'])
def comment():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = add_comment(auth_code, data)
    return json.dumps({"msg": resp})


@product.route("/comment/show", methods=['POST'])
def comment_show():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = show_comment(auth_code, data)
    return json.dumps({"msg": resp})


@product.route("/comment/upvote", methods=['POST'])
def upvoted():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = upvote(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/comment/downvote", methods=['POST'])
def downvoted():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = downvote(auth_code, data)
    return json.dumps({"msg": resp})

@product.route("/rating", methods=['POST'])
def ratings():
    auth_code = request.headers['auth_code']
    data = request.json
    resp = add_ratings(auth_code, data)
    return json.dumps({"msg": resp})




