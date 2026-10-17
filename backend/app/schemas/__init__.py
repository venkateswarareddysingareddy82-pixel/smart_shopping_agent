from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    phone: str = Field(default="", max_length=20)
    preferred_language: str = "en"


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=100)


class ProfileIn(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    preferred_language: str | None = None


class AddressIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=7, max_length=20)
    line1: str = Field(min_length=3, max_length=200)
    line2: str = Field(default="", max_length=200)
    city: str = Field(min_length=2, max_length=80)
    state: str = Field(min_length=2, max_length=80)
    pincode: str = Field(min_length=4, max_length=10)
    is_default: bool = False


class CartAddIn(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, le=20)


class CartUpdateIn(BaseModel):
    quantity: int = Field(ge=1, le=20)


class CheckoutIn(BaseModel):
    address_id: int | None = None
    address: AddressIn | None = None
    payment_method: str = Field(default="cod", pattern="^(cod|demo_online)$")
    coupon_code: str = ""
    buy_now_product_id: int | None = None
    buy_now_quantity: int = Field(default=1, ge=1, le=20)


class ReviewIn(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    language: str = "en"
    history: list[dict] = []
    state: dict = {}
    context_product_ids: list[int] = []
    product_id: int | None = None


class ExplainIn(BaseModel):
    language: str = "en"
    question: str = Field(default="", max_length=500)


class CompareIn(BaseModel):
    product_ids: list[int] = Field(min_length=2, max_length=4)
    language: str = "en"
    priority: str | None = None
    question: str = Field(default="", max_length=500)


class ProductIn(BaseModel):
    name: str = Field(min_length=2, max_length=240)
    category: str
    subcategory: str = ""
    brand: str = Field(min_length=1, max_length=100)
    description: str = ""
    price: int = Field(gt=0)
    original_price: int | None = Field(default=None, gt=0)
    rating: float = Field(default=0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    stock: int = Field(default=0, ge=0)
    specifications: dict = {}
    metrics: dict = {}
    features: list[str] = []
    advantages: list[str] = []
    disadvantages: list[str] = []
    delivery_information: str = "Free delivery in 3-5 days"
    seller: str = "Demo Seller"
    tags: list[str] = []
    search_keywords: str = ""
    is_active: bool = True


class CategoryIn(BaseModel):
    slug: str = Field(min_length=2, max_length=60, pattern="^[a-z0-9-]+$")
    name: str = Field(min_length=2, max_length=100)
    group: str = Field(min_length=2, max_length=60)
    emoji: str = "🛍️"


class CouponIn(BaseModel):
    code: str = Field(min_length=3, max_length=30)
    description: str = ""
    percent: int = Field(ge=1, le=90)
    max_discount: int = Field(default=500, ge=0)
    min_order: int = Field(default=0, ge=0)
    active: bool = True


class OrderStatusIn(BaseModel):
    status: str
