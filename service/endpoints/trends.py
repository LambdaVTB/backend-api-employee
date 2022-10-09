
from uuid import UUID
from pytz import timezone
from datetime import datetime
from fastapi import APIRouter, Form, Body, Query
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
from service.services.trends import get_trends_for_user

trends_router = APIRouter(tags=["Функции для трендов"])


@trends_router.get("/trends", response_model=list[dict])
async def get_trends(
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> list[NewsOut]:
    user = await get_user(login, session)
    news = await get_trends_for_user(user,session)
    return news

@trends_router.get("/trends/tags", response_model=list[dict])
async def get_trends_by_tags(
    tags: list[str] = Query(...),
    login: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user = await get_user(login, session)
    # news = await get_trends_by_tags()
