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
    response = requests.post(ACTION_SERVER, json=payload, timeout=15)
    return response.json()


def tester(label, etat_slot, texte, intent):
    slots = {"etat": etat_slot}
    resultat = envoyer_message(f"test-nonnum-{label}", texte, intent, slots)
    messages = [r["text"] for r in resultat.get("responses", [])]
    slot_events = [e for e in resultat.get("events", []) if e.get("event") == "slot"]
    print(f"--- {label} : entrée = '{texte}' ---")
    print("MESSAGES :", messages)
    print("SLOTS MODIFIÉS :", slot_events)
    print()


tester("age_texte_pur", "age", "abc", "donner_age")
tester("age_vide", "age", "", "donner_age")
tester("age_espaces", "age", "   ", "donner_age")
tester("revenu_texte_pur", "revenu", "beaucoup", "donner_revenu")
tester("montant_texte_pur", "montant_demande", "je ne sais pas", "donner_montant")
tester("charges_emoji", "charges", "😀😀😀", "donner_charges")