#!/usr/bin/env python3
"""Strip local paths and session ids from raw stream-json logs.
Usage: sanitize.py <file>...   (rewrites in place)"""
import json
import os
import re
import sys

HOME = os.path.expanduser("~")


def scrub(o):
    if isinstance(o, dict):
        return {k: scrub(v) for k, v in o.items() if k not in ("session_id", "uuid", "parent_tool_use_id_session", "cwd")}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    if isinstance(o, str):
        o = re.sub(r"/tmp/mcp-e4-[A-Za-z0-9_]+", "<tmp>", o)
        o = re.sub(r"-tmp-mcp-e4-[A-Za-z0-9_-]+", "<tmp>", o)
        return o.replace(HOME, "~")
    return o


def clean_line(line):
    return json.dumps(scrub(json.loads(line)))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        lines = [clean_line(l) for l in open(p) if l.strip()]
        open(p, "w").write("\n".join(lines) + "\n")
