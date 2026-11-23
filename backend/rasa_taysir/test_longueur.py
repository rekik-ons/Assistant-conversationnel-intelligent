import requests
import json

texte_long = "a" * 400  # 400 caractères, garanti > 300

payload = {
    "next_action": "action_llm_reponse",
    "sender_id": "test-longueur",
    "tracker": {
        "sender_id": "test-longueur",
        "slots": {},
        "latest_message": {
            "text": texte_long,
            "intent": {"name": "nlu_fallback", "confidence": 1.0},
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
    timeout=60
)

print("STATUS :", response.status_code)
print("REPONSE :", json.dumps(response.json(), indent=2, ensure_ascii=False))