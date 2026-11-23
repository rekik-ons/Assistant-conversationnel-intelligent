import requests
import json

def tester_telephone(numero, etat_initial="telephone"):
    payload = {
        "next_action": "action_traiter_reponse",
        "sender_id": f"test-tel-{numero}",
        "tracker": {
            "sender_id": f"test-tel-{numero}",
            "slots": {"etat": etat_initial},
            "latest_message": {
                "text": numero,
                "intent": {"name": "donner_telephone", "confidence": 1.0},
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

    response = requests.post(
        "http://localhost:5055/webhook",
        json=payload,
        timeout=15
    )

    data = response.json()
    messages = [r["text"] for r in data.get("responses", [])]
    events_slots = [
        e for e in data.get("events", [])
        if e.get("event") == "slot" and e.get("name") == "telephone"
    ]

    print(f"NUMERO TESTE : {numero}")
    print("MESSAGES     :", messages)
    print("SLOT TELEPHONE ENREGISTRE :", events_slots)
    print("-" * 50)


# Numéros à tester
tester_telephone("21345678")   # valide, attendu : accepté
tester_telephone("00000000")   # invalide (que des 0), attendu : refusé
tester_telephone("11111111")   # invalide (chiffre unique), attendu : refusé
tester_telephone("01234567")   # invalide (commence par 0), attendu : refusé
tester_telephone("98765432")   # valide, attendu : accepté