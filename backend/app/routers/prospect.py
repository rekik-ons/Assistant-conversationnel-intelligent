from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

import csv
from io import StringIO

from app.database import SessionLocal, get_db
from app.models.prospect import ProspectModel
from app.schemas.prospect import ProspectCreate, ProspectUpdate
from app.services.scoring import calculate_score

router = APIRouter(
    prefix="/prospects",
    tags=["Prospects"]
)



@router.post("/")
def create_prospect(data: ProspectCreate):

    db = SessionLocal()

    try:
        prospect_data = data.model_dump()

        
        resultat = calculate_score(prospect_data)
        

        prospect = ProspectModel(
            nom=data.nom,
            prenom=data.prenom,
            telephone=data.telephone,
            age=data.age,
            profession=data.profession,

            revenu=data.revenu,
            charges=data.charges,

            montant_demande=data.montant_demande,
            zone_geographique=data.zone_geographique,

            capacite_remboursement=resultat["capacite_remboursement"],
            score=resultat["score"],
            qualification=resultat["qualification"],
            eligibilite=resultat["eligibilite"],

            statut_conseiller=data.statut_conseiller
)
        db.add(prospect)
        db.commit()
        db.refresh(prospect)

        return {
            "message": "Prospect créé avec succès",
            "id": prospect.id,
            "nom": prospect.nom,
            "prenom": prospect.prenom,
            "telephone": prospect.telephone,
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "charges": prospect.charges,
            "montant_demande": prospect.montant_demande,
            "zone_geographique": prospect.zone_geographique,
            "capacite_remboursement": prospect.capacite_remboursement,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "eligibilite": prospect.eligibilite,
            "statut_conseiller": prospect.statut_conseiller
}

    finally:
        db.close()



@router.get("/")
def get_prospects():

    db = SessionLocal()

    try:
        prospects = db.query(ProspectModel).all()

        result = []

        for prospect in prospects:

            result.append({
                "id": prospect.id,
                "session_id": prospect.session_id,

                "nom": prospect.nom,
                "prenom": prospect.prenom,
                "telephone": prospect.telephone,
                "age": prospect.age,
                "profession": prospect.profession,

                "revenu": prospect.revenu,
                "charges": prospect.charges,
                "montant_demande": prospect.montant_demande,
                "zone_geographique": prospect.zone_geographique,

                "capacite_remboursement": prospect.capacite_remboursement,

                "score": prospect.score,
                "qualification": prospect.qualification,
                "eligibilite": prospect.eligibilite,

                "statut_conseiller": prospect.statut_conseiller
})
        return result

    finally:
        db.close()


@router.get("/export/csv")
def export_prospects_csv():
    db = SessionLocal()

    try:
        prospects = db.query(ProspectModel).all()

        output = StringIO()

        writer = csv.writer(output)

        
        writer.writerow([
            "id",
            "session_id",
            "nom",
            "prenom",
            "telephone",
            "age",
            "profession",
            "revenu",
            "charges",
            "montant_demande",
            "zone_geographique",
            "capacite_remboursement",
            "score",
            "qualification",
            "eligibilite",
            "statut_conseiller"
        ])

        
        for prospect in prospects:
            writer.writerow([
                prospect.id,
                prospect.session_id,
                prospect.nom,
                prospect.prenom,
                prospect.telephone,
                prospect.age,
                prospect.profession,
                prospect.revenu,
                prospect.charges,
                prospect.montant_demande,
                prospect.zone_geographique,
                prospect.capacite_remboursement,
                prospect.score,
                prospect.qualification,
                prospect.eligibilite,
                prospect.statut_conseiller
            ])

        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=prospects.csv"
            }
        )

    finally:
        db.close()

@router.get("/{prospect_id}")
def get_prospect(prospect_id: int):

    db = SessionLocal()

    try:
        prospect = (
            db.query(ProspectModel)
            .filter(ProspectModel.id == prospect_id)
            .first()
        )

        if not prospect:
            raise HTTPException(
                status_code=404,
                detail="Prospect introuvable"
            )

        return {
            "id": prospect.id,
            "session_id": prospect.session_id,
            "nom": prospect.nom,
            "prenom": prospect.prenom,
            "telephone": prospect.telephone,
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "zone_geographique": prospect.zone_geographique,
            "montant_demande": prospect.montant_demande,
            "capacite_remboursement": prospect.capacite_remboursement,
            "charges": prospect.charges,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "eligibilite": prospect.eligibilite,
            "statut_conseiller": prospect.statut_conseiller
        }

    finally:
        db.close()


@router.delete("/{prospect_id}")
def delete_prospect(prospect_id: int):

    db = SessionLocal()

    try:
        prospect = (
            db.query(ProspectModel)
            .filter(ProspectModel.id == prospect_id)
            .first()
        )

        if not prospect:
            raise HTTPException(
                status_code=404,
                detail="Prospect introuvable"
            )

        db.delete(prospect)
        db.commit()

        return {
            "message": "Prospect supprimé avec succès",
            "id": prospect_id
        }

    finally:
        db.close()


@router.patch("/{prospect_id}")
def update_prospect(
    prospect_id: int,
    data: ProspectUpdate
):

    db = SessionLocal()

    try:
        prospect = (
            db.query(ProspectModel)
            .filter(ProspectModel.id == prospect_id)
            .first()
        )

        if not prospect:
            raise HTTPException(
                status_code=404,
                detail="Prospect introuvable"
            )

        updates = data.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="Aucune modification fournie"
            )

        
        for field, value in updates.items():
            setattr(prospect, field, value)

        
        prospect_data = {
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "montant_demande": prospect.montant_demande,
            "charges": prospect.charges
        }

        resultat = calculate_score(prospect_data)
        prospect.score = resultat["score"]
        prospect.qualification = resultat["qualification"]

        db.commit()
        db.refresh(prospect)

        return {
            "message": "Prospect modifié avec succès",
            "id": prospect.id,
            "nom": prospect.nom,
            "prenom": prospect.prenom,
            "telephone": prospect.telephone,
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "montant_demande": prospect.montant_demande,
            "charges": prospect.charges,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "statut_conseiller": prospect.statut_conseiller
        }

    finally:
        db.close()



@router.patch("/{prospect_id}/statut")
def modifier_statut_prospect(
    prospect_id: int,
    statut: str,
    db: Session = Depends(get_db)
):

    prospect = (
        db.query(ProspectModel)
        .filter(ProspectModel.id == prospect_id)
        .first()
    )

    if not prospect:
        raise HTTPException(
            status_code=404,
            detail="Prospect introuvable"
        )

    statuts_valides = [
        "non_traite",
        "en_cours",
        "traite"
    ]

    if statut not in statuts_valides:
        raise HTTPException(
            status_code=400,
            detail="Statut invalide. Valeurs autorisées : "
                   "non_traite, en_cours, traite"
        )

    prospect.statut_conseiller = statut

    db.commit()
    db.refresh(prospect)

    return {
        "message": "Statut modifié avec succès",
        "id": prospect.id,
        "statut_conseiller": prospect.statut_conseiller
    }

