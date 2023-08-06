import hashlib
import json
import os
import time
from pathlib import Path
from typing import Iterator, Tuple

import magic
from watchdog.observers import Observer

from riseact import ui
from riseact.topics.theme.consts import ASSETS_BLACKLIST
from riseact.topics.theme.data import AssetMap, LocalAsset, Theme, ThemeManifest
from riseact.topics.theme.observer import AssetChange, AssetEvent, AssetEventHandler
from riseact.topics.theme.remote import (
    asset_create,
    asset_delete,
    asset_update,
    theme_create,
    theme_delete,
)


def theme_parse_manifest(path: str) -> ThemeManifest:
    manifest_path = Path(path) / "manifest.json"
    with open(manifest_path, "r") as f:
        content = f.read()

    data = json.loads(content)

    theme = ThemeManifest(**data)

    return theme


def theme_push_theme(path: str) -> Tuple[Theme, AssetMap]:
    manifest = theme_parse_manifest(path)
    theme = theme_create(manifest=manifest, dev=False)
    assets = theme_create_assets(path, theme)

    return theme, assets


def theme_create_development_theme(path: str) -> Tuple[Theme, AssetMap]:
    manifest = theme_parse_manifest(path)
    theme = theme_create(manifest=manifest, dev=False)
    assets = theme_create_assets(path, theme)

    return theme, assets


def theme_delete_development_theme(theme: Theme) -> None:
    theme_delete(theme)


def theme_create_assets(path: str, theme: Theme) -> AssetMap:
    assets_map: AssetMap = {}
    asset_paths = list(theme_scan_assets(path))

    with ui.progress() as progress:
        task = progress.add_task("[green]Uploading", total=len(asset_paths))

        for asset_path in asset_paths:
            asset_key = asset_path.replace(path, "")[1:]
            local_asset = theme_load_local_asset(asset_key, asset_path)

            asset = asset_create(local_asset, theme)
            assets_map[asset.key] = asset

            progress.update(task, advance=1)
            ui.success(asset.key)

    return assets_map


def theme_load_local_asset(asset_key: str, asset_path: str) -> LocalAsset:
    with open(asset_path, "r") as f:
        content = f.read()

    local_asset = LocalAsset(
        key=asset_key,
        value=content,
        contentType=magic.from_file(asset_path, mime=True),
        checksum=hashlib.md5(content.encode("utf-8")).hexdigest(),
    )

    return local_asset


def theme_local_assets(path: str) -> list[LocalAsset]:
    local_assets = []
    for asset_path in theme_scan_assets(path):
        asset_key = asset_path.replace(path, "")[1:]
        local_assets.append(theme_load_local_asset(asset_key, asset_path))
    return local_assets


def theme_scan_assets(path: str) -> Iterator[str]:
    for entry in os.scandir(path):
        for bl in ASSETS_BLACKLIST:
            if path.startswith(bl):
                continue
        if os.path.basename(entry.path) in ASSETS_BLACKLIST:
            continue
        if entry.is_dir(follow_symlinks=False):
            yield from theme_scan_assets(entry.path)
        else:
            yield entry.path


def theme_watch_current_folder(
    path: str,
    theme: Theme,
    assets: AssetMap,
):
    event_handler = AssetEventHandler(
        path=path,
        theme=theme,
        assets=assets,
        handler=theme_handle_changes,
    )
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        theme_delete_development_theme(theme)
        observer.stop()

    observer.join()


def theme_handle_changes(
    change: AssetChange,
    theme: Theme,
    assets: AssetMap,
):
    try:
        if change.event == AssetEvent.CREATED:
            local_asset = theme_load_local_asset(change.key, change.path)
            ui.log_asset_change(f"[green]CREATED[/green] {change.key}")
            asset = asset_create(local_asset, theme)
            assets[asset.key] = asset
        elif change.event == AssetEvent.MODIFIED and change.asset:
            local_asset = theme_load_local_asset(change.key, change.path)
            ui.log_asset_change(f"[green]CHANGED[/green] {change.key}")
            asset_update(change.asset, local_asset, theme)
        elif change.event == AssetEvent.MOVED and change.asset:
            local_asset = theme_load_local_asset(change.key, change.path)
            ui.log_asset_change(f"[orange]MOVED[/orange] {change.key}")
            asset_update(change.asset, local_asset, theme)
        elif change.event == AssetEvent.DELETED and change.asset:
            ui.log_asset_change(f"[red]DELETED[/red] {change.key}")
            asset_delete(change.asset)
            del assets[change.key]
    except Exception as e:
        ui.console.print(
            f"ERROR: Cannot handle file change on {change.path}: {e}",
            style="red",
        )
