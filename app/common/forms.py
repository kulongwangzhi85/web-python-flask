# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms.validators import Optional, Length, DataRequired
from wtforms import SelectField, StringField, SubmitField, TextAreaField, FileField
from app.users import models

class SystemSettings(Form):
    '''
    系统设置表单验证
    view:   WebsiteManager
    model:  SystemSettings
    '''
    websitename = StringField(validators=[Optional(), Length(max=24)])
    about_website = TextAreaField(validators=[Optional()])
    title = StringField(validators=[Optional(), Length(max=12)])
    submit = SubmitField('Submit')

class  PostCategoryManager(Form):
    '''
    post分类页面的变淡验证
    view:   PostCategoryManager
    model:  PostCategory
    '''
    CategoryName = StringField(validators=[DataRequired(), Length(max=12)])
    small = StringField(validators=[Optional(), Length(max=12)])
    comment = StringField(validators=[Optional(), Length(max=64)])
    image = FileField(Optional())
    manager = SelectField(coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostCategoryManager, self).__init__(*args, **kwargs)
        self.manager.choices = [ ( user.id , user.username ) \
                                 for user in models.Users.query.order_by(models.Users.username).all() ]