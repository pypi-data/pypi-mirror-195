import os
import re
import shutil
import signal
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Optional, TypedDict

import git
import inquirer
import toml
from attr import dataclass
from inquirer.questions import is_pathname_valid
from pyngrok import ngrok

from riseact import SETTINGS, ui
from riseact.client import execute_partner_query
from riseact.topics.app.data import Application, ApplicationData
from riseact.topics.settings.services import settings_store_ngrok_token

ngrok.set_auth_token("25aplhPjeiVEeWP43iTvLF24gN0_5Q6A4Kvr5dxKZUCVNKJLW")

MANIFEST_FILE = "riseact.app.toml"

REPO = "https://github.com/riseact/riseact-app-template-node.git"

sys.path.append(os.path.realpath("."))


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class AppManifest(TypedDict):
    name: str
    dev_commands: list[str]
    client_id: Optional[str]


@dataclass
class AppData(TypedDict):
    path: Path
    manifest: AppManifest


def app_init_form() -> Optional[AppData]:
    app_name = inquirer.text(
        "App name",
        validate=lambda _, x: x not in ["", "."],
    )

    app_path = inquirer.text(
        "App location",
        default=f"./{slugify(app_name)}",
        validate=lambda _, x: is_pathname_valid(x),
    )

    app_template = inquirer.list_input(
        "App template",
        choices=[("Node", "node")],
    )

    app_path = Path(app_path)

    try:
        os.mkdir(app_path)
    except FileExistsError:
        pass

    if app_template == "node":
        dev_commands = ["yarn dev"]
    else:
        dev_commands = []

    return AppData(
        path=app_path,
        manifest=AppManifest(
            name=str(app_name),
            dev_commands=dev_commands,
            client_id=None,
        ),
    )


def app_clone_template(data: AppData):
    git.Repo.clone_from(  # type: ignore
        REPO,
        data["path"],
        branch="master",
        multi_options=["--recurse-submodule"],
    )

    Path(data["path"] / ".gitmodules").unlink(missing_ok=True)

    for git_folder in Path(data["path"]).rglob(".git"):
        if git_folder.is_dir:
            try:
                shutil.rmtree(git_folder, ignore_errors=False)
            except Exception:
                Path(git_folder).unlink(missing_ok=True)
        else:
            Path(git_folder).unlink(missing_ok=True)

    # cloned_repo.submodule_update(recursive=True)


def app_generate_toml(data: AppData) -> str:
    content = toml.dumps(data["manifest"])
    with open(data["path"] / MANIFEST_FILE, "w") as f:
        f.write(content)

    return MANIFEST_FILE


def app_read_manifest() -> AppManifest:
    if not os.path.exists(MANIFEST_FILE):
        ui.console.print("The app manifest cannot be found.")
        sys.exit()

    try:
        with open(MANIFEST_FILE, "r") as f:
            manifest_content = f.read()

        manifest_data = toml.loads(manifest_content)
    except Exception:
        ui.console.print("The app manifest cannot be read.")
        sys.exit()

    return AppManifest(**manifest_data)


def app_start_tunnel() -> ngrok.NgrokTunnel:
    ngrok_token = SETTINGS.ngrok_token
    if ngrok_token is None:
        ngrok_token = inquirer.text("Please paste yout ngrok token")
        settings_store_ngrok_token(token=str(ngrok_token))

    ngrok.set_auth_token(ngrok_token)
    http_tunnel: ngrok.NgrokTunnel = ngrok.connect(3000, bind_tls=True)
    # hmr_tunnel: ngrok.NgrokTunnel = ngrok.connect(3030, bind_tls=True)
    # print(hmr_tunnel)
    ngrok.get_ngrok_process()

    return http_tunnel


def app_install_node_template(data: AppData):
    os.chdir(data["path"])
    app_workdir = os.getcwd()
    process = subprocess.Popen(["yarn"])
    process.wait()

    os.chdir("./src/frontend")
    process = subprocess.Popen(["yarn"])
    process.wait()
    process = subprocess.Popen(["yarn", "build"])
    process.wait()

    os.chdir(app_workdir)


def app_create_dev_process(command: list[str]) -> subprocess.Popen:
    dev_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    def _signal_handler(signum, frame):
        app_stop_dev_processes(dev_process.pid)

    signal.signal(signal.SIGINT, _signal_handler)

    return dev_process


def app_stop_dev_processes(dev_process_pid: int):
    try:
        with ui.console.status("[magenta]Stopping dev process..."):
            os.killpg(os.getpgid(dev_process_pid), signal.SIGTERM)
        ui.success("Dev process stopped")

        with ui.console.status("[magenta]Stopping ngrok tunnel..."):
            ngrok.kill()
        ui.success("Ngrok tunnel stopped")
    except Exception:
        pass


def app_create(
    *,
    name: str,
    organization_id: int,
) -> Application:
    result = execute_partner_query(
        """
        mutation AppCreate($data: AppInput!) {
            appCreate(data: $data) {
                app {
                    id
                    name
                    type
                    organization
                    appUrl
                    installUrl
                    authorName
                    authorHomepageUrl
                    redirectUris
                    clientId
                    clientSecret
                }
            }
        }""",
        variable_values={
            "data": ApplicationData(
                name=name,
                type="PRIVATE",
                organization=organization_id,
            ).dict(),
        },
    )

    return Application(**result["appCreate"]["app"])


def app_update_redirect_uris(
    *,
    app: Application,
    ngrok_redirect_uri: str,
):
    redirect_uris = (app.redirectUris or "").split()
    redirect_uris = [u for u in redirect_uris if "ngrok.io" not in u]
    redirect_uris.append(ngrok_redirect_uri)

    execute_partner_query(
        """
        mutation RedirectUriMutation($id: Int!, $redirectUris: String!) {
            appUpdateRedirectUris(id: $id, redirectUris: $redirectUris) {
                app {
                    id
                }
            }
        }""",
        variable_values={
            "redirectUris": "\n".join(redirect_uris),
            "id": app.id,
        },
    )
