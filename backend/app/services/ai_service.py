import re


def extraire_informations(message: str) -> dict:

    resultat = {
        "nom": None,
        "prenom": None,
        "telephone": None,
        "age": None,
        "profession": None,
        "revenu": None,
        "montant_demande": None,
        "charges": None,
        "zone_geographique": None,
    }

    texte = message.strip()
    texte_lower = texte.lower()

    #tel
    match = re.search(r"\b\d{8}\b", texte)

    if match:
        resultat["telephone"] = match.group(0)

    #age
    patterns_age = [
        r"\b(?:j['’]ai)\s+(\d{1,2})\s+ans?\b",
        r"\b(?:age|âgé|âgée)\s*(?:de)?\s*(\d{1,2})\b",
    ]

    for pattern in patterns_age:

        match = re.search(pattern, texte_lower)

        if match:
            resultat["age"] = int(match.group(1))
            break

    #revenu
    match = re.search(
        r"(?:revenu|salaire|gagne|gagner|touche|paie)"
        r".{0,40}?(\d+(?:[.,]\d+)?)",
        texte_lower
    )

    if match:
        resultat["revenu"] = float(
            match.group(1).replace(",", ".")
        )

    #charges
    match = re.search(
        r"(?:charges|dépenses|depenses|frais)"
        r".{0,40}?(\d+(?:[.,]\d+)?)",
        texte_lower
    )

    if match:
        resultat["charges"] = float(
            match.group(1).replace(",", ".")
        )

    #montant demandé
    match = re.search(
        r"(?:demande|demandé|demander|financement|besoin)"
        r".{0,40}?(\d+(?:[.,]\d+)?)",
        texte_lower
    )

    if match:
        resultat["montant_demande"] = float(
            match.group(1).replace(",", ".")
        )

    return resultat