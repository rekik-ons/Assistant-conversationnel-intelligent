def calculate_score(data):
    score = 0

    revenu = float(data.get("revenu", 0) or 0)
    charges = float(data.get("charges", 0) or 0)
    montant = float(data.get("montant_demande", 0) or 0)



    capacite = revenu - charges


    if capacite < 0:
        capacite = 0

  

    if revenu >= 1500:
        score += 30

    elif revenu >= 1000:
        score += 20

    elif revenu >= 500:
        score += 10



    if capacite >= 500:
        score += 30

    elif capacite >= 300:
        score += 20

    elif capacite > 0:
        score += 10


    if montant > 0 and capacite >= montant * 0.3:
        score += 20



    if data.get("zone_geographique"):
        score += 20



    if score >= 70:
        qualification = "Prospect chaud"

    elif score >= 40:
        qualification = "Prospect tiède"

    elif score > 0:
        qualification = "Prospect froid"

    else:
        qualification = "Non qualifié"

    

    if capacite > 0:
        eligibilite = "Éligible"

    else:
        eligibilite = "Non éligible"



    return {
        "score": score,
        "qualification": qualification,
        "eligibilite": eligibilite,
        "capacite_remboursement": capacite
    }