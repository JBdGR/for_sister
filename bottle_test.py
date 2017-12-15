# Тестовый пример из методички. Отображение статей без оценки
from bottle import route, run, template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

# На основе Base будем создавать наш класс. Это все мутки с ORM, т.ч. прими как должное
Base = declarative_base()


class News(Base):
    '''
    Класс для работы с базой данных
    '''
    __tablename__ = "news"  # Имя таблица
    id = Column(Integer, primary_key=True)  # id - уникальный номер записи, является pk
    title = Column(String)  # Название статьи
    author = Column(String)  # Автор
    url = Column(String)  # url-ссылка на статью
    comments = Column(Integer)  # Колличество комментарием. Фиг его знает, зачем они нам
    points = Column(Integer)  # Количество лайков. Опять же - фиг его знает зачем
    label = Column(String)  # Наша метка - понравилось/пофиг/не понравилось.


engine = create_engine("sqlite:///news.db")  # Пробуем открыть файл с базой данных. Если его нет - создаем.
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)  # Открываем сессию для работы с базой


@route('/')  # Декоратор, показывающий, что функция работает при вызове начальной страницы http://localhost:8080/
@route('/hello/<name>')  # Эта же фукнция будет обрабатывать адрес http://localhost:8080/hello/любое_значение
def index(name="Stranger"):  # Значение по умолчанию используется на http://localhost:8080/
    return template('hello_template', name=name)  # Вызываем шаблон hello_template.tpl


@route('/news')  # Функция будет работать при адресе http://localhost:8080/news
def news_list():
    s = session()
    rows = s.query(News).filter(News.label==None).all()  # Получаем из базы все записи, в которых label = None
    return template('news_template', rows=rows)  # Передаем записи в шаблон news_template.tpl. По шаблону будет
                                                 # формироваться страница


run(host='localhost', port=8080)  # Запуск сервера - доступен в браузере по адресу http://localhost:8080/

