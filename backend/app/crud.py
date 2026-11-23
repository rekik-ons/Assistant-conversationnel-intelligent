from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.prospect import Prospect


def create_prospect(data: dict):

    db: Session = SessionLocal()

    prospect = Prospect(
        nom=data.get("nom"),
        prenom=data.get("prenom"),
        telephone=data.get("telephone"),
        age=int(data.get("age", 0)),
        profession=data.get("profession"),
        revenu=float(data.get("revenu", 0)),
        montant_demande=float(data.get("montant_demande", 0)),
        score=int(data.get("score", 0)),
        qualification=data.get("qualification"),
    
    )

    db.add(prospect)
    db.commit()
    db.refresh(prospect)
    db.close()

    return prospect