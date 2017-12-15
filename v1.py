from bottle import route, run, template, redirect, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
import fasttest

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)
s = session()


@route('/update_news')
def update_news():
    news_list = fasttest.get_news('https://news.ycombinator.com/newest')
    rows = s.query(News).all()
    for i in news_list:
        news = News(title=i['title'], author=i['author'], url=i['url'],
                    comments=i['comments'], points=i['points'])
        for z in rows:
            if z.title == news.title and z.author == news.author:
                break
        else:
            s.add(news)
    s.commit()
    redirect('/')


@route('/')
def news_list():
    rows = s.query(News).filter(News.label==None).all()
    return template('news_template', rows=rows)

@route('/show_all')
def show_all():
    rows = s.query(News).all()
    return template('news_template_all', rows=rows)

@route('/add_label/')
def add_label():
    label = request.query.label
    id = request.query.id
    s.query(News).filter(News.id == int(id)).update({News.label: label}, synchronize_session=False)
    s.commit()
    redirect('/')


run(host='localhost', port=8080)

session.close_all()
