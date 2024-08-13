from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
import datetime
import os

db_url = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER','postgres')}:{os.environ.get('POSTGRES_PASSWORD','password')}@\
{os.environ.get('POSTGRES_HOST','localhost')}:{os.environ.get('POSTGRES_PORT','5432')}/{os.environ.get('POSTGRES_DB','postgres')}"
# sql_engine = create_engine(db_url)
# session_obj = sessionmaker(bind=sql_engine)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine(db_url, echo=True)
session_obj = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Define the Base class
Base = declarative_base()


# User model
class User(Base):
    __tablename__ = 'user_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(400), unique=True)
    author = Column(String(200))
    genre = Column(String(200))
    year_published = Column(Integer)
    summary = Column(String(10000))
    created_at = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('user_record.id'))
    review_text = Column(String(10000))
    rating = Column(Integer)
    created_at = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# table creation
# Base.metadata.create_all(async_engine)
