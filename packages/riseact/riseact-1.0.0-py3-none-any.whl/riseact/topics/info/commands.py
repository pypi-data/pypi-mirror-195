import typer

from riseact import ui
from riseact.topics.info.selectors import organization_get, partner_get, user_get

app = typer.Typer()


@app.command()
def partner():
    with ui.console.status("[magenta]Retrieving informations..."):
        partner = partner_get()

        table = ui.table()
        table.add_row("Partner", partner.name)
        ui.console.print(table)


@app.command()
def organization():
    with ui.console.status("[magenta]Retrieving informations..."):
        organization = organization_get()

        table = ui.table()
        table.add_row("Organization", organization.name)
        table.add_row("Sitefront URL", organization.sitefrontUrl)
        ui.console.print(table)


@app.command()
def user():
    with ui.console.status("[magenta]Retrieving informations..."):
        user = user_get()

        table = ui.table()
        table.add_row("Name", user.name)
        table.add_row("Email", user.email)
        ui.console.print(table)
