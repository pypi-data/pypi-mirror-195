import typer
from rich import print

from riseact import SETTINGS, conf, ui

app = typer.Typer()


@app.command()
def show():
    table = ui.table()

    for key, value in SETTINGS.dict().items():
        table.add_row(key, value)

    ui.console.print(table)


@app.command()
def path():
    print(conf.SETTINGS_PATH)
