# -*- coding:utf-8 -*-
from app import app, db
from . import models
from . import forms
from flask_login import login_required
from app.users import decorators
from flask import render_template, g, request, jsonify, make_response

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    title = 'Flask-App'
    return render_template('index.html', user=user, title=title, systemsetting=g.systemsetting )

@app.errorhandler(404)
def page_404(e):
    title = '404 NOT FOUND!'
    return render_template('404.html', title=title), 404

@app.errorhandler(403)
def page_404(e):
    title = '403 Access Denied'
    return render_template('403.html', title=title), 403

@app.errorhandler(500)
def page_404(e):
    title = 'Internal Server Error'
    return render_template('500.html', title=title), 500


@app.route('/test/')
@login_required
@decorators.admin_required
def admin_only():
    user = g.user
    title = 'Flask-App'
    return render_template('test.html', user=user, title=title)

@app.route('/test1/')
@login_required
@decorators.permssion_required(0x07)
def user_required():
    user = g.user
    title = 'Flask-App'
    return render_template('test.html', user=user, title=title)

@app.route('/Category/', methods=['GET'])
def PostCategory():
    return render_template('Category.html', user=g.user)

#系统设置视图
@app.route('/websitemanager/', methods=['GET', 'POST'])
@login_required
@decorators.admin_required
def WebsiteManager():
    form = forms.SystemSettings()
    setting = models.SystemSettings.query.get(1)
    if request.method == 'POST' and form.validate_on_submit():
        if setting is None:
            setting = models.SystemSettings(websitename='')
            setting.websitename = form.websitename.data
            setting.about_website = form.about_website.data
            setting.save()
        else:
            setting.websitename = form.websitename.data
            setting.about_website = form.about_website.data
            setting.save()
        return make_response(jsonify({'status': 200}))
    form.websitename.data = setting.websitename
    form.about_website.data = setting.about_website
    return render_template('WebSite_Manager.html', user=g.user, setting=setting, form=form)


@app.route('/post/', methods=['GET'])
@login_required
@decorators.admin_required
def Post():
    return render_template('Post.html', user=g.user)
