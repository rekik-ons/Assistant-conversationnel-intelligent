from pydantic import BaseModel
from typing import Optional


class ProspectCreate(BaseModel):

    nom: str
    prenom: str
    telephone: str
    age: int
    profession: str
    revenu: float
    charges: float
    montant_demande: float
    zone_geographique: str

    statut_conseiller: str = "non_traite"


class ProspectUpdate(BaseModel):

    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    age: Optional[int] = None
    profession: Optional[str] = None
    revenu: Optional[float] = None
    charges: Optional[float] = None
    montant_demande: Optional[float] = None
    zone_geographique: Optional[str] = None
    statut_conseiller: Optional[str] = None