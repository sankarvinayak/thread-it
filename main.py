from os import environ

from sqlalchemy import create_engine, Column, String, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Bot.bot import *

Base = declarative_base()


Consumer_key_bot = environ['Consumer_key_bot']
Consumer_key_Secret_bot = environ['Consumer_key_Secret_bot']
Api_key_bot = environ['Api_key_bot']
Api_key_Secret_bot = environ['Api_key_Secret_bot']


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    user = Column('user_id', String)
    tweet = Column('tweet', String)
    
    
class Last(Base):
    __tablename__ = 'last'
    id = Column('id', Integer, primary_key=True)
    lastid = Column('lastid', BigInteger) 


engine = create_engine('postgresql+psycopg2://dncayxqe:7apaHxS2RAN6NliSH3v66RKmNKnGu4av@batyr.db.elephantsql.com/dncayxqe', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def update_db(thread_text, user):
    new_user = User()
    new_user.user = user
    new_user.tweet = thread_text
    session.add(new_user)
    session.commit()
    
    
def get_last_seen_id():
    last_seen = session.query(Last).first()
    return last_seen.lastid


def set_last_seen_id(last_seen_id):
    last_seen = session.query(Last).first()
    last_seen.lastid = last_seen_id
    session.commit()
    return


if __name__ == '__main__':
    auth_api = authenticate(Consumer_key_bot,Consumer_key_Secret_bot,Api_key_bot,Api_key_Secret_bot)
    while True:
        last_seen_id = get_last_seen_id()
        last_seen_id, status_id, author_id, user,is_it_tweet = get_mentioned_thread(auth_api, last_seen_id)
        if last_seen_id == 0 and status_id == 0 and author_id == 0 and user == 0:
            continue
        set_last_seen_id(last_seen_id)
        if is_it_tweet==1:
            thread = get_tweet_text(auth_api,status_id)
        else:
            thread = get_thread_text(auth_api, author_id, status_id)
        try:
            auth_api.send_direct_message(user,thread)
            update_db(thread, user)
        except Exception as e:
            print(e)
