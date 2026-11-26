#!/usr/bin/env python3
"""Check a BUSINESS.md against "How BUSINESS.md reads" in docs/how-business-md-works.md.

    python3 lint_plan.py [--public | --private] BUSINESS.md

Prints whether the repo looks public, then one line per problem; exits 1 if there are any.

Public or private: with neither flag, the script decides. A LICENSE or LICENCE
file at the repo root, or `gh repo view` saying PUBLIC, means public. A file
outside git, or a repo with no remote or that gh calls PRIVATE, means private.
Anything else counts as public. The gh check is the only network call.

--public  public-repo mode. Any amount of money outside the Price line is a problem
          (amounts with $, £ or €, a currency code like AUD, or next to revenue,
          income, profit or sales; read the file once more yourself before you push)
          ("Revenue was $12,400", "Bright Dental: $79 a month"). Use it when the plan
          will sit in a public repository. Without it, only a named person next to an
          amount is flagged.
"""
import re
import subprocess
import sys
from pathlib import Path

SECTIONS = ["Top 3 Business Focus", "What we do", "Metrics", "Who owns what", "How we decide", "Decisions", "Open questions"]
JARGON = [r"\bplaybooks?\b", r"\bround\b", r"\bfoundations?\b", r"\bhard rule", r"\bbets?\b", r"\bnorth star\b",
          r"\bassumed\b", r"\b[A-Z]\d{1,2}\b(?=[:\s])", r"\bsuper ic\b", r"\bdecisions\.json\b", r"\bconflicts to settle\b", r"\bcohort\b", r"\bsame-week\b", r"\bvanity\b", r"\(Q\d+\)", r"\bMRR\b", r"\bARR\b", r"\bKPIs?\b", r"\bnet new\b", r"decide\.html"]
MAX_WORDS, MAX_LINES, MAX_CELL, MAX_BULLET = 25, 120, 20, 35

PRIVATE = [
    ("an API key or token", re.compile(r"\b(?:(?:sk|pk|rk)[-_](?:live|test)[-_]|(?:sk|pk|rk)-)[A-Za-z0-9_\-]{8,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}|\bxox[abprs]-[A-Za-z0-9\-]{10,}|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b|\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}|(?i:\bbearer\s+[A-Za-z0-9._~+/\-]{12,})")),
    ("a password", re.compile(r"(?i)\b(?:password|passwd|pwd)\b\s*[:=]\s*\S+|\bpassword\s+(?:is\s+)?(?=\S*\d)\S{6,}")),
    ("an email address", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("a phone number", re.compile(r"(?<![\w$.,])(?:(?:\+?1[\s.\-]?)?(?:\(\d{3}\)[\s.\-]?|\d{3}[\s.\-])\d{3}[\s.\-]\d{4}|\+\d{1,3}[\s.\-]?\(?\d{1,4}\)?(?:[\s.\-]?\d{2,4}){2,4}|04\d{2}[\s.\-]?\d{3}[\s.\-]?\d{3}|1[38]00[\s.\-]?\d{3}[\s.\-]?\d{3}|\(?0\d\)?[\s.\-]?\d{4}[\s.\-]?\d{4})(?![\d\-])")),
    ("a name next to an amount of money", re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:paid|pays|owes|owe|owed|billed|invoiced|spent|is owed)\b[^.\n]{0,40}[$£€]\s?\d|[$£€]\s?[\d,]+(?:\.\d+)?[kKmM]?\s+(?:from|to|owed by|paid by)\s+[A-Z][a-z]+")),
]

AMOUNT = r"(?:\d{1,3}(?:,\d{3})+|\d{4,}|\d+(?:\.\d+)?\s?[kKmM]\b)(?:\.\d+)?"  # 12,400 · 12400 · 12k · 1.2m
MONEY = re.compile(
    r"[$£€]\s?\d"                                             # a currency sign
    r"|\b(?:AUD|USD|EUR|GBP|NZD|CAD)\s?\d"                   # a currency code
    r"|\b(?:revenue|income|profit|turnover|MRR|ARR)\b[^.\n|]{0,25}?" + AMOUNT +  # a money word, then an amount-shaped number
    r"|\bsales\s*[:=]\s*" + AMOUNT + r"|\bearn(?:s|ed)?\b[^.\n|]{0,15}?" + AMOUNT,
    re.I)  # --public: money, with or without a sign. Dates, counts and the "Profit ·" label pass.
MONEY_ROW = re.compile(r"^\s*\|[^|]*\b(?:revenue|income|profit|turnover|MRR|ARR|money in|fees)\b[^|]*\|(.*)$", re.I)
AMOUNT_RE = re.compile(AMOUNT)
DATE = re.compile(r"\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b(?:\s+\d{4})?|\b(?:19|20)\d{2}\b", re.I)


TEST_DOMAINS = re.compile(r"@(?:[\w.\-]+\.)?(?:example\.(?:com|org|net)|[\w\-]+\.(?:invalid|test|example|localhost))$", re.I)


def is_test_value(found):
    """Obviously fake test values may appear in rules: reserved example emails and all-zero sandbox numbers."""
    if "@" in found:
        return bool(TEST_DOMAINS.search(found))
    national = re.sub(r"^\+\d{1,3}", "", found.strip())  # drop a country code
    digits = re.sub(r"\D", "", national).lstrip("0")
    return len(digits) >= 7 and set(digits[1:]) == {"0"}  # 400 000 000, 9000 0000 is real


def repo_visibility(path):
    """('public' | 'private', reason) for the repo holding path."""
    folder = path.resolve().parent
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=folder, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return "private", "git not available, so treated as outside a repo"
    if root.returncode != 0:
        return "private", "not in a git repo"
    top = Path(root.stdout.strip())
    if any((top / n).exists() for n in ("LICENSE", "LICENCE", "LICENSE.md", "LICENCE.md", "LICENSE.txt")):
        return "public", "a LICENSE file"
    remote = subprocess.run(["git", "remote"], cwd=top, capture_output=True, text=True).stdout.strip()
    if not remote:
        return "private", "no remote"
    try:
        gh = subprocess.run(["gh", "repo", "view", "--json", "visibility", "-q", ".visibility"],
                            cwd=top, capture_output=True, text=True, timeout=10)
        vis = gh.stdout.strip().upper()
        if vis in ("PRIVATE", "INTERNAL"):
            return "private", "gh says " + vis
        if vis == "PUBLIC":
            return "public", "gh says PUBLIC"
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "public", "can't tell, so treated as public (pass --private if it isn't)"


def strip(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "code", text)


def main():
    args = sys.argv[1:]
    forced = "public" if "--public" in args else "private" if "--private" in args else None
    args = [a for a in args if a not in ("--public", "--private")]
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return 2
    path = Path(args[0])
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"lint_plan.py: cannot read {path}: {getattr(err, 'strerror', None) or 'not valid UTF-8 text'}")
        return 2
    if forced:
        public, why = forced == "public", "--" + forced
    else:
        vis, why = repo_visibility(path)
        public = vis == "public"
    print(f"{path}: public repo: {'yes' if public else 'no'} ({why})")
    own = re.search(r"<!--\s*our words:(.*?)-->", raw, re.I)
    allowed = {w.strip().lower() for w in own.group(1).split(",")} if own else set()
    text = strip(raw)
    problems = []

    lines = raw.splitlines()
    if len(lines) > MAX_LINES:
        problems.append(f"{len(lines)} lines; keep it under {MAX_LINES} and move old decisions to BUSINESS-archive.md")
    top = re.split(r"^## ", text, maxsplit=1, flags=re.M)[0]
    note = " ".join(re.sub(r"^>\s?", "", l) for l in top.splitlines() if l.startswith(">"))
    note = re.sub(r"\s+", " ", note).lower()
    if "read it before you start" not in note and "reads it before they start" not in note:
        problems.append('missing the note at the top ("How we run ..., for people and agents. Read it before you start.")')

    heads = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, re.M)]
    missing = [s for s in SECTIONS if s not in heads]
    if missing:
        problems.append("missing sections: " + ", ".join(missing))
    order = [h for h in heads if h in SECTIONS]
    if order != [s for s in SECTIONS if s in order]:
        problems.append("sections out of order; expected: " + " / ".join(SECTIONS))

    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    for block in blocks:
        title, _, body = block.partition("\n")
        title = title.strip()
        if title not in SECTIONS or title == "Open questions":
            continue
        if "not written yet" in body.lower():
            continue
        if not re.search(r"^Sources:", body, re.M):
            problems.append(f'"{title}" has no Sources: line')
    oq = next((b for b in blocks if b.startswith("Open questions")), "")
    asked = [l for l in oq.splitlines() if l.startswith("- ")]
    if len(asked) > 7:
        problems.append(f"{len(asked)} open questions; keep the 7 that unblock most here, the rest on the decision page")
    decide = next((b for b in blocks if b.startswith("How we decide")), "")
    anyone = re.search(r"\*\*What anyone can do:\*\*\n((?:- .*\n?)+)", decide)
    if anyone:
        for l in anyone.group(1).splitlines():
            if l.startswith("- ") and not re.match(r"- (We|Our|Nobody|No one|Agents) ", l):
                problems.append(f'a rule under "What anyone can do" should start "We": {l[:50]}')
    def rows(name):
        blk = next((b for b in blocks if b.startswith(name)), "")
        return [l for l in blk.splitlines() if l.startswith("|") and not re.match(r"\|\s*:?-", l)][1:]
    for name, cap in (("Metrics", 5), ("Who owns what", 8), ("Decisions", 8)):
        if len(rows(name)) > cap:
            problems.append(f"{len(rows(name))} table rows in {name}; keep {cap} at most")
    rules = [l for l in decide.splitlines() if l.startswith("- ")]
    if len(rules) > 12:
        problems.append(f"{len(rules)} rules in How we decide; keep 12 at most")
    learned = re.search(r"\*\*What we learned[^\n]*\n((?:- .*\n?)+)", next((b for b in blocks if b.startswith("Decisions")), ""))
    if learned and len([l for l in learned.group(1).splitlines() if l.startswith("- ")]) > 3:
        problems.append("more than 3 lessons under What we learned")
    now = next((b for b in blocks if b.startswith("Top 3 Business Focus")), "")
    focus = [l for l in now.splitlines() if re.match(r"\d+\. ", l)]
    if len(focus) > 3:
        problems.append("more than 3 items in Top 3 Business Focus")
    for l in focus:
        if not re.match(r"\d+\. \*\*(Profit|Customer|People|Purpose) · ", l):
            problems.append(f"a focus needs a type (Profit, Customer, People or Purpose): {l[:50]}")
    for line in oq.splitlines():
        if line.startswith("- ") and not re.match(r"- \*\*For [^*]+:\*\*", line):
            problems.append(f'open question not addressed to a person ("- **For <who>:** ..."): {line[:60]}')

    for n, line in enumerate(strip(raw).splitlines(), 1):
        if line.startswith("|") and re.search(r"\b(awk|grep|sed|python3?|curl|psql)\b", line):
            problems.append(f"line {n}: a command in a table; put commands in scripts/metrics.sh")
        if line.startswith("|") and not re.match(r"\|\s*-", line):
            for cell in line.strip("|").split("|"):
                if len(cell.split()) > MAX_CELL:
                    problems.append(f"line {n}: a {len(cell.split())}-word table cell; keep cells under {MAX_CELL} words")
                    break
        if line.startswith(("|", "#", "Sources:", "Readings:")):
            continue
        if re.match(r"\s*(- |\d+\. )", line) and len(line.split()) > MAX_BULLET:
            problems.append(f"line {n}: a {len(line.split())}-word bullet; keep bullets under {MAX_BULLET} words")
        unquoted = re.sub(r'"[^"]*"|“[^”]*”', "", line)
        if re.search(r"\b(I|I'd|I'm|I've|my|me)\b", unquoted):
            problems.append(f"line {n}: write as \"we\", not \"I\" or \"my\" (outside quotes)")
        if re.search(r"\b[0-9a-f]{7}\b", line) and re.search(r"[a-f]", re.search(r"\b[0-9a-f]{7}\b", line).group(0)):
            problems.append(f"line {n}: commit hash in the text; put it in the Sources line")
        for pat in JARGON:
            m = re.search(pat, line, re.I if "A-Z" not in pat else 0)
            if m and (m.group(0).lower() in allowed or m.group(0).lower().rstrip("s") in allowed
                      or (re.fullmatch(r"[A-Z]\d{1,2}", m.group(0)) and m.group(0)[0].lower() + "n" in allowed)):
                continue
            if m:
                problems.append(f"line {n}: our word, not theirs: {m.group(0)!r}")
        for sentence in re.split(r"(?<=[.!?])\s+", re.sub(r"^\s*[-*\d.]+\s*", "", line)):
            words = len(sentence.split())
            if words > MAX_WORDS:
                problems.append(f"line {n}: {words}-word sentence; keep under {MAX_WORDS}")

    for n, line in enumerate(raw.splitlines(), 1):
        for label, pat in PRIVATE:
            if any(not is_test_value(m.group(0)) for m in pat.finditer(line)):
                problems.append(f"line {n}: {label}; keep private details out of the plan")
        row = MONEY_ROW.match(line)
        money_row = row and AMOUNT_RE.search(DATE.sub("", row.group(1)))
        if public and (MONEY.search(DATE.sub("", line)) or money_row) and not re.match(r"\s*(?:[-*]\s*)?\**Price", line):
            problems.append(f"line {n}: an amount of money; in a public repo only the Price line may hold one")

    for p in problems:
        print(f"{path}: {p}")
    if not problems:
        print(f"{path}: reads well")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
