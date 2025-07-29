# app/schemas/token_schema.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class  TokenData(BaseModel):
    email: str | None = None