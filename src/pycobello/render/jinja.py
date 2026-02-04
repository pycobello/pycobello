"""Jinja env and template rendering. Step 5."""

from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_env(templates_dir: Path, site: dict, collections: dict) -> Environment:
    """Create Jinja environment with globals and filters."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(("html", "htm")),
    )
    env.globals["site"] = site
    env.globals["collections"] = collections
    env.globals["now"] = datetime.now(UTC)

    def url_for(path: str) -> str:
        base = (site.get("base_url") or "").rstrip("/")
        p = path if path.startswith("/") else f"/{path}"
        return f"{base}{p}"

    env.globals["url_for"] = url_for

    def datefmt(d: str | datetime | None, fmt: str = "%Y-%m-%d") -> str:
        if d is None:
            return ""
        if isinstance(d, datetime):
            return d.strftime(fmt)
        return str(d)

    env.filters["datefmt"] = datefmt
    _apply_plugin_jinja(env)
    return env


def _apply_plugin_jinja(env: Environment) -> None:
    """Add plugin-registered filters and globals to the Jinja env."""
    try:
        from pycobello.api.app import get_app

        app = get_app()
        env.globals.update(app.jinja_globals)
        env.filters.update(app.jinja_filters)
    except Exception:
        pass


def render_template(
    env: Environment,
    template_name: str,
    context: dict,
) -> str:
    """Render a template with context."""
    t = env.get_template(template_name)
    return t.render(**context)
