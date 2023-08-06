import typer

from riseact import ui
from riseact.topics.settings.services import settings_store_ngrok_token

app = typer.Typer()


@app.command()
def token(token: str):
    settings_store_ngrok_token(token=str(token))
    ui.success("ngrok token stored")
