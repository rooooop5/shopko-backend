from app.db.seeds.seed_tables import create_tables, engine
from app.db.seeds.seed_rbac import seed_permissions
from app.db.seeds.seed_rbac import seed_roles, seed_roles_permissions
from app.models.rbac_models import Roles
from sqlmodel import Session, select


# -----entry point for database connnection and seeds-----
def initialise_database():
    create_tables()
    with Session(engine) as session:
        seed_permissions(session=session)
        seed_roles(session=session)
        seed_roles_permissions(session=session)


initialise_database()

with Session(engine) as session:
    results = session.exec(select(Roles).where(Roles.role == "customer"))
    print(results.one().permissions)
