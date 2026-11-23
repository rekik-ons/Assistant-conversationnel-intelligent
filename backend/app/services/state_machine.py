from enum import Enum


class ConversationState(str, Enum):

    NOM = "nom"
    PRENOM = "prenom"
    TELEPHONE = "telephone"
    AGE = "age"
    PROFESSION = "profession"
    REVENU = "revenu"
    MONTANT_DEMANDE = "montant_demande"
    CHARGES = "charges"
    ZONE_GEOGRAPHIQUE = "zone_geographique"
    FIN = "fin"


NEXT_STATE = {

    ConversationState.NOM:
        ConversationState.PRENOM,

    ConversationState.PRENOM:
        ConversationState.TELEPHONE,

    ConversationState.TELEPHONE:
        ConversationState.AGE,

    ConversationState.AGE:
        ConversationState.PROFESSION,

    ConversationState.PROFESSION:
        ConversationState.REVENU,

    ConversationState.REVENU:
        ConversationState.MONTANT_DEMANDE,

    ConversationState.MONTANT_DEMANDE:
        ConversationState.CHARGES,

    ConversationState.CHARGES:
        ConversationState.ZONE_GEOGRAPHIQUE,

    ConversationState.ZONE_GEOGRAPHIQUE:
        ConversationState.FIN,
}


EXPECTED_INTENT = {

    ConversationState.NOM:
        "donner_nom",

    ConversationState.PRENOM:
        "donner_prenom",

    ConversationState.TELEPHONE:
        "donner_telephone",

    ConversationState.AGE:
        "donner_age",

    ConversationState.PROFESSION:
        "donner_profession",

    ConversationState.REVENU:
        "donner_revenu",

    ConversationState.MONTANT_DEMANDE:
        "donner_montant",

    ConversationState.CHARGES:
        "donner_charges",

    ConversationState.ZONE_GEOGRAPHIQUE:
        "donner_zone",
}


def verifier_transition(etat, intent):

    return EXPECTED_INTENT.get(etat) == intent


def etat_suivant(etat):

    return NEXT_STATE.get(
        etat,
        ConversationState.FIN
    )