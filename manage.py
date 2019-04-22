from app import create_app
from flask_script import Manager
from flask_script.commands import Server
from flask_migrate import Migrate, MigrateCommand
from app.models import db

from app.config import SubServer, SubShowUrls
import app.models

ft_app = create_app()
ft_manager = Manager(ft_app)
ft_manager.add_command('runserver',
                       SubServer(ft_app, host='127.0.0.1', port=5100))
ft_manager.add_command('urls', SubShowUrls(ft_app))


def make_shell_context():
    return dict(app=app, db=db, models=app.models)


xapp = create_app()
manager = Manager(xapp)
migrate = Migrate(xapp, db, render_as_batch=True)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='127.0.0.1'))


if __name__ == '__main__':
    manager.run()