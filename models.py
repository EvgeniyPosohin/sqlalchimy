import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
import json

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    def __repr__(self):
        return f'{self.id} {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")

    def __repr__(self):
        return f'{self.id} {self.title} {self.id_publisher}'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60))

    def __repr__(self):
        return f'{self.id} {self.name}'


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    book = relationship(Book, backref="books")
    shop = relationship(Shop, backref="shops")

    def __repr__(self):
        return f'{self.id} {self.id_book} {self.id_shop} {self.count}'


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    stock = relationship(Stock, backref="stocks")

    def __repr__(self):
        return f'{self.id} {self.price} {self.date_sale} {self.id_stock} {self.count}'


def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

def create_bd(session):
    current = os.getcwd()
    file_name = 'tests_data.json'
    full_path = os.path.join(current, file_name)
    with open(full_path, 'r') as f:
        data = json.load(f)
        for line in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[line.get('model')]
            session.add(
                model(id=line.get('pk'), **line.get('fields')))
            session.commit()


def get_info(info, session):
    result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Publisher).join(Stock).join(Shop)\
        .join(Sale)
    if type(info) is int:
        search = result.filter(
            Publisher.id == info).all()
    elif type(info) is str:
        search = result.filter(
            Publisher.name == info).all()
    else:
        print("неверный запрос")
    for i in search:
        print(f'{i[0]:<40}\t|\t{i[1]:^15}\t|\t{i[2]}\t|\t{i[3].strftime("%Y-%m-%d")}')
