# -*- coding:utf-8 -*-
from app import app, db
from . import models
from . import forms
from flask_login import login_required
from app.users import decorators
from flask import render_template, g, request, jsonify, make_response, json
import os

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    title = 'Flask-App'
    return render_template('index.html', user=user, setting=g.systemsetting )

@app.errorhandler(404)
def page_404(e):
    title = '404 NOT FOUND!'
    return render_template('404.html', setting=g.systemsetting), 404

@app.errorhandler(403)
def page_404(e):
    title = '403 Access Denied'
    return render_template('403.html', setting=g.systemsetting), 403

@app.errorhandler(500)
def page_404(e):
    title = 'Internal Server Error'
    return render_template('500.html', setting=g.systemsetting), 500


#用于测试视图,方便使用
@app.route('/test/')
@login_required
@decorators.admin_required
def admin_only():
    user = g.user
    title = 'Flask-App'
    return render_template('test.html', user=user, setting=g.systemsetting)

#用于测试视图,方便使用
@app.route('/test1/')
@login_required
@decorators.permssion_required(0x07)
def user_required():
    user = g.user
    title = 'Flask-App'
    return render_template('test.html', user=user, setting=g.systemsetting)

#系统设置视图
@app.route('/websitemanager/', methods=['GET', 'POST'])
@login_required
@decorators.admin_required
def WebsiteManager():
    form = forms.SystemSettings()
    if request.method == 'POST' and form.validate_on_submit():
        if g.systemsetting is None:
            g.systemsetting.websitename = form.websitename.data
            g.systemsetting.about_website = form.about_website.data
            g.systemsetting.title = form.title.data
            g.systemsetting.save()
        else:
            g.systemsetting.title = form.title.data
            g.systemsetting.websitename = form.websitename.data
            g.systemsetting.about_website = form.about_website.data
            g.systemsetting.save()
        return make_response(jsonify({'status': 200}))
    form.websitename.data = g.systemsetting.websitename
    form.about_website.data = g.systemsetting.about_website
    form.title.data = g.systemsetting.title
    return render_template('WebSite_Manager.html', user=g.user, setting=g.systemsetting, form=form)

#上传站点图片视图
@app.route('/websitemanager/image/', methods=['POST'])
@login_required
@decorators.admin_required
def WebsiteImage():
    f = request.files['websiteimage']
    setting = models.SystemSettings.query.get(1)
    setting.images = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()

#上传用户头像视图
@app.route('/websitemanager/uploadPicture/', methods=['POST'])
@login_required
@decorators.admin_required
def UploadPicture():
    f = request.files['uploadpicture']
    setting = models.SystemSettings.query.get(1)
    setting.picture = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()

#上传站点icon图片
@app.route('/websitemanager/websiteicon/', methods=['POST'])
@login_required
@decorators.admin_required
def WebsiteIcon():
    f = request.files['websiteicon']
    setting = models.SystemSettings.query.get(1)
    setting.icon = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()

#文章视图
# @app.route('/post/', methods=['GET'])
# @login_required
# @decorators.admin_required
# def Post():
#     return render_template('Post.html', user=g.user, setting=g.systemsetting)

#站点文章分类视图
@app.route('/Category/', methods=['GET', 'POST'])
def PostCategory():
    form = forms.PostCategoryManager()
    postcategory_all = models.PostCategory.query.order_by(models.PostCategory.name).all()
    return render_template('Category.html', form=form, user=g.user, setting=g.systemsetting, postcategory_all=postcategory_all)

#站点文章分类管理视图
@app.route('/CategoryManager/', methods=['GET', 'POST'])
@login_required
@decorators.admin_required
def PostCategoryManager():
    form = forms.PostCategoryManager()
    postcategory_all = models.PostCategory.query.order_by(models.PostCategory.name).all()
    if request.method == 'POST' and form.validate_on_submit():
        vaildata = models.PostCategory.query.filter_by(name=form.CategoryName.data).first()
        if vaildata is not None:
            vaildata.name = form.CategoryName.data
            vaildata.small = form.small.data
            vaildata.comment = form.comment.data
            f = form.image.data
            if f.filename != '':
                vaildata.image = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            vaildata.manager = form.manager.data
            vaildata.save()
        else:
            postcategory = models.PostCategory(name=form.CategoryName.data)
            postcategory.small = form.small.data
            postcategory.comment = form.comment.data
            f = form.image.data
            if f.filename != '':
                postcategory.image = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            postcategory.manager = form.manager.data
            postcategory.save()
    return render_template('PostCategory_Manager.html', form=form, user=g.user, setting=g.systemsetting, postcategory_all=postcategory_all)

@app.route('/CategoryManagerModify/', methods=['POST'])
@login_required
def PostCategoryManagerModify():
    if request.method == 'POST' and request.is_xhr:
        id = request.form.to_dict()
        postcategory = models.PostCategory.query.get(int(id['id']))
        CategoryName = postcategory.name
        small = postcategory.small
        comment = postcategory.comment
        manager = postcategory.manager
        return jsonify({
            'CategoryName': CategoryName,
            'small': small,
            'comment': comment,
            'manager': manager
        })


@app.route('/CategoryDel/', methods=['POST'])
@login_required
@decorators.admin_required
def PostCategoryDel():
    if request.method == 'POST' and request.is_xhr:
        id = request.form.to_dict()
        obj = models.PostCategory.query.get(int(id['id']))
        return json.dumps({'name': obj.name})

@app.route('/CategoryDeleteing/', methods=['POST'])
@login_required
@decorators.admin_required
def PostCategoryDeleteing():
    if request.method == 'POST' and request.is_xhr:
        arg = request.form.to_dict()
        obj = models.PostCategory.query.filter_by(name=arg['submit']).first()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(obj.image)))
        obj.delete()

        return make_response()
