from ..models.categorymodel import Category , Tree , db
from flask_sqlalchemy import sqlalchemy
from flask import current_app
import time
import jwt


def add(dct,auth_head):
    auth_code = jwt.decode(auth_head,current_app.config["SECRET_KEY"])
    if auth_code['time']<=time.time():
        return "time expired login again"
    if auth_code['role']!="admin":
        return "user not allowed to add categories"

    if dct['ancestor'] == dct['name']:
    
        category = Category.query.filter_by(name=dct['name']).first()
        if category == None:
            cats = Category(dct['name'],dct['description'])
            cats.put()
            new_cat = Category.query.filter_by(name=dct['name']).first()
            cat_id = new_cat.id
            tree = Tree(cat_id, cat_id, 0)
            tree.put()
            return "category added"
        else:
            return "Category name already exists"
    else:
        category = Category.query.filter_by(name=dct['name']).first()
        if category == None:
            anc = Category.query.filter_by(name=dct['ancestor']).first()
            if anc == None:
                return "invalid ancestor"
            cats = Category(dct['name'], dct['description'])
            cats.put()
            new_cat = Category.query.filter_by(name=dct['name']).first()
            cat_id = new_cat.id
            
            ancestors = Tree.query.filter_by(descendant=anc.id).all()
            for each in ancestors:
                tree = Tree(each.ancestor, cat_id, each.length+1)
                tree.put()

            tree = Tree(cat_id, cat_id, 0)
            tree.put()
            return "category added"

        else:
            return "Category name already exists"


def category_show(auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    query = 'select * from categories as c join (select descendant , count(*) as cd from tree group by descendant)counts on c.id = counts.descendant where counts.cd=1;'
    categories = db.session.execute(query)
    ls = []
    for each in categories:
        
        ls.append(each.name)
    return ls

def category_sub(auth_head, category):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    check = Category.query.filter_by(name=category).first()
    if check == None:
        return "category does not exist"
    query = "select * from categories as c join tree as t on c.id=t.descendant where t.ancestor= {} and t.length=1;".format(check.id)
    categories = db.session.execute(query)
    ls = []
    for each in categories:
        ls.append(each.name)
    return ls

        
    

    