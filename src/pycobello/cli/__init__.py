"""Typer CLI app and commands."""

import typer

from pycobello import __version__

app = typer.Typer(
    name="pycobello",
    help="A blazing fast, dependency-light static site generator.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pycobello {__version__}")
        raise typer.Exit(0)


@app.callback()
def main(
    _: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """PyCobello SSG."""
    pass


@app.command()
def init(
    project_root: str = typer.Argument(
        ".",
        help="Directory to initialize (default: current).",
    ),
) -> None:
    """Create a new pycobello site scaffold."""
    from pycobello.cli._init import run_init

    run_init(project_root)


@app.command()
def new(
    kind: str = typer.Argument(..., help="Content type: 'post' or 'page'."),
    title: str = typer.Argument(..., help="Title of the post or page."),
    project_root: str = typer.Argument(".", help="Project root (default: current)."),
) -> None:
    """Create a new post or page."""
    from pycobello.cli._new import run_new

    run_new(kind, title, project_root)


@app.command()
def build(
    project_root: str = typer.Argument(".", help="Project root."),
    clean: bool = typer.Option(False, "--clean", help="Clean output dir before build."),
) -> None:
    """Build the site."""
    from pycobello.cli._build import run_build

    run_build(project_root, clean=clean)


@app.command()
def preview(
    project_root: str = typer.Argument(".", help="Project root."),
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve on."),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch and rebuild on changes."),
) -> None:
    """Serve the built site; optionally watch and rebuild."""
    from pycobello.cli._preview import run_preview

    run_preview(project_root, port=port, watch=watch)


@app.command()
def check(
    project_root: str = typer.Argument(".", help="Project root."),
) -> None:
    """Run diagnostics (links, slugs, front matter)."""
    from pycobello.cli._check import run_check

    run_check(project_root)


@app.command("deploy")
def deploy_cmd(
    target: str = typer.Argument(..., help="Deploy target, e.g. 'github-pages'."),
    project_root: str = typer.Argument(".", help="Project root."),
) -> None:
    """Generate deploy workflow (e.g. github-pages)."""
    from pycobello.cli._deploy import run_deploy

    run_deploy(target, project_root)
