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


print("========== CAS 1 : parcours interrompu puis repris avec les MÊMES slots ==========\n")

sender_id = "test-interruption-1"
slots = {"etat": "nom"}

# Début du parcours
resultat = envoyer_message(sender_id, "Dupont", "donner_nom", slots)
for e in resultat.get("events", []):
    if e.get("event") == "slot":
        slots[e["name"]] = e["value"]
print("Après 'Dupont' -> etat =", slots.get("etat"), "| messages :", [r["text"] for r in resultat.get("responses", [])])

resultat = envoyer_message(sender_id, "Jean", "donner_prenom", slots)
for e in resultat.get("events", []):
    if e.get("event") == "slot":
        slots[e["name"]] = e["value"]
print("Après 'Jean' -> etat =", slots.get("etat"), "| messages :", [r["text"] for r in resultat.get("responses", [])])

print("\n--- SIMULATION D'INTERRUPTION (l'utilisateur part) ---\n")
print("Slots au moment de l'interruption :", slots)

print("\n--- REPRISE : l'utilisateur revient et répond à la question suivante (téléphone) ---\n")
resultat = envoyer_message(sender_id, "24123456", "donner_telephone", slots)
for e in resultat.get("events", []):
    if e.get("event") == "slot":
        slots[e["name"]] = e["value"]
print("Après reprise avec '24123456' -> etat =", slots.get("etat"), "| messages :", [r["text"] for r in resultat.get("responses", [])])
print("Slots complets après reprise :", slots)


print("\n\n========== CAS 2 : nouvelle session (sender_id différent), slots vides ==========\n")

sender_id_2 = "test-interruption-2-nouvelle-session"
slots_2 = {}  # Aucun état -> simule une toute nouvelle conversation

resultat = envoyer_message(sender_id_2, "Bonjour", "greet", slots_2)
print("Réponse à 'Bonjour' sur nouvelle session :", [r["text"] for r in resultat.get("responses", [])])
print("Events reçus :", resultat.get("events", []))