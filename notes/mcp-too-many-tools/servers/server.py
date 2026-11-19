#!/usr/bin/env python3
"""Dummy stdio MCP server for the tool-count test.

Usage: server.py <server-name> <tools.json> <call-log>
tools.json is a list of {"name", "description", "params": {arg: description}}.
Every tools/call is appended to <call-log> as one JSON line and answered with
a fixed "ok: <server>.<tool>" text, so the only thing that differs between
runs is which tools the client sees.
"""
import json
import sys
import time

server, tools_path, log_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(tools_path) as f:
    TOOLS = json.load(f)


def schema(t):
    props = {k: {"type": "string", "description": v} for k, v in t.get("params", {}).items()}
    req = [k for k in t.get("params", {}) if not k.endswith("?")]
    props = {k.rstrip("?"): v for k, v in props.items()}
    return {"type": "object", "properties": props, "required": [r for r in req]}


def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except ValueError:
        continue
    method, mid = msg.get("method"), msg.get("id")
    if mid is None:
        continue  # notifications
    if method == "initialize":
        pv = msg.get("params", {}).get("protocolVersion", "2025-06-18")
        send({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": pv,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": server, "version": "0.1.0"}}})
    elif method == "tools/list":
        send({"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": t["name"], "description": t["description"], "inputSchema": schema(t)} for t in TOOLS]}})
    elif method == "tools/call":
        p = msg.get("params", {})
        with open(log_path, "a") as lf:
            lf.write(json.dumps({"t": time.time(), "server": server, "tool": p.get("name"),
                                 "args": p.get("arguments", {})}) + "\n")
        send({"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text", "text": f"ok: {server}.{p.get('name')}"}]}})
    elif method == "ping":
        send({"jsonrpc": "2.0", "id": mid, "result": {}})
    else:
        send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found"}})
