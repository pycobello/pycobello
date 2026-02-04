"""Jinja env and template rendering. Step 5."""

from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pycobello.render.context import build_context


def create_env(templates_dir: Path, site: dict, collections: dict) -> Environment:
    """Create Jinja environment with globals and filters."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(("html", "htm")),
    )
    env.globals["site"] = site
    env.globals["collections"] = collections
    env.globals["now"] = datetime.utcnow()

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
    return env


def render_template(
    env: Environment,
    template_name: str,
    context: dict,
) -> str:
    """Render a template with context."""
    t = env.get_template(template_name)
    return t.render(**context)
