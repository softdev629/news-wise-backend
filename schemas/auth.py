from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    fullname: str
    password: str


class UserInfo(BaseModel):
    email: str
    fullname: str
    settings: dict
