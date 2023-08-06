import os
from pathlib import Path

from riseact import SETTINGS, conf
from riseact.topics.settings.data import Settings, StoredSettings


def settings_create_default(filename: Path) -> None:
    data = StoredSettings().json()
    config_dir = os.path.dirname(filename)
    Path(config_dir).mkdir(exist_ok=True, parents=True)
    with open(filename, "w") as f:
        f.write(data)


def settings_store(settings: Settings):
    data = StoredSettings(
        access_token=settings.access_token,
        refresh_token=settings.refresh_token,
        ngrok_token=settings.ngrok_token,
    )

    if not os.path.exists(conf.APP_DIR):
        os.mkdir(conf.APP_DIR)

    with open(conf.SETTINGS_PATH, "w+") as f:
        f.write(data.json())


def settings_store_ngrok_token(*, token: str) -> None:
    SETTINGS.ngrok_token = token
    settings_store(SETTINGS)


def settings_store_credentials(
    *,
    access_token: str,
    refresh_token: str,
) -> None:
    SETTINGS.access_token = access_token
    SETTINGS.refresh_token = refresh_token
    settings_store(SETTINGS)


def settings_delete_credentials() -> None:
    SETTINGS.access_token = None
    SETTINGS.refresh_token = None
    settings_store(SETTINGS)
