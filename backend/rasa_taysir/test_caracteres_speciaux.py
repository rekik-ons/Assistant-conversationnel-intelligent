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


noms_a_tester = [
    "Robert'); DROP TABLE prospects;--",
    "<script>alert('xss')</script>",
    "Ahmed العربي",
    "Jean-François O'Brien",
]

for nom_test in noms_a_tester:
    sender_id = f"test-special-{noms_a_tester.index(nom_test)}"
    slots = {"etat": "nom"}

    resultat = envoyer_message(sender_id, nom_test, "donner_nom", slots)
    messages = [r["text"] for r in resultat.get("responses", [])]
    slot_events = [e for e in resultat.get("events", []) if e.get("event") == "slot" and e.get("name") == "nom"]

    print(f"--- Nom testé : {nom_test!r} ---")
    print("MESSAGES :", messages)
    print("SLOT NOM ENREGISTRÉ :", slot_events)
    print()
