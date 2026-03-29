from pydantic import BaseModel, ConfigDict


class CartSchema(BaseModel):

    user_id: str
    items: list[CartItemResponse] = []


class CartWithId(CartSchema):
    id: str

class CartWithProducts(BaseModel):
    id: str
    user_id: str
    items: list[CartItemWithProduct] = []
    total_amount: float = 0

class CartCreate(BaseModel):
    id: str
    user_id: str


class CartItemCreate(BaseModel):
    id: str
    cart_id: str
    product_id: str
    quantity: int

class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemFilter(BaseModel):
    id: str | None = None
    cart_id: str | None = None
    product_id: str | None = None


class CartItemResponse(BaseModel):
    id: str
    cart_id: str
    product_id: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class CartItemWithProduct(BaseModel):
    id: str
    product_id: str
    quantity: int
    title: str
    price: float
    color: str
    brand_logo: str | None = None

    model_config = ConfigDict(from_attributes=True)
