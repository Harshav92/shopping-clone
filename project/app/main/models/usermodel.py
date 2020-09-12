from ..import db
import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    mobile_no = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, dct):
        self.name = dct['name']
        self.email = dct['email']
        self.mobile_no = dct['mobile_no']
        self.password = dct['password']
        self.role = dct['role']


    def put(self):
        db.session.add(self)
        db.session.commit()


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"))
    name = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(70))
    state_UT = db.Column(db.String(70))
    district = db.Column(db.String(70))
    city_village = db.Column(db.String(70))
    locality = db.Column(db.String(70))
    house_no = db.Column(db.String(70) )
    pincode = db.Column(db.String(10),nullable=False)

    

    def __init__(self,dct,user_id):
        self.user_id = user_id
        self.name = dct['name']
        self.phone = dct['mobile_no']
        self.country = dct['country']
        self.state_UT = dct['state/ut']
        self.district = dct['district']
        self.city_village = dct['city/village']
        self.locality = dct['locality']
        self.house_no = dct['house_no']
        self.pincode = dct['pincode']
        

    def put(self):
        db.session.add(self)
        db.session.commit()
    
    

        
