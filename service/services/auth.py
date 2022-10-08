from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from migrations.models.users import Users
from migrations.models.jobs import Jobs
from service.exceptions.common import NotFoundException


async def add_new_user(login: str, hashed_password: str, job_name: str, session: AsyncSession) -> None:
    try:
        query = insert(Jobs).values(
            name = job_name
        )
        await session.execute(query)
    except IntegrityError:
        pass
    query = select(Jobs).where(Jobs.name == job_name)
    job = (await session.execute(query)).scalars().first()
    query = insert(Users).values(
        username=login,
        password=hashed_password,
        job_id = str(job.id)
    )
    await session.execute(query)
    await session.commit()

async def get_user(login: str, session: AsyncSession) -> Users:
    query = select(Users).where(
        Users.username == login
    )
    result = (await session.execute(query)).scalars().first()
    if not result:
        raise NotFoundException("User not found")
    return result
