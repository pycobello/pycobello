"""Build context dict for templates. Step 5."""


def build_context(
    site: dict,
    collections: dict,
    page: dict | None = None,
    post: dict | None = None,
) -> dict:
    """Context for Jinja: site, collections, current page/post."""
    ctx: dict = {"site": site, "collections": collections}
    if page is not None:
        ctx["page"] = page
    if post is not None:
        ctx["post"] = post
    return ctx
