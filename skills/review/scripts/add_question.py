#!/usr/bin/env python3
"""Add one open question to BUSINESS.md and .business/decisions.json.

    python3 add_question.py BUSINESS.md --for Jo --skill goals \\
        --question "Who owns keeping clinics?" --why "Clinics that left rose three months running." \\
        --option "Jo, for now*" --option "Leave unowned" [--multi] [--first]

A trailing * marks the recommended option: exactly one, or at least one with
--multi. The question goes under "## Open questions" as
"- **For <who>:** <question>" and into .business/decisions.json next to
BUSINESS.md. --first puts it at the top of both (a money mismatch goes first).
Open questions holds seven at most; past that, the question goes to
decisions.json only, so it still reaches the decide page. A question already
recorded is not added twice. Questions written into BUSINESS.md by hand are
copied into decisions.json first, so none is lost and all reach the decide
page. In a git repo, .business/ is added to .gitignore.
Private details are refused, and so is money when the repo looks public.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_plan import DATE, MONEY, PRIVATE, is_test_value, repo_visibility  # noqa: E402

MAX_OPEN = 7
PLACEHOLDER = re.compile(r"<[A-Za-z][\w -]*>")
LINE_RE = re.compile(r"^- \*\*For (.+?):\*\*\s*(.+?)\s*$")


def norm(q):
    """Compare questions without case, spacing or end punctuation."""
    return re.sub(r"[\s?.!]+$", "", " ".join(q.split())).lower()


def problem(text, public):
    for label, pat in PRIVATE:
        if any(not is_test_value(m.group(0)) for m in pat.finditer(text)):
            return label
    if public and MONEY.search(DATE.sub("", text)):
        return "an amount of money (the repo looks public)"
    return None


def open_section(text):
    """(start, end) of the Open questions body, or None."""
    m = re.search(r"^## Open questions[^\n]*\n", text, re.M)
    if not m:
        return None
    nxt = re.search(r"^## ", text[m.end():], re.M)
    return m.end(), (m.end() + nxt.start() if nxt else len(text))


def main():
    ap = argparse.ArgumentParser(description="Add one open question to BUSINESS.md and .business/decisions.json.")
    ap.add_argument("business_md")
    ap.add_argument("--for", dest="who", required=True, help="who decides, by name or role")
    ap.add_argument("--skill", required=True, help="the skill asking, e.g. goals")
    ap.add_argument("--question", required=True)
    ap.add_argument("--why", default="", help="what you found, in one or two sentences")
    ap.add_argument("--option", action="append", default=[], help="an answer; end it with * if recommended")
    ap.add_argument("--multi", action="store_true", help="the person may pick more than one option")
    ap.add_argument("--first", action="store_true", help="put it first (a money mismatch goes first)")
    a = ap.parse_args()

    path = Path(a.business_md)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as err:
        print(f"add_question.py: cannot read {path}: {err.strerror}")
        return 2
    who, question = a.who.strip(), " ".join(a.question.split())
    if not who or PLACEHOLDER.search(who) or PLACEHOLDER.search(question):
        print("add_question.py: --for and --question need real text, not a placeholder like <who>")
        return 2
    if len(question.split()) < 3:
        print("add_question.py: --question needs a whole question (three words or more)")
        return 2
    options = [{"label": o.strip().rstrip("*").strip(), **({"recommended": True} if o.strip().endswith("*") else {})}
               for o in a.option if o.strip().rstrip("*").strip()]
    recs = sum(1 for o in options if o.get("recommended"))
    if len(options) < 2:
        print("add_question.py: give at least two --option values")
        return 2
    if recs == 0 or (recs > 1 and not a.multi):
        print("add_question.py: mark exactly one --option as recommended with a trailing * (or use --multi)")
        return 2
    public = repo_visibility(path)[0] == "public"
    fields = [("--for", who), ("--question", question), ("--why", a.why)] + [("--option", o["label"]) for o in options]
    for flag, field in fields:
        label = problem(field, public)
        if label:
            print(f"add_question.py: {label} in {flag} {field!r}; take it out")
            return 1

    # .business/decisions.json: the full list, which feeds the decide page
    folder = path.resolve().parent / ".business"
    folder.mkdir(exist_ok=True)
    dj = folder / "decisions.json"
    try:
        items = json.loads(dj.read_text(encoding="utf-8")) if dj.exists() else []
    except json.JSONDecodeError:
        print(f"add_question.py: {dj} is not valid JSON; fix or delete it first")
        return 2
    # copy questions written into BUSINESS.md by hand, so none is lost
    sec = open_section(text)
    known = {norm(q.get("question", "")) for q in items}
    if sec:
        for l in text[sec[0]:sec[1]].splitlines():
            m = LINE_RE.match(l)
            if m and "<" not in m.group(1) and norm(m.group(2)) not in known:
                items.append({"id": "", "skill": "by hand", "for": m.group(1).strip(), "question": m.group(2).strip(),
                              "why": "", "multi": False, "options": []})
                known.add(norm(m.group(2)))
    if norm(question) in known:
        for i, q in enumerate(items, 1):
            q["id"] = f"Q{i}"
        dj.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"already recorded, nothing added: {question}")
        return 0
    entry = {"id": "", "skill": a.skill, "for": who, "question": question, "why": a.why,
             "multi": a.multi, "options": options}
    if a.first:
        items.insert(0, entry)
    else:
        items.append(entry)
    for i, q in enumerate(items, 1):
        q["id"] = f"Q{i}"
    dj.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # BUSINESS.md: Open questions, seven at most
    line = f"- **For {who}:** {question}"
    sec = open_section(text)
    if not sec:
        text = text.rstrip("\n") + "\n\n## Open questions\n\nWhat we're still deciding, and who decides.\n\n" + line + "\n"
        where = "Open questions"
    else:
        start, end = sec
        body = re.sub(r"^- \*\*For <who>:\*\*.*\n?", "", text[start:end], flags=re.M)
        lines = body.rstrip("\n").split("\n")
        idx = [i for i, l in enumerate(lines) if l.startswith("- **For ")]
        if len(idx) >= MAX_OPEN and not a.first:
            where = "the decide page only (Open questions already holds seven)"
        else:
            if not idx:
                if lines and lines[-1].strip():
                    lines.append("")
                lines.append(line)
            elif a.first:
                if len(idx) >= MAX_OPEN:  # the last one moves to the decide page only
                    del lines[idx[-1]]
                lines.insert(idx[0], line)
            else:
                lines.insert(idx[-1] + 1, line)
            where = "Open questions" + (", first" if a.first else "")
        new_body = "\n".join(lines).rstrip("\n") + "\n" + ("\n" if end < len(text) else "")
        text = text[:start] + new_body + text[end:].lstrip("\n")
    path.write_text(text, encoding="utf-8")

    # .gitignore, in a git repo only
    root = path.resolve().parent
    if (root / ".git").exists():
        gi = root / ".gitignore"
        cur = gi.read_text(encoding="utf-8") if gi.exists() else ""
        if not re.search(r"^/?\.business/?\s*$", cur, re.M):
            gi.write_text(cur + ("" if cur.endswith("\n") or not cur else "\n") + ".business/\n", encoding="utf-8")

    print(f"added to {where}: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
