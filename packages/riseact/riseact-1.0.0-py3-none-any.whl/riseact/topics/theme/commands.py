import os

import inquirer
import typer

from riseact import SETTINGS, ui
from riseact.topics.info.selectors import organization_search
from riseact.topics.theme.remote import theme_create
from riseact.topics.theme.services import (
    theme_create_development_theme,
    theme_parse_manifest,
    theme_push_theme,
    theme_watch_current_folder,
)
from riseact.topics.theme.validators import theme_validate_path

app = typer.Typer()


@app.command()
def serve():
    cwd = os.getcwd()

    partner_organizations = organization_search()
    organization_id = inquirer.list_input(
        "Which organization would you like to use to serve your theme?",
        choices=[(o.name, o.id) for o in partner_organizations],
    )

    organization = None
    for o in partner_organizations:
        if o.id == organization_id:
            organization = o

    if organization is None:
        ui.console.print("[red]Error retrieving organization")
        return

    with ui.console.status("[magenta]Validating path...") as status:
        validation = theme_validate_path(cwd)
        if validation.error:
            ui.console.print(f"[bold red]ERROR:[/bold red] {validation.message}")
            raise typer.Exit(1)

        status.update(status="[magenta]Parsing manifest...")
        manifest = theme_parse_manifest(cwd)

        status.update(status="[magenta]Creating remote theme...")
        theme = theme_create(manifest=manifest, dev=False)

    theme, assets = theme_create_development_theme(cwd)

    ui.console.print()
    ui.success("Theme uploaded")

    table = ui.table()
    table.add_row("Name", theme.name)
    table.add_row("UUID", theme.uuid)
    table.add_row("Preview", f"{organization.sitefrontUrl}?__preview={theme.uuid}")
    table.add_row("Editor", f"{SETTINGS.admin_host}/themes/{theme.uuid}/editor")
    ui.console.print(table)
    ui.console.print()

    with ui.console.status("[magenta]Watching for file changes") as status:
        theme_watch_current_folder(cwd, theme, assets)


@app.command()
def push():
    cwd = os.getcwd()

    with ui.console.status("[magenta]Validating path...") as status:
        validation = theme_validate_path(cwd)
        if validation.error:
            ui.console.print(f"[bold red]ERROR:[/bold red] {validation.message}")
            raise typer.Exit(1)

        status.update(status="[magenta]Retrieving Organization info...")

        partner_organizations = organization_search()
        organization_id = inquirer.list_input(
            "Which organization would you like to use to serve your theme?",
            choices=[(o.name, o.id) for o in partner_organizations],
        )

        organization = None
        for o in partner_organizations:
            if o.id == organization_id:
                organization = o

        if organization is None:
            ui.console.print("[red]Error retrieving organization")
            return

    theme, assets = theme_push_theme(cwd)

    ui.console.print()
    ui.success("Theme pushed")

    table = ui.table()
    table.add_row("Name", theme.name)
    table.add_row("UUID", theme.uuid)
    table.add_row("Preview", f"{organization.sitefrontUrl}?__preview={theme.uuid}")
    table.add_row("Editor", f"{SETTINGS.admin_host}/themes/{theme.uuid}/editor")
    ui.console.print(table)
    ui.console.print()
