from ollama import chat

SYSTEM_PROMPT = (
    "Tu es un assistant conversationnel de Taysir Microfinance en Tunisie. "
    "Tu réponds uniquement en français, de façon claire et concise. "
    "CONTEXTE AUTORISE (les seules informations que tu as le droit d'utiliser) : "
    "Taysir Microfinance a été créée en 2013. Elle propose des services de "
    "microfinance en Tunisie. Le chatbot est destiné à la qualification "
    "initiale des prospects. "
    "REGLE ABSOLUE : si la réponse à la question n'est pas ECRITE MOT POUR MOT "
    "dans le CONTEXTE AUTORISE ci-dessus, tu dois répondre UNIQUEMENT : "
    "\"Je ne dispose pas de cette information. Elle doit être confirmée auprès "
    "de Taysir Microfinance.\" "
    "Ne donne JAMAIS de liste, d'exemple ou de supposition qui ne provient pas "
    "du contexte, même si le sujet te semble familier."
)

FALLBACK_PHRASE = "Je ne dispose pas de cette information"

def nettoyer_reponse(answer: str) -> str:
    """Si le modèle a hallucine puis ajoute la phrase de repli,
    on ne garde QUE la phrase de repli."""
    if FALLBACK_PHRASE in answer:
        index = answer.find(FALLBACK_PHRASE)
        return answer[index:].strip()
    return answer.strip()

questions = [
    "En quelle année Taysir a-t-elle été créée ?",
    "Quels documents faut-il pour faire une demande de financement ?",
    "Quel est le taux d'intérêt applique ?",
    "Est-ce que Taysir propose des prêts pour les etudiants ?",
]

for q in questions:
    print(f"\n=== QUESTION : {q} ===")
    response = chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "user", "content": "(Rappel : réponds uniquement à partir du contexte autorisé, sinon dis que tu ne sais pas.)"}
        ],
        think=False,
        options={"temperature": 0.2}
    )
    brute = response.message.content.strip()
    finale = nettoyer_reponse(brute)
    print("REPONSE BRUTE  :", brute.replace("\n", " | "))
    print("REPONSE FINALE :", finale)