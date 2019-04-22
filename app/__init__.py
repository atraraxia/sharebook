
from flask import Flask
from app.views.blueprint import web

from app.models import db, login_manager
from app.helper.email import mail


def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.register_blueprint(web)
    db.init_app(app)
    db.create_all(app=app)
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'
    login_manager.login_message = '请先登录'
    mail.init_app(app)
    return app
