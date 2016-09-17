import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY='n+Vh9DhZRs4FrIFpY1CR2KnJfu+l6b48yzAdJzRyAKE='
FLASK_ADMIN_EMAIL = 'admin@localhost.com'
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/app.db' % basedir
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = os.path.join(basedir, 'app/static/images/')
WEBSITEIMAGE = '/static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
CACHE_DEFAULT_TIMEOUT = 60
CACHE_DIR = os.path.join(basedir, 'cached')
