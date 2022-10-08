from pytz import timezone
from datetime import datetime
from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import get_current_user
from service.exceptions.common import ForbiddenException 
from service.schemas.news import NewsOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user 

news_router = APIRouter(tags=["Функции для новостей"])


@news_router.get("/news", response_model=list[NewsOut])
async def get_news(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    return [NewsOut(
        url="http:\\google.com",
        summary="Краткая выжимка",
        tags=["Генеральный директор",],
        created_at = datetime.now(timezone("UTC"))
    )]

@news_router.get("/news/personalized", response_model=list[NewsOut])
async def get_personalized_news(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    return [NewsOut(
        url="http:\\google.com",
        summary="Краткая выжимка",
        tags=["Генеральный директор",],
        created_at = datetime.now(timezone("UTC"))
    )]

@news_router.get("/news/search", response_model=list[NewsOut])
async def search_news(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    return [NewsOut(
        url="http:\\google.com",
        summary="Краткая выжимка",
        tags=["Генеральный директор",],
        created_at = datetime.now(timezone("UTC"))
    )]
