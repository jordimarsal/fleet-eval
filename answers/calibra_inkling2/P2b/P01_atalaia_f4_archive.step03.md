=== FILE: src/atalaia/api.py ===
import subprocess
from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .actions import action_log_tail, declared_actions, run_action
from .archive import load_archived
import atalaia.archive as archive_module
from .detectors import probe_docker, probe_port, probe_process
from .detail import git_info, read_readme, tail_log, uptime_seconds
from .ids import project_id, resolve_id
from .models import Project, default_roots
from .scanner import discover_projects


class ActionBody(BaseModel):
    confirm: bool = False


SERVE_HOST = "127.0.0.1"
SERVE_PORT = 8901


def project_status(
    project: Project,
    uptime: int | None = None,
    docker_port: int | None = None,
    scan_port: int | None = None,
    archived: set[str] | None = None,
) -> dict:
    docker = probe_docker(project)
    open_port = probe_port(project.port or docker_port)
    process = probe_process(project)
    alive = docker == "up" or open_port or process == "up"
    pid = project_id(project.path)
    if archived is None:
        archived = load_archived()
    return {
        "id": pid,
        "name": project.name,
        "path": str(project.path),
        "type": project.kind,
        "status": "up" if alive else "down",
        "port": project.port or docker_port or scan_port,
        "uptime": uptime,
        "protected": project.protected,
        "archived": pid in archived,
    }


def detail_payload(
    project: Project,
    docker_port: int | None = None,
    scan_port: int | None = None,
    archived: set[str] | None = None,
) -> dict:
    payload = project_status(
        project, uptime=uptime_seconds(project), docker_port=docker_port, scan_port=scan_port, archived=archived
    )
    payload["git"] = git_info(project)
    payload["readme"] = read_readme(project)
    payload["log"] = tail_log(project)
    payload["actions"] = declared_actions(project)
    payload["action_log"] = action_log_tail(project)
    return payload


class NoCacheStaticFiles(StaticFiles):
    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response


def _projects_for(discover: Callable[[list[Path]], list[Project]]) -> list[Project]:
    roots = default_roots()
    try:
        found = discover(roots)
    except TypeError:
        found = discover([])
    return [p for p in found if isinstance(p, Project)]


def _find_by_id(pid: str, projects: list[Project] | None = None) -> Project | None:
    target = resolve_id(pid) or pid
    for proj in projects or []:
        if project_id(proj.path) == pid or project_id(proj.path) == target:
            return proj
    return None


def create_app(discover=None, web_dir: Path | str | None = None) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    def current_projects() -> list[Project]:
        if discover is None:
            return discover_projects(default_roots())
        return _projects_for(discover)

    @app.get("/", include_in_schema=False)
    async def index():
        root = Path(web_dir) if web_dir else Path(__file__).resolve().parents[2] / "web"
        index_path = root / "index.html"
        if not index_path.is_file():
            raise HTTPException(404, detail="not found")
        response = FileResponse(index_path)
        response.headers["Cache-Control"] = "no-cache"
        return response

    if web_dir or (Path(__file__).resolve().parents[2] / "web").exists():
        static_root = Path(web_dir) if web_dir else Path(__file__).resolve().parents[2] / "web"
        app.mount("/static", NoCacheStaticFiles(directory=str(static_root)), name="static")

    @app.get("/api/projects")
    async def list_projects():
        projects = current_projects()
        archived = load_archived()
        return [project_status(p, archived=archived) for p in projects]

    @app.get("/api/projects/{pid}")
    async def get_project(pid: str):
        projects = current_projects()
        project = _find_by_id(pid, projects=projects)
        if project is None:
            raise HTTPException(404, detail="unknown project")
        archived = load_archived()
        return detail_payload(project, scan_port=None, archived=archived)

    active_actions = {"start", "stop"}

    @app.post("/api/projects/{pid}/start")
    async def start_project(pid: str, request: Request):
        projects = current_projects()
        project = _find_by_id(pid, projects=projects)
        if project is None:
            raise HTTPException(404, detail="unknown project")
        declared = declared_actions(project)
        start_line = next((ln for ln in declared if isinstance(ln, dict) and ln.get("name") == "start"), None)
        if start_line is None:
            raise HTTPException(404, detail="unknown project")
        try:
            body_raw = await request.json()
        except Exception:
            body_raw = {}
        confirm = bool(body_raw.get("confirm", False)) if isinstance(body_raw, dict) else False
        if project.protected and not confirm:
            raise HTTPException(403, detail="confirm required")
        result = run_action(project, "start")
        pid_value = (result or {}).get("pid") if isinstance(result, dict) else None
        payload = {"status": "launched"}
        if pid_value is not None:
            payload["pid"] = int(pid_value)
        return JSONResponse(status_code=202, content=payload)

    @app.post("/api/projects/{pid}/stop")
    async def stop_project(pid: str, request: Request):
        projects = current_projects()
        project = _find_by_id(pid, projects=projects)
        if project is None:
            raise HTTPException(404, detail="unknown project")
        declared = declared_actions(project)
        stop_line = next((ln for ln in declared if isinstance(ln, dict) and ln.get("name") == "stop"), None)
        if stop_line is None:
            raise HTTPException(404, detail="unknown project")
        try:
            body_raw = await request.json()
        except Exception:
            body_raw = {}
        confirm = bool(body_raw.get("confirm", False)) if isinstance(body_raw, dict) else False
        if project.protected and not confirm:
            raise HTTPException(403, detail="confirm required")
        exit_code = run_action(project, "stop") or 0
        return JSONResponse(status_code=200, content={"status": "stopped", "exit": int(exit_code)})

    @app.post("/api/projects/{pid}/archive")
    async def archive_project(pid: str):
        projects = current_projects()
        if _find_by_id(pid, projects=projects) is None:
            raise HTTPException(404, detail="unknown project")
        archive_module.archive(pid)
        return JSONResponse(status_code=202, content={"status": "archived"})

    @app.post("/api/projects/{pid}/unarchive")
    async def unarchive_project(pid: str):
        projects = current_projects()
        if _find_by_id(pid, projects=projects) is None:
            raise HTTPException(404, detail="unknown project")
        archive_module.unarchive(pid)
        return JSONResponse(status_code=202, content={"status": "unarchived"})

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host=SERVE_HOST, port=SERVE_PORT)
=== END FILE ===