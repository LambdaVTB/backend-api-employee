from datetime import datetime
from pydantic import BaseModel, Field

class NewsOut(BaseModel):
    url: str = Field(None, description='Ссылка на новость')
    summary: str = Field(None, description='Краткая выжимка')
    created_at: datetime  = Field(None, description='Время публикации новости')
    tags: list[str] = Field(None, description='Список тегов')
    id: str = Field(None, description='Идентификатор новости')

