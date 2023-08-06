from pydantic import BaseModel


class Partner(BaseModel):
    id: int
    name: str


class Organization(BaseModel):
    id: int
    name: str
    domain: str
    sitefrontUrl: str


class User(BaseModel):
    name: str
    email: str
