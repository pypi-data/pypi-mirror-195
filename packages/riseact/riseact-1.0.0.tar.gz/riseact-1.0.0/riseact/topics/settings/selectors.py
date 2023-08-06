import json
import os

from riseact import conf
from riseact.topics.settings.data import Settings

SETTINGS_DATA: Settings | None = None


def settings_load() -> Settings:
    global SETTINGS_DATA

    if not SETTINGS_DATA:
        if conf.CLI_ENV == "STAGING":
            env_data = conf.PROD_ENV
        elif conf.CLI_ENV == "DEV":
            env_data = conf.DEV_ENV
        else:
            env_data = conf.PROD_ENV

        if os.path.exists(conf.SETTINGS_PATH):
            with open(conf.SETTINGS_PATH, "r") as f:
                content = f.read()

            stored_data = json.loads(content)
            args = {**stored_data, **env_data}
        else:
            args = {**env_data}

        SETTINGS_DATA = Settings(**args)

    return SETTINGS_DATA
