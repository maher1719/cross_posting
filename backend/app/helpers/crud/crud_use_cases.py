# backend/app/helpers/crud_use_cases.py

from app.core.db import db
from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4

ModelType = TypeVar("ModelType", bound=DeclarativeBase) # For the SQLAlchemy model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel) # For the Pydantic create schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) # For the Pydantic update schema
RepoType = TypeVar("RepoType", bound=CRUDBase)
DisplaySchemaType = TypeVar("DisplaySchemaType", bound=BaseModel)

RepoType = TypeVar("RepoType", bound=CRUDBase)
DisplaySchemaType = TypeVar("DisplaySchemaType", bound=BaseModel)

class CRUDUseCases(Generic[RepoType, CreateSchemaType, UpdateSchemaType, DisplaySchemaType]):
    def __init__(self, repository: RepoType):
        self.repository = repository

    def get_by_id(self, id: uuid4) -> DisplaySchemaType | None:
        db_obj = self.repository.get(id)
        if db_obj:
            return DisplaySchemaType.from_orm(db_obj)
        return None

    def get_all(self) -> list[DisplaySchemaType]:
        db_objs = self.repository.get_all()
        return [DisplaySchemaType.from_orm(obj) for obj in db_objs]

    def create(self, *, obj_in: CreateSchemaType) -> DisplaySchemaType:
        db_obj = self.repository.create(obj_in=obj_in)
        return DisplaySchemaType.from_orm(db_obj)

    def update(self, *, id: uuid4, obj_in: UpdateSchemaType) -> DisplaySchemaType | None:
        db_obj = self.repository.get(id)
        if not db_obj:
            return None
        updated_db_obj = self.repository.update(db_obj=db_obj, obj_in=obj_in)
        return DisplaySchemaType.from_orm(updated_db_obj)

    def delete(self, *, id: uuid4) -> bool:
        deleted_obj = self.repository.delete(id=id)
        return deleted_obj is not None