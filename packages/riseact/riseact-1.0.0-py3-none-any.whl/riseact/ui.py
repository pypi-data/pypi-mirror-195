from datetime import datetime

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import (Progress, RenderableColumn, SpinnerColumn,
                           TimeElapsedColumn)
from rich.table import Table

console = Console()


def table() -> Table:
    return Table(
        show_header=False,
        show_lines=True,
        highlight=True,
    )


def progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=False,
        console=console,
    )


def app_dev_progress(footer: str) -> Progress:
    return Progress(
        RenderableColumn(
            Panel(
                Padding(footer, 1),
            )
        ),
        expand=True,
    )


def log_asset_change(msg: str):
    log_time_display = datetime.now().strftime("[%X]")
    console.print(f"[log.time]{log_time_display}[/log.time] {msg}")


def success(msg: str):
    console.print(f"[bold green]✔[/bold green] {msg}")
