import uuid
from datetime import datetime

from db.pg import Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column


class UserRole(Base):
    __tablename__ = 'users_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    role_id = mapped_column(ForeignKey('roles.id', ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<UserRoles {self.id}>'
