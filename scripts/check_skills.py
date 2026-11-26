#!/usr/bin/env python3
"""Check every skills/*/SKILL.md against WRITING-SKILLS.md. Exit 1 on any failure.

    python3 scripts/check_skills.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "## Before you start",
    "## Hard rules",
    "## When tempted",
    "## Steps",
    ("## The section it writes", "## The sections it writes"),
    "## Examples",
    "## The self-check",
    "## When to run it again",
    "## What to run next",
]
TOOLS = {"business-page"}  # skills that run a script rather than write a section
UTM = "utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content="
# Writing rules we check automatically. The full guidance is WRITING-SKILLS.md.
WRITING_RULES = [
    (r"\bannsa\b", re.I, "names a product: skills work for the person using them, so they never pitch one"),
    (r"\bsign up\b", re.I, "asks the reader to sign up: no calls to action inside a skill"),
    (r"\bnon-technical\b", re.I, 'says "non-technical": say "new to coding" if it matters at all'),
    (r"\b(MUST|NEVER|ALWAYS)\b", 0, "shouts in capitals: plain words work better and read calmer"),
]


def check(path):
    problems = []
    text = path.read_text(encoding="utf-8")
    name = path.parent.name
    front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not front:
        return [f"{name}: no front matter"]
    meta = front.group(1)
    if not re.search(rf"^name:\s*{re.escape(name)}\s*$", meta, re.M):
        problems.append(f"{name}: front matter name must be '{name}'")
    if "description:" not in meta:
        problems.append(f"{name}: no description")
    else:
        desc = meta.split("description:", 1)[1]
        desc = " ".join(l.strip() for l in desc.splitlines() if l.strip() and l.strip() != ">")
        if len(desc) > 600:
            problems.append(f"{name}: description is {len(desc)} chars; keep it under 600")
        if not re.match(r"[A-Z][\w .\"-]{1,40}:", desc):
            problems.append(f"{name}: description should lead with what it is, then a colon ('Goals: ...')")
    if name in TOOLS:
        return problems  # a tool skill (it runs a script) writes no section: front matter only
    positions = []
    for heading in REQUIRED:
        options = heading if isinstance(heading, tuple) else (heading,)
        found = next((m for h in options for m in [re.search(rf"^{re.escape(h)}\s*$", text, re.M)] if m), None)
        heading = options[0]
        if not found:
            problems.append(f"{name}: missing '{heading}'")
        else:
            positions.append(found.start())
    if positions != sorted(positions):
        problems.append(f"{name}: sections are out of order (see WRITING-SKILLS.md)")
    if name != "review":
        for must, why in [("Open questions", "questions go to the Open questions section"),
                          ("add_question.py", "questions are recorded with add_question.py"),
                          ("lint_plan.py", "the self-check runs lint_plan.py"),
                          ("Point agents at BUSINESS.md", "agents are pointed at BUSINESS.md"),
                          ("CLAUDE.md, GEMINI.md or Copilot's file if they exist", "its files-it-may-write line names every agent file it may touch")]:
            if must not in text:
                problems.append(f"{name}: never mentions '{must}' ({why})")
    if "BUSINESS.md" not in text and name != "business":
        problems.append(f"{name}: never mentions BUSINESS.md")
    for pattern, flags, why in WRITING_RULES:
        if re.search(pattern, text, flags):
            problems.append(f"{name}: {why}")
    if len(text.splitlines()) > 200:
        problems.append(f"{name}: over 200 lines; move detail into references/")
    return problems


def main():
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skills:
        print("no skills found under skills/")
        return 1
    problems = [p for s in skills for p in check(s)]
    for page in [ROOT / "README.md"] + sorted(ROOT.glob("docs/*.md")):
        for link in re.findall(r"https://annsa\.ai[^\s)\"']*", page.read_text(encoding="utf-8")):
            if UTM not in link:
                problems.append(f"{page.relative_to(ROOT)}: annsa.ai link without its tag: {link}")
    prompt, tpl = ROOT / "plans/chat-prompt.md", ROOT / "skills/business/assets/BUSINESS.md"
    if prompt.exists() and tpl.read_text(encoding="utf-8").rstrip("\n") not in prompt.read_text(encoding="utf-8"):
        problems.append("plans/chat-prompt.md: its template differs from skills/business/assets/BUSINESS.md; copy it in again")
    for p in problems:
        print("FAIL", p)
    print(f"{len(skills)} skills checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
