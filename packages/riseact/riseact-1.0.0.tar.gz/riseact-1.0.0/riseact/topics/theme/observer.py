from dataclasses import dataclass
from enum import Enum
from fnmatch import fnmatch
from typing import Callable, Optional

from watchdog.events import FileSystemEventHandler

from riseact.topics.theme.data import Asset, AssetMap, Theme


class AssetEvent(Enum):
    CREATED = 1
    DELETED = 2
    MOVED = 3
    MODIFIED = 3


@dataclass
class AssetChange:
    event: AssetEvent
    key: str
    path: str
    dest_key: Optional[str] = None
    dest_path: Optional[str] = None
    asset: Optional[Asset] = None


AssetChangeHandler = Callable[[AssetChange, Theme, AssetMap], None]


def is_ignored_path(path: str):
    content = None

    with open(".riseactignore", "r") as f:
        content = f.read()

    for ignore in content.split("\n"):
        if fnmatch(path, ignore):
            print(f"check {path} {ignore} True")
            return True

    return False


class AssetEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    path: str
    handler: AssetChangeHandler
    theme: Theme
    assets: AssetMap

    def __init__(
        self,
        *,
        path: str,
        theme: Theme,
        assets: AssetMap,
        handler: AssetChangeHandler,
    ):
        super().__init__()
        self.path = path
        self.handler = handler
        self.theme = theme
        self.assets = assets

    def on_moved(self, event):
        super().on_moved(event)
        asset_key = event.src_path.replace(self.path + "/", "")
        if event.is_directory or is_ignored_path(asset_key):
            return

        asset_dest_key = event.dest_path.replace(self.path + "/", "")
        self.handler(
            AssetChange(
                event=AssetEvent.MOVED,
                key=asset_key,
                path=event.src_path,
                dest_key=asset_dest_key,
                dest_path=event.dest_path,
                asset=self.assets[asset_key],
            ),
            self.theme,
            self.assets,
        )

    def on_created(self, event):
        super().on_created(event)
        asset_key = event.src_path.replace(self.path + "/", "")
        if event.is_directory or is_ignored_path(asset_key):
            return

        self.handler(
            AssetChange(
                event=AssetEvent.CREATED,
                key=asset_key,
                path=event.src_path,
            ),
            self.theme,
            self.assets,
        )

    def on_deleted(self, event):
        super().on_deleted(event)
        asset_key = event.src_path.replace(self.path + "/", "")
        if event.is_directory or is_ignored_path(asset_key):
            return

        self.handler(
            AssetChange(
                event=AssetEvent.DELETED,
                asset=self.assets[asset_key],
                key=asset_key,
                path=event.src_path,
            ),
            self.theme,
            self.assets,
        )

    def on_modified(self, event):
        super().on_modified(event)
        asset_key = event.src_path.replace(self.path + "/", "")
        if event.is_directory or is_ignored_path(asset_key):
            return

        self.handler(
            AssetChange(
                event=AssetEvent.MODIFIED,
                asset=self.assets[asset_key],
                key=asset_key,
                path=event.src_path,
            ),
            self.theme,
            self.assets,
        )
