from typing import Dict, Optional

from pydantic import BaseModel


class ThemeManifest(BaseModel):
    name: str
    slug: str
    version: str
    documentation_url: Optional[str]
    support_url: Optional[str]


class Theme(ThemeManifest):
    id: int
    uuid: str
    isDevelopment: bool
    isPublished: bool


class LocalAsset(BaseModel):
    key: str
    value: str
    contentType: str
    checksum: str


class Asset(BaseModel):
    key: str
    contentType: str
    checksum: str
    value: Optional[str]

    id: int
    attachment: Optional[str]
    size: int
    updatedAt: str
    createdAt: str


AssetMap = Dict[str, Asset]
