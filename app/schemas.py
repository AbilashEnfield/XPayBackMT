from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, constr

from fastapi import Query


class UserSchema(BaseModel):
    """This class can be used both for response_model and for serialization"""

    full_name: Annotated[str, Query(min_length=5, max_length=50)] = ...
    email: EmailStr
    password: constr(min_length=8)
    phone: Annotated[str, Query(min_length=10, max_length=10)] = ...

    class Config:
        orm_mode = True

