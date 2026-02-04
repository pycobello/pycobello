"""Init scaffold and new post/page. Step 3."""

from datetime import date
from pathlib import Path


def create_scaffold(project_root: str) -> None:
    """Create pycobello.yml, content, theme, static. Step 3."""
    root = Path(project_root).resolve()
    _write_config(root)
    _write_content(root)
    _write_theme(root)
    (root / "static").mkdir(parents=True, exist_ok=True)
    _update_gitignore(root)


def create_new(kind: str, title: str, project_root: str) -> None:
    """Create a new post or page. Step 3."""
    root = Path(project_root).resolve()
    if kind == "post":
        today = date.today().isoformat()
        slug = _slug(title)
        path = root / "content" / "posts" / f"{today}-{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\ntitle: {title!r}\ndate: {today}\n---\n\nWrite your post here.\n",
            encoding="utf-8",
        )
        print(f"Created {path}")
    elif kind == "page":
        slug = _slug(title)
        path = root / "content" / "pages" / f"{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\ntitle: {title!r}\n---\n\nWrite your page here.\n",
            encoding="utf-8",
        )
        print(f"Created {path}")
    else:
        raise SystemExit(f"Unknown kind: {kind}. Use 'post' or 'page'.")


def _slug(s: str) -> str:
    from slugify import slugify

    return slugify(s, lowercase=True)


def _write_config(root: Path) -> None:
    cfg = root / "pycobello.yml"
    if cfg.exists():
        print(f"{cfg} already exists; skipping.")
        return
    cfg.write_text(
        """# pycobello config
site:
  title: My Site
  base_url: ""
  author: ""

build:
  content_dir: content
  theme_dir: theme
  static_dir: static
  output_dir: dist
  clean_urls: true
  ignore: []

collections:
  posts:
    path: posts
    url_prefix: blog
    template: post.html
  pages:
    path: pages
    url_prefix: ""
    template: page.html

plugins:
  enabled: []
""",
        encoding="utf-8",
    )
    print(f"Created {cfg}")


def _write_content(root: Path) -> None:
    (root / "content" / "pages").mkdir(parents=True, exist_ok=True)
    (root / "content" / "posts").mkdir(parents=True, exist_ok=True)
    about = root / "content" / "pages" / "about.md"
    if not about.exists():
        about.write_text("---\ntitle: About\n---\n\nAbout this site.\n", encoding="utf-8")
        print(f"Created {about}")
    today = date.today().isoformat()
    hello = root / "content" / "posts" / f"{today}-hello.md"
    if not hello.exists():
        hello.write_text(
            f"---\ntitle: Hello\ndate: {today}\n---\n\nFirst post.\n",
            encoding="utf-8",
        )
        print(f"Created {hello}")


def _write_theme(root: Path) -> None:
    theme = root / "theme"
    (theme / "templates").mkdir(parents=True, exist_ok=True)
    (theme / "static").mkdir(parents=True, exist_ok=True)

    base = theme / "templates" / "base.html"
    if not base.exists():
        base.write_text(
            """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ site.title }}{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static/style.css') }}">
</head>
<body>
  {% block body %}{% endblock %}
</body>
</html>
""",
            encoding="utf-8",
        )
        print(f"Created {base}")

    page = theme / "templates" / "page.html"
    if not page.exists():
        page.write_text(
            """{% extends "base.html" %}
{% block title %}{{ page.title }} | {{ site.title }}{% endblock %}
{% block body %}
<article>
  <h1>{{ page.title }}</h1>
  {{ page.content | safe }}
</article>
{% endblock %}
""",
            encoding="utf-8",
        )
        print(f"Created {page}")

    post = theme / "templates" / "post.html"
    if not post.exists():
        post.write_text(
            """{% extends "base.html" %}
{% block title %}{{ post.title }} | {{ site.title }}{% endblock %}
{% block body %}
<article>
  <h1>{{ post.title }}</h1>
  <time>{{ post.date | datefmt }}</time>
  {{ post.content | safe }}
</article>
{% endblock %}
""",
            encoding="utf-8",
        )
        print(f"Created {post}")

    index = theme / "templates" / "index.html"
    if not index.exists():
        index.write_text(
            """{% extends "base.html" %}
{% block title %}{{ site.title }}{% endblock %}
{% block body %}
<header><h1>{{ site.title }}</h1></header>
<ul>
  {% for post in collections.posts %}
  <li><a href="{{ url_for(post.url_path) }}">{{ post.title }}</a> — {{ post.date | datefmt }}</li>
  {% endfor %}
</ul>
{% endblock %}
""",
            encoding="utf-8",
        )
        print(f"Created {index}")


def _update_gitignore(root: Path) -> None:
    gi = root / ".gitignore"
    additions = ["dist/", ".pycobello/"]
    if not gi.exists():
        gi.write_text("\n".join(additions) + "\n", encoding="utf-8")
        print(f"Created {gi}")
        return
    text = gi.read_text()
    missing = [a for a in additions if a not in text]
    if missing:
        text = text.rstrip() + "\n" + "\n".join(missing) + "\n"
        gi.write_text(text, encoding="utf-8")
        print(f"Updated {gi}")
