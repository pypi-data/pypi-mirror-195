from typing import Optional

from pydantic import BaseModel


class StoredSettings(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    ngrok_token: Optional[str] = None


class Settings(StoredSettings):
    redirect_uri: str
    client_id: str
    admin_host: str
    core_host: str
    accounts_host: str
