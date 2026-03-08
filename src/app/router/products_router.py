from fastapi import APIRouter, Depends
from app.auth.security import get_session, authenticate_role
from services.products_services import list_product
from db.models.product_model import Products
from schemas.product_schemas import ProductRegister
products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.post("/list-product")
def list_product_endpoint(product:ProductRegister,active_role=Depends(authenticate_role), session=Depends(get_session)):
    return list_product(product=product,active_role_dict=active_role,session=session)