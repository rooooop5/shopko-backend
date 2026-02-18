from app.db.seeds.seed_tables import create_tables, engine
from app.db.seeds.seed_rbac import seed_permissions
from app.db.seeds.seed_roles import seed_roles
from sqlmodel import Session


# -----entry point for database connnection and seeds-----
def initialise_database():
    create_tables()
    with Session(engine) as session:
        seed_permissions(session=session)
        seed_roles(session=session)


initialise_database()
