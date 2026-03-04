from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str = Field(unique=True)
    description: str
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class ProductRegister(ProductBase):
    pass


class ProductRegisterResponse(ProductBase):
    seller: str
    seller_id: int
