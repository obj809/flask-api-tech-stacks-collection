# app/models.py

from datetime import datetime, timezone
from sqlalchemy import BigInteger
from . import db

class Todo(db.Model):
    """Model for the todos table."""
    __tablename__ = 'todos'
    # Use BigInteger for PostgreSQL (Supabase), Integer for SQLite (tests)
    id = db.Column(
        BigInteger().with_variant(db.Integer, 'sqlite'),
        primary_key=True,
        autoincrement=True
    )
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    title = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Todo {self.id}: {self.title}>"
