from app import db
from sqlalchemy import UniqueConstraint
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, unique = False)
    description = db.Column(db.String(500), unique = False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    surname = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50), unique = False)
    description = db.Column(db.String(240), unique = False)
    following = db.Column(db.Integer, unique = False)
    followers = db.Column(db.Integer, unique = False)
    np = db.Column(db.Integer, unique = False)
    posts = db.relationship('Post', backref = 'account', lazy = 'dynamic')

# association object
class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key = True)
    this_id = db.Column(Integer, db.ForeignKey('account.id'), nullable = False)
    other_id = db.Column(Integer, db.ForeignKey('account.id'), nullable = False)
    UniqueConstraint('this_id', 'other_id', name='thisother')
    friends1 = db.relationship('Account', foreign_keys = [this_id])
    friends2 = db.relationship('Account', foreign_keys = [other_id])
