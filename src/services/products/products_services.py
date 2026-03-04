from sqlmodel import Session
from policies.product_policies import ProductPolicy
from services.rbac.roles_services import fetch_user_and_role
from db.models.product_model import Products
from db.models.user_models import Users
from schemas.product_schemas import ProductRegister


def list_product(active_role_dict: dict, product: ProductRegister, session: Session):
    db_user, role = fetch_user_and_role(active_role_dict, session)
    policy = ProductPolicy(db_user, role, product, session)
    if policy.can_list():
        db_product = Products(**product.model_dump(), seller_id=db_user.id)
        session.add(db_product)
        session.flush()
        session.refresh(db_product)
        response = db_product.model_dump()
        response.update({"seller": db_product.seller.username})
        return response
    else:
        return {"not allowed": f"Action not allowed under role {role}"}
