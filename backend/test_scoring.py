from app.database import SessionLocal
from app.models.prospect import ProspectModel


db = SessionLocal()

prospects = db.query(ProspectModel).order_by(
    ProspectModel.id
).all()

for p in prospects:
    print(
        p.session_id,
        "|",
        p.nom,
        "|",
        p.score,
        "|",
        p.qualification
    )

db.close()