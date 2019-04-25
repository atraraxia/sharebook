
from sqlalchemy import Column, Integer, String
from . import Base, db


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='佚名')
    publisher = Column(String(50))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass

    @classmethod
    def insert_into_sql(cls, books):
        # book model 写入
        for b in books: # books是一个列表，每个元素是一个Book实例化后的对象
            if Book.query.filter_by(isbn=b.isbn).first():  # 因为重复的isbn不能添加
                        continue
            with db.auto_commit():
                book = Book()
                book.set_attrs(b.__dict__)  # [b1, b2, b3]
                # 类实例化后的一个对象 b.author b.title
                db.session.add(book)

