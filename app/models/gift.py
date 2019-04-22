
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.spider.share_book import ShareBooks
from . import Base, db
from app.models.wish import Wish
from app.models.book import Book


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))

    isbn = Column(String(15), nullable=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @property
    def book(self):
        share_book = ShareBooks()
        # book = Book.query.filter_by(isbn=self.isbn).first()
        # if book:
        #     return book
        # else:
        share_book.search_by_isbn(self.isbn)
        return share_book.first

    @property
    def books(self):
        book = Book.query.filter_by(isbn=self.isbn).first()
        return book

    @property
    def want(self):
        wish=Wish.query.filter_by(isbn=self.isbn).all()
        return len(wish)


    @classmethod
    def recent(cls):
        recent_gift = Gift.query.\
            filter_by(launched=False).group_by(Gift.isbn).\
            order_by(desc(Gift.create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).\
            distinct().all()
        return recent_gift

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                                                             Wish.isbn.in_(isbn_list),
                                                                             Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @classmethod
    def wish_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                                                             Wish.isbn.in_(isbn_list),
                                                                             Wish.status == 1).group_by(Wish.isbn).all()
        count = [ w[0] for w in count_list]
        return count
