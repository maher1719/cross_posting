# backend/app/helpers/crud.py

from app.core.db import db
# --- 1. IMPORT THE NECESSARY TYPING TOOLS ---
from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

# --- 2. DEFINE GENERIC TYPE VARIABLES ---
# This tells Python we'll be using some generic types
ModelType = TypeVar("ModelType", bound=DeclarativeBase) # For the SQLAlchemy model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel) # For the Pydantic create schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) # For the Pydantic update schema
RepoType = TypeVar("RepoType", bound=CRUDBase)
DisplaySchemaType = TypeVar("DisplaySchemaType", bound=BaseModel)


# --- 3. MAKE CRUDBase A GENERIC CLASS ---
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, id: any) -> ModelType | None:
        return db.session.get(self.model, id)

    def get_all(self) -> list[ModelType]:
        return self.model.query.all()

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        # --- ENHANCED: Unpack the Pydantic model safely ---
        db_obj = self.model(**obj_in.model_dump())
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj) # Good practice to refresh after create
        return db_obj

    def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        # --- ENHANCED: More robust update logic ---
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def delete(self, *, id: any) -> ModelType | None:
        obj = self.get(id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
        return obj # Return the deleted object or None