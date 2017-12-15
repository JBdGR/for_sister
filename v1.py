'''
Наш основной рабочий файл. Позволяет обновлять записи (Берем только то, чего нет в базе), ставить метки на статьи
'''
from bottle import route, run, template, redirect, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
import fasttest

# На основе Base будем создавать наш класс. Это все мутки с ORM, т.ч. прими как должное
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


engine = create_engine("sqlite:///news.db")  # Пробуем открыть файл. В отличии от db_test - если файл есть, мы его
                                             # не удаляем. По хорошему нужно exception, т.к. если файл не открыть
                                             # (например, открыт другой софтиной) - будем падать
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()


# Декоратор, показывающий, что функция работает при вызове начальной страницы http://localhost:8080/update_news
@route('/update_news')
def update_news():
    news_list = fasttest.get_news('https://news.ycombinator.com/newest')  # Получаем список новостйе
    rows = s.query(News).all()  # Получаем список тех новостей, которые уже есть в базе
    for i in news_list:  # Для каждой новой носоти
        news = News(title=i['title'], author=i['author'], url=i['url'],
                    comments=i['comments'], points=i['points'])  # Создаем экземпляр, заполняем атрибуты
        # Это стоит перевернуть - сначала проверка по наличию новости, потом создание экземпляра

        for z in rows:  # Для всех записей в базе
            if z.title == news.title and z.author == news.author:  # Автор и название совпадают
                break  # Выходим из цикла
        else:  # Выполнится, только если нет совпадений
            s.add(news)  # Добавляем строку
    s.commit()  # Коммитимся
    redirect('/')  # Возвращаемся на основную страницу


@route('/')  # Основная страница - отображение всех статей без меток
def news_list():
    rows = s.query(News).filter(News.label==None).all()  # Запрос на все новости, на которые нет оценок
    return template('news_template', rows=rows)  # Передача информации в шаблон

@route('/show_all')  # Отображение всех статей (И с оценками, и без)
def show_all():
    rows = s.query(News).all()
    return template('news_template_all', rows=rows)  # Используется свой шаблон

@route('/add_label/')  # Добавить метку
def add_label():
    label = request.query.label  # Из GET-а получаем значение label
    id = request.query.id  # Из GET-а получаем значение id
    # Обновляем поле label для записи, у которой id соответсвет полученному.
    s.query(News).filter(News.id == int(id)).update({News.label: label}, synchronize_session=False)
    s.commit()
    redirect('/')


run(host='localhost', port=8080)