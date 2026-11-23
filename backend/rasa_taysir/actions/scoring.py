def calculate_score(data):
    score = 0

    revenu = float(data.get("revenu", 0) or 0)
    charges = float(data.get("charges", 0) or 0)
    montant = float(data.get("montant_demande", 0) or 0)

    # ==========================================================
    # 1. CAPACITÉ DE REMBOURSEMENT
    # ==========================================================

    capacite = revenu - charges

    if capacite < 0:
        capacite = 0

    # ==========================================================
    # 2. SCORE SELON LE REVENU
    # ==========================================================

    if revenu >= 1500:
        score += 30

    elif revenu >= 1000:
        score += 20

    elif revenu >= 500:
        score += 10

    # ==========================================================
    # 3. SCORE SELON LA CAPACITÉ
    # ==========================================================

    if capacite >= 500:
        score += 30

    elif capacite >= 300:
        score += 20

    elif capacite > 0:
        score += 10

    # ==========================================================
    # 4. SCORE SELON LE MONTANT DEMANDÉ
    # ==========================================================

    if montant > 0 and capacite >= montant * 0.3:
        score += 20

    # ==========================================================
    # 5. SCORE SELON LA ZONE
    # ==========================================================

    if data.get("zone_geographique"):
        score += 20

    # ==========================================================
    # 6. QUALIFICATION
    # ==========================================================

    if score >= 70:
        qualification = "Prospect chaud"

    elif score >= 40:
        qualification = "Prospect tiède"

    elif score > 0:
        qualification = "Prospect froid"

    else:
        qualification = "Non qualifié"

    # ==========================================================
    # 7. ÉLIGIBILITÉ
    # ==========================================================

    if capacite > 0:
        eligibilite = "Éligible"
    else:
        eligibilite = "Non éligible"

    # ==========================================================
    # 8. RÉSULTAT
    # ==========================================================

    return {
        "score": score,
        "qualification": qualification,
        "eligibilite": eligibilite,
        "capacite_remboursement": capacite
    }