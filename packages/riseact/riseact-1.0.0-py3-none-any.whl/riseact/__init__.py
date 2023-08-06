"""Riseact CLI"""

__version__ = "1.0.0"


from riseact.topics.settings.selectors import settings_load

SETTINGS = settings_load()
