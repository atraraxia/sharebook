
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
    user = cur_user.summary
    # summary返回一个自定义的字典，详情在user模型下
    # b = a.summary
    gifts = Gift.get_user_gifts(uid)
    wishes = Wish.get_user_wishes(uid)
    return render_template('personal.html', user=user,gifts=gifts,wishes=wishes)  # 网页模板下
