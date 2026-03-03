from sqlmodel import SQLModel, create_engine, Session
from settings.settings import Settings
from db.models.product_model import Products
from db.models.rbac_models import Permissions, RolePermissions, Roles
from db.models.user_models import Users, UsersRoles

# -----url of the database from the .env through the Settings object------
url = Settings.DATABASE_URL

# -----create the database engine-----
engine = create_engine(url)


def create_tables():
    SQLModel.metadata.create_all(engine)


def delete_tables():
    SQLModel.metadata.drop_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
        try:
            session.commit()
        except Exception:
            session.rollback()
