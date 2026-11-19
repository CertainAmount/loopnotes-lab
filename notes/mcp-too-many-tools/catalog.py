#!/usr/bin/env python3
"""Tool catalog and config builder for the MCP tool-count test.

Sets (every set holds the 5 right tools, one per request):
  clean     - right tools + filler (write/admin actions no request needs)
  lookalike - right tools + lookalikes (same verb, other server; 1 per request
              at 10 tools, 2 per request from 25 up) + filler
  fixa      - lookalike-100 catalog with the servers that hold this request's
              lookalikes switched off (per request)
  fixb      - a task set of 10: the right tool + 9 filler tools, no lookalikes
Filler is taken in a fixed order, so the 10-tool set is inside the 25-tool
set, and so on.
Usage: catalog.py build   -> writes config/*.json and servers/tools/*.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SERVERS = ["github", "slack", "docs", "db", "ci", "flags", "observability"]

REQUESTS = [
    {"id": "R1", "text": "Find the recent code changes to the payments service that could explain today's outage.",
     "right": ("github", "list_commits")},
    {"id": "R2", "text": "What did the team say about the deploy freeze?",
     "right": ("slack", "search_messages")},
    {"id": "R3", "text": "Show me the runbook page for cache eviction.",
     "right": ("docs", "get_page")},
    {"id": "R4", "text": "Which feature flags are on for checkout in production?",
     "right": ("flags", "list_flags")},
    {"id": "R5", "text": "Did last night's CI run for the main branch fail?",
     "right": ("ci", "get_run")},
]

RIGHT = {
    ("github", "list_commits"): ("List commits in a repository, newest first, optionally filtered by path or date.", {"repo": "Repository name", "since?": "ISO date", "path?": "Path filter"}),
    ("slack", "search_messages"): ("Search messages across Slack channels the bot can read.", {"query": "Search text", "channel?": "Channel name"}),
    ("docs", "get_page"): ("Get a documentation page by its title.", {"title": "Page title"}),
    ("flags", "list_flags"): ("List feature flags and whether each is on, per environment.", {"environment?": "Environment name", "service?": "Service name"}),
    ("ci", "get_run"): ("Get the status and result of a CI pipeline run.", {"pipeline": "Pipeline name", "run?": "Run id or 'latest'"}),
}

# two lookalikes per request: same verb as the right tool, on another server
LOOKALIKES = {
    "R1": [("docs", "list_changes", "List recent changes to documentation pages.", {"space?": "Docs space"}),
           ("flags", "list_changes", "List recent changes to feature flag settings.", {"environment?": "Environment name"})],
    "R2": [("github", "search_issues", "Search issues and pull requests by text.", {"query": "Search text", "repo?": "Repository name"}),
           ("docs", "search", "Search all documentation pages by text.", {"query": "Search text"})],
    "R3": [("github", "get_file", "Get the contents of a file in a repository.", {"repo": "Repository name", "path": "File path"}),
           ("observability", "get_dashboard", "Get a monitoring dashboard by its name.", {"name": "Dashboard name"})],
    "R4": [("db", "list_settings", "List application settings rows from the config table.", {"service?": "Service name"}),
           ("ci", "list_env_vars", "List environment variables set for a pipeline.", {"pipeline": "Pipeline name"})],
    "R5": [("github", "get_check", "Get the status of a status check on a commit.", {"repo": "Repository name", "ref": "Commit or branch"}),
           ("observability", "get_job", "Get the status of a scheduled job.", {"job": "Job name"})],
}

# filler: write/admin actions no request needs (no list/search/get/find verbs)
FILLER_RAW = {
    "github": ["create_branch", "delete_branch", "merge_pull_request", "add_label", "remove_label", "assign_reviewer",
               "close_issue", "reopen_issue", "create_release", "archive_repository", "rename_branch", "add_collaborator",
               "fork_repository", "create_tag"],
    "slack": ["post_message", "set_status", "create_channel", "archive_channel", "invite_user", "pin_message",
              "add_reaction", "remove_reaction", "schedule_message", "rename_channel", "set_topic", "kick_user",
              "upload_file", "delete_message"],
    "docs": ["create_page", "update_page", "delete_page", "move_page", "rename_page", "add_comment", "restrict_page",
             "export_page", "watch_page", "copy_page", "archive_space", "add_attachment", "publish_draft", "add_page_label"],
    "db": ["create_index", "drop_index", "vacuum_table", "create_snapshot", "restore_snapshot", "grant_role",
           "revoke_role", "rotate_password", "kill_session", "analyze_table", "create_replica", "promote_replica",
           "truncate_staging", "set_parameter"],
    "ci": ["trigger_pipeline", "cancel_run", "retry_job", "pause_pipeline", "resume_pipeline", "add_secret",
           "delete_secret", "clear_cache", "approve_deploy", "rollback_deploy", "pin_runner", "drain_runner",
           "set_concurrency", "rename_pipeline"],
    "flags": ["create_flag", "toggle_flag", "archive_flag", "add_rule", "remove_rule", "set_rollout",
              "add_segment", "remove_segment", "schedule_toggle", "copy_flag", "rename_flag", "lock_flag",
              "set_default", "tag_flag"],
    "observability": ["create_alert", "mute_alert", "unmute_alert", "ack_incident", "resolve_incident",
                      "create_monitor", "delete_monitor", "set_threshold", "add_annotation", "create_slo",
                      "page_oncall", "rotate_api_key", "set_retention", "silence_host"],
}


def filler_list():
    """Round-robin across servers so every count spreads over servers."""
    out, i = [], 0
    while any(i < len(v) for v in FILLER_RAW.values()):
        for s in SERVERS:
            if i < len(FILLER_RAW[s]):
                name = FILLER_RAW[s][i]
                verb, _, noun = name.partition("_")
                out.append((s, name, f"{verb.capitalize()} {noun.replace('_', ' ')}.".replace("  ", " "),
                            {"target": f"The {noun.replace('_', ' ') or 'item'} to act on"}))
        i += 1
    return out


FILLER = filler_list()


def right_tools():
    return [(s, n, *RIGHT[(s, n)]) for (s, n) in [r["right"] for r in REQUESTS]]


def lookalikes(n):
    per = 1 if n < 25 else 2
    return [la for r in REQUESTS for la in LOOKALIKES[r["id"]][:per]]


def tool_set(kind, n, req=None):
    base = right_tools()
    if kind == "clean":
        return base + FILLER[: n - len(base)]
    if kind == "lookalike":
        la = lookalikes(n)
        return base + la + FILLER[: n - len(base) - len(la)]
    if kind == "fixa":
        full = tool_set("lookalike", 100)
        off = {s for (s, *_r) in LOOKALIKES[req["id"]]}
        return [t for t in full if t[0] not in off]
    if kind == "fixb":
        rs, rn = req["right"]
        own = [t for t in FILLER if t[0] == rs]
        other = [t for t in FILLER if t[0] != rs]
        return [(rs, rn, *RIGHT[(rs, rn)])] + (own + other)[:9]
    raise ValueError(kind)


def write_config(name, tools):
    tdir = os.path.join(HERE, "servers", "tools", name)
    os.makedirs(tdir, exist_ok=True)
    servers = {}
    for s in SERVERS:
        ts = [{"name": n, "description": d, "params": p} for (sv, n, d, p) in tools if sv == s]
        if not ts:
            continue
        path = os.path.join(tdir, f"{s}.json")
        with open(path, "w") as f:
            json.dump(ts, f, indent=1)
        servers[s] = {"type": "stdio", "command": "python3",
                      "args": ["-I", "{EVIDENCE}/servers/server.py", s,
                               "{EVIDENCE}/" + os.path.relpath(path, HERE), "{EVIDENCE}/logs/calls.jsonl"]}
    with open(os.path.join(HERE, "config", f"{name}.json"), "w") as f:
        json.dump({"mcpServers": servers}, f, indent=1)
    return {"config": name, "n_tools": len(tools), "servers": sorted(servers),
            "per_server": {s: sum(1 for t in tools if t[0] == s) for s in sorted(servers)}}


def build():
    summary = []
    for kind in ("clean", "lookalike"):
        for n in (10, 25, 50, 100):
            summary.append(write_config(f"{n}-{kind}", tool_set(kind, n)))
    for r in REQUESTS:
        summary.append(write_config(f"fixa-{r['id']}", tool_set("fixa", 100, r)))
        summary.append(write_config(f"fixb-{r['id']}", tool_set("fixb", 10, r)))
    with open(os.path.join(HERE, "config", "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    for s in summary:
        print(s["config"], s["n_tools"], s["per_server"])


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build()
