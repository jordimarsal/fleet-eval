def _debrief_sink(
    settings: Settings, project: HarnessProject, feature_name: str
) -> debrief_log.DebriefSink:
    """The episode sink for one feature: resume its open log when a previous
    invocation left one unfinished (parked at a human gate), else open a fresh
    exec dir. Base is BW_DEBRIEF_ROOT (the central debrief evidence tree the MCP
    reads) or, unset, the project's own artifacts/ (self-contained mode)."""
    base = settings.debrief_root or (project.root / "artifacts")
    project_name = project.feature_list.project.name
    roles = {
        "planner": settings.role_model("planner"),
        "worker": settings.role_model("worker"),
        "reviewer": settings.role_model("reviewer"),
    }
    existing = debrief_log.find_open_episode(base, project_name, feature_name)
    if existing is not None:
        return debrief_log.DebriefSink(
            existing, feature=feature_name, engine=debrief_log.engine_build(), roles=roles
        )
    exec_id = f"exec{datetime.now(UTC):%Y%m%dT%H%MZ}"
    return debrief_log.DebriefSink(
        base / project_name / exec_id / f"{feature_name}.log",
        feature=feature_name,
        engine=debrief_log.engine_build(),
        roles=roles,
        run_id=f"{feature_name}-{datetime.now(UTC):%Y-%m-%dT%H-%MZ}",
    )

