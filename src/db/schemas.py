from pydantic import BaseModel, HttpUrl, PositiveInt, field_validator


class SiteDTO(BaseModel):
    title: str | int
    url: HttpUrl
    xpath: str | int

    @field_validator('title', 'xpath')
    def check_not_empty(cls, value):
        if value is None or not hasattr(value, '__str__'):
            raise ValueError('Значение не может быть пустым и должно иметь строковое представление')
        if not str(value).strip():
            raise ValueError('Значение не может быть пустым')
        return value


class ReadOnlySiteDTO(BaseModel):
    id: PositiveInt
    title: str | int
    url: HttpUrl
    xpath: str | int
