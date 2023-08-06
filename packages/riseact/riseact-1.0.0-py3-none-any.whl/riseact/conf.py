import os
from pathlib import Path

from typer import get_app_dir

APP_NAME = "riseact"

APP_DIR = get_app_dir(APP_NAME)

SETTINGS_PATH: Path = Path(APP_DIR) / "config.json"

CLI_ENV = os.getenv("RISEACT_CLI_ENV", "PROD").upper()

DEV_ENV = {
    "redirect_uri": "http://localhost:55443",
    "client_id": "VUpZM6CDKimnGgCSkzxLWsHP60DytxfHeRJXgVA2",
    "admin_host": "http://localhost:4500",
    "core_host": "http://core.localhost:8000",
    "accounts_host": "http://accounts.localhost:8000",
}

PROD_ENV = {
    "redirect_uri": "http://localhost:55443",
    "client_id": "oigtjb908t2i3lnkjvgfjdSFGHY43gk90ufsdfsd",
    "admin_host": "https://admin.riseact.org",
    "core_host": "https://core.riseact.org",
    "accounts_host": "https://accounts.riseact.org",
}
