from pydantic import BaseModel


class Token(BaseModel):
    auth_token: str
    refresh_token: str
