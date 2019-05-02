from flask import flash, redirect, url_for,current_app, request
from flask import request, render_template
from flask_login import current_user,login_required
from flask import flash,jsonify
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from .blueprint import web
from app.helper.lib import is_isbn_or_key
from app.spider.share_book import ShareBooks
from app.forms.book import *
from app.view_models.book import BookViewModel, BookCollection
from app.models.book import Book
from app.models import db


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()


    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        book=Book.query.filter_by(title=q).all()
        if book:
            books=book
            key=q
            num=len(book)

        else:
            isbn_or_key = is_isbn_or_key(q)
            share_book = ShareBooks()

            if isbn_or_key == 'isbn':
                share_book.search_by_isbn(q)
            else:
                share_book.search_by_keyword(q, page)

            books.fill(share_book, q)
            key=books.keyword
            num=books.total
            Book.insert_into_sql(books.books)
            books=books.books

    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")
    return render_template('search_result.html',keyword=key,total=num ,books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    share_book = ShareBooks()
    share_book.search_by_isbn(isbn)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    book1=Book.query.filter_by(isbn=isbn).first()
    user_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    user_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    wishs_total = len(user_wishes)
    gifts_total = len(user_gifts)

    if book1:
        book=book1
        _wish=[]
        for i in user_wishes:
            _wish.append(TradeInfo._map_to_trade(i))

        _gift=[]
        for i in user_gifts:
            _gift.append(TradeInfo._map_to_trade(i))

    else:
        book = BookViewModel(share_book.first)
        _wish_of_user = TradeInfo(user_wishes)
        _gift_of_user = TradeInfo(user_gifts)

        _wish=_wish_of_user .trades
        _gift=_gift_of_user.trades


    return render_template('book_detail.html',
                           book=book,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes_total=wishs_total,
                           gifts_total=gifts_total,
                           wishes=_wish,
                           gifts=_gift
                           )


@web.route('/book/uplode',methods=['GET', 'POST'])
@login_required
def book_uplode():
    book_form = LengForm(request.form)
    my_book = Book()
    uid = current_user.id
    if request.method == 'POST' and book_form.validate():

        image=request.files['image']
        image_fname=image.filename
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'jpg']
        flag = '.' in image_fname and image_fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        if not flag:
            flash('文件类型错误,请检查上传的图片类型，仅限于png、PNG、jpg、JPG')
            return redirect(url_for('views.book_uplode'))
        if Book.query.filter_by(isbn=book_form.isbn.data).first():
            flash("已经存在这本书了，快去搜索栏搜索吧")
        else:
            with db.auto_commit():
                image.save('{}{}'.format(UPLOAD_FOLDER,image_fname))
                my_book.image = '/static/uplode/{}'.format(image_fname)
                my_book.title=book_form.title.data
                my_book.author=book_form.author.data
                my_book.isbn=book_form.isbn.data
                my_book.publisher=book_form.publisher.data
                my_book.summary=book_form.summary.data
                db.session.add(my_book)
                flash("提交成功")

        if Gift.query.filter_by(isbn=my_book.isbn, uid=uid,launched=False).first():
            flash('这本书已经添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
        else:
            with db.auto_commit():
                gift = Gift()
                gift.isbn = book_form.isbn.data
                gift.uid = uid
                current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
                db.session.add(gift)

        return redirect(url_for('views.book_uplode'))
    return render_template('book_uplode.html', form=book_form)
