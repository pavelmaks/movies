import hashlib
import uuid
from datetime import datetime

from db.pg import Base
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    salt = 'SUPER_STRONG_SALT'
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username: str, password: str, first_name: str, last_name: str) -> None:
        self.username = username
        self.password = self.hash_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def hash_password(self, password: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt.encode(), 100000).hex()

    def check_password(self, password: str) -> bool:
        return self.password == hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt.encode(), 100000).hex()

    def __repr__(self) -> str:
        return f'<User {self.username}>'
