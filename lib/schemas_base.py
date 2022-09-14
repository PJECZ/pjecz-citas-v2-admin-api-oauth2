"""
Schemas Base
"""
from pydantic import BaseModel


class BaseOut(BaseModel):
    """BaseOut"""

    success: bool = True
    message: str = "Success"
