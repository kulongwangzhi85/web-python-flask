# -*- coding:utf-8 -*-


import os
import copy
from datetime import datetime
from purifier.purifier import HTMLPurifier

from flask import render_template, g, request, jsonify, make_response, json
from flask_login import login_required

from app import app, db
from app import cache
from app.users import decorators
from app.users import models as usermod
from . import models
from . import forms


@app.route('/')
@app.route('/index')
@cache.cached(timeout=10)
def index():
    return render_template('index.html')


@app.errorhandler(404)
@cache.cached(timeout=10)
def page_404(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
@cache.cached(timeout=10)
def page_403(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
@cache.cached(timeout=10)
def page_500(e):
    return render_template('500.html'), 500


@app.route('/help/', methods=['GET'])
@cache.cached(timeout=10)
def page_help():
    return render_template('help.html')

@app.route('/test/')
@login_required
@decorators.admin_required
def admin_only():
    """

    用于测试视图,方便使用

    """
    return render_template('test.html')


@app.route('/test1/')
@login_required
@decorators.permssion_required(0x07)
def user_required():
    """

    用于测试视图,方便使用

    """
    return render_template('test.html')


@app.route('/websitemanager/', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=10)
@decorators.admin_required
def WebsiteManager():
    """

    系统设置视图

    """
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
    return render_template('WebSite_Manager.html', form=form)


@app.route('/websitemanager/image/', methods=['POST'])
@login_required
@decorators.admin_required
def WebsiteImage():
    """

    上传站点图片视图

    """

    f = request.files['websiteimage']
    setting = models.SystemSettings.query.get(1)
    setting.images = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()


@app.route('/websitemanager/uploadPicture/', methods=['POST'])
@login_required
@decorators.admin_required
def UploadPicture():

    """

    上传用户头像视图

    """
    f = request.files['uploadpicture']
    setting = models.SystemSettings.query.get(1)
    setting.picture = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()


@app.route('/websitemanager/websiteicon/', methods=['POST'])
@login_required
@decorators.admin_required
def WebsiteIcon():

    """

    上传站点icon图片

    """
    f = request.files['websiteicon']
    setting = models.SystemSettings.query.get(1)
    setting.icon = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
    setting.save()
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return make_response()


@app.route('/Category/', methods=['GET', 'POST'])
@cache.cached(timeout=10)
def PostCategory():

    """

    站点文章分类视图

    """

    form = forms.PostCategoryManager()
    postcategory_all = models.PostCategory.query.order_by(models.PostCategory.name).all()
    return render_template('Category.html', form=form, postcategory_all=postcategory_all)


@app.route('/CategoryManager/', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=10)
@decorators.admin_required
def PostCategoryManager():

    """

    站点文章分类管理视图

    """
    form = forms.PostCategoryManager()
    postcategory_all = models.PostCategory.query.order_by(models.PostCategory.name).all()
    if request.method == 'POST' and form.validate_on_submit():
        vaildata = models.PostCategory.query.filter_by(name=form.CategoryName.data).first()
        if vaildata is not None:
            vaildata.name = form.CategoryName.data
            vaildata.small = form.small.data
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
            postcategory.url = os.path.join('/posts/', postcategory.name)
            f = form.image.data
            if f.filename != '':
                postcategory.image = os.path.join(app.config['WEBSITEIMAGE'], f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            postcategory.manager = form.manager.data
            postcategory.save()
    return render_template('PostCategory_Manager.html', form=form, postcategory_all=postcategory_all)


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
    """
    删除分类视图
    :return:
    """
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


@app.route('/posts/<string:category>/', methods=['GET', 'POST'])
def posts(category):

    """
    此方法是提供posts页面的方法
    此方法和模型有些不够好的,只能用于测试使用,
    在第二步骤中,需要对模型进行分区
    :param category: 指定post分类名称,类型: string
    :return:
    """
    categorydb = models.PostCategory.query.filter_by(name=category).first()
    categorydb.clicks += 1
    categorydb.save()
    return render_template('posts.html', category=categorydb)


@app.route('/posts/page/', methods=['GET', 'POST'])
def getpostspage():
    """
    posts页面的post获取数据用的分页测试
    :return:
    """
    page = 1
    purifier = HTMLPurifier(remove_entity=True)
    if request.method == 'GET'and request.is_xhr:

        category = request.args['category']
        page = int(request.args['page'])
        categorydb = models.PostCategory.query.filter_by(name=category).first()
        postsdb = categorydb.post.paginate(page, int(app.config['POSTS_PER_PAGE']), False)

        postdblist = []
        postdbdict = {}
        for post in postsdb.items:
            postdbdict['id'] = post.id
            postdbdict['name'] = post.name
            postdbdict['small'] = post.small
            postdbdict['ctime'] = post.ctime
            postdbdict['mtime'] = post.mtime
            postdbdict['author'] = post.get_author.username
            postdbdict['clicks'] = post.clicks
            postdbdict['category'] = category
            containerhtml = post.container
            postdbdict['container'] = purifier.feed(containerhtml)
            postdblist.append(copy.deepcopy(postdbdict))
        return jsonify(postdblist), 200

    if request.method == 'POST' and request.is_xhr:
        category = request.form.to_dict()
        paginatedict = {}
        categorydb = models.PostCategory.query.filter_by(name=category['category']).first()
        postsdb = categorydb.post.paginate(page, int(app.config['POSTS_PER_PAGE']), False)
        paginatedict['pages'] = postsdb.pages
        return jsonify(paginatedict), 200


@app.route('/posts/add/', methods=['POST'])
@login_required
def createpost():

    """
    创建post
    :return:
    """
    if request.method == 'POST' and request.is_xhr:
        data = request.form.to_dict()
        db = models.Post(name=data['title'])
        db.small = data['small']
        db.category = data['categoryid']
        db.author = g.user.id
        db.container = data['container']
        db.save()
    return make_response()


@app.route('/posts/modify/', methods=['POST'])
@login_required
def modifypost():

    """
    修改post信息
    :return:
    """
    if request.method == 'POST' and request.is_xhr:
        data = request.form.to_dict()
        db = models.Post.query.get(data['id'])
        db.small = data['small']
        db.container = data['container']
        db.mtime = datetime.utcnow()
        db.save()
    return make_response()


@app.route('/posts/getpost/', methods=['POST'])
@login_required
def getpost():

    """
    获取post数据到修改信息模态框
    :return:
    """
    if request.method == 'POST' and request.is_xhr:
        data = request.form.to_dict()
        db = models.Post.query.get(data['id'])
        return jsonify({
            'name':db.name,
            'small':db.small,
            'container':db.container
        })


@app.route('/posts/delpost/', methods=['POST'])
@login_required
def delpost():
    if request.method == 'POST' and request.is_xhr:
        data = request.form.to_dict()
        dbinfo = models.Post.query.get(data['id'])
        dbinfo.delete()
        return make_response()


@app.route('/posts/getprofilepost/', methods=['GET', 'POST'])
@login_required
def getprofilepost():
    page = 1
    if request.method == "POST" and request.is_xhr:
        pagedata = request.form.to_dict()
        userid = usermod.Users.query.filter_by(username=pagedata['username']).first()
        postdb = models.Post.query.filter_by(author=userid.id)
        page = pagedata['page']
        postsdb = postdb.paginate(int(page), int(app.config['POSTS_PER_PAGE']), False)
        postlist = []
        postdict = {}
        for posts in postsdb.items:
            postdict['id'] = posts.id
            postdict['name'] = posts.name
            postdict['small'] = posts.small
            postdict['clicks'] = posts.clicks
            postdict['author'] = posts.get_author.username
            postdict['ctime'] = posts.ctime
            postdict['category'] = posts.category
            postdict['container'] = posts.container
            postdict['picture'] = posts.get_author.getmaster.picture
            postlist.append(copy.deepcopy(postdict))
        return jsonify(postlist)

    if request.method == 'GET' and request.is_xhr:
        username = request.args['username']
        userid = usermod.Users.query.filter_by(username=username).first()
        postdict = {}
        postdb = models.Post.query.filter_by(author=userid.id)
        postsdb = postdb.paginate(int(page), int(app.config['POSTS_PER_PAGE']), False)
        postdict['pages'] = postsdb.pages
        return jsonify(postdict)


@app.route('/posts/<string:category>/<int:postid>/', methods=['GET', 'POST'])
def post(category, postid):
    """
    用于post的数据获取
    :param: category, postname
    :return:  post.html, post
    """
    post = models.Post.query.get(postid)
    if request.is_xhr and request.method == 'POST':
        postdict = {}
        postdict['id'] = post.id
        postdict['name'] = post.name
        postdict['small'] = post.small
        postdict['category'] = post.get_post.name
        postdict['ctime'] = post.ctime
        postdict['clicks'] = post.clicks
        postdict['mtime'] = post.mtime
        postdict['picture'] = post.get_author.getmaster.picture
        postdict['author'] = post.get_author.username
        postdict['container'] = post.container
        return jsonify(postdict)
    post.clicks += 1
    post.save()
    return render_template('post.html')


@app.route('/posts/comments/get/', methods=['GET', 'POST'])
def postcomment():
    """
    用于获取post文章评论的数据
    :return:
    """
    if request.method == 'GET' and request.is_xhr:
        jsondata = request.args

        post = models.Post.query.get(int(jsondata['post_id']))
        commentdb = post.comment.paginate(int(jsondata['page']), int(app.config['POSTS_PER_PAGE']), False)
        commentsdict = {}
        data = []
        for comments in commentdb.items:
            commentsdict['id'] = comments.id
            commentsdict['author'] = comments.follow_author.username
            commentsdict['picture'] = comments.follow_author.getmaster.picture
            commentsdict['ctime'] = comments.ctime
            commentsdict['mtime'] = comments.mtime
            commentsdict['container'] = comments.container

            commentsjson = copy.deepcopy(commentsdict)
            data.append(commentsjson)
            data.append(commentdb.pages)
        return jsonify(data)

    if request.method == 'POST' and request.is_xhr:
        jsondata = request.form.to_dict()
        commentdb = models.PostComment.query.get(jsondata['commentid'])
        commentsdict = {}
        commentsdict['id'] = commentdb.id
        commentsdict['author'] = commentdb.follow_author.username
        commentsdict['picture'] = commentdb.follow_author.getmaster.picture
        commentsdict['container'] = commentdb.container
        return jsonify(commentsdict)


@app.route('/posts/comments/modify/', methods=['GET', 'POST'])
def commentmodiry():
    """
    执行修改评论方法
    :return:
    """
    if request.method == 'POST' and request.is_xhr:
        jsondata = request.form.to_dict()
        commentdb = models.PostComment.query.get(int(jsondata['id']))
        commentdb.container = jsondata['container']
        commentdb.save()
        return make_response()


@app.route('/posts/comments/add/', methods=['POST'])
def commentadd():
    """用于增加评论"""

    if request.method == 'POST' and request.is_xhr:
        jsondata = request.form.to_dict()
        addcomment = models.PostComment(container=jsondata['container'])
        addcomment.author = g.user.id
        addcomment.post = int(jsondata['id'])
        addcomment.save_outtime()
        return make_response()