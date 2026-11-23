import requests

RASA_SERVER = "http://localhost:5005/webhooks/rest/webhook"

INTENTIONS_FAQ = [
    "faq_financement",
    "faq_eligibilite",
    "faq_documents",
    "faq_montant",
    "faq_remboursement",
    "faq_delai",
    "faq_conditions",
    "faq_agence",
    "faq_contact",
    "faq_frais",
    "faq_demande",
    "faq_simulation",
]

for i, intention in enumerate(INTENTIONS_FAQ):
    sender_id = f"test-faq-{i}"

    # On envoie directement l'intention au format /intent_name
    # (syntaxe spéciale de Rasa pour forcer une intention sans NLU)
    payload = {
        "sender": sender_id,
        "message": f"/{intention}"
    }

    response = requests.post(RASA_SERVER, json=payload, timeout=15)
    data = response.json()

    messages = [m.get("text", "") for m in data]

    print(f"--- {intention} ---")
    print("REPONSE :", messages)
    print()