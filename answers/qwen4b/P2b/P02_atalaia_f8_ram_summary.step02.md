To update the API endpoint to serve `free_ram_mb` from `/proc/meminfo`, I need to add the `/api/system` route to `src/atalaia/api.py`. This route will call the `free_ram_mb` function imported from `.detectors` and return its result as JSON.

Here is the updated `src/atalaia/api.py`:

```python
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
import json

from .models import Project
from .detectors import (
    free_ram_mb,
    docker_containers,
    docker_ports,
    probe_docker,
    probe_port_owned,
    probe_process,
    ram_for_path,
    process_cwd,
)
from .scanner import discover_projects
from .detail import git_info, read_readme, tail_log, uptime_seconds
from .actions import run_action, action_log_tail, declared_actions
from .archive import load_archived, archive, unarchive
from .ids import project_id


def create_app(discover=None, web_dir: Optional[Path] = None):
    app = FastAPI(docs_url=None, redoc_url=None)

    # Default discover function
    if discover is None:
        def default_discover(roots):
            return discover_projects(roots)
        discover = default_discover

    # Static files setup
    static_dir = None
    index_file = None
    if web_dir:
        static_dir = web_dir / "static"
        index_file = web_dir / "index.html"

    @app.get("/")
    async def root():
        if index_file and index_file.exists():
            content = index_file.read_text()
            return Response(content=content, media_type="text/html")
        return JSONResponse({"error": "Index not found"}, status_code=404)

    if static_dir and static_dir.exists():
        from fastapi.staticfiles import StaticFiles
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/api/system")
    async def system_info():
        ram = free_ram_mb()
        return {"free_ram_mb": ram}

    @app.get("/api/projects")
    async def list_projects():
        projects = discover(None)
        archived_ids = load_archived()
        result = []
        for p in projects:
            pid = project_id(p.path)
```