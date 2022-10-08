from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, select
from migrations.models.users import Users
from migrations.models.news import News
from migrations.models.tags_jobs import TagsJobs
from migrations.models.tags_news import TagsNews

async def get_news_for_user(user: Users, session: AsyncSession) -> list[News]:
    query = select(News).join(
        TagsNews, TagsNews.news_id == News.id
    ).join(
        TagsJobs, TagsJobs.tag_id == TagsNews.tag_id
    ).where(
        TagsJobs.job_id == user.job_id
    ).order_by(
        desc(News.created_at)
    ).limit(20)
    data = (await session.execute(query)).scalars().all()
    return data
