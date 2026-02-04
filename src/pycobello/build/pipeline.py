"""Build pipeline: discovery -> parse -> render -> write. Steps 5–7."""

from datetime import date
from pathlib import Path

from pycobello.build.assets import copy_assets
from pycobello.build.cache import file_sha256, load_cache, save_cache
from pycobello.build.result import BuildResult
from pycobello.build.writer import write_if_changed
from pycobello.config.models import PyCobelloSettings
from pycobello.content.discovery import discover_items
from pycobello.content.markdown import markdown_to_html
from pycobello.render.context import build_context
from pycobello.render.jinja import create_env, render_template
from pycobello.render.routing import output_path_for_item


def run_pipeline(
    config: PyCobelloSettings,
    project_root: str | Path = ".",
    clean: bool = False,
) -> BuildResult:
    """Run full build. Returns BuildResult with written/skipped/errors."""
    project_root = Path(project_root).resolve()
    content_dir = project_root / config.build.content_dir
    output_dir = project_root / config.build.output_dir
    theme_dir = project_root / config.build.theme_dir
    templates_dir = theme_dir / "templates"
    theme_static = theme_dir / "static"
    user_static = project_root / config.build.static_dir
    output_static = output_dir / "static"
    cache_dir = project_root / ".pycobello"
    cache_path = cache_dir / "cache.json"

    if clean and output_dir.exists():
        import shutil

        shutil.rmtree(output_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = load_cache(cache_path)

    from pycobello.plugins.manager import load_plugins

    load_plugins(config.plugins.enabled)

    written: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    # Collections as dict for discovery
    coll_dict = {
        "posts": config.collections.posts,
        "pages": config.collections.pages,
    }
    items = discover_items(
        content_dir,
        coll_dict,
        ignore=config.build.ignore,
    )

    site_dict = {
        "title": config.site.title,
        "base_url": config.site.base_url,
        "author": config.site.author,
    }

    posts = [i for i in items if i.kind.value == "post"]
    pages = [i for i in items if i.kind.value == "page"]
    posts_sorted = sorted(
        posts,
        key=lambda x: x.date or date.min,
        reverse=True,
    )
    collections_dict = {
        "posts": [_item_to_ctx(i, markdown_to_html(i.body_markdown)) for i in posts_sorted],
        "pages": [_item_to_ctx(i, markdown_to_html(i.body_markdown)) for i in pages],
    }

    env = create_env(templates_dir, site_dict, collections_dict)

    # Index page
    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "index.html"
    index_ctx = build_context(site_dict, collections_dict)
    index_content = render_template(env, "index.html", index_ctx)
    out_key = "index.html"
    cached_out = (cache.get("outputs") or {}).get(out_key, {}).get("sha256")
    did_write, new_hash = write_if_changed(index_path, index_content, cached_out)
    if did_write:
        written.append(str(index_path))
    else:
        skipped.append(str(index_path))
    cache.setdefault("outputs", {})[out_key] = {"sha256": new_hash}

    # Each post and page
    for item in items:
        out_path = output_path_for_item(
            output_dir,
            item.url_path,
            clean_urls=config.build.clean_urls,
        )
        template_name = item.template or (
            config.collections.posts.template
            if item.kind.value == "post"
            else config.collections.pages.template
        )
        html = markdown_to_html(item.body_markdown)
        ctx = build_context(
            site_dict,
            collections_dict,
            page=_item_to_ctx(item, html) if item.kind.value == "page" else None,
            post=_item_to_ctx(item, html) if item.kind.value == "post" else None,
        )
        try:
            content = render_template(env, template_name, ctx)
        except Exception as e:
            errors.append(f"{item.source_path}: {e}")
            continue
        rel_out = str(out_path.relative_to(output_dir))
        cached_out = (cache.get("outputs") or {}).get(rel_out, {}).get("sha256")
        did_write, new_hash = write_if_changed(out_path, content, cached_out)
        if did_write:
            written.append(str(out_path))
        else:
            skipped.append(str(out_path))
        cache.setdefault("outputs", {})[rel_out] = {"sha256": new_hash}
        cache.setdefault("source_to_output", {})[str(item.source_path)] = rel_out
        # Record source file in cache for incremental invalidation
        try:
            st = item.source_path.stat()
            cache.setdefault("files", {})[str(item.source_path)] = {
                "mtime": st.st_mtime,
                "size": st.st_size,
                "sha256": file_sha256(item.source_path),
            }
        except OSError:
            pass

    copy_assets(theme_static, user_static, output_static)

    save_cache(cache_path, cache)
    return BuildResult(written=written, skipped=skipped, errors=errors)


def _item_to_ctx(item, html: str) -> dict:
    return {
        "title": item.front_matter.get("title", ""),
        "slug": item.slug,
        "url_path": item.url_path,
        "date": item.date,
        "content": html,
        "front_matter": item.front_matter,
    }
