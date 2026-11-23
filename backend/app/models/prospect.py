from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class ProspectModel(Base):

    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, unique=True, index=True)

    nom = Column(String)
    prenom = Column(String)
    telephone = Column(String)
    age = Column(Integer)
    profession = Column(String)

    revenu = Column(Float)
    charges = Column(Float)

    capacite_remboursement = Column(Float)

    montant_demande = Column(Float)

    zone_geographique = Column(String)

    score = Column(Integer)
    qualification = Column(String)
    eligibilite = Column(String)

    statut_conseiller = Column(
        String,
        default="non_traite",
        nullable=False
    )