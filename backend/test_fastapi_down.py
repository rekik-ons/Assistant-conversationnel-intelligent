import requests

ACTION_SERVER = "http://localhost:5055/webhook"


def envoyer_message(sender_id, texte, intent, slots_actuels):
    payload = {
        "next_action": "action_traiter_reponse",
        "sender_id": sender_id,
        "tracker": {
            "sender_id": sender_id,
            "slots": slots_actuels,
            "latest_message": {
                "text": texte,
                "intent": {"name": intent, "confidence": 1.0},
                "entities": []
            },
            "events": [],
            "latest_event_time": 0,
            "followup_action": None,
            "paused": False,
            "latest_input_channel": "test",
            "active_loop": {},
            "latest_action_name": "action_listen"
        },
        "domain": {},
        "version": "3.6.21"
    }
    response = requests.post(ACTION_SERVER, json=payload, timeout=20)
    return response.json()


reponses = [
    ("TestPanne", "donner_nom"),
    ("FastAPI", "donner_prenom"),
    ("25123456", "donner_telephone"),
    ("28", "donner_age"),
    ("Testeur", "donner_profession"),
    ("1200", "donner_revenu"),
    ("3000", "donner_montant"),
    ("300", "donner_charges"),
    ("Tunis", "donner_zone"),
]

slots = {"etat": "nom"}
for texte, intent in reponses:
    resultat = envoyer_message("test-fastapi-down", texte, intent, slots)
    for e in resultat.get("events", []):
        if e.get("event") == "slot":
            slots[e["name"]] = e["value"]
    messages = [r["text"] for r in resultat.get("responses", [])]
    print(f"'{texte}' -> {messages}")

print("\nSlots finaux :", slots)