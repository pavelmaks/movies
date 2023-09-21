import uuid
from datetime import datetime

from db.pg import Base
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID


class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
