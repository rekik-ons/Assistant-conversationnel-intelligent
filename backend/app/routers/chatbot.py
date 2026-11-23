from fastapi import APIRouter
from app.services.conversation import Conversation

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)

conversations = {}


@router.post("/chat/{session_id}")
def chat(session_id: str, message: str):

    
    if session_id not in conversations:
        conversations[session_id] = Conversation(session_id)

    conversation = conversations[session_id]

    response = conversation.traiter_message(message)

    return {
        "session_id": session_id,
        "message_utilisateur": message,
        "reponse_assistant": response,
        "etape": conversation.etape,
        "donnees_prospect": conversation.data
    }