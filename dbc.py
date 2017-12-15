from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class News(Base):
    '''
    Класс для работы базой данных через ORM. Вообще, нужно выкинуть его в отдельный файл.
    '''
    __tablename__ = "news"  # Имя таблица
    id = Column(Integer, primary_key=True)  # id - уникальный номер записи, является pk
    title = Column(String)  # Название статьи
    author = Column(String)  # Автор
    url = Column(String)  # url-ссылка на статью
    comments = Column(Integer)  # Колличество комментарием. Фиг его знает, зачем они нам
    points = Column(Integer)  # Количество лайков. Опять же - фиг его знает зачем
    label = Column(String)  # Наша метка - понравилось/пофиг/не понравилось.
