
import os
DEBUG = True
basedir= os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'data.sqlite')
SECRET_KEY = 'hakhkakak'

MAIL_PORT = 25
MAIL_SERVER = 'smtp.163.com'
# MAIL_USE_SSL = True
MAIL_USE_TSL = True
MAIL_USERNAME = 'wxinyi735@163.com'
MAIL_PASSWORD = 'sharebook123'
FLASKY_MAIL_SENDER = 'Share Book <wxinyi735@163.com'


PER_PAGE = 15

BEANS_UPLOAD_ONE_BOOK = 0.5

RECENT_BOOK_COUNT = 30

UPLOAD_FOLDER=os.getcwd()+'\\app\\static\\uplode\\'