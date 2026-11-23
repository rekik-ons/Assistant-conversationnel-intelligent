from app.services.ai_service import extraire_informations


tests = [
    "Je gagne 3000 DT par mois et j'ai 600 DT de charges.",
    "Mon salaire est de 2500 dinars.",
    "Je souhaite demander 50000 DT.",
    "J'ai 25 ans.",
    "Mon numéro est 24235698."
]


for message in tests:

    print("=" * 70)
    print("MESSAGE :", message)

    resultat = extraire_informations(message)

    print("RESULTAT :", resultat)