"""
Schemas Base
"""
from pydantic import BaseModel


class BaseOut(BaseModel):
    """BaseOut"""

    success: bool = True
    message: str = "Success"

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
