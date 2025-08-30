from pydantic import BaseModel, ConfigDict


def _to_camel(name: str) -> str:
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CamelSchema(BaseSchema):
    model_config = ConfigDict(alias_generator=_to_camel)
