from service.migrations.models.users import Users

async def add_new_user(login: str, hashed_password: str) -> None:
    pass

async def get_user(login: str) -> Users:
    pass
