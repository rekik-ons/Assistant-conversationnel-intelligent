from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime

from app.database import Base


class ConversationModel(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, unique=True, index=True)

    etape = Column(String)

    data = Column(JSON)

    date_creation = Column(DateTime, default=datetime.utcnow)