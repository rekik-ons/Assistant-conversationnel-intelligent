import requests
import json

ACTION_SERVER = "http://localhost:5055/webhook"


def envoyer_message(sender_id, texte, intent, slots_actuels):
    """Envoie un message à action_traiter_reponse et retourne les nouveaux events."""
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


def derouler_parcours(sender_id, reponses):
    """
    Déroule un parcours complet de qualification.
    reponses = liste de (texte, intent) dans l'ordre nom->prenom->...->zone
    """
    slots = {"etat": "nom"}
    dernier_resultat = None

    for texte, intent in reponses:
        resultat = envoyer_message(sender_id, texte, intent, slots)
        dernier_resultat = resultat

        # Mettre à jour les slots avec les nouveaux events
        for event in resultat.get("events", []):
            if event.get("event") == "slot":
                slots[event["name"]] = event["value"]

    return slots, dernier_resultat


# ============================================================
# PROFIL 1 : Revenu élevé, charges faibles -> attendu "chaud"
# ============================================================

reponses_1 = [
    ("Profil1", "donner_nom"),
    ("Test", "donner_prenom"),
    ("21111111", "donner_telephone"),
    ("35", "donner_age"),
    ("Ingenieur", "donner_profession"),
    ("3000", "donner_revenu"),
    ("5000", "donner_montant"),
    ("500", "donner_charges"),
    ("Tunis", "donner_zone"),
]

slots_1, _ = derouler_parcours("test-calc-1", reponses_1)
print("=== PROFIL 1 (revenu eleve, charges faibles) ===")
print("Capacité :", slots_1.get("capacite_remboursement"))
print("Score :", slots_1.get("score"))
print("Qualification :", slots_1.get("qualification"))
print("Éligibilité :", slots_1.get("eligibilite"))
print()


# ============================================================
# PROFIL 2 : Revenu faible, charges élevées -> attendu "froid"/"non éligible"
# ============================================================

reponses_2 = [
    ("Profil2", "donner_nom"),
    ("Test", "donner_prenom"),
    ("24222222", "donner_telephone"),
    ("40", "donner_age"),
    ("Ouvrier", "donner_profession"),
    ("600", "donner_revenu"),
    ("5000", "donner_montant"),
    ("700", "donner_charges"),
    ("Sfax", "donner_zone"),
]

slots_2, _ = derouler_parcours("test-calc-2", reponses_2)
print("=== PROFIL 2 (revenu faible, charges > revenu) ===")
print("Capacité :", slots_2.get("capacite_remboursement"))
print("Score :", slots_2.get("score"))
print("Qualification :", slots_2.get("qualification"))
print("Éligibilité :", slots_2.get("eligibilite"))
print()


# ============================================================
# PROFIL 3 : Montant demandé disproportionné -> score réduit
# ============================================================

reponses_3 = [
    ("Profil3", "donner_nom"),
    ("Test", "donner_prenom"),
    ("23333333", "donner_telephone"),
    ("30", "donner_age"),
    ("Commercant", "donner_profession"),
    ("2000", "donner_revenu"),
    ("50000", "donner_montant"),
    ("500", "donner_charges"),
    ("Sousse", "donner_zone"),
]

slots_3, _ = derouler_parcours("test-calc-3", reponses_3)
print("=== PROFIL 3 (montant tres eleve vs capacite) ===")
print("Capacité :", slots_3.get("capacite_remboursement"))
print("Score :", slots_3.get("score"))
print("Qualification :", slots_3.get("qualification"))
print("Éligibilité :", slots_3.get("eligibilite"))