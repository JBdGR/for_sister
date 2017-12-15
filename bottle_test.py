from bottle import route, run, template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)


session = sessionmaker(bind=engine)


@route('/')
@route('/hello/<name>')
def index(name="Stranger"):
    return template('hello_template', name=name)


@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label==None).all()
    return template('news_template', rows=rows)


run(host='localhost', port=8080)

session.close_all()
