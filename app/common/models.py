# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class SystemSettings(db.Model):

    """

    主要站点设置模型

    """

    __tablename__ = 'systemsettings'
    id = db.Column(db.Integer, primary_key=True)
    websitename = db.Column(db.String)
    title = db.Column(db.String(12))
    images = db.Column(db.String)
    picture = db.Column(db.String)
    icon = db.Column(db.String)
    about_website = db.Column(db.String)

    def __init__(self, picture='/static/images/users/user.png', websitename='Flask_Web'):
        self.picture = picture
        self.websitename = websitename

    def save(self):
        db.session.add(self)
        db.session.commit()


class PostCategory(db.Model):

    """

    文章分类模型

    forms:
    views:     PostCategory

    """

    __tablename__ = 'postcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    small = db.Column(db.String)
    image = db.Column(db.String)
    url = db.Column(db.String)
    manager = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.Column(db.String(64))
    post = db.relationship('Post', backref=db.backref('get_post'), lazy='dynamic')
    clicks = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.clicks = 0

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):

    """

    文章模型
    可改进的地方:增加一个字段用于索引使用,以方便使用

    """

    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    small = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    ctime = db.Column(db.DateTime(), default=datetime.utcnow)
    mtime = db.Column(db.DateTime())
    container = db.Column(db.PickleType)
    category = db.Column(db.Integer, db.ForeignKey('postcategory.id'))
    clicks = db.Column(db.Integer)


    def __init__(self, *args, **kwargs):
        self.ctime = datetime.utcnow()
        self.name = kwargs['name']
        self.clicks = 0


    def __repr__(self):
        return self.name


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()