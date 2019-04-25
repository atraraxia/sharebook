
from app.helper.httper import Http
from flask import current_app


class ShareBooks(object):

    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'


    def __init__(self):
        self.total = 0
        self.books = []

    def _fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def _fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @staticmethod
    def calculate_start(page):
        return (page-1) * current_app.config['PER_PAGE']

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self._fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], ShareBooks.calculate_start(page))
        result = Http.get(url)
        self._fill_collection(result)

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
