from sqlalchemy import Column, Integer, String

from app.database import Base


class UtilisateurModel(Base):

    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "administrateur" ou "conseiller"