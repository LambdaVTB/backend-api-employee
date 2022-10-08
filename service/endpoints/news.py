from uuid import UUID
from pytz import timezone
from datetime import datetime
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from service.utils.auth import get_current_user
from service.exceptions.common import ForbiddenException
from service.schemas.common import SuccessfullResponse
from service.schemas.news import NewsOut
from migrations.connection.session import get_session
from service.services.auth import add_new_user, get_user
from service.services.news import get_news_for_user, get_recomendations, click_news

news_router = APIRouter(tags=["Функции для новостей"])


@news_router.post("/news", response_model=SuccessfullResponse)
async def interact_with_news(
    id: UUID = Body(..., description='Идентификатор новости'),
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user = await get_user(login, session)
    await click_news(user, id, session)
    return SuccessfullResponse()

@news_router.get("/news", response_model=list[NewsOut])
async def get_news(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    news = await get_news_for_user(user,session)
    return [NewsOut(
        url=el.url,
        summary=el.summary,
        tags=[],
        created_at=el.created_at,
        id = el.id
    ) for el in news]

@news_router.get("/news/personalized", response_model=list[dict])
async def get_personalized_news(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    news = await get_recomendations(user,session)
    return news

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
