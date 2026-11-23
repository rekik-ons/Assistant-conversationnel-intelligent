from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.utilisateur import UtilisateurModel

router = APIRouter(prefix="/auth", tags=["Authentification"])


class LoginData(BaseModel):
    login: str
    mot_de_passe: str


@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(UtilisateurModel).filter(
        UtilisateurModel.login == data.login,
        UtilisateurModel.mot_de_passe == data.mot_de_passe,
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")

    return {"id": user.id, "login": user.login, "role": user.role}