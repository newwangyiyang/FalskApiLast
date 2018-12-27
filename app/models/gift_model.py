"""
    gift模型
"""
from sqlalchemy import Column, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class GiftModel(BaseModel):
    gift_id = Column(String(32), primary_key=True)
    user = relationship('UserModel')
    user_id = Column(String(32), ForeignKey)
    book = relationship('BookModel')
    book_id = Column(String(32), ForeignKey)
    lunched = Column(SmallInteger, default=0)