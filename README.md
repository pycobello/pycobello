# pycobello

A blazing fast, dependency-light static site generator (SSG) for Python 3.12+.

- **Markdown + YAML front matter** → HTML
- **Jinja2 themes** (`.html` templates)
- **CLI-first** (Typer): `init`, `new`, `build`, `preview`, `check`, `deploy`
- **Incremental builds** with a JSON cache and write-avoidance by content hash
- **Preview server** via stdlib `http.server`; optional `--watch` with `[watch]` extra
- **Diagnostics** (`check`): duplicate URLs, required front matter, internal links
- **Plugin system** via Python entry points (`pycobello.plugins`)

## Install

```bash
uv add pycobello
# or
pip install pycobello
```

Optional watch support (live rebuild on file changes):

```bash
uv add "pycobello[watch]"
```

## Quick start

```bash
# Create a new site
pycobello init

# Build
pycobello build

# Serve the built site
pycobello preview
```

## Commands

| Command | Description |
|--------|-------------|
| `pycobello init [DIR]` | Create scaffold: `pycobello.yml`, content, theme, static |
| `pycobello new post "Title"` | Create a new post (with date prefix) |
| `pycobello new page "Title"` | Create a new page |
| `pycobello build [--clean]` | Build site into `dist/` (default: incremental) |
| `pycobello preview [--port 8000] [--watch]` | Serve `dist/`; optional watch + rebuild |
| `pycobello check` | Run diagnostics (URLs, front matter, links) |
| `pycobello deploy github-pages` | Generate GitHub Actions workflow for GitHub Pages |

## Config

Config file: `pycobello.yml` in the project root (YAML only).

- **site**: `title`, `base_url`, `author`
- **build**: `content_dir`, `theme_dir`, `static_dir`, `output_dir`, `clean_urls`, `ignore`
- **collections**: `posts` and `pages` (each: `path`, `url_prefix`, `template`)
- **plugins**: `enabled` (list of plugin names)

## Theme contract

Templates live in `theme/templates/`. Required:

- `base.html` – base layout
- `page.html` – pages
- `post.html` – posts
- `index.html` – index (blog listing)

Context: `site`, `collections`, current `page` or `post`. Helpers: `url_for`, filter `datefmt`.

## Development

```bash
uv sync --all-groups
uv run pre-commit install
```

Linting (ruff check) and formatting (ruff format) run automatically before each commit. To run them manually: `uv run ruff check .`, `uv run ruff format .`, and `uv run pytest`.

## License

Apache License 2.0. See [LICENSE](LICENSE).
