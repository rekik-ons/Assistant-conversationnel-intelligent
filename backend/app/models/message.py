from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class MessageModel(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    role = Column(String)

    contenu = Column(String)

    date_creation = Column(DateTime, default=datetime.utcnow)