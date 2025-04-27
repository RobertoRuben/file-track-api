"""seed_inital_data

Revision ID: 1d24f5f7cf65
Revises: e51cd95457a8
Create Date: 2025-04-24 21:53:52.701873

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d24f5f7cf65'
down_revision: Union[str, None] = 'e51cd95457a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insertar rol
    op.execute("INSERT INTO roles(name) VALUES ('SUPER ADMIN');")

    # Insertar departamento
    op.execute("INSERT INTO departments(name) VALUES ('Tecnologias de Informacion');")

    # Insertar posición
    op.execute("INSERT INTO positions(name) VALUES ('Data Engineer');")

    # Insertar empleado
    op.execute(
        """
               INSERT INTO employees(
                   dni,
                   paternal_surname,
                   maternal_surname,
                   names,
                   gender,
                   position_id,
                   department_id
               ) VALUES (
                            74978113,
                            'Chavez',
                            'Vargas',
                            'Roberto',
                            'Male',
                            1,
                            1
                        );
               """
    )

    # Insertar usuario
    op.execute(
        """
               INSERT INTO users(
                   username,
                   password,
                   is_active,
                   role_id,
                   employee_id
               ) VALUES (
                            'rchavezv',
                            '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
                            true,
                            1,
                            1
                        );
               """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar en orden inverso para respetar las restricciones de clave foránea
    op.execute("DELETE FROM users WHERE username = 'rchavezv';")
    op.execute("DELETE FROM employees WHERE dni = 74978113;")
    op.execute("DELETE FROM positions WHERE name = 'Data Engineer';")
    op.execute("DELETE FROM departments WHERE name = 'Tecnologias de Informacion';")
    op.execute("DELETE FROM roles WHERE name = 'SUPER ADMIN';")
