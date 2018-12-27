"""
    book的模型
"""
import uuid

from flask import g
from sqlalchemy import Column, String, Float, orm, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel, db


class BookModel(BaseModel):
    book_id = Column(String(32), primary_key=True)
    title = Column(String(100), nullable=False, default='未名')
    price = Column(Float, default=0.0)
    author = Column(String(50))

    # 用于序列化start
    @orm.reconstructor
    def __init__(self):
        self.feilds = ['book_id', 'title', 'price', 'author', 'user']
    #   用于序列化end

    @staticmethod
    def add_book(attrs_dict):
        with db.auto_commit():
            book = BookModel()
            book.book_id = str(uuid.uuid4()).replace('-', '')
            book.user_id = g.user.uid
            book.set_attrs(attrs_dict)
            db.session.add(book)
