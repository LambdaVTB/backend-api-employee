import neo4j
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.users import Users
from migrations.models.jobs import Jobs
from service.exceptions.common import BadRequest,NotFoundException
from service.schemas.common import JobsOut
from service.utils.graph import Graph


async def add_new_user(login: str, hashed_password: str, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            username=login,
            password=hashed_password,
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise BadRequest("User already exist", e) from e
    user = await get_user(login, session)
    cypher = """create (i: User{identifier: $id})"""
    try:
        await Graph.write(cypher, id=user.id)
    except neo4j.exceptions.ConstraintError as e:
        raise BadRequest('User already exists', e)
async def get_user(login: str, session: AsyncSession) -> Users:
    query = select(Users).where(
        Users.username == login
    )
    result = (await session.execute(query)).scalars().first()
    if not result:
        raise NotFoundException("User not found")
    return result

async def get_jobs(session: AsyncSession) -> list[JobsOut]:
    query = select(Jobs)
    data = (await session.execute(query)).scalars().all()
    return [JobsOut(
        name = el.name,
        id = el.id
    ) for el in data]

async def update_user_job(login: str, job: str, session: AsyncSession):
    try:
        query = update(Users).values(
            job_id = str(job)
        ).where(
            Users.username == str(login)
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise BadRequest("Job is not found", e) from e
