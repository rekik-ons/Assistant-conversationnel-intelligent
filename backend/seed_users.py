from app.database import Base, engine, SessionLocal
from app.models.utilisateur import UtilisateurModel

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if not db.query(UtilisateurModel).first():
    db.add(UtilisateurModel(login="admin", mot_de_passe="admin123", role="administrateur"))
    db.add(UtilisateurModel(login="conseiller", mot_de_passe="conseiller123", role="conseiller"))
    db.commit()

db.close()
print("Utilisateurs créés.")