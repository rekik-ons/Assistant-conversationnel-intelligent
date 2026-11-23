from fastapi import APIRouter, HTTPException

from app.schemas.conversation import MessageRequest
from app.services.conversation import Conversation
from app.database import SessionLocal

from app.models.conversation import ConversationModel
from app.models.message import MessageModel
from app.models.prospect import ProspectModel


router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"]
)



conversations = {}



def save_message(session_id, role, contenu):

    db = SessionLocal()

    try:

        message = MessageModel(
            session_id=session_id,
            role=role,
            contenu=contenu
        )

        db.add(message)
        db.commit()

    finally:

        db.close()



@router.get("/terminees")
def get_conversations_terminees(
    qualification: str = None
):

    db = SessionLocal()

    try:

        conversations_terminees = db.query(
            ConversationModel
        ).filter(
            ConversationModel.etape == "fin"
        ).all()

        result = []

        for conversation in conversations_terminees:

            prospect = db.query(
                ProspectModel
            ).filter(
                ProspectModel.session_id
                == conversation.session_id
            ).first()

           
            if qualification:

                if not prospect:

                    continue

                qualification_recherchee = (
                    qualification.lower().strip()
                )

                qualification_prospect = (
                    prospect.qualification.lower()
                    if prospect.qualification
                    else ""
                )

                if qualification_recherchee not in qualification_prospect:

                    continue

           
            result.append({

                "session_id": conversation.session_id,

                "etape": conversation.etape,

                "prospect": {

                    "nom": (
                        prospect.nom
                        if prospect else None
                    ),

                    "prenom": (
                        prospect.prenom
                        if prospect else None
                    ),

                    "telephone": (
                        prospect.telephone
                        if prospect else None
                    ),

                    "age": (
                        prospect.age
                        if prospect else None
                    ),

                    "profession": (
                        prospect.profession
                        if prospect else None
                    ),

                    "revenu": (
                        prospect.revenu
                        if prospect else None
                    ),

                    "charges": (
                        prospect.charges
                        if prospect else None
                    ),

                    "capacite_remboursement": (
                        prospect.capacite_remboursement
                        if prospect else None
                    ),

                    "montant_demande": (
                        prospect.montant_demande
                        if prospect else None
                    ),

                    "zone_geographique": (
                        prospect.zone_geographique
                        if prospect else None
                    ),

                    "score": (
                        prospect.score
                        if prospect else None
                    ),

                    "qualification": (
                        prospect.qualification
                        if prospect else None
                    ),

                    "eligibilite": (
                        prospect.eligibilite
                        if prospect else None
                    )
                }
            })

        return result

    finally:

        db.close()



@router.get("/{session_id}")
def get_conversation(session_id: str):

    db = SessionLocal()

    try:

        conversation = db.query(
            ConversationModel
        ).filter(
            ConversationModel.session_id == session_id
        ).first()

        
        if not conversation:

            raise HTTPException(
                status_code=404,
                detail="Conversation introuvable"
            )

        return {

            "session_id": conversation.session_id,

            "etape": conversation.etape,

            "data": conversation.data
        }

    finally:

        db.close()



@router.post("/message/{session_id}")
def send_message(
    session_id: str,
    data: MessageRequest
):

    
    if session_id not in conversations:

        conversations[session_id] = Conversation(
            session_id
        )

    conversation = conversations[session_id]

    
    save_message(
        session_id,
        "user",
        data.message
    )

    
    response = conversation.traiter_message(
        data.message
    )

    
    if isinstance(response, dict):

        response_text = response.get(
            "message",
            ""
        )

    else:

        response_text = response

    
    save_message(
        session_id,
        "assistant",
        response_text
    )

   
    return {

        "session_id": session_id,

        "etape": conversation.etape,

        "response": response
    }



@router.delete("/{session_id}")
def delete_conversation(session_id: str):

    db = SessionLocal()

    try:

        
        conversation = db.query(
            ConversationModel
        ).filter(
            ConversationModel.session_id
            == session_id
        ).first()

       
        messages_exist = db.query(
            MessageModel
        ).filter(
            MessageModel.session_id
            == session_id
        ).first()

       
        if not conversation and not messages_exist:

            raise HTTPException(
                status_code=404,
                detail="Conversation introuvable"
            )

        
        deleted_messages = db.query(
            MessageModel
        ).filter(
            MessageModel.session_id
            == session_id
        ).delete(
            synchronize_session=False
        )

        
        if conversation:

            db.delete(conversation)

        db.commit()

        
        if session_id in conversations:

            del conversations[session_id]

        return {

            "message":
                "Conversation et historique supprimés avec succès",

            "session_id":
                session_id,

            "messages_supprimes":
                deleted_messages
        }

    finally:

        db.close()



@router.get("/{session_id}/messages")
def get_messages(session_id: str):

    db = SessionLocal()

    try:

        conversation = db.query(
            ConversationModel
        ).filter(
            ConversationModel.session_id
            == session_id
        ).first()

        if not conversation:

            raise HTTPException(
                status_code=404,
                detail="Conversation introuvable"
            )

        
        messages = db.query(
            MessageModel
        ).filter(
            MessageModel.session_id
            == session_id
        ).order_by(
            MessageModel.date_creation
        ).all()

        
        result = []

        for message in messages:

            result.append({

                "id": message.id,

                "session_id":
                    message.session_id,

                "role":
                    message.role,

                "contenu":
                    message.contenu,

                "date_creation":
                    message.date_creation
            })

        return result

    finally:

        db.close()