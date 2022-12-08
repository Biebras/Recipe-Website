import os

# get base direction
basedir = os.path.abspath(os.path.dirname(__file__))
#get db file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# set sql settings
SQLALCHEMY_TRACK_MODIFICATIONS = True
# set wtf settings
WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-secret'