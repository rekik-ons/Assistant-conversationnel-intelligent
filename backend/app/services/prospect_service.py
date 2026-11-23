from app.database import SessionLocal
from app.models.prospect import ProspectModel


def save_prospect(data):

    db = SessionLocal()

    try:

        prospect = ProspectModel(
            session_id=data["session_id"],

            nom=data["nom"],
            prenom=data["prenom"],
            telephone=data["telephone"],

            age=data["age"],
            profession=data["profession"],

            revenu=data["revenu"],
            charges=data["charges"],
            capacite_remboursement=data["capacite_remboursement"],

            montant_demande=data["montant_demande"],

            zone_geographique=data["zone_geographique"],

            score=data["score"],
            qualification=data["qualification"],
            eligibilite=data["eligibilite"]
        )

        db.add(prospect)
        db.commit()
        db.refresh(prospect)

        return prospect

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()