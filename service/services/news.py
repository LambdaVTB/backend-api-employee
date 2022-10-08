import neo4j
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, select
from migrations.models.users import Users
from migrations.models.news import News
from migrations.models.tags_jobs import TagsJobs
from migrations.models.tags_news import TagsNews
from service.exceptions.common import BadRequest
from service.utils.graph import Graph

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

async def get_recomendations(user: Users, session: AsyncSession) -> list[News]:
    cypher = """
        match (i:Item)<-[:LIKE]-(u:User)-[:LIKE]->(i2:Item)<-[:LIKE]-(u0:User)
        where u0.identifier = $identifier
        return i, count(i.identifier)
    """
    print(user)
    result = await Graph.read(cypher, identifier=user.id)
    result.sort(key=lambda x: x['count(i.identifier)'], reverse=True)
    return result

async def click_news(user: Users, id_news: str, session: AsyncSession) -> None:
    cypher = """
        match (u:User)
        match (i:Item)
        where u.identifier = $identifier and i.identifier = $identifier2
        merge (u)-[:LIKE]->(i)
    """
    print(str(user.id), str(id_news))
    try:
        await Graph.write(cypher, identifier=str(user.id), identifier2=str(id_news))
    except neo4j.exceptions.ConstraintError as e:
        raise BadRequest("Already clicked", e) from e
