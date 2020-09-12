from ..models.usermodel import db , User , Address
from flask_sqlalchemy import sqlalchemy
from flask import current_app
import time
import jwt



def register_user(det):
    try:
        user = User.query.filter_by(email=det['email']).first()
        if user == None:
            user_mobile = User.query.filter_by(mobile_no=det['mobile_no']).first()
            if user_mobile == None:
                row = User(det)
                row.put()
                return "user added"
            else:
                return "User with mobile already exist"
        else:
            return "User with email already exist try another email"
    except Exception as e:
        return str(e)

def jwt_encode(key, role, user_id):
    """ jwt encoding """
    payload = {"role":role, "time":time.time()+36000, "user_id":user_id }
    jwt_code = jwt.encode(payload,key)
    return jwt_code.decode()


def login_user(dct):
    try:
        if "email" in dct.keys():
            user = User.query.filter_by(email=dct["email"]).first()
            if user == None:
                return "No account with email . please register"
            else:
                if user.password == dct['password']:
                    key = current_app.config['SECRET_KEY']
                    auth_code = jwt_encode(key, user.role, user.id)
                    return {"auth_code":auth_code,"login_msg":"login successfull"}

                else:
                    return "login details do not match"
                    

        else:
            user = User.query.filter_by(mobile_no=dct["mobile_no"]).first()
            if user == None:
                return "No account with mobile number . please register"
            else:
                if user.password == dct['password']:
                    key = current_app.config['SECRET_KEY']
                    auth_code = jwt_encode(key, user.role, user.id)
                    return {"auth_code":auth_code,"login_msg":"login_succesfull"}

                else:
                    return "login details do not match"
    except TypeError:
        return "type error"

def delete_user(dct):
    auth_code = jwt.decode(dct["auth_code"],current_app.config["SECRET_KEY"])
    if auth_code['time']>time:
        return "session expired. please login"
    if auth_code['role'] == admin:
        user = User.query.filter_by(email=dct['email']).first()
        if user == None:
            return "User doesnt exist"
        else:
            db.session.delete(user)
            db.commit()
            return "account removed"
    if auth_code['role'] == 'owner' or auth_code['role'] == 'user':
        user = User.query.filter_by(email=auth_code['user_id']).first()
        if user.password == dct['password']:
            db.session.delete(user)
            db.commit()
            return "account removed"
        else:
            return "invalid password"


def address_edit(dct,auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed to add addresses"
    address = Address.query.filter_by(address_id=dct['id'],user_id=auth_code['user_id']).first()
    if address == None:
        return "invalid address"
    
    if "country" in data.keys():
        address.country = data['country']
    if "state/ut" in data.keys():
        address.state_UT = data['state/ut']
    if "name" in data.keys():
        address.name = data['name']
    if "city/village" in data.keys():
        address.city_village = data['city/village']
    if "district" in data.keys():
        address.district = data['district']
    if "locality" in data.keys():
        address.locality = data['locality']
    if "house_no" in data.keys():
        address.house_no = data['house_no']
    if "pincode" in data.keys():
        address.pincode = data['pincode']
    
    db.session.commit()
    return "address edited"

def address_add(data, auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "user not allowed to add addresses"
    address = Address(data,auth_code['user_id'])
    address.put()
    return "address added"

def address_show(auth_head):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role'] != "user":
        return "no permission "
    address = Address.query.filter_by(user_id=auth_code['user_id']).all()
    if address == None:
        return "no address added please add"
    ls = []
    for each in address:
        row = {}
        row['city'] = each.city_village
        row['locality'] = each.locality
        row['house_no'] = each.house_no
        row['name'] = each.name
        row["id"] = each.id 
        ls.append(row)
    return ls





    