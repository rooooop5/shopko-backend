from app.db.seeds.seed_tables import create_tables, delete_tables,engine
from app.db.seeds.seed_rbac import seed_permissions
from app.db.seeds.seed_rbac import seed_roles, seed_roles_permissions
from sqlmodel import Session


# -----entry point for database connnection and seeds-----
def startup():
    create_tables()
    with Session(engine) as session:
        seed_permissions(session=session)
        seed_roles(session=session)
        seed_roles_permissions(session=session)

def cleanup():
    delete_tables()