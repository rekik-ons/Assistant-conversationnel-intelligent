import requests

payload = {
    "next_action": "action_llm_reponse",
    "sender_id": "test-ollama-down",
    "tracker": {
        "sender_id": "test-ollama-down",
        "slots": {},
        "latest_message": {
            "text": "En quelle année Taysir a-t-elle été créée ?",
            "intent": {"name": "question_generale", "confidence": 1.0},
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
print("REPONSE :", response.json())