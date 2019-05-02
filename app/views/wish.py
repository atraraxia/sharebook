
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.helper.email import send_email
from app.models import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from .blueprint import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_mine = Wish.get_person_wishes(uid)

    return render_template('my_wish.html', wishes=wishes_mine)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已经添加至你的出借或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('views.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有出借此书')
    else:
        send_email(wish.user.email, '有人想借阅你一本书', 'email/satisify_wish.html', wish=wish, gift=gift)
        flash('已向他发生邮件')
    return redirect(url_for('views.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/delete')
def delete_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    db.session.delete(wish)
    db.session.commit()
    return redirect(url_for('views.my_wish'))

