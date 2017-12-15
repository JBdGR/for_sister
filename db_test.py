# Тестовый пример из методички. Заполняем базу новостями
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
import fasttest
import os

# На основе Base будем создавать наш класс. Это все мутки с ORM, т.ч. прими как должное
Base = declarative_base()

class News(Base):
    '''
    Класс для работы базой данных через ORM. Вообще, нужно выкинуть его в отдельный файл.
    Из dbc.py тянуть не будем, т.к. это финальная версия примера
    '''
    __tablename__ = "news"  # Имя таблица
    id = Column(Integer, primary_key=True)  # id - уникальный номер записи, является pk
    title = Column(String)  # Название статьи
    author = Column(String)  # Автор
    url = Column(String)  # url-ссылка на статью
    comments = Column(Integer)  # Колличество комментарием. Фиг его знает, зачем они нам
    points = Column(Integer)  # Количество лайков. Опять же - фиг его знает зачем
    label = Column(String)  # Наша метка - понравилось/пофиг/не понравилось.


if os.path.exists("test.db"):  # Если файл test.db существует, то удаляем его
    os.remove("test.db")

engine = create_engine("sqlite:///test.db")  # Создаем файл с базой данных, создаем связь, создаем сессию
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()

news_list = fasttest.get_news('https://news.ycombinator.com/')  # Через написанную нами ранее функцию получаем новости
for i in news_list:  # Для каждой новости из списка
    news = News(title=i['title'], author=i['author'], url=i['url'],
                comments=i['comments'], points=i['points']) # Создаем экземляр класса, заполняем атрибуты
    s.add(news)  # Добавляем строку в базу

s.commit()  # Коммитим (Применяем изменения в базе
