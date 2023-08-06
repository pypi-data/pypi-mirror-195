import typer
from rich.prompt import Prompt

from riseact import SETTINGS, ui
from riseact.client import client_init
from riseact.topics.app.commands import app as app_commands
from riseact.topics.auth.commands import app as auth_commands
from riseact.topics.auth.services import auth_login, auth_refresh_access_token
from riseact.topics.info.commands import app as info_commands
from riseact.topics.ngrok.commands import app as ngrok_commands
from riseact.topics.settings.commands import app as settings_commands
from riseact.topics.settings.services import settings_store_credentials
from riseact.topics.theme.commands import app as theme_commands

app = typer.Typer(
    rich_markup_mode=None,
    rich_help_panel=None,
)

app.add_typer(auth_commands, name="auth")
app.add_typer(settings_commands, name="settings")
app.add_typer(theme_commands, name="theme")
app.add_typer(info_commands, name="info")
app.add_typer(app_commands, name="app")
app.add_typer(ngrok_commands, name="ngrok")


@app.callback()
def warmup():
    if not SETTINGS.access_token:
        ui.console.print("To run this command, log in to Riseact Partners.")
        Prompt.ask("👉 Press any key to open the login page on your browser")
        auth_login()

    if SETTINGS.refresh_token:
        token = auth_refresh_access_token(SETTINGS.refresh_token)
        if token:
            settings_store_credentials(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
            )

    client_init()


def run():
    app()


if __name__ == "__main__":
    run()
