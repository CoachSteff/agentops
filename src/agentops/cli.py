from __future__ import annotations

import typer

from agentops import __version__
from agentops.paths import CONFIG_FILE

app = typer.Typer(name="agentops", help="AgentOps — companion browser for local agent services")


@app.callback(invoke_without_command=True)
def _main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        _run()


@app.command("run")
def run_cmd() -> None:
    """Launch the AgentOps window (default)."""
    _run()


@app.command("config-path")
def config_path_cmd() -> None:
    """Print the path to the user config file."""
    typer.echo(str(CONFIG_FILE))


def _run() -> None:
    from agentops.app import launch

    launch()
