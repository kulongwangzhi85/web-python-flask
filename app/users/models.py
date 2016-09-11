# -*- coding:utf-8 -*-
from app import db, app, lm
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

Picture = '/static/images/users/picture.jpg'

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(128), index=True, unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    create_datatime = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime)
    role = db.Column(db.Integer, db.ForeignKey('roles.id')) #角色
    post = db.relationship('Post', backref=db.backref('get_author'), lazy='dynamic') #文章所有者
    managercategory = db.relationship('PostCategory', backref=db.backref('get_manager'), lazy='dynamic') #category管理者
    profile = db.Column(db.Integer, db.ForeignKey('userprofile.id')) #用户档案

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.password(kwargs['password'])
        if self.role is None:
            if self.email == app.config['FLASK_ADMIN_EMAIL']:
                role = Role.query.filter_by(permssions=0xff).first()
                self.role = role.id
            if self.role is None:
                role = Role.query.filter_by(default=True).first()
                self.role = role.id

    def can(self, permssions):
        return self.role is not None and (self.get_role.permssions & permssions ) == permssions

    def is_administrator(self):
        return self.can(Permssion.ADMINISTER)

    def get_token(self, expiration=3600):
        t = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return t.dumps({ 'confirm': self.id })

    def confirm_token(self, token):
        r = Serializer(app.config['SECRET_KEY'])
        try:
            data = r.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()


    def save(self):
        if self.profile == None:
            p = UserProfile()
            p.save()
            self.profile = p.id
        db.session.add(self)
        db.session.commit()

    # @property
    # def password(self):
    #     raise AttributeError('Password is not a raadable attribute')

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users: %r>' % self.username

class UserProfile(db.Model):
    __tablename__ = 'userprofile'
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    picture = db.Column(db.String)
    location = db.Column(db.String)
    phone = db.Column(db.Integer)
    about_me = db.Column(db.PickleType)
    about_me_text = db.Column(db.String)
    master = db.relationship('Users', backref=db.backref('getmaster'), lazy='select', uselist=False)

    def __init__(self, picture=Picture):
        self.picture = picture

    def save(self):
        db.session.add(self)
        db.session.commit()

class Permssion():
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    default = db.Column(db.Boolean, default=True, index=True)
    permssions = db.Column(db.Integer)
    users = db.relationship('Users', backref=db.backref('get_role'), lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User' : (
                Permssion.FOLLOW |
                Permssion.COMMENT |
                Permssion.WRITE_ARTICLES, True
                      ),
            'Moderator': (
                Permssion.FOLLOW |
                Permssion.COMMENT |
                Permssion.WRITE_ARTICLES |
                Permssion.MODERATE_COMMENTS, False
            ),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permssions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()



class AnonymousUser(AnonymousUserMixin):
    username = 'Anonymous'
    picture = Picture
    def can(self, permssions):
        return False
    def is_administrator(self):
        return False

lm.anonymous_user = AnonymousUser