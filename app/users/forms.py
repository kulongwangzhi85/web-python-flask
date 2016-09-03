# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms.validators import Email,EqualTo,DataRequired,Length, Optional
from wtforms import TextAreaField, SelectField,StringField,BooleanField,PasswordField,SubmitField, ValidationError, IntegerField
from models import Users, Role

class LoginForm(Form):
    '''
    用户登入表单验证
    '''
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField(default=False)
    submit = SubmitField()

    def validate_username(self, field):
        u = Users.query.filter_by(username=self.username.data).first()
        if u is None or field.data != u.username:
            raise ValidationError('Username Is Erroor')

    def validate_password(self, field):
        u = Users.query.filter_by(username=self.username.data).first()
        if not u.verify_password(field.data):
            raise ValidationError('Password Is Erroor')

class UserRegisterForm(Form):
    '''
    用户注册表单验证
    '''
    username = StringField(validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=5, max=128), EqualTo('password_confirm')])
    password_confirm = PasswordField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()

class UserProfileForm(Form):
    '''
    用户档案表单验证
    '''
    firstname = StringField(validators=[Optional(),Length(max=32)])
    lastname = StringField(validators=[Optional(),Length(max=32)])
    email = StringField(validators=[Optional(),Email(), Length(max=128)])
    phone = IntegerField(validators=[Optional()])
    location = StringField(validators=[Optional(),Length(max=256)])
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    '''
    管理员编辑用户档案的form表单验证
    call-view: EditProfiles
    '''
    firstname = StringField(validators=[Optional(),Length(max=32)])
    lastname = StringField(validators=[Optional(),Length(max=32)])
    email = StringField(validators=[Optional(),Email(), Length(max=128)])
    phone = IntegerField(validators=[Optional()])
    # confirm = BooleanField()
    location = StringField(validators=[Optional(),Length(max=256)])
    role = SelectField(coerce=int)
    about_me = TextAreaField(validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [ ( role.id, role.name ) \
                              for role in Role.query.order_by(Role.name).all() ]
        self.user = Users

    def validate_email(self, field):
        if field.data != self.user.email and \
            Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
