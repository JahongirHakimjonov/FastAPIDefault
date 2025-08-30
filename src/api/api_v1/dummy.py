from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.param_functions import Depends
from pydantic import TypeAdapter

from db.crud.dummy import DummyCRUD
from schemas.dummy import Dummy, DummyCreate

router = APIRouter(prefix="/dummy", tags=["dummy"])


@router.get("/", summary="Получить список объектов")
async def get_dummy_models(
    limit: Annotated[int, Query(description="Размер страницы")] = 10,
    page: Annotated[int, Query(description="Индекс страницы")] = 0,
    dummy_crud: DummyCRUD = Depends(),
) -> list[Dummy]:
    """
    Получить список объектов из базы данных.
    """
    result = await dummy_crud.get_all_dummies(limit=limit, offset=page * limit)
    type_adapter = TypeAdapter(list[Dummy])
    return type_adapter.validate_python(result)


@router.post("/", summary="Создать новый объект", status_code=HTTPStatus.CREATED)
async def create_dummy_model(
    new_dummy_object: DummyCreate,
    dummy_crud: DummyCRUD = Depends(),
) -> None:
    """
    Создать новый объект в базе данных.
    """
    await dummy_crud.create(name=new_dummy_object.name)
