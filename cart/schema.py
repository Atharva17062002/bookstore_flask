from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import re
from settings import settings

class CartSchema(BaseModel):
    book: int
    qunatity: int
    