
from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.helper.enums import PendingStatus
from app.models import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from .blueprint import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_person_gifts(uid)
    return render_template('my_gifts.html', gifts=gifts_of_mine)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已经添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('views.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/delete')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这本书正处于借阅交易状态，请先完成借阅交易')
    else:
        # with db.auto_commit():
        current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
        #     gift.delete()
        db.session.delete(gift)
        db.session.commit()
    return redirect(url_for('views.my_gifts'))
