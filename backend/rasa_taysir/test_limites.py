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


def tester_valeur_unique(label, etat_slot, texte, intent):
    """Teste une seule valeur pour un slot donné, en isolant le test."""
    slots = {"etat": etat_slot}
    resultat = envoyer_message(f"test-limite-{label}", texte, intent, slots)

    messages = [r["text"] for r in resultat.get("responses", [])]
    slot_events = [
        e for e in resultat.get("events", [])
        if e.get("event") == "slot"
    ]

    print(f"--- {label} : entrée = '{texte}' ---")
    print("MESSAGES :", messages)
    print("SLOTS MODIFIÉS :", slot_events)
    print()


# ============================================================
# TESTS SUR L'ÂGE
# ============================================================

tester_valeur_unique("age_17_refuse_attendu", "age", "17", "donner_age")
tester_valeur_unique("age_18_accepte_attendu", "age", "18", "donner_age")
tester_valeur_unique("age_100_accepte_attendu", "age", "100", "donner_age")
tester_valeur_unique("age_101_refuse_attendu", "age", "101", "donner_age")

# ============================================================
# TESTS SUR LE REVENU
# ============================================================

tester_valeur_unique("revenu_0_accepte_attendu", "revenu", "0", "donner_revenu")
tester_valeur_unique("revenu_negatif_refuse_attendu", "revenu", "-500", "donner_revenu")

# ============================================================
# TESTS SUR LE MONTANT DEMANDÉ
# ============================================================

tester_valeur_unique("montant_0_refuse_attendu", "montant_demande", "0", "donner_montant")
tester_valeur_unique("montant_1_accepte_attendu", "montant_demande", "1", "donner_montant")

# ============================================================
# TESTS SUR LES CHARGES
# ============================================================

tester_valeur_unique("charges_0_accepte_attendu", "charges", "0", "donner_charges")
tester_valeur_unique("charges_negatif_refuse_attendu", "charges", "-100", "donner_charges")