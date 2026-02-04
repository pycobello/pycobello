"""Write GitHub Pages workflow and print instructions. Step 11."""

from pathlib import Path


def generate_workflow(project_root: str) -> None:
    """Write .github/workflows/deploy.yml idempotently; print instructions."""
    root = Path(project_root).resolve()
    workflow_dir = root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    path = workflow_dir / "deploy.yml"
    content = _workflow_content()
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")
    print("Enable GitHub Pages: Repo → Settings → Pages → Source: GitHub Actions.")


def _workflow_content() -> str:
    return """# GitHub Pages deploy via pycobello
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      - name: Install dependencies
        run: uv sync
      - name: Build site
        run: uv run pycobello build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deploy
        uses: actions/deploy-pages@v4
"""
