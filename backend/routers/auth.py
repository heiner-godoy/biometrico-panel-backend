from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth import login, me
from schemas.usuario import ResponseUser
from sqlalchemy.orm import Session
from core.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login_route(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await login(form=form, db=db)

@router.get("/me", response_model=ResponseUser)
def me_route(resultado=Depends(me)):
    return resultado