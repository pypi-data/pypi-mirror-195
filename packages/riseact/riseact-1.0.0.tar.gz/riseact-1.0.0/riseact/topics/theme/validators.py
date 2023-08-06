import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from riseact.topics.theme.data import ThemeManifest

MANIFEST_FILENAME = "manifest.json"


@dataclass
class ThemeValidationResult:
    error: bool
    message: Optional[str] = None


VALID_FOLDERS = [
    "assets",
    "config",
    "layout",
    "sections",
    "snippets",
    "templates",
]

FOLDERS_WHITELIST = ["node_modules", ".git", ".github"]


def theme_validate_structure(path: str) -> Tuple[bool, Optional[str]]:
    main_layout_path = Path(path) / "layout" / "theme.html"

    if not os.path.exists(main_layout_path):
        return False, "You must provide default layout/theme.html, check you t7po."

    return True, None


def theme_validate_folders(path: str) -> Tuple[bool, Optional[str]]:
    for entry in os.scandir(path):
        if not entry.is_dir():
            continue

        folder_name = os.path.basename(entry.path)

        if folder_name in FOLDERS_WHITELIST:
            continue

        if folder_name not in VALID_FOLDERS:
            valid_names = ", ".join(VALID_FOLDERS)
            return (
                False,
                f"Folder {folder_name} is not a valid directory name. Allowed names: {valid_names}",
            )

    return True, None


def theme_validate_manifest(path: str) -> Tuple[bool, Optional[str]]:
    manifest_path = Path(path) / MANIFEST_FILENAME

    if not os.path.exists(manifest_path):
        return (
            False,
            f"manifest.json file not found in {path}, are you in the right place?",
        )

    try:
        with open(manifest_path, "r") as f:
            manifest_content = f.read()

        manifest_data = json.loads(manifest_content)
    except Exception:
        return False, "manifest.json is not a valid json file, check your commas."

    try:
        ThemeManifest(**manifest_data)
    except Exception as e:
        return False, f"Some manifest.json fields are not valid: {e}"

    return True, None


def theme_validate_path(path: str) -> ThemeValidationResult:
    result = ThemeValidationResult(error=False)

    manifest_valid, manifest_error = theme_validate_manifest(path)

    if not manifest_valid:
        result.error = True
        result.message = manifest_error
        return result

    folders_valid, folders_error = theme_validate_folders(path)

    if not folders_valid:
        result.error = True
        result.message = folders_error
        return result

    structure_valid, structure_error = theme_validate_structure(path)

    if not structure_valid:
        result.error = True
        result.message = structure_error
        return result

    return result
