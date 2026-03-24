from fastapi import APIRouter, Depends
from controllers.auth import login, me
from schemas.usuario import ResponseUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login_route(resultado=Depends(login)):
    return resultado


@router.get("/me", response_model=ResponseUser)
def me_route(resultado=Depends(me)):
    return resultado
