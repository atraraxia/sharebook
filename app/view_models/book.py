


class BookViewModel(object):
    def __init__(self, book):
        self.isbn = book['isbn']
        self.title = book['title']
        self.author = '、'.join(book['author'])
        # self.binding = book['binding']
        self.publisher = book['publisher']
        self.image = book['image']
        # self.price = book['price']
        # self.pubdate = book['pubdate']
        # summuy长度最多取1000.
        self.summary = book['summary'][:1000] if book['summary'] else ''
        # self.pages = book['pages'].replace('页', '') if book['pages'] else None

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher])
        return '/'.join(intros)


class BookCollection(object):
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, share_book, keyword):
        self.total = share_book.total
        self.books = [BookViewModel(book) for book in share_book.books]
        self.keyword = keyword
