"""Database initialization migration.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-02-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema"""
    
    # Crear tabla barbers
    op.create_table(
        'barbers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_barbers_id'), 'barbers', ['id'], unique=False)
    op.create_index(op.f('ix_barbers_name'), 'barbers', ['name'], unique=True)
    
    # Crear tabla services
    op.create_table(
        'services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)
    op.create_index(op.f('ix_services_name'), 'services', ['name'], unique=True)
    
    # Crear tabla appointments
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('client_name', sa.String(255), nullable=False),
        sa.Column('client_phone', sa.String(20), nullable=True),
        sa.Column('barber_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('appointment_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'confirmed', 'completed', 'cancelled'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['barber_id'], ['barbers.id'], ),
        sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('barber_id', 'appointment_date', name='unique_barber_appointment_date')
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)
    op.create_index(op.f('ix_appointments_client_name'), 'appointments', ['client_name'], unique=False)
    op.create_index(op.f('ix_appointments_appointment_date'), 'appointments', ['appointment_date'], unique=False)
    op.create_index(op.f('ix_appointments_status'), 'appointments', ['status'], unique=False)
    op.create_index(op.f('ix_appointments_barber_id'), 'appointments', ['barber_id'], unique=False)
    op.create_index(op.f('ix_appointments_service_id'), 'appointments', ['service_id'], unique=False)


def downgrade() -> None:
    """Drop initial database schema"""
    
    # Eliminar tabla appointments
    op.drop_index(op.f('ix_appointments_service_id'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_barber_id'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_status'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_appointment_date'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_client_name'), table_name='appointments')
    op.drop_index(op.f('ix_appointments_id'), table_name='appointments')
    op.drop_table('appointments')
    
    # Eliminar tabla services
    op.drop_index(op.f('ix_services_name'), table_name='services')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')
    
    # Eliminar tabla barbers
    op.drop_index(op.f('ix_barbers_name'), table_name='barbers')
    op.drop_index(op.f('ix_barbers_id'), table_name='barbers')
    op.drop_table('barbers')
