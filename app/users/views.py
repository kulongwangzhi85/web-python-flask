# -*- coding:utf-8 -*-

import os
from purifier.purifier import HTMLPurifier
from flask import json, send_from_directory, render_template, redirect, flash, g, session, url_for, request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from datetime import datetime

import forms
import models
import decorators
from config import UPLOAD_FOLDER
from app.common.models import SystemSettings
from app.common.models import PostCategory
from app.common.models import Post
from app import app, lm, db, csrf



@app.teardown_request
def teardown_request(excaption=None):
    db.session.remove()


@app.before_request
def befor_request():
    g.user = current_user
    g.systemsetting = SystemSettings.query.get(1)
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()


@lm.user_loader
def load_user(id):
    return models.Users.query.get(int(id))


@app.route('/users/login/', methods=['GET', 'POST'])
def UserLogin():
    form = forms.LoginForm()
    if g.user is not None and g.user.is_authenticated:
        return redirect('/')
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = models.Users.query.filter_by(username=form.username.data).first()
        login_user(user, session['remember_me'])
        return redirect(url_for('UserProfile', username=user.username, setting=g.systemsetting))
    return render_template('login.html', form=form, setting=g.systemsetting)


@app.route('/users/register/', methods=['GET', 'POST'])
def UserRegister():
    form = forms.UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        u = models.Users(username=username, email=email, password=password)
        u.save()
        flash('Confirm Your Access')
        login_user(u)
        return redirect(url_for('confirmed', username=u.username, setting=g.systemsetting))
    return render_template('user_register.html', form=form, title='User Register', setting=g.systemsetting)

@app.route('/users/confirmed/<username>')
@login_required
def confirmed(username):
    token = g.user.get_token()
    return render_template('access_confirm.html', token=token, title='Confirmed Account', user=username, setting=g.systemsetting)

@app.route('/users/confirm/<username>/<token>', methods=['GET'])
@login_required
def confirm(username,token):
    if g.user.confirmed:
        return redirect('/')
    if g.user.confirm_token(token=token):
        flash('register account ok')
    else:
        flash('The register link is invalid or has expired')
        return redirect('/')

@app.route('/user/<username>/', methods=['GET', 'POST'])
@login_required
def UserProfile(username):
    form = forms.UserProfileForm()
    if form.validate_on_submit():
        g.user.getmaster.firstname = form.firstname.data
        g.user.getmaster.lastname = form.lastname.data
        g.user.getmaster.email = form.email.data
        g.user.getmaster.phone = form.phone.data
        g.user.getmaster.location = form.location.data
        g.user.getmaster.save()
    form.firstname.data = g.user.getmaster.firstname
    form.lastname.data = g.user.getmaster.lastname
    form.email.data = g.user.getmaster.email
    form.phone.data = g.user.getmaster.phone
    form.location.data = g.user.getmaster.location
    return render_template('user_profile.html', user=g.user, title='User Profile', form=form, setting=g.systemsetting)

@app.route('/users/logout/', methods=['GET'])
@login_required
def UserLogout():
    logout_user()
    return redirect('/')


@app.route('/users/profile/', methods=['GET'])
@login_required
@decorators.admin_required
def EditProfileAdmin():

    """
    admin管理员编辑用户的信息
    """

    userdb = models.Users.query.all()
    return render_template('EditProfileAdmin.html', user=g.user, userdb=userdb, title='Edit Profile', setting=g.systemsetting)


@app.route('/api/v1.0/infocount/', methods=['GET', 'POST'])
def websiteinfocount():

    userscount = models.Users.query.all()
    categorycount = PostCategory.query.all()
    m = "%04d" % len(userscount)
    c = "%04d" % len(categorycount)
    return jsonify({'users_count': m, 'category_count': c})


@app.route('/api/v1.0/users/aboutme', methods=['GET', 'POST'])
def EditProfileAboutmeAjax():
    if request.method == 'POST':
        contextHtml = request.form.get('about')
        g.user.getmaster.about_me=contextHtml
        purifier = HTMLPurifier(remove_entity=True)
        g.user.getmaster.about_me_text=purifier.feed(contextHtml)
        g.user.getmaster.save()
        return make_response()

    if request.method == 'GET':
        return render_template('aboutme.html', title='About Me', user=g.user, setting=g.systemsetting)


@app.route('/api/v1.0/users/aboutme/post/<username>', methods=['GET'])
def EditProfileAboutme(username):
    userdb = models.Users.query.filter_by(username=username).first()
    return jsonify(userdb.getmaster.about_me)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/users/uploads/images/', methods=['POST'])
def upload_file():
    if request.method == "POST":
        picturepath = '/static/images/users/'
        uploadpicturepath = os.path.join(UPLOAD_FOLDER, 'users')
        f = request.files['files[]']
        g.user.getmaster.picture = os.path.join(picturepath, f.filename)
        g.user.getmaster.save()
        f.save(os.path.join(uploadpicturepath, f.filename))

        return make_response()


@app.route('/users/edit/profiles/<username>', methods=['GET', 'POST'])
@login_required
@decorators.admin_required
def EditProfiles(username):
    '''
    用于管理员编辑用户的档案
    :param username:
    '''
    userdb = models.Users.query.filter_by(username=username).first()
    form = forms.EditProfileAdminForm()
    categorydb = PostCategory.query.all()
    postdb = Post.query.all()
    if form.validate_on_submit():
        userdb.getmaster.firstname = form.firstname.data
        userdb.getmaster.lastname = form.lastname.data
        userdb.getmaster.email = form.email.data
        userdb.getmaster.phone = form.phone.data
        userdb.getmaster.location = form.location.data
        userdb.role = form.role.data
        userdb.getmaster.save()
        userdb.save()
    form.firstname.data = userdb.getmaster.firstname
    form.lastname.data = userdb.getmaster.lastname
    form.email.data = userdb.getmaster.email
    form.phone.data = userdb.getmaster.phone
    form.location.data = userdb.getmaster.location
    form.role.data = userdb.get_role.id
    return render_template('EditUserProfile_admin.html', form=form, user=g.user, setting=g.systemsetting, userdb=userdb,
                           categorydb=categorydb)
