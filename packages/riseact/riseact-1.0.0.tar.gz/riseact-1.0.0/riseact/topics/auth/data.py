from dataclasses import dataclass
from typing import Literal, TypedDict


class OAuthParams(TypedDict):
    response_type: Literal["code"]
    code_challenge_method: Literal["S256"]
    code_challenge: str
    client_id: str
    redirect_uri: str


@dataclass
class AccessToken:
    access_token: str
    refresh_token: str


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
