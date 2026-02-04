"""Deploy command implementation."""


def run_deploy(target: str, project_root: str) -> None:
    """Generate deploy workflow. Implemented in Step 11."""
    from pycobello.deploy.github_pages import generate_workflow

    if target == "github-pages":
        generate_workflow(project_root)
    else:
        raise SystemExit(f"Unknown deploy target: {target}")
