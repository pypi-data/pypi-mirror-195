from dataclasses import dataclass
from typing import Literal, TypedDict

from pydantic import BaseModel


class Application(BaseModel):
    id: int
    name: str
    type: str
    organization: int | None
    appUrl: str | None
    installUrl: str | None
    authorName: str | None
    authorHomepageUrl: str | None
    redirectUris: str | None
    clientId: str
    clientSecret: str


class ApplicationData(BaseModel):
    name: str
    type: str
    organization: int | None


class OAuthParams(TypedDict):
    response_type: Literal["code"]
    code_challenge_method: Literal["S256"]
    code_challenge: str
    client_id: str
    redirect_uri: str


@dataclass
class AppTemplate:
    name: str
    default_dev_command: list[str]


class OAuthTokenPayload(TypedDict):
    client_id: str
    code_verifier: str
    code: str
    redirect_uri: str
    grant_type: Literal["authorization_code"]


class OAuthRefreshTokenPayload(TypedDict):
    client_id: str
    refresh_token: str
    redirect_uri: str
    grant_type: Literal["refresh_token"]


APP_TEMPLATES = [AppTemplate("node", ["yarn", "dev"])]
