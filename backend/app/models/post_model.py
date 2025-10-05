# backend/app/models/post_model.py
import uuid
import datetime
from sqlalchemy import Text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.db import db

# Add a basic Post model for future use
class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),  # Use the UUID type from your dialect
        primary_key=True,
        default=uuid.uuid4)
    content_html: Mapped[str] = mapped_column(Text, nullable=False)
    # --- ADD THE NEW COLUMN ---
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    generate_for_twitter: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        db.ForeignKey('users.id'), 
        nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        db.DateTime, 
        default=datetime.datetime.utcnow)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.id}>'