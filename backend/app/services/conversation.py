import math
import re

from app.services.prospect_service import save_prospect
from app.services.scoring import calculate_score

from app.database import SessionLocal
from app.models.conversation import ConversationModel



def nom_valide(text):
    if not text or not text.strip():
        return False

    text = text.strip()

    
    if len(text.split()) > 3:
        return False

    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+", text))



QUESTIONS_ETAPES = {
    "accueil": "Quel est votre nom ?",
    "nom": "Quel est votre nom ?",
    "prenom": "Quel est votre prénom ?",
    "telephone": "Quel est votre numéro de téléphone ?",
    "age": "Quel est votre âge ?",
    "profession": "Quelle est votre situation professionnelle ?",
    "revenu": "Quel est votre revenu mensuel ?",
    "montant_demande": "Quel montant de financement souhaitez-vous ?",
    "charges": "Quelles sont vos charges mensuelles approximatives ?",
    "zone_geographique": "Dans quelle zone géographique habitez-vous ?",
}

MOTS_INTERROGATIFS = (
    "quel", "quelle", "quels", "quelles", "comment", "combien",
    "pourquoi", "quand", "où", "ou ", "est-ce", "est ce", "puis-je",
    "peut-on", "y a-t-il", "qu'est", "qui ", "cest qui", "c'est qui",
    "c est qui", "que ", "quoi",
)

FAQ = [
    (["trouve", "adresse", "localisation", "ou est", "où est", "agence"],
     "Vous pouvez contacter Taysir afin de connaître l'agence la plus proche de votre zone."),
    (["condition", "éligib", "eligib"],
     "Les conditions dépendent du produit de financement et du profil du demandeur."),
    (["document", "pièce", "piece"],
     "Les documents nécessaires dépendent du type de financement et de la situation du demandeur."),
    (["montant", "somme"],
     "Le montant dépend du profil du demandeur, de son besoin et de sa capacité de remboursement."),
    (["rembours", "mensualit"],
     "Le remboursement s'effectue selon un échéancier défini en fonction des conditions du financement."),
    (["délai", "delai", "temps"],
     "Le délai de traitement dépend de la demande et de la vérification des informations fournies."),
    (["contact", "téléphone", "telephone"],
     "Vous pouvez contacter Taysir via ses canaux de communication officiels."),
    (["frais", "coût", "cout", "commission"],
     "Les frais dépendent du produit de financement et des conditions applicables."),
    (["taysir", "qui êtes", "qui etes", "qui est", "cest qui", "c'est qui"],
     "Taysir Microfinance, créée en 2013, propose des services de microfinance en Tunisie."),
    (["crédit", "credit", "prêt", "pret", "financement", "microfinance"],
     "Taysir propose différents types de financements adaptés aux besoins des clients."),
]


def est_question_faq(text):
    t = text.lower().strip()
    return "?" in t or t.startswith(MOTS_INTERROGATIFS)


def contient_mot_faq(text):
    t = text.lower()
    return any(m in t for mots, _ in FAQ for m in mots)


def reponse_valide_pour_etape(etape, message):
    """True si le message ressemble à une vraie réponse à l'étape."""
    if etape in ("nom", "prenom"):
        return nom_valide(message)
    if etape == "telephone":
        return message.isdigit() and len(message) == 8
    if etape == "age":
        return message.isdigit()
    if etape in ("revenu", "montant_demande", "charges"):
        try:
            float(message)
            return True
        except ValueError:
            return False
    return True  


def repondre_faq(text):
    t = text.lower()
    for mots_cles, reponse in FAQ:
        if any(mot in t for mot in mots_cles):
            return reponse
    return (
        "Je ne dispose pas de cette information. "
        "Elle doit être confirmée auprès de Taysir Microfinance."
    )


class Conversation:

    def __init__(self, session_id):

        self.session_id = session_id
        self.data = {}
        self.terminee = False

        db = SessionLocal()

        conversation = db.query(ConversationModel).filter(
            ConversationModel.session_id == session_id
        ).first()

        if conversation:

            self.etape = conversation.etape
            self.data = conversation.data or {}

            if self.etape == "fin":
                self.terminee = True

        else:

            self.etape = "accueil"

            conversation = ConversationModel(
                session_id=self.session_id,
                etape=self.etape,
                data=self.data
            )

            db.add(conversation)
            db.commit()

        db.close()


    def sauvegarder_etape(self):

        db = SessionLocal()

        conversation = db.query(ConversationModel).filter(
            ConversationModel.session_id == self.session_id
        ).first()

        if conversation:

            conversation.etape = self.etape
            conversation.data = self.data

        else:

            conversation = ConversationModel(
                session_id=self.session_id,
                etape=self.etape,
                data=self.data
            )

            db.add(conversation)

        db.commit()
        db.close()


    def traiter_message(self, message):

        message = str(message).strip()

        if self.etape in QUESTIONS_ETAPES:

            est_question = est_question_faq(message)

            hors_sujet = (
                not reponse_valide_pour_etape(self.etape, message)
                and contient_mot_faq(message)
            )

            if est_question or hors_sujet:
                return (
                    f"{repondre_faq(message)}\n\n"
                    f"Pour continuer votre demande : "
                    f"{QUESTIONS_ETAPES[self.etape]}"
                )

        if self.etape == "accueil":

            self.etape = "nom"
            self.sauvegarder_etape()

            return (
                "Bonjour, bienvenue chez Taysir Microfinance. "
                "Quel est votre nom ?"
            )

        elif self.etape == "nom":

            if not message:
                return "Veuillez saisir votre nom."

            if not nom_valide(message):
                return "Merci d'entrer un nom valide (lettres uniquement)."

            self.data["nom"] = message.strip().title()

            self.etape = "prenom"
            self.sauvegarder_etape()

            return "Merci. Quel est votre prénom ?"

        elif self.etape == "prenom":

            if not message:
                return "Veuillez saisir votre prénom."

            if not nom_valide(message):
                return "Merci d'entrer un prénom valide (lettres uniquement)."

            self.data["prenom"] = message.strip().title()

            self.etape = "telephone"
            self.sauvegarder_etape()

            return "Quel est votre numéro de téléphone ?"

        elif self.etape == "telephone":

            telephone = message

            if not telephone:
                return "Veuillez saisir votre numéro de téléphone."

            if not telephone.isdigit():
                return "Veuillez saisir un numéro de téléphone valide."

            if len(telephone) != 8:
                return "Le numéro de téléphone doit contenir 8 chiffres."

            self.data["telephone"] = telephone

            self.etape = "age"
            self.sauvegarder_etape()

            return "Quel est votre âge ?"

        elif self.etape == "age":

            try:
                age = int(message)

                if age < 18 or age > 100:
                    return "Votre âge n'est pas accepté."

                self.data["age"] = age

            except ValueError:
                return "Veuillez saisir un âge valide, par exemple : 35."

            self.etape = "profession"
            self.sauvegarder_etape()

            return "Quelle est votre situation professionnelle ?"

        elif self.etape == "profession":

            self.data["profession"] = message.strip().title()
            self.etape = "revenu"
            self.sauvegarder_etape()

            return "Quel est votre revenu mensuel ?"

        elif self.etape == "revenu":

            try:
                revenu = float(message)

                if not math.isfinite(revenu):
                    raise ValueError

                if revenu <= 0:
                    return "Le revenu doit être supérieur à 0."

                self.data["revenu"] = revenu

            except ValueError:
                return "Veuillez saisir un revenu valide, par exemple : 1500."

            self.etape = "montant_demande"
            self.sauvegarder_etape()

            return "Quel montant de financement souhaitez-vous ?"

        elif self.etape == "montant_demande":

            try:
                montant = float(message)

                if not math.isfinite(montant):
                    raise ValueError

                if montant <= 0:
                    return "Veuillez saisir un montant de financement valide."

                self.data["montant_demande"] = montant

            except ValueError:
                return "Veuillez saisir un montant valide, par exemple : 5000."

            self.etape = "charges"
            self.sauvegarder_etape()

            return "Quelles sont vos charges mensuelles approximatives ?"

        elif self.etape == "charges":

            try:
                charges = float(message)

                if not math.isfinite(charges):
                    raise ValueError

                if charges < 0:
                    return "Les charges ne peuvent pas être négatives."

                self.data["charges"] = charges

            except ValueError:
                return (
                    "Veuillez saisir un montant de charges "
                    "valide, par exemple : 500."
                )

            capacite = self.data["revenu"] - self.data["charges"]
            self.data["capacite_remboursement"] = capacite

            self.etape = "zone_geographique"
            self.sauvegarder_etape()

            return "Dans quelle zone géographique habitez-vous ?"

        elif self.etape == "zone_geographique":

            zone = message

            if not zone:
                return "Veuillez saisir votre zone géographique."

            self.data["zone_geographique"] = zone.strip().title()

            result = calculate_score(self.data)

            self.data["score"] = result["score"]
            self.data["qualification"] = result["qualification"]
            self.data["capacite_remboursement"] = result["capacite_remboursement"]
            self.data["eligibilite"] = result["eligibilite"]
            self.data["session_id"] = self.session_id

            if not self.terminee:
                save_prospect(self.data)
                self.terminee = True

            self.etape = "fin"
            self.sauvegarder_etape()

            return {
                "message": (
                    "Merci pour vos informations. "
                    "Votre profil a été analysé."
                ),
                "data": {
                    "nom": self.data["nom"],
                    "prenom": self.data["prenom"],
                    "telephone": self.data["telephone"],
                    "age": self.data["age"],
                    "profession": self.data["profession"],
                    "revenu": self.data["revenu"],
                    "montant_demande": self.data["montant_demande"],
                    "charges": self.data["charges"],
                    "capacite_remboursement": self.data["capacite_remboursement"],
                    "zone_geographique": self.data["zone_geographique"],
                    "score": self.data["score"],
                    "qualification": self.data["qualification"],
                    "eligibilite": self.data["eligibilite"],
                }
            }

        elif self.etape == "fin":

            return {
                "message": "Cette conversation est terminée.",
                "data": self.data
            }

        else:

            return (
                "Une erreur est survenue dans le parcours "
                "de la conversation."
            )