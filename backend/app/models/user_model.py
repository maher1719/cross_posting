# backend/app/models/user_model.py
import uuid
import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.db import db


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),  # Use the UUID type from your dialect
        primary_key=True,
        default=uuid.uuid4)
    username: Mapped[str] = mapped_column(
        String(80),
        unique=True, 
        nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), 
        unique=True, 
        nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        String(255), 
        nullable=False) # ADD THIS LINE
    created_at: Mapped[datetime.datetime] = mapped_column(
        db.DateTime, 
        default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'