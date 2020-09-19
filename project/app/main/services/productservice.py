from ..models.categorymodel import *
from ..models.ordermodel import *
from ..models.usermodel import *
from ..models.commentsmodel import *
from flask_sqlalchemy import sqlalchemy
from flask import current_app
import time
import jwt


def add_product(auth_head, data):
    try:
        if auth_code == None:
            return "401 invalid auth "
        auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
        if auth_code['time'] <= time.time():
            return "time expired login again"
        if auth_code['role'] != "owner":
            return "user not allowed to add categories"
        owner_id = auth_code["user_id"]
        prod_code = data['prod_code']
        name = data['name']
        price = data['price']
        row = Product.query.filter_by(prod_code=prod_code).first()
        if row==None:
            prod = Product()
            prod.name = name
            prod.prod_code = prod_code
            prod.price = price
            prod.owner_id = owner_id
            db.session.add(prod)
            db.session.commit()
            return "product added"

        else:
            return "product with product code already exist"
    except Exception as e:
        return str(e)


def edit_product(auth_head, data):
    try:
        if auth_code == None:
            return "401  invalid auth "
        auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
        if auth_code['time'] <= time.time():
            return "time expired login again"
        if auth_code['role'] == 'user':
            return "no permission"
        if auth_code['role'] == "owner":
            prod = Product.query.filter_by(id=data['prod_id']).first()
            if prod == None:
                return "product not found"
            if prod.owner_id != auth_code['user_id']:
                return "not the owner of product"
            
            if 'prod_code' in data.keys():
                prod.prod_code = data['prod_code']

            if 'name' in data.keys():
                prod.name = data['name']
            if 'price' in data.keys():
                prod.price = data['price']
            db.session.commit()
            return "product data edited"
        elif auth_code['role'] == "admin":
            prod = Product.query.filter_by(id=data['prod_id']).first()
            if prod == None:
                return "product not found"
            if 'prod_code' in data.keys():
                prod.prod_code = data['prod_code']
            if 'name' in data.keys():
                prod.name = data['name']
            if 'price' in data.keys():
                prod.price = data['price']
            db.session.commit()
            return "product data edited"
    except Exception as e :
        return str(e)


        


def product_show(auth_head, page, items_page):
    try:
        
        auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
        if auth_code == None:
            return "401 invalid auth"
        if auth_code['time'] <= time.time():
            return "time expired login again"
        start = (page-1)*items_page
        end = page*items_page
        ls = []
        if auth_code['role'] == "owner":
            query = "select  p.name as name, mp.image1_url as image ,floor(p.rating) as rating, p.id as prod_id, mp.inventory_count as quantity  from products as p join products_meta as mp on mp.product_id=p.id  order by p.id where p.owner_id = {} limit {},{};".format(auth_code['user_id'],start,end)
        else:
            query = "select  p.name as name, mp.image1_url as image ,floor(p.rating) as rating, p.id as prod_id, mp.inventory_count as quantity from products as p join products_meta as mp on mp.product_id=p.id  order by p.id  limit {},{};".format(start,end)
            
        data = db.session.execute(query)
        for each in data:
            row = {}
            
            row['id'] = each.prod_id
            row['image1_url'] = each.image
            row['quantity'] = each.quantity
            row['name'] = each.name
            row['rating'] = each.rating
            ls.append(row)

        return ls
    except Exception as e:
        return str(e)





def add_product_meta(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "owner":
        return "user not allowed "
    owner = Product.query.filter_by(id=data['prod_id']).first()
    if owner == None:
        return "product not found"
    if owner.owner_id != auth_code['user_id']:
        return "unauthorized to access the product"
    meta = MetaProduct.query.filter_by(product_id=data['prod_id']).first()
    if meta == None:
        prod_meta = MetaProduct()
        prod_meta.product_id = data['prod_id']
        if "image1_url" in data.keys():
            prod_meta.image1_url = data['image1_url']
        if "description" in data.keys():
            prod_meta.description = data['description']
        if "inventory_count" in data.keys():
            prod_meta.inventory_count = data['inventory_count']
        
        db.session.add(prod_meta)
        db.session.commit()
        return "meta info added"
    else:
        if "image1_url" in data.keys():
            meta.image1_url = data['image1_url']
        if "description" in data.keys():
            meta.description = data['description']
        if "inventory_count" in data.keys():
            meta.inventory_count = data['inventory_count']
        db.session.commit()
        return "meta info edited"


def prod_cat(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "admin":
        return "user not allowed "
    prod_id = data['prod_id']
    category_id = data['category_id']
    prod = Product.query.filter_by(id=prod_id).first()
    if prod == None:
        return "product_id invalid"
    ancestors = Tree.query.filter_by(descendant=category_id).all()
    for each in ancestors:
        data = ProductCategories.query.filter_by(category_id=each.ancestor, product_id=prod_id).first()
        if data == None:
            pc = ProductCategories()
            pc.category_id = each.ancestor
            pc.product_id = prod_id
            db.session.add(pc)
            db.session.commit()
    return "category assigned"
        

def prod_search(auth_head,cat,page ):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] == "owner":
        return "user not allowed "
    start = (page-1)*3
    end = page*3
    query = "p.name as name, p.price as price,p.id as id ,floor(p.rating) as rating, mp.image1_url as image, mp.inventory_count as quantity from products as p join product_categories as pc on pc.product_id = p.id join categories as c  on c.id = pc.category_id join products_meta as mp on mp.product_id=p.id  where c.name like '%{}%'  order by p.id limit {}, {} ;".format(cat,start,end)
    prod = db.session.execute(query)
    ls = []
    for each in prod:
        row= {}
        row['id'] = each.id
        row['name'] = each.name
        row['price'] = each.price
        row['image'] = each.image
        row['quantity'] = each.quantity
        row['rating'] = each.rating
        
        ls.append(row)
    if len(ls)==0:
        return "no products found"
    return ls


def wish_add(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    prod_id = data['prod_id']
    wish = WhishList()
    wish.user_id = user_id
    wish.product_id = prod_id
    wl = WhishList.query.filter_by(user_id=user_id, product_id=prod_id).first()
    if wl == None:
        db.session.add(wish)
        db.session.commit()
        return "added to wishlist"
    else:
        return "already in wishlist"

def wish_delete(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    prod_id = data['prod_id']
    wl = WhishList.query.filter_by(user_id=user_id, product_id=prod_id).first()
    if wl != None:
        db.session.delete(wl)
        db.session.commit()
        return "wish deleted"
    return "prod with user wish not found"


def cart_add(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    prod_id = data['prod_id']
    prod = MetaProduct.query.filter_by(product_id=prod_id).first()
    if prod == None:
        return "Inventory empty"
    if prod.inventory_count < 1:
        return "Inventory empty"

    cart = Cart.query.filter_by(product_id=prod_id, user_id=user_id).first()
    if cart==None:
        ct = Cart()
        ct.product_id = prod_id
        ct.user_id = user_id
        ct.quantity = 1
        db.session.add(ct)
        db.session.commit()
    else:
        cart.quantity = cart.quantity + 1
        db.session.commit()
    return "added to cart"

def cart_delete(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    prod_id = data['prod_id']
    cart = Cart.query.filter_by(product_id=prod_id, user_id=user_id).first()
    if cart == None:
        return "item not in cart"
    else:
        if cart.quantity>1:
            cart.quantity = cart.quantity-1
            db.session.commit()
            return "item count reduced"
        else:
            db.session.delete(cart)
            db.session.commit()
            return "item deleted"

def buy_product(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    prod_id = data['prod_id']
    address_id = data['address_id']
    address = Address.query.filter_by(id=address_id, user_id=auth_code['user_id']).first()
    if address==None:
        return "address not found add address"
    query = "select mp.inventory_count as quantity , p.price as price   from products as p join products_meta as mp on mp.product_id=p.id where mp.product_id ={}; ".format(prod_id)
    meta_prod = db.session.execute(query)
   
    if meta_prod==None:
        return "Inventory empty please try later"
    for each in meta_prod:
        if each.quantity==None or each.quantity<1:
            return "Inventory empty please try later"
    
        if data['mode'] == "cod":
            pay = Payment()
            pay.pay_amount = each.price
            pay.pay_method = "cod"
            pay.user_id = auth_code['user_id']
            db.session.add(pay)
            db.session.commit()
            pay_id = pay.id
            order  = Orders()
            order.order_value = each.price
            order.user_id = auth_code['user_id']
            order.payment_id = pay_id
            order.status = "initiated"
            order.address_id = address_id
            db.session.add(order)
            db.session.commit()
            curr_order_id = order.id
            order_prod = OrderProducts()
            order_prod.order_id = curr_order_id
            order_prod.product_id = prod_id
            order_prod.quantity = 1
            order_prod.cost = each.price
            db.session.add(order_prod)
            db.session.commit()
            return "order placed your order id {}".format(order.id)
        else:
            return "service not available please select cod"

def wish_show(auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    query = "select p.name as name from products as p join wishlist as w on w.product_id = p.id where w.user_id = {};".format(user_id)
    wish = db.session.execute(query)
    ls = []
    for each in wish:
        ls.append(each.name)
    if len(ls)==0:
        return "empty wish list"
    return ls
        
    

def cart_show(auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    query = "select p.name as name, c.quantity as quantity, p.id as prod_id from products as p join cart as c on c.product_id = p.id where c.user_id = {};".format(user_id)
    wish = db.session.execute(query)
    ls = []
    for each in wish:
        row = {}
        row['id'] = each.prod_id
        row['name'] = each.name
        row['quantity'] = each.quantity
        ls.append(row)
    if len(ls)==0:
        return "empty cart"
    return ls


def cart_checkout(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    address_id = data['address_id']
    address = Address.query.filter_by(id=address_id, user_id=auth_code['user_id']).first()
    if address==None:
        return "address not found add address"
    query = "select c.quantity as quantity, mp.inventory_count as inventory,p.id as prod_id, p.name as name, p.price as price from cart as c join products as p on p.id=c.product_id join products_meta as mp on p.id=mp.product_id where c.user_id={};".format(auth_code['user_id'])
    rows = db.session.execute(query)
    
    data_list = []
    for each in rows:
        data_list.append(each)
    if len(data_list) == 0:
        return "cart empty"

    for each in data_list:
        if each.quantity>each.inventory:
            return "{} not available".format(each.name)
    total_price = 0
    for each in data_list:
        total_price = total_price+(each.quantity*each.price)
    if data['mode'] == "cod":
        pay = Payment()
        pay.pay_amount = total_price
        pay.pay_method = "cod"
        pay.user_id = auth_code['user_id']
        db.session.add(pay)
        db.session.commit()
        pay_id = pay.id
        order  = Orders()
        order.order_value = total_price
        order.user_id = auth_code['user_id']
        order.payment_id = pay_id
        order.status = "initiated"
        order.address_id = address_id
        db.session.add(order)
        db.session.commit()
        for each in data_list:
            curr_order_id = order.id
            order_prod = OrderProducts()
            order_prod.order_id = curr_order_id
            order_prod.product_id = each.prod_id
            order_prod.quantity = each.quantity
            order_prod.cost = each.quantity*each.price
            db.session.add(order_prod)
            db.session.commit()
        cart_items = Cart.query.filter_by(user_id=auth_code['user_id']).all()
        for each in cart_items:
            db.session.delete(each)
            db.session.commit()
        send = []
        send.append({"order_id":order.id})
        order_prod = OrderProducts.query.filter_by(order_id=order.id).all()
        for each in order_prod:
            row = {}
            row["prod_id"] = each.order_id
            row['quantity'] = each.quantity
            row['cost'] = each.order_value
            send.append(row)

        return send


           
    else:
        return "service not available please select cod"


def add_comment(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    user_id = auth_code['user_id']
    prod_id = data['prod_id']
    item = Product.query.filter_by(id=prod_id).first()
    if item == None:
        return "product not found"
    comment = Comment()
    comment.prod_id = prod_id
    comment.user_id = user_id
    comment.comment = data['comment']
    db.session.add(comment)
    db.session.commit()
    return "Comment added"

def show_comment(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    prod_id = data['prod_id']
    rows =  Comment.query.filter_by(prod_id=prod_id).all()
    ls_data = []
    for each in rows:
        ls_data.append(each)
    if len(ls_data) == 0:
        return "no user commented"
    ls = []
    for each in ls_data:
        row = {}
        row['comment_id'] = each.id 
        row["comment"] = each.comment
        row["user_id"] = each.user_id
        row['upvotes'] = each.upvotes
        row['downvotes'] = each.downvotes
        ls.append(row)
    return ls

def upvote(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    comment_id = data['comment_id']
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment == None:
        return "comment removed"
    if comment.upvotes == None:
        comment.upvotes = 1
    else:
        comment.upvotes = comment.upvotes+1
    db.session.commit()
    return "upvoted"

def downvote(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    comment_id = data['comment_id']
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment == None:
        return "comment removed"
    if comment.downvotes == None:
        comment.downvotes = 1
    else:
        comment.downvotes = comment.downvotes+1
    db.session.commit()
    return "downvoted"


def add_ratings(auth_head, data):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed "
    rating = data['rating']
    user_id = auth_code['user_id']
    product_id = data['prod_id']
    if rating>5 or rating<0:
        return "invalid rating"
    prod = Product.query.filter_by(id = product_id).first()
    if prod == None:
        return "invalid product id"
    rate = Rating.query.filter_by(product_id=product_id, user_id=user_id).first()
    if rate == None:
        row = Rating()
        row.user_id = user_id
        row.product_id = product_id
        row.rating = rating
        if prod.rating == None:
            prod.rating = rating
        else:
            count = db.session.execute("select count(*) from ratings where product_id = product_id ;").scalar()
            prod.rating = ((count*prod.rating)+rating)/count+1

        db.session.add(row)
        db.session.commit()
        return "rating added"
    else:
        count = db.session.execute("select count(*) from ratings where product_id = product_id ;").scalar()
        
        new_rating = (((prod.rating)*count)-rate.rating+rating)/count
        rate.rating = rating
        prod.rating = new_rating
        db.session.commit()
        return "rating edited"


    

    
    

        









    



