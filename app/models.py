from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_hash = db.Column(db.String(255))

    blogs = db.relationship('Blog', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return f'User {self.username}'  


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.String(),nullable=False)
    posted_on = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_blog(id):
        blog = Blog.query.filter_by(id=id).first()

        return blog

    def __repr__(self):
        return f'Blog {self.title}'
