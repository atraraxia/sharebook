
from flask import render_template

from app.models.gift import Gift
from app.models.wish import Wish
from app.models.user import User
from app.view_models.book import BookViewModel
from .blueprint import web
from flask_login import login_required, current_user
from app.models.book import Book

@web.route('/index')
def index():
    recent_gifts = Gift.recent()
    books=[]
    for gift in recent_gifts:
        book = Book.query.filter_by(isbn=gift.isbn).first()
        books.append(book)
    return render_template('index.html', recent=books)


@web.route('/personal')
@login_required
def personal_center():
    uid = current_user.id
    cur_user = User.query.get_or_404(uid)
    user_center = cur_user.summary
    user_gift = Gift.get_person_gifts(uid)
    user_wishes = Wish.get_person_wishes(uid)
    return render_template('personal.html', user=user_center,gifts=user_gift,wishes=user_wishes)  # 网页模板下
