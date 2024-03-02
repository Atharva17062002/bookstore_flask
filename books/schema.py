from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import re
from settings import settings

class BookSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    price: int = Field(min_value=0)
    quantity: int = Field(min_value=0)
    super_user_id: int = Field(min_value=0)

    