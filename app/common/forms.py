# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms.validators import Optional, Length
from wtforms import SelectField, StringField, SubmitField, TextAreaField

class SystemSettings(Form):
    '''
    系统设置表单验证
    view:  WebsiteManager
    model: SystemSettings
    '''
    websitename = StringField(validators=[Optional(), Length(max=24)])
    about_website = TextAreaField(validators=[Optional()])
    submit = SubmitField('Submit')
