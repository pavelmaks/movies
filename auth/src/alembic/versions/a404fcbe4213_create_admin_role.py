"""create admin role

Revision ID: a404fcbe4213
Revises: ca8d1ffdaefd
Create Date: 2023-08-13 14:17:23.726570

"""
from typing import Sequence, Union

from alembic import op
from db.models.role import Role
from sqlalchemy import orm

ADMIN_ROLE_NAME = 'admin'

# revision identifiers, used by Alembic.
revision: str = 'a404fcbe4213'
down_revision: Union[str, None] = 'ca8d1ffdaefd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    role = Role(name=ADMIN_ROLE_NAME)
    session.add(role)
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(Role).where(Role.name == ADMIN_ROLE_NAME).delete()
    session.commit()
