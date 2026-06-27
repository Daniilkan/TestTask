from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    art: str
    name: str
    url: str

    price: float
    category: str

    rating: float
    reviews: int

    collected_at: datetime