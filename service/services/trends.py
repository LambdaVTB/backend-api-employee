from sqlalchemy import select, and_, desc
from migrations.models.users import Users
from migrations.models.news import News
from migrations.models.tags_news import TagsNews
from migrations.models.tags_jobs import TagsJobs
from sqlalchemy.ext.asyncio import AsyncSession
from migrations.enums.news_types import NewsTypes


async def get_trends_for_user(user: Users, session: AsyncSession) -> list[News]:
    query = select(News).join(
        TagsNews, News.id == TagsNews.news_id
    ).join(
        TagsJobs, TagsJobs.tag_id == TagsNews.tag_id
    ).where(
        and_(
            TagsJobs.job_id == user.job_id,
            News.news_type == NewsTypes.TREND
        )
    ).order_by(desc(News.created_at))
    result = (await session.execute(query)).scalars().all()
    return result
