from app.database import SessionLocal
from app.models.conversation import ConversationModel
from app.models.message import MessageModel


# ==========================================================
# DONNÉES DE TEST
# ==========================================================

TESTS = {

    "test-01": {
        "nom": "Ben Salem",
        "prenom": "Ahmed",
        "telephone": "22123456",
        "age": 35,
        "profession": "Commercant",
        "revenu": 1500,
        "montant_demande": 5000,
        "charges": 500,
        "capacite_remboursement": 1000,
        "zone_geographique": "Tunis",
        "etape": "fin",
    },

    "test-02": {
        "nom": "Jlassi",
        "prenom": "Mariem",
        "telephone": "27563489",
        "age": 27,
        "profession": "Coiffeuse",
        "revenu": 1000,
        "montant_demande": 7000,
        "charges": 300,
        "capacite_remboursement": 700,
        "zone_geographique": "Sousse",
        "etape": "fin",
    },

    "test-03": {
        "nom": "Guedri",
        "prenom": "Salma",
        "telephone": "20123456",
        "age": 20,
        "profession": "Ouvrier",
        "revenu": 500,
        "montant_demande": 15000,
        "charges": 300,
        "capacite_remboursement": 200,
        "zone_geographique": "Tunis",
        "etape": "fin",
    },

    "test-04": {
        "nom": "Ben Amor",
        "prenom": "Ines",
        "telephone": "31874562",
        "age": 31,
        "profession": "Vendeuse",
        "revenu": 1200,
        "montant_demande": 7000,
        "charges": 400,
        "capacite_remboursement": 800,
        "zone_geographique": "Ariana",
        "etape": "fin",
    },

    "test-05": {
        "nom": "Cherif",
        "prenom": "Amira",
        "telephone": "98451263",
        "age": 34,
        "profession": "Couturiere",
        "revenu": 1200,
        "montant_demande": 5000,
        "charges": 300,
        "capacite_remboursement": 900,
        "zone_geographique": "Monastir",
        "etape": "fin",
    },

    "test-06": {
        "nom": "Brahmi",
        "prenom": "Karim",
        "telephone": "25123456",
        "age": 25,
        "profession": "Ouvrier",
        "revenu": 600,
        "montant_demande": 12000,
        "charges": 300,
        "capacite_remboursement": 300,
        "zone_geographique": "Sfax",
        "etape": "fin",
    },

    "test-07": {
        "nom": "Trabelsi",
        "prenom": "Yassine",
        "telephone": "98456732",
        "age": 41,
        "profession": "Chauffeur",
        "revenu": 1500,
        "montant_demande": 5000,
        "charges": 600,
        "capacite_remboursement": 900,
        "zone_geographique": "Ben Arous",
        "etape": "fin",
    },

    "test-08": {
        "nom": "Khelifi",
        "prenom": "Walid",
        "telephone": "96432157",
        "age": 39,
        "profession": "Ouvrier",
        "revenu": 900,
        "montant_demande": 10000,
        "charges": 400,
        "capacite_remboursement": 500,
        "zone_geographique": "Manouba",
        "etape": "fin",
    },

    "test-09": {
        "nom": "Ayari",
        "prenom": "Noura",
        "telephone": "93214567",
        "age": 30,
        "profession": "Commerçante",
        "revenu": 900,
        "montant_demande": 5000,
        "charges": 300,
        "capacite_remboursement": 600,
        "zone_geographique": "Sousse",
        "etape": "fin",
    },

    "test-10": {
        "nom": "Gharbi",
        "prenom": "Sami",
        "telephone": "52345678",
        "age": 38,
        "profession": "Electricien",
        "revenu": 1500,
        "montant_demande": 8000,
        "charges": 500,
        "capacite_remboursement": 1000,
        "zone_geographique": "Sfax",
        "etape": "fin",
    },

    "test-11": {
        "nom": "Mansouri",
        "prenom": "Hatem",
        "telephone": "55234178",
        "age": 52,
        "profession": "Ouvrier",
        "revenu": 650,
        "montant_demande": 9000,
        "charges": 300,
        "capacite_remboursement": 350,
        "zone_geographique": "Monastir",
        "etape": "fin",
    },

    "test-12": {
        "nom": "Chaabane",
        "prenom": "Fares",
        "telephone": "54123678",
        "age": 40,
        "profession": "Artisan",
        "revenu": 900,
        "montant_demande": 7000,
        "charges": 350,
        "capacite_remboursement": 550,
        "zone_geographique": "Ariana",
        "etape": "fin",
    },

    "test-13": {
        "nom": "Saidi",
        "prenom": "Nabil",
        "telephone": "27345681",
        "age": 45,
        "profession": "Agriculteur",
        "revenu": 800,
        "montant_demande": 10000,
        "charges": 300,
        "capacite_remboursement": 500,
        "zone_geographique": "Sousse",
        "etape": "fin",
    },

    # ======================================================
    # CONVERSATION INTERROMPUE 1
    # ======================================================

    "test-14": {
        "nom": "Mejri",
        "prenom": "Karim",
        "telephone": "50123456",
        "age": 28,
        "profession": "Ouvrier",
        "revenu": 700,
        "montant_demande": 6000,
        "etape": "revenu",
    },

    # ======================================================
    # CONVERSATION INTERROMPUE 2
    # ======================================================

    "test-15": {
        "nom": "Ben Youssef",
        "prenom": "Mourad",
        "telephone": "55123456",
        "age": 32,
        "profession": "Artisan",
        "revenu": 900,
        "montant_demande": 8000,
        "etape": "charges",
    },
}


# ==========================================================
# FONCTIONS
# ==========================================================

def ajouter_message(db, session_id, role, contenu):
    db.add(
        MessageModel(
            session_id=session_id,
            role=role,
            contenu=contenu
        )
    )


def conversation_complete(db, session_id, data):

    ajouter_message(
        db,
        session_id,
        "user",
        "bonjour"
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Bonjour, bienvenue chez Taysir Microfinance. Quel est votre nom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["nom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Merci. Quel est votre prénom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["prenom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre numéro de téléphone ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["telephone"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre âge ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["age"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quelle est votre situation professionnelle ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["profession"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre revenu mensuel ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["revenu"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel montant de financement souhaitez-vous ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["montant_demande"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quelles sont vos charges mensuelles approximatives ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["charges"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Dans quelle zone géographique habitez-vous ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["zone_geographique"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Merci pour vos informations. Votre profil a été analysé."
    )


def conversation_interrompue_revenu(
    db,
    session_id,
    data
):

    ajouter_message(
        db,
        session_id,
        "user",
        "bonjour"
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Bonjour, bienvenue chez Taysir Microfinance. Quel est votre nom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["nom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Merci. Quel est votre prénom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["prenom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre numéro de téléphone ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["telephone"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre âge ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["age"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quelle est votre situation professionnelle ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["profession"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre revenu mensuel ?"
    )


def conversation_interrompue_charges(
    db,
    session_id,
    data
):

    ajouter_message(
        db,
        session_id,
        "user",
        "bonjour"
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Bonjour, bienvenue chez Taysir Microfinance. Quel est votre nom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["nom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Merci. Quel est votre prénom ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["prenom"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre numéro de téléphone ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["telephone"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre âge ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["age"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quelle est votre situation professionnelle ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        data["profession"]
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel est votre revenu mensuel ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["revenu"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quel montant de financement souhaitez-vous ?"
    )

    ajouter_message(
        db,
        session_id,
        "user",
        str(data["montant_demande"])
    )

    ajouter_message(
        db,
        session_id,
        "assistant",
        "Quelles sont vos charges mensuelles approximatives ?"
    )


# ==========================================================
# SCRIPT PRINCIPAL
# ==========================================================

db = SessionLocal()

try:

    # ------------------------------------------------------
    # SUPPRESSION DES ANCIENNES CONVERSATIONS DE TEST
    # ------------------------------------------------------

    test_ids = list(TESTS.keys())

    db.query(MessageModel).filter(
        MessageModel.session_id.in_(test_ids)
    ).delete(
        synchronize_session=False
    )

    db.query(ConversationModel).filter(
        ConversationModel.session_id.in_(test_ids)
    ).delete(
        synchronize_session=False
    )

    db.commit()


    # ------------------------------------------------------
    # CRÉATION DES CONVERSATIONS
    # ------------------------------------------------------

    for session_id, data in TESTS.items():

        conversation_data = {
            "nom": data["nom"],
            "prenom": data["prenom"],
            "telephone": data["telephone"],
            "age": data["age"],
            "profession": data["profession"],
            "revenu": data["revenu"],
            "montant_demande": data["montant_demande"],
            "session_id": session_id
        }

        conversation = ConversationModel(
            session_id=session_id,
            etape=data["etape"],
            data=conversation_data
        )

        db.add(conversation)

        # --------------------------------------------------
        # 13 CONVERSATIONS TERMINÉES
        # --------------------------------------------------

        if session_id not in ["test-14", "test-15"]:

            conversation_complete(
                db,
                session_id,
                data
            )

        # --------------------------------------------------
        # TEST-14 : INTERRUPTION À L'ÉTAPE REVENU
        # --------------------------------------------------

        elif session_id == "test-14":

            conversation_interrompue_revenu(
                db,
                session_id,
                data
            )

        # --------------------------------------------------
        # TEST-15 : INTERRUPTION À L'ÉTAPE CHARGES
        # --------------------------------------------------

        elif session_id == "test-15":

            conversation_interrompue_charges(
                db,
                session_id,
                data
            )


    db.commit()

    print()
    print("=" * 60)
    print("JEU DE TEST CRÉÉ AVEC SUCCÈS")
    print("=" * 60)

    print()

    print("Conversations terminées :")

    for i in range(1, 14):
        print(f"  test-{i:02d} → fin")

    print()

    print("Conversations interrompues :")

    print("  test-14 → revenu")
    print("  test-15 → charges")

    print()

    print("Total : 15 conversations")

except Exception as e:

    db.rollback()

    print(
        "Erreur lors de la création :",
        e
    )

finally:

    db.close()