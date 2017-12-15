from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
import fasttest
import os

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


if os.path.exists("news.db"):
    os.remove("news.db")

engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)


session = sessionmaker(bind=engine)
s = session()

news_list = fasttest.get_news('https://news.ycombinator.com/')
for i in news_list:
    print(i)
    news = News(title=i['title'], author=i['author'], url=i['url'],
            comments=i['comments'], points=i['points'])
    s.add(news)

s.commit()