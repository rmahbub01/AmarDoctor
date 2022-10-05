# Import all the models, so that Base has them before being
# imported by Alembic
from doctor.db.base_class import Base
from doctor.models.usermodel import User
from doctor.models.usermodel import DummyDoctor