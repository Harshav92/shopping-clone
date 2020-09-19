from ..import db   


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(250))

    def __init__(self,name,description):
        self.name = name
        self.description = description
    

    def put(self):
        db.session.add(self)
        db.session.commit()

class Tree(db.Model):
    __tablename__ = "tree"
    descendant = db.Column(db.Integer,db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
    ancestor = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
    length = db.Column(db.Integer,nullable=False)

    def __init__(self, ancestor, descendant, length):
        self.ancestor = ancestor
        self.descendant = descendant
        self.length = length

    def put(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    prod_code = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Float)
    

class MetaProduct(db.Model):
    __tablename__ = "products_meta"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey("products.id", ondelete="CASCADE"))
    image1_url = db.Column(db.String(500))
    description = db.Column(db.String(500))
    inventory_count = db.Column(db.Integer)


class ProductCategories(db.Model):
    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"))
    db.UniqueConstraint("product_id","category_id")

class WhishList(db.Model):
    __tablename__ ="wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))
    quantity = db.Column(db.Integer)
    db.CheckConstraint(quantity>0)

class Rating(db.Model):
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    product_id =  db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    rating = db.Column(db.Integer)

