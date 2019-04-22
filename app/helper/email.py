
from threading import Thread

from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()


def send_email(to, subject, template, **kwargs):
    msg = Message('[共享书籍]' + ' ' + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # msg.body = render_template(template , **kwargs)
    msg.html = render_template(template , **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send, args=[app, msg])
    thr.start()
    mail.send(msg)
#
def send(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
