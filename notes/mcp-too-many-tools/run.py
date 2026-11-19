#!/usr/bin/env python3
"""Run one request against one MCP config with headless Claude Code and
append one row to runs.csv.

Usage: run.py <config-name> <request-id> <set> <n_tools> <tool_search on|off> <rep> [model]
"""
import csv
import datetime
import json
import os
import subprocess
import sys
import tempfile

import catalog
import sanitize

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ["run_id", "date_utc", "cc_version", "model", "tool_search", "set", "n_tools", "n_lookalikes",
          "request_id", "correct_tool", "first_tool", "first_correct", "reached_correct", "calls_to_correct",
          "toolsearch_calls", "toolsearch_returned", "mcp_calls", "first_ctx_tokens", "input_tokens",
          "cache_read_tokens", "cache_creation_tokens", "output_tokens", "total_cost_usd", "num_turns"]
WORK = tempfile.mkdtemp(prefix="mcp-e4-")  # empty cwd: no CLAUDE.md, no project settings


def main():
    cfg, rid, kind, n, ts, rep = sys.argv[1:7]
    model = sys.argv[7] if len(sys.argv) > 7 else "sonnet"
    req = next(r for r in catalog.REQUESTS if r["id"] == rid)
    right = "mcp__%s__%s" % req["right"]
    env = dict(os.environ)
    if ts == "off":
        env["ENABLE_TOOL_SEARCH"] = "false"
    else:
        env.pop("ENABLE_TOOL_SEARCH", None)
    cmd = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=2G",
           "claude", "-p", req["text"], "--model", model,
           "--strict-mcp-config", "--mcp-config", os.path.join(HERE, "config", cfg + ".json"),
           "--setting-sources", "", "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--permission-mode", "bypassPermissions",
           "--disallowedTools", "Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,Task,Agent,NotebookEdit,TodoWrite,Skill",
           "--max-budget-usd", "0.40"]
    with open(os.path.join(HERE, "config", cfg + ".json")) as f:
        resolved = f.read().replace("{EVIDENCE}", HERE)
    cfg_path = os.path.join(WORK, "mcp.json")
    with open(cfg_path, "w") as f:
        f.write(resolved)
    cmd[cmd.index("--mcp-config") + 1] = cfg_path
    p = subprocess.run(cmd, cwd=WORK, env=env, capture_output=True, text=True, timeout=300)
    raw_dir = os.path.join(HERE, "logs", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    run_id = f"{cfg}-{rid}-{ts}-{rep}"
    events = []
    for line in p.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    with open(os.path.join(raw_dir, run_id + ".jsonl"), "w") as f:
        for e in events:
            if e.get("type") == "system" and e.get("subtype") == "init":
                e = {k: e.get(k) for k in ("type", "subtype", "model", "tools", "mcp_servers", "claude_code_version")}
            f.write(sanitize.clean_line(json.dumps(e)) + "\n")
    calls, ts_returned, first_ctx, version, used_model = [], [], None, "", model
    for e in events:
        if e.get("type") == "system" and e.get("subtype") == "init":
            version = e.get("claude_code_version", "")
            used_model = e.get("model", model)
        if e.get("type") == "assistant":
            msg = e.get("message", {})
            u = msg.get("usage", {})
            if first_ctx is None and u:
                first_ctx = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            for b in msg.get("content", []):
                if b.get("type") == "tool_use":
                    calls.append((b.get("name"), b.get("input")))
        if e.get("type") == "user":
            for b in (e.get("message", {}).get("content") or []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        for x in c:
                            if isinstance(x, dict) and x.get("type") == "tool_reference":
                                ts_returned.append(x.get("tool_name"))
    res = next((e for e in events if e.get("type") == "result"), {})
    u = res.get("usage", {})
    mcp = [c for c, _ in calls if c and c.startswith("mcp__")]
    tsc = sum(1 for c, _ in calls if c == "ToolSearch")
    first = mcp[0] if mcp else ""
    row = {"run_id": run_id, "date_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M"),
           "cc_version": version, "model": used_model, "tool_search": ts, "set": kind, "n_tools": next(c["n_tools"] for c in json.load(open(os.path.join(HERE, "config", "summary.json"))) if c["config"] == cfg),
           "n_lookalikes": len(catalog.lookalikes(int(n))) if kind == "lookalike" else 0,
           "request_id": rid, "correct_tool": right, "first_tool": first,
           "first_correct": "y" if first == right else "n",
           "reached_correct": "y" if right in mcp else "n",
           "calls_to_correct": (mcp.index(right) + 1) if right in mcp else "",
           "toolsearch_calls": tsc, "toolsearch_returned": "|".join(ts_returned), "mcp_calls": "|".join(mcp),
           "first_ctx_tokens": first_ctx or "", "input_tokens": u.get("input_tokens", ""),
           "cache_read_tokens": u.get("cache_read_input_tokens", ""),
           "cache_creation_tokens": u.get("cache_creation_input_tokens", ""),
           "output_tokens": u.get("output_tokens", ""), "total_cost_usd": res.get("total_cost_usd", ""),
           "num_turns": res.get("num_turns", "")}
    out = os.path.join(HERE, "runs.csv")
    new = not os.path.exists(out)
    with open(out, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(json.dumps({k: row[k] for k in ("run_id", "model", "first_tool", "first_correct", "toolsearch_calls",
                                           "toolsearch_returned", "first_ctx_tokens", "total_cost_usd")}))
    if p.returncode and not events:
        print(p.stderr[-800:], file=sys.stderr)


if __name__ == "__main__":
    main()
