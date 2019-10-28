from . import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_hash = db.Column(db.String(255))

    blogs = db.relationship('Blog', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'  


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)


    def __repr__(self):
        return f'Blog {self.title}'
