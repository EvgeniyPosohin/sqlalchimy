import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *
import config



password = os.getenv('password')
database = os.getenv('database')
user = os.getenv('user')
DSN = f'postgresql://{user}:{password}@localhost:5432/{database}'
engine = sqlalchemy.create_engine(DSN)
drop_tables(engine)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

#Добавляем самостоятельно по классам данные - ДЗ-1
publisher_1 = Publisher(name="Эксмо")
publisher_2 = Publisher(name="Феникс")
publisher_3 = Publisher(name="Дрофа")
session.add_all([publisher_1, publisher_2, publisher_3])

book_1 = Book(title="Капитанская дочка", publisher=publisher_1)
book_2 = Book(title="Евгений Онегин", publisher=publisher_3)
book_3 = Book(title="Три мушкетера", publisher=publisher_2)
book_4 = Book(title="Война и мир", publisher=publisher_1)
book_5 = Book(title="Бесы", publisher=publisher_3)
book_6 = Book(title="Капитал", publisher=publisher_2)
session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])

shop_1 = Shop(name="ЛитРес")
shop_2 = Shop(name="Флибуста")
shop_3 = Shop(name="Лабиринт")
session.add_all([shop_1, shop_2, shop_3])

stock_1 = Stock(count=25, book=book_1, shop=shop_1)
stock_2 = Stock(count=48, book=book_2, shop=shop_2)
stock_3 = Stock(count=225, book=book_3, shop=shop_3)
stock_4 = Stock(count=256, book=book_4, shop=shop_1)
stock_5 = Stock(count=322, book=book_5, shop=shop_2)
stock_6 = Stock(count=112, book=book_6, shop=shop_3)
session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6])

sale_1 = Sale(price=526, date_sale="08-02-2022", count=18, stock=stock_1)
sale_2 = Sale(price=456, date_sale="09-11-2010", count=22, stock=stock_2)
sale_3 = Sale(price=123, date_sale="22-02-2018", count=100, stock=stock_3)
sale_4 = Sale(price=5284, date_sale="06-01-2012", count=455, stock=stock_4)
sale_5 = Sale(price=255, date_sale="10-12-2023", count=123, stock=stock_5)
sale_6 = Sale(price=56, date_sale="20-08-2008", count=10, stock=stock_6)
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6])
session.commit()

result = get_info('Феникс', session)
result = get_info(1, session)


# Загружаем из Json и осуществляем поиск
drop_tables(engine)
create_tables(engine)
create_bd(session)
result = get_info('Pearson', session)
result = get_info(2, session)

session.close()