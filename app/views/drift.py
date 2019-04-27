
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.helper.email import send_email
from app.helper.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.models.book import Book
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from .blueprint import web
from app.models import db


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    form = DriftForm(request.form)
    current_gift = Gift.query.get_or_404(gid)
    uid=current_user.id
    if current_gift.is_yourself_gift(uid):
        flash('这本书是你自己的')
        return redirect(url_for('views.book_detail', isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    print(can)
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    wish = Wish.query.filter_by(isbn=current_gift.isbn, uid=uid).first()
    if wish:
        pass
    else:
        with db.auto_commit():
            wish = Wish()
            wish.isbn =current_gift.isbn
            wish.uid = current_user.id
            db.session.add(wish)
    print(wish)
    if request.method == 'POST' and form.validate():

        save_dirft(form, current_gift)
        try:
            flash("提交成功")
        except:
            flash("请确认信息全部填写")
        send_email(current_gift.user.email, '有人想要一本书',
                   'email/get_gift.html', wisher=current_user, gift=current_gift)

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(desc(Drift.create_time)).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did, Gift.id == current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('views.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('views.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        print(drift)
        drift.pending = PendingStatus.Success
        print(drift.pending)
        current_user.beans += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        wish = Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=False).first_or_404()
        wish.launched = True
        print(wish)
    return redirect(url_for('views.pending'))


def save_dirft(form, current_gift):
    with db.auto_commit():
        dirft = Drift()
        form.populate_obj(dirft)
        dirft.gift_id = current_gift.id
        dirft.requester_id = current_user.id
        dirft.requester_nickname = current_user.nickname
        dirft.gifter_id = current_gift.user.id
        dirft.gifter_nickname = current_gift.user.nickname

        gift= current_gift
        book=Book.query.filter_by(isbn=gift.isbn).first()
        dirft.book_title = book.title
        dirft.book_author = book.author
        dirft.book_img = book.image
        dirft.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(dirft)
