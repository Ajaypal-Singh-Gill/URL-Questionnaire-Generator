from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.dbconfig import Base

class URLRecord(Base):
    __tablename__ = 'url_records'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2083), unique=True, nullable=False)
    status = Column(String(50), nullable=False)

    # Relationship to content
    content = relationship("ContentRecord", back_populates="url_record")

class ContentRecord(Base):
    __tablename__ = 'content_records'

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey('url_records.id'), nullable=False)
    content = Column(Text, nullable=False)
    questions = Column(Text, nullable=False)

    # Relationship back to URLRecord
    url_record = relationship("URLRecord", back_populates="content")
