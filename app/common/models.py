# -*- coding:utf-8 -*-
from app import db
from datetime import datetime


class SystemSettings(db.Model):
    '''
    主要站点设置模型
    '''
    __tablename__ = 'systemsettings'
    id = db.Column(db.Integer, primary_key=True)
    websitename = db.Column(db.String)
    images = db.Column(db.String)
    picture = db.Column(db.String)
    icon = db.Column(db.String)
    about_website = db.Column(db.String)

    def __init__(self, picture='/static/images/users/picture.jpg', websitename='Flask_Web'):
        self.picture = picture
        self.websitename = websitename

    def save(self):
        db.session.add(self)
        db.session.commit()


class PostCategory(db.Model):
    '''
    文章分类模型
    '''
    __tablename__ = 'postcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    small = db.Column(db.String)
    image = db.Column(db.String)
    manager = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.relationship('Post', backref=db.backref('get_post'), lazy='dynamic')

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return self.name

class Post(db.Model):
    '''
    文章模型
    '''
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    small = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String)
    ctime = db.Column(db.DateTime())
    mtime = db.Column(db.DateTime())
    category = db.Column(db.Integer, db.ForeignKey('postcategory.id'))

    def __init__(self):
        self.ctime = datetime.utcnow()

    def __repr__(self):
        return self.name
