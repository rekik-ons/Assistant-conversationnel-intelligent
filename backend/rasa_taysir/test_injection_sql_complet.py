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
    ("Robert'); DROP TABLE prospects;--", "donner_nom"),
    ("Test", "donner_prenom"),
    ("26123456", "donner_telephone"),
    ("30", "donner_age"),
    ("<script>alert(1)</script>", "donner_profession"),
    ("1000", "donner_revenu"),
    ("2000", "donner_montant"),
    ("300", "donner_charges"),
    ("Tunis'; DELETE FROM prospects WHERE '1'='1", "donner_zone"),
]

slots = {"etat": "nom"}
for texte, intent in reponses:
    resultat = envoyer_message("test-sql-injection", texte, intent, slots)
    for e in resultat.get("events", []):
        if e.get("event") == "slot":
            slots[e["name"]] = e["value"]
    messages = [r["text"] for r in resultat.get("responses", [])]
    print(f"'{texte[:40]}...' -> {messages}")

print("\nSlots finaux :", slots)

# Vérifier que la table existe toujours et contient bien cette entrée
print("\n--- Vérification post-injection ---")
r = requests.get("http://127.0.0.1:8000/prospects/", timeout=10)
print("STATUS API prospects/ :", r.status_code)
data = r.json()
liste_prospects = data.get("value", []) if isinstance(data, dict) else data
nb_prospects = len(liste_prospects)
noms_presents = [p.get("nom", "") for p in liste_prospects[-3:]]
print("Derniers noms en base :", noms_presents)
print("Nombre de prospects encore présents :", nb_prospects)