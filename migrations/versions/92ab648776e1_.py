"""empty message

Revision ID: 92ab648776e1
Revises: 4048fe01f9af
Create Date: 2024-07-23 20:01:41.783203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92ab648776e1'
down_revision: Union[str, None] = '4048fe01f9af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
