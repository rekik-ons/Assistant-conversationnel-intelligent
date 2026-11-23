from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func

from app.database import SessionLocal
from app.models.prospect import ProspectModel


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("")
def get_dashboard():

    db = SessionLocal()

    try:
        total_prospects = db.query(ProspectModel).count()

        chauds = db.query(ProspectModel).filter(
            ProspectModel.qualification == "Prospect chaud"
        ).count()

        tiedes = db.query(ProspectModel).filter(
            ProspectModel.qualification == "Prospect tiède"
        ).count()

        froids = db.query(ProspectModel).filter(
            ProspectModel.qualification == "Prospect froid"
        ).count()

        
        eligibles = db.query(ProspectModel).filter(
            ProspectModel.eligibilite == "Éligible"
        ).count()

        non_eligibles = db.query(ProspectModel).filter(
            ProspectModel.eligibilite == "Non éligible"
        ).count()

        revenu_moyen = db.query(
            func.avg(ProspectModel.revenu)
        ).scalar()

        montant_demande_moyen = db.query(
            func.avg(ProspectModel.montant_demande)
        ).scalar()

        return {
            "total_prospects": total_prospects,
            "chauds": chauds,
            "tiedes": tiedes,
            "froids": froids,
            "eligibles": eligibles,
            "non_eligibles": non_eligibles,
            "revenu_moyen": round(revenu_moyen, 2) if revenu_moyen else 0,
            "montant_demande_moyen": round(montant_demande_moyen, 2)
            if montant_demande_moyen else 0
        }

    finally:
        db.close()

@router.get("/qualifications")
def get_qualifications(
    qualification: str = Query(...)
):

    db = SessionLocal()

    try:

        qualification = qualification.lower().strip()

        valeurs = {
            "chaud": "Prospect chaud",
            "tiede": "Prospect tiede",
            "tiède": "Prospect tiede",
            "froid": "Prospect froid"
        }

        if qualification not in valeurs:

            return {
                "message": "Qualification invalide",
                "valeurs_acceptées": [
                    "chaud",
                    "tiede",
                    "froid"
                ]
            }

        qualification_db = valeurs[qualification]

        prospects = db.query(ProspectModel).filter(
            ProspectModel.qualification == qualification_db
        ).all()

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
                "capacite_remboursement": (
                    prospect.capacite_remboursement
                ),
                "montant_demande": prospect.montant_demande,
                "zone_geographique": (
                    prospect.zone_geographique
                ),
                "score": prospect.score,
                "qualification": prospect.qualification,
                "eligibilite": prospect.eligibilite
            })

        return {
            "qualification": qualification_db,
            "nombre": len(result),
            "prospects": result
        }

    finally:
        db.close()


@router.get("/revenus")
def get_revenus():

    db = SessionLocal()

    try:

        prospects = db.query(ProspectModel).all()

        if not prospects:

            return {
                "total_prospects": 0,
                "revenu_moyen": 0,
                "charges_moyennes": 0,
                "capacite_remboursement_moyenne": 0,
                "montant_demande_moyen": 0,
                "revenu_minimum": 0,
                "revenu_maximum": 0,
                "montant_demande_minimum": 0,
                "montant_demande_maximum": 0
            }

        revenus = [
            p.revenu
            for p in prospects
            if p.revenu is not None
        ]

        charges = [
            p.charges
            for p in prospects
            if p.charges is not None
        ]

        capacites = [
            p.capacite_remboursement
            for p in prospects
            if p.capacite_remboursement is not None
        ]

        montants = [
            p.montant_demande
            for p in prospects
            if p.montant_demande is not None
        ]

        return {
            "total_prospects": len(prospects),

            "revenu_moyen":
                round(sum(revenus) / len(revenus), 2)
                if revenus else 0,

            "charges_moyennes":
                round(sum(charges) / len(charges), 2)
                if charges else 0,

            "capacite_remboursement_moyenne":
                round(sum(capacites) / len(capacites), 2)
                if capacites else 0,

            "montant_demande_moyen":
                round(sum(montants) / len(montants), 2)
                if montants else 0,

            "revenu_minimum":
                min(revenus) if revenus else 0,

            "revenu_maximum":
                max(revenus) if revenus else 0,

            "montant_demande_minimum":
                min(montants) if montants else 0,

            "montant_demande_maximum":
                max(montants) if montants else 0
        }

    finally:
        db.close()



@router.get("/profils")
def get_profils():

    db = SessionLocal()

    try:

        prospects = db.query(ProspectModel).all()

        if not prospects:

            return {
                "total_prospects": 0,
                "age_moyen": 0,
                "professions": {},
                "zones_geographiques": {},
                "eligibilite": {
                    "eligible": 0,
                    "non_eligible": 0
                },
                "tranches_age": {
                    "18-25": 0,
                    "26-35": 0,
                    "36-45": 0,
                    "46-55": 0,
                    "56+": 0
                }
            }

        ages = [
            p.age
            for p in prospects
            if p.age is not None
        ]

        age_moyen = (
            round(sum(ages) / len(ages), 2)
            if ages else 0
        )

        professions = {}

        for p in prospects:

            if p.profession and p.profession.strip():

                cle = p.profession.strip().title()

                professions[cle] = (
                    professions.get(cle, 0) + 1
                )

        zones = {}

        for p in prospects:

            if p.zone_geographique and p.zone_geographique.strip():

                cle = p.zone_geographique.strip().title()

                zones[cle] = (
                    zones.get(cle, 0) + 1
                )

        eligible = sum(
            1 for p in prospects
            if p.eligibilite == "Éligible"
        )

        non_eligible = sum(
            1 for p in prospects
            if p.eligibilite == "Non éligible"
        )

        tranches_age = {
            "18-25": 0,
            "26-35": 0,
            "36-45": 0,
            "46-55": 0,
            "56+": 0
        }

        for age in ages:

            if 18 <= age <= 25:
                tranches_age["18-25"] += 1

            elif 26 <= age <= 35:
                tranches_age["26-35"] += 1

            elif 36 <= age <= 45:
                tranches_age["36-45"] += 1

            elif 46 <= age <= 55:
                tranches_age["46-55"] += 1

            else:
                tranches_age["56+"] += 1

        return {
            "total_prospects": len(prospects),
            "age_moyen": age_moyen,
            "professions": professions,
            "zones_geographiques": zones,

            "eligibilite": {
                "eligible": eligible,
                "non_eligible": non_eligible
            },

            "tranches_age": tranches_age
        }

    finally:
        db.close()



@router.get("/recent")
def get_recent_prospects():

    db = SessionLocal()

    try:

        prospects = db.query(
            ProspectModel
        ).order_by(
            ProspectModel.id.desc()
        ).limit(10).all()

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
                "capacite_remboursement":
                    prospect.capacite_remboursement,
                "montant_demande":
                    prospect.montant_demande,
                "zone_geographique":
                    prospect.zone_geographique,
                "score": prospect.score,
                "qualification":
                    prospect.qualification,
                "eligibilite":
                    prospect.eligibilite,
                "statut_conseiller":
                    prospect.statut_conseiller
            })

        return result

    finally:

        db.close()

@router.get("/eligibilite")
def get_eligibilite(
    eligibilite: str = Query(...)
):

    db = SessionLocal()

    try:

        eligibilite = eligibilite.lower().strip()

        valeurs = {
            "eligible": "Éligible",
            "éligible": "Éligible",
            "non eligible": "Non éligible",
            "non éligible": "Non éligible"
        }

        if eligibilite not in valeurs:

            return {
                "message": "Valeur d'éligibilité invalide",
                "valeurs_acceptées": [
                    "eligible",
                    "non eligible"
                ]
            }

        eligibilite_db = valeurs[eligibilite]

        prospects = db.query(ProspectModel).filter(
            ProspectModel.eligibilite == eligibilite_db
        ).all()

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
                "capacite_remboursement": (
                    prospect.capacite_remboursement
                ),
                "montant_demande": prospect.montant_demande,
                "zone_geographique": (
                    prospect.zone_geographique
                ),
                "score": prospect.score,
                "qualification": prospect.qualification,
                "eligibilite": prospect.eligibilite
            })

        return {
            "eligibilite": eligibilite_db,
            "nombre": len(result),
            "prospects": result
        }

    finally:
        db.close()

@router.get("/qualification/{qualification}")
def get_prospects_by_qualification(qualification: str):

    db = SessionLocal()

    qualification_normalisee = qualification.lower().strip()

    correspondances = {
        "chaud": "Prospect chaud",
        "tiede": "Prospect tiède",
        "froid": "Prospect froid"
    }

    if qualification_normalisee not in correspondances:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Qualification invalide"
        )

    valeur = correspondances[qualification_normalisee]

    prospects = db.query(ProspectModel).filter(
        ProspectModel.qualification == valeur,
        ProspectModel.eligibilite == "Éligible"
    ).all()

    result = []

    for prospect in prospects:

        result.append({
            "id": prospect.id,
            "nom": prospect.nom,
            "prenom": prospect.prenom,
            "telephone": prospect.telephone,
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "charges": prospect.charges,
            "montant_demande": prospect.montant_demande,
            "capacite_remboursement":
                prospect.capacite_remboursement,
            "zone_geographique":
                prospect.zone_geographique,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "eligibilite": prospect.eligibilite
        })

    db.close()

    return {
        "qualification": qualification_normalisee,
        "nombre": len(result),
        "prospects": result
    }

@router.get("/non-qualifies")
def get_prospects_non_qualifies():

    db = SessionLocal()

    prospects = db.query(ProspectModel).filter(
        ProspectModel.eligibilite == "Non éligible"
    ).all()

    result = []

    for prospect in prospects:

        result.append({
            "id": prospect.id,
            "nom": prospect.nom,
            "prenom": prospect.prenom,
            "telephone": prospect.telephone,
            "age": prospect.age,
            "profession": prospect.profession,
            "revenu": prospect.revenu,
            "charges": prospect.charges,
            "montant_demande": prospect.montant_demande,
            "capacite_remboursement":
                prospect.capacite_remboursement,
            "zone_geographique":
                prospect.zone_geographique,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "eligibilite": prospect.eligibilite
        })

    db.close()

    return {
        "categorie": "non_qualifie",
        "nombre": len(result),
        "prospects": result
    }


@router.get("/statut")
def get_prospects_par_statut(statut: str):

    db = SessionLocal()

    statuts_valides = [
        "non_traite",
        "en_cours",
        "traite"
    ]

    if statut not in statuts_valides:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Statut invalide"
        )

    prospects = db.query(ProspectModel).filter(
        ProspectModel.statut_conseiller == statut
    ).all()

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
            "capacite_remboursement":
                prospect.capacite_remboursement,
            "montant_demande":
                prospect.montant_demande,
            "zone_geographique":
                prospect.zone_geographique,
            "score": prospect.score,
            "qualification": prospect.qualification,
            "eligibilite": prospect.eligibilite,
            "statut_conseiller":
                prospect.statut_conseiller
        })

    db.close()

    return {
        "statut": statut,
        "nombre": len(result),
        "prospects": result
    }