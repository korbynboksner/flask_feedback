"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bycrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Feedback(db.Model):
    __tablename__ = "feeback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text,db.string(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="feedback")


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text,db.String(20),  nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, db.String(50), nullable=False)
    first_name = db.Column(db.Text, db.String(30), nullable=False)
    last_name = db.Column(db.Text, db.String(30), nullable=False)

#    def to_dict(self):

#        return {
#            "id":self.id,
#            "flavor":self.flavor,
#            "size":self.size,
#            "rating":self.rating,
#            "image":self.image,}

    @classmethod
    def register(cls, username, pwd):

        hashed = bcrypt.generated_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)
    

    @classmethod
    def authenticate(cls, username, pwd):


        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False