from ..import db


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    prod_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    db.UniqueConstraint("user_id","prod_id")
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)