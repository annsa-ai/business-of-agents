#!/usr/bin/env python3
"""Find every question your coding agents asked you, from the Claude Code and Codex session logs on this computer.

Reads Claude Code logs (~/.claude/projects) and Codex logs (~/.codex/sessions).
Makes no network calls. Writes one JSON line per ask to a file you choose.

    python3 find_asks.py --list                  # folders and counts only; never reads what was said
    python3 find_asks.py --days 14 --yes         # after the person says yes

Standard library only. Python 3.8+.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

HOME = Path.home()
SOURCES = {
    "claude-code": HOME / ".claude" / "projects",
    "codex": HOME / ".codex" / "sessions",
}

# Messages that look like a person's reply but were written by the tool, a hook or another agent.
NOT_A_PERSON = re.compile(
    r"^\s*(<|# AGENTS\.md|Base directory for this skill|Caveat:|\[Request interrupted)",
)

SECRET_PATTERNS = [
    (re.compile(r"\b(sk|pk|rk)[-_](live|test)[-_][A-Za-z0-9_\-]{8,}"), "[redacted]"),
    (re.compile(r"\b(sk|pk|rk)-[A-Za-z0-9_\-]{16,}"), "[redacted]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "[redacted]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "[redacted]"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"), "[redacted]"),
    (re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"), "[redacted]"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "[redacted]"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/\-]{12,}=*"), "[redacted]"),
    (re.compile(r"(?i)\b(password|passwd|pwd|passcode)\b\s*(?:is\s*)?[:=]?\s*\S+"), "[redacted]"),
    (re.compile(r"\b[0-9a-f]{40,}\b"), "[redacted]"),
    (re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), "[redacted]"),
    # Phone numbers: US (415) 555-0134, 415-555-0134, 415.555.0134, +1 415 555 0134; +61 4.., Australian 04xx xxx xxx / (02) xxxx xxxx, and other +cc numbers
    (re.compile(r"(?<![\w$.,])(?:\+?1[\s.\-]?)?(?:\(\d{3}\)[\s.\-]?|\d{3}[\s.\-])\d{3}[\s.\-]\d{4}(?![\d\-])"), "[redacted]"),
    (re.compile(r"(?<![\w])\+\d{1,3}[\s.\-]?\(?\d{1,4}\)?(?:[\s.\-]?\d{2,4}){2,4}(?!\d)"), "[redacted]"),
    (re.compile(r"(?<![\w])04\d{2}[\s.\-]?\d{3}[\s.\-]?\d{3}(?!\d)"), "[redacted]"),
    (re.compile(r"(?<![\w])\(?0\d\)?[\s.\-]?\d{3,4}[\s.\-]?\d{3,4}(?!\d)"), "[redacted]"),
]

QUESTION = re.compile(r"[^.?!\n]*\?")


def redact(text):
    for pattern, stand_in in SECRET_PATTERNS:
        text = pattern.sub(stand_in, text)
    return text


def clip(text, limit):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def is_a_real_question(q):
    """Drop fragments: URL bits, table cells, quoted examples, labels."""
    if len(q) < 15 or len(q.split()) < 3:
        return False
    if q.lower().startswith(("http", "www.")) or re.search(r"\S/\S*\?$", q):
        return False
    if q[0] in "\"'“‘`" or q.count("`") >= 2 or q.count('"') % 2 or (q.count("“") != q.count("”")):
        return False  # quoted text: an example prompt, a UI label, code
    return True


def questions_in(text):
    """The questions to the person: sentences ending in '?' in the last paragraph that has any."""
    if not text:
        return []
    # Ignore code blocks, table rows and block quotes: a '?' there is not a question to you.
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith(("|", ">"))]
    blocks = [b for b in re.split(r"\n\s*\n", "\n".join(lines)) if "?" in b]
    if not blocks:
        return []
    found = [q.strip(" -*#\t") for q in QUESTION.findall(blocks[-1])]
    return [q for q in found if is_a_real_question(q)]


def text_of(content, kinds):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") in kinds
        )
    return ""


def claude_code_asks(path):
    """Yield asks from one Claude Code session file."""
    last_text, last_ts, pending_tool = "", None, {}
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if record.get("isSidechain"):
                continue  # a subagent talking to its parent, not to you
            kind = record.get("type")
            message = record.get("message") or {}
            content = message.get("content")
            if kind == "assistant" and isinstance(content, list):
                for part in content:
                    if part.get("type") == "text" and part.get("text", "").strip():
                        last_text, last_ts = part["text"], record.get("timestamp")
                    elif part.get("type") == "tool_use" and part.get("name") == "AskUserQuestion":
                        questions = [q.get("question", "") for q in (part.get("input") or {}).get("questions", [])]
                        pending_tool[part.get("id")] = (questions, record.get("timestamp"))
            elif kind == "user":
                if isinstance(content, list) and any(p.get("type") == "tool_result" for p in content if isinstance(p, dict)):
                    for part in content:
                        tool_id = part.get("tool_use_id") if isinstance(part, dict) else None
                        if tool_id in pending_tool:
                            questions, ts = pending_tool.pop(tool_id)
                            reply = text_of(part.get("content"), {"text"})
                            for question in questions:
                                yield {"how": "question tool", "ts": ts, "question": question, "reply": reply,
                                       "project": record.get("cwd", "")}
                    continue
                if record.get("isMeta"):
                    continue
                reply = text_of(content, {"text"})
                if not reply.strip() or NOT_A_PERSON.match(reply):
                    continue
                for question in questions_in(last_text):
                    yield {"how": "in the reply", "ts": last_ts, "question": question, "reply": reply,
                           "project": record.get("cwd", "")}
                last_text = ""


def codex_asks(path):
    """Yield asks from one Codex session file. Encrypted turns are skipped."""
    last_text, last_ts, project = "", None, ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            payload = record.get("payload") or {}
            if record.get("type") == "turn_context":
                project = payload.get("cwd", project)
            if record.get("type") != "response_item" or payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role == "assistant":
                text = text_of(payload.get("content"), {"output_text"})
                if text.strip():
                    last_text, last_ts = text, record.get("timestamp")
            elif role == "user":
                reply = text_of(payload.get("content"), {"input_text"})
                if not reply.strip() or NOT_A_PERSON.match(reply):
                    continue
                for question in questions_in(last_text):
                    yield {"how": "in the reply", "ts": last_ts, "question": question, "reply": reply,
                           "project": project}
                last_text = ""



def encode(path):
    """Claude Code names a project's session folder after its absolute path, every non-alphanumeric as '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def project_folder(source, root, path):
    """Claude Code keeps one folder per project; subagent logs sit in folders under it."""
    return path.relative_to(root).parts[0] if source == "claude-code" else "codex sessions"


def cwd_matches(cwd, project):
    """True for the project folder itself or a worktree under <project>/.claude/worktrees/."""
    if not cwd:
        return False
    cwd = os.path.normpath(cwd)
    project = os.path.normpath(project)
    return cwd == project or cwd.startswith(project + "/.claude/worktrees/")


def in_project(source, path, project, root=None):
    """Decide from the folder name, or the first line only, whether a session belongs to the project."""
    if source == "claude-code":
        folder, enc = project_folder(source, root, path), encode(project)
        return folder == enc or folder.startswith(enc + "--claude-worktrees-")
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            first = json.loads(f.readline(65536))  # Codex writes the session's folder in its first line
    except (OSError, ValueError):
        return False
    return cwd_matches(((first or {}).get("payload") or {}).get("cwd", ""), project)


READERS = {"claude-code": claude_code_asks, "codex": codex_asks}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=14, help="how far back to read (default 14)")
    parser.add_argument("--source", choices=["all", *READERS], default="all")
    parser.add_argument("--project", default=None,
                        help="the project's folder path (default: the current folder's full path). "
                             "Matches that folder exactly, plus its worktrees under .claude/worktrees/")
    parser.add_argument("--all-projects", action="store_true",
                        help="read every project's sessions; ask the person first")
    parser.add_argument("--list", action="store_true",
                        help="only list the matching session folders and counts; reads folder names and the first line of Codex sessions, never what was said")
    parser.add_argument("--yes", action="store_true",
                        help="the person said yes to reading these sessions; without it nothing is read")
    parser.add_argument("--out", default=str(HOME / ".ask-less" / "asks.jsonl"),
                        help="where to write the asks (default ~/.ask-less/asks.jsonl, outside any repo)")
    args = parser.parse_args()
    if args.all_projects:
        args.project = ""
    else:
        args.project = str(Path(args.project or Path.cwd()).expanduser().resolve())

    since = time.time() - args.days * 86400
    since_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(since))
    out = Path(args.out).expanduser()

    if args.list or not args.yes:
        matched, elsewhere = {}, __import__("collections").Counter()
        for name, root in SOURCES.items():
            if args.source not in ("all", name) or not root.exists():
                continue
            for path in sorted(root.rglob("*.jsonl")):
                if path.stat().st_mtime < since:
                    continue
                if args.project and not in_project(name, path, args.project, root):
                    elsewhere[project_folder(name, root, path)] += 1
                    continue
                key = (name, project_folder(name, root, path))
                matched[key] = matched.get(key, 0) + 1
        print(f"Session logs from the last {args.days} days that would be read "
              f"({args.project or 'all projects'}); nothing said in them has been read:", file=sys.stderr)
        for (name, folder), n in sorted(matched.items()):
            print(f"  {n:5d}  {name}: {folder}", file=sys.stderr)
        if not matched:
            print("  none", file=sys.stderr)
        if elsewhere:
            print(f"{sum(elsewhere.values())} more are in other folders (names only; nothing said in them is read):", file=sys.stderr)
            for folder, n in elsewhere.most_common(8):
                print(f"  {n:5d}  {folder}", file=sys.stderr)
        if args.list:
            return 0
        print("Not read. Ask the person, then run again with --yes.", file=sys.stderr)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)

    files = sessions = asks = repeats = 0
    elsewhere = __import__("collections").Counter()
    with open(out, "w", encoding="utf-8") as sink:
        for name, root in SOURCES.items():
            if args.source not in ("all", name) or not root.exists():
                continue
            for path in sorted(root.rglob("*.jsonl")):
                if path.stat().st_mtime < since:
                    continue  # untouched since the window opened: nothing in it can be newer
                if args.project and not in_project(name, path, args.project, root):
                    elsewhere[project_folder(name, root, path)] += 1
                    continue  # another project's session: only its header line is read
                files += 1
                seen, counted = set(), False
                for ask in READERS[name](path):
                    if (ask.get("ts") or "") < since_iso:
                        continue  # asked before the window
                    if args.project and name == "codex" and not cwd_matches(ask.get("project"), args.project):
                        continue
                    key = re.sub(r"\W+", " ", ask["question"].lower()).strip()
                    if key in seen:
                        repeats += 1  # the same words again in this session ("Still open: ...")
                        continue
                    seen.add(key)
                    if not counted:
                        sessions, counted = sessions + 1, True
                    asks += 1
                    sink.write(json.dumps({
                        "id": f"a{asks}",
                        "source": name,
                        "session": path.stem[-12:],
                        # Asks with the same turn came in one message and share one next_message.
                        "turn": f"{path.stem[-6:]}-{ask.get('ts')}",
                        "project": os.path.basename(ask.get("project") or ""),
                        "ts": ask.get("ts"),
                        "how": ask["how"],
                        "question": redact(clip(ask["question"], 400)),
                        # The person's next message. Often the answer, sometimes about something else.
                        "next_message": redact(clip(ask["reply"], 300)),
                    }, ensure_ascii=False) + "\n")

    print(f"{asks} asks from {sessions} sessions ({files} log files read) in the last {args.days} days "
          f"({repeats} word-for-word repeats in the same session left out) -> {out}", file=sys.stderr)
    if elsewhere:
        print(f"{sum(elsewhere.values())} sessions from the same days are in other folders and were not read. "
              "If the person works on this project from those folders, ask before reading them:", file=sys.stderr)
        for folder, n in elsewhere.most_common(8):
            print(f"  {n:5d}  {folder}", file=sys.stderr)
    elif sessions == 0:
        print("No session logs found. Looked in: " + ", ".join(str(p) for p in SOURCES.values()), file=sys.stderr)


if __name__ == "__main__":
    main()
