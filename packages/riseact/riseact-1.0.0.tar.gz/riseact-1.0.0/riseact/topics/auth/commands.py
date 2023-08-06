import typer

from riseact import ui
from riseact.topics.auth.services import auth_login
from riseact.topics.settings.services import settings_delete_credentials

app = typer.Typer()


@app.command()
def login():
    auth_login()


@app.command()
def logout():
    with ui.console.status("[magenta]Logging out..."):
        settings_delete_credentials()

    ui.success("Logged out from Riseact.")
