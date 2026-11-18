"""E1 step 1: clean the Kubernetes docs and build chunks for settings A, B, C, D.

Cleaning: drop YAML front matter (keep title for the heading path), replace
glossary_tooltip shortcodes with their text/term_id, drop other Hugo shortcodes,
turn [text](url) links into text. Tokens are counted with tiktoken cl100k_base.
"""
import json, os, re, sys
import tiktoken

ROOT = os.path.expanduser("<workdir>/k8s/content/en/docs")
OUT = os.path.expanduser("<workdir>/work")
enc = tiktoken.get_encoding("cl100k_base")

def clean(text):
    title = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm = text[3:end]
        m = re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M)
        title = m.group(1) if m else ""
        text = text[end + 4:]
    def tip(m):
        s = m.group(0)
        t = re.search(r'text="([^"]*)"', s) or re.search(r'term_id="([^"]*)"', s)
        return t.group(1) if t else ""
    text = re.sub(r"\{\{<\s*glossary_tooltip[^>]*>\}\}", tip, text)
    text = re.sub(r"\{\{[<%].*?[%>]\}\}", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text

def norm(s):
    s = s.lower().replace("`", "").replace("*", "")
    s = s.replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()

def windows(text, size, overlap):
    ids = enc.encode(text)
    if len(ids) <= size:
        return [text]
    out, step = [], size - overlap
    for i in range(0, len(ids), step):
        out.append(enc.decode(ids[i:i + size]))
        if i + size >= len(ids):
            break
    return out

def sections(title, text):
    """Split at Markdown headings outside code fences; yield (path, body)."""
    path = [title]
    cur, buf, fence = [title], [], False
    out = []
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{2,6})\s+(.*)$", line)
        if m:
            if "".join(buf).strip():
                out.append((list(cur), "\n".join(buf).strip()))
            level = len(m.group(1))
            path = path[:level - 1] + [m.group(2).strip()]
            cur, buf = list(path), [line]
        else:
            buf.append(line)
    if "".join(buf).strip():
        out.append((list(cur), "\n".join(buf).strip()))
    return out

def main():
    # Corpus subset (fixed before any run, to fit CPU time on this machine): 13 doc sections
    # whole, plus the top level of tasks/administer-cluster (its kubeadm/ and other subfolders left out).
    SUBS = ["concepts/workloads", "concepts/configuration", "concepts/containers", "concepts/storage",
            "concepts/services-networking", "concepts/overview", "concepts/architecture",
            "tasks/configure-pod-container", "tasks/manage-daemon", "tasks/access-application-cluster",
            "tasks/run-application", "tasks/job", "tasks/configmap-secret"]
    files = []
    for sub in SUBS:
        for d, _, fs in os.walk(os.path.join(ROOT, sub)):
            for f in sorted(fs):
                if f.endswith(".md"):
                    files.append(os.path.relpath(os.path.join(d, f), ROOT))
    top = os.path.join(ROOT, "tasks/administer-cluster")
    files += [f"tasks/administer-cluster/{f}" for f in sorted(os.listdir(top)) if f.endswith(".md")]
    files.sort()
    settings = {k: [] for k in "ABCD"}
    corpus_norm = {}
    for rel in files:
        title, text = clean(open(os.path.join(ROOT, rel), encoding="utf-8").read())
        corpus_norm[rel] = norm(text)
        section_word = "Concepts" if rel.startswith("concepts") else "Tasks"
        for k, (size, ov) in {"A": (500, 100), "B": (1000, 200)}.items():
            for i, w in enumerate(windows(text, size, ov)):
                settings[k].append({"id": f"{k}:{rel}#{i}", "file": rel, "text": w})
        n = 0
        for path, body in sections(title, text):
            hp = " > ".join([section_word] + [p for p in path if p])
            for w in windows(body, 500, 100):
                settings["C"].append({"id": f"C:{rel}#{n}", "file": rel, "text": f"{hp}\n\n{w}"})
                settings["D"].append({"id": f"D:{rel}#{n}", "file": rel, "text": w})
                n += 1
    for k, ch in settings.items():
        for c in ch:
            c["tokens"] = len(enc.encode(c["text"]))
        with open(f"{OUT}/chunks-{k}.jsonl", "w") as f:
            for c in ch:
                f.write(json.dumps(c) + "\n")
        print(k, len(ch), "chunks, mean tokens", sum(c["tokens"] for c in ch) // len(ch))
    print("files", len(files))
    # gold span check
    qs = [json.loads(l) for l in open(f"{OUT}/questions.jsonl")]
    for q in qs:
        g = norm(q["gold_span"])
        hits = [r for r, t in corpus_norm.items() if g in t]
        ok = q["gold_file"] in hits
        print(q["id"], "OK" if ok else "MISSING", len(hits), "files" if not ok else "")

if __name__ == "__main__":
    main()
