from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from service.utils.auth import create_access_token, get_password_hash, verify_password
from service.exceptions.common import ForbiddenException 
from service.utils.formatter import format_model
from service.schemas.common import SuccessfullResponse, TokenOut
from service.migrations.connection import get_session

auth_router = APIRouter(tags=["Функции пользователей"])


@auth_router.post("/user/register", response_model=SuccessfullResponse)
async def user_register(
    request: OAuth2PasswordRequestForm = Depends(),
) -> SuccessfullResponse:
    request.password = get_password_hash(request.password)
    add_new_user(request.login, request.password)
    return SuccessfullResponse()


@auth_router.post("/user/login", response_model=TokenOut)
async def user_login(request: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)) -> TokenOut:
    user = await get_user(request.username, session)
    if not verify_password(request.password, user.hashed_password):
        raise ForbiddenException("Wrong password")
    access_token = create_access_token(data={"sub": user.username})
    token = TokenOut(access_token=access_token, token_type="bearer")
    return token

