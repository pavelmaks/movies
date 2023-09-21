import uuid
from datetime import datetime

from db.pg import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column


class UserOauth(Base):
    __tablename__ = 'users_oauth'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    oauth_name = Column(String(30), nullable=False)
    oauth_id = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f'<UserOauth {self.id}>'
