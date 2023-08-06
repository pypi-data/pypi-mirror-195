import webbrowser

import inquirer
import typer

from riseact import SETTINGS, ui
from riseact.topics.app.selectors import (
    app_get,
    app_get_by_client_id,
    app_get_config,
    app_search,
)
from riseact.topics.app.services import (
    app_clone_template,
    app_create,
    app_create_dev_process,
    app_generate_toml,
    app_init_form,
    app_install_node_template,
    app_read_manifest,
    app_start_tunnel,
    app_update_redirect_uris,
)
from riseact.topics.info.selectors import organization_search
from riseact.topics.settings.services import settings_store_ngrok_token

app = typer.Typer()


@app.command()
def init():
    # create new app
    data = app_init_form()
    if not data:
        raise typer.Exit()

    app_clone_template(data)
    filename = app_generate_toml(data)
    ui.success(f"Your '{filename}' has been generated.")
    ui.console.print("Installing app")

    with ui.console.status("[magenta]Installing app..."):
        app_install_node_template(data)
        ui.success("Application created")

    dev()


@app.command()
def dev():
    """
    - load app config
    """
    app_config = app_get_config()
    app_manifest = app_read_manifest()

    current_app = None
    if app_config.get("CLIENT_ID", None):
        current_app = app_get_by_client_id(client_id=app_config["CLIENT_ID"])

    if current_app is None:
        ui.console.print(
            "Looks like this is the first time you're running dev for this project."
        )
        ui.console.print("Configure your preferences by answering a few questions.")
        ui.console.print(
            "\nBefore you preview your work, it needs to be associated with an app."
        )

        create_new_app = inquirer.list_input(
            "Create this project as a new app on Riseact?",
            choices=[
                ("Yes, create it as a new app", True),
                ("No, connect it to an existing app", False),
            ],
            default=True,
        )

        if create_new_app:
            app_name = inquirer.text("App name", default=app_manifest["name"])

            partner_organizations = organization_search()
            app_organization_id = inquirer.list_input(
                "Which organization would you like to use to view your project?",
                choices=[(o.name, o.id) for o in partner_organizations],
            )

            with ui.console.status("[magenta]Creating application...") as status:
                current_app = app_create(
                    name=str(app_name), organization_id=int(app_organization_id)
                )
                ui.success("Application created")
        else:
            partner_apps = app_search()
            app_id = inquirer.list_input(
                "Which existing app is this for?",
                choices=[(a.name, a.id) for a in partner_apps],
            )
            app_id = int(app_id)
            current_app = app_get(id=app_id)

            if current_app is None:
                ui.console.print(
                    "There has been an error retrieving this app. Contact support."
                )
                return

        with ui.console.status("[magenta]Writing .env...") as status:
            with open("./.env", "w") as fh:
                fh.write(
                    "\n".join(
                        [
                            f"CLIENT_ID={current_app.clientId}",
                            f"CLIENT_SECRET={current_app.clientSecret}",
                        ]
                    )
                )
            ui.success(".env updated")

    ngrok_tunnel = app_start_tunnel()
    with ui.console.status("[magenta]Updating redirect URIs...") as status:
        app_update_redirect_uris(
            app=current_app,
            ngrok_redirect_uri=f"{ngrok_tunnel.public_url}/oauth/callback",
        )
        ui.success("Redirect URIs updated")

    if not SETTINGS.ngrok_token:
        ui.console.print(
            "To make your local code accessible to your dev organization, you need to use a"
        )
        ui.console.print("Riseact-trusted tunneling service called ngrok.")
        ui.console.print(
            "To sign up and get an auth token: https://dashboard.ngrok.com/get-started/your-authtoken"
        )

        ngrok_token = inquirer.password(
            "Enter your ngrok token",
            validate=_ngrok_answer_validate,
        )

        settings_store_ngrok_token(token=str(ngrok_token))
        ui.success("Ngrok token stored")

    with ui.console.status("[magenta]Starting ngrok tunnel...") as status:
        ui.success("Ngrok tunnel started")
        status.update("[magenta]Starting dev process...")

        dev_process = app_create_dev_process(["yarn", "dev"])
        ui.success("Dev process started")

    with ui.app_dev_progress(
        f"[bold green]✔[/bold green] Preview URL: {ngrok_tunnel.public_url}"
    ) as progress:
        progress.add_task("", total=None)
        webbrowser.open((ngrok_tunnel.public_url))
        for line in iter(dev_process.stdout.readline, ""):  # type: ignore
            print(line.decode())


def _ngrok_answer_validate(answers, current):
    return bool(current)
