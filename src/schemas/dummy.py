from pydantic import Field

from .base import BaseSchema


class Dummy(BaseSchema):
    """
    DTO для модели Dummy.
    """

    id: int = Field(title="ID", examples=[1])
    name: str = Field(title="Name", examples=["Test"])


class DummyCreate(BaseSchema):
    """
    DTO создания модели Dummy.
    """

    name: str = Field(title="Name of dummy model", examples=["Test"])
