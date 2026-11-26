#!/usr/bin/env python3
"""Build decide.html from a round file and the template. No network calls.

    python3 build_decide.py round.json decide.html

round.json is written by the review skill: title, subtitle, card,
summary and groups of ranked questions. The shape is in
assets/round.example.json.
"""
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "decide-template.html"

PRIVATE = [  # same patterns as lint_plan.py, beside this script
    ("an API key or token", re.compile(r"\b(?:(?:sk|pk|rk)[-_](?:live|test)[-_]|(?:sk|pk|rk)-)[A-Za-z0-9_\-]{8,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}|\bxox[abprs]-[A-Za-z0-9\-]{10,}|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b|\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}|(?i:\bbearer\s+[A-Za-z0-9._~+/\-]{12,})")),
    ("a password", re.compile(r"(?i)\b(?:password|passwd|pwd)\b\s*[:=]\s*\S+")),
    ("an email address", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("a phone number", re.compile(r"(?<![\w$.,])(?:(?:\+?1[\s.\-]?)?(?:\(\d{3}\)[\s.\-]?|\d{3}[\s.\-])\d{3}[\s.\-]\d{4}|\+\d{1,3}[\s.\-]?\(?\d{1,4}\)?(?:[\s.\-]?\d{2,4}){2,4}|04\d{2}[\s.\-]?\d{3}[\s.\-]?\d{3}|1[38]00[\s.\-]?\d{3}[\s.\-]?\d{3}|\(?0\d\)?[\s.\-]?\d{4}[\s.\-]?\d{4})(?![\d\-])")),
    ("a name next to an amount of money", re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:paid|pays|owes|owe|owed|billed|invoiced|spent|is owed)\b[^.\n]{0,40}[$£€]\s?\d|[$£€]\s?[\d,]+(?:\.\d+)?[kKmM]?\s+(?:from|to|owed by|paid by)\s+[A-Z][a-z]+")),
]


def shape_problem(d):
    """The first way round.json differs from the expected shape, or None."""
    def s(x): return isinstance(x, str)
    if not isinstance(d, dict):
        return "the top level must be an object"
    for k in ("title", "subtitle"):
        if k in d and not s(d[k]):
            return f"'{k}' must be text"
    card = d.get("card", {})
    if not isinstance(card, dict):
        return "'card' must be an object"
    if not isinstance(card.get("moves", []), list) or not all(s(m) for m in card.get("moves", [])):
        return "'card.moves' must be a list of text"
    for k in ("kicker", "headline", "foot"):
        if k in card and not s(card[k]):
            return f"'card.{k}' must be text"
    summary = d.get("summary", [])
    if not isinstance(summary, list) or not all(isinstance(x, dict) and s(x.get("label", "")) and s(x.get("text", "")) for x in summary):
        return "'summary' must be a list of {label, text}"
    groups = d.get("groups", [])
    if not isinstance(groups, list):
        return "'groups' must be a list"
    for gi, g in enumerate(groups):
        if not isinstance(g, dict) or not isinstance(g.get("questions", []), list):
            return f"groups[{gi}] must be an object with a 'questions' list"
        for k in ("title", "intro"):
            if k in g and not s(g[k]):
                return f"groups[{gi}].{k} must be text"
        for qi, q in enumerate(g.get("questions", [])):
            where = f"groups[{gi}].questions[{qi}]"
            if not isinstance(q, dict):
                return f"{where} must be an object"
            for k in ("id", "question", "skill", "why", "for"):
                if k in q and not s(q[k]):
                    return f"{where}.{k} must be text"
            if "multi" in q and not isinstance(q["multi"], bool):
                return f"{where}.multi must be true or false"
            opts = q.get("options")
            if not opts:
                return f"{where} has no options yet: give it at least two, with one recommended"
            if not isinstance(opts, list) or len(opts) < 2 or not all(isinstance(o, dict) and s(o.get("label")) and o.get("label") for o in opts):
                return f"{where}.options must be a list of at least two {{label, recommended}}"
            if any("recommended" in o and not isinstance(o["recommended"], bool) for o in opts):
                return f"{where}.options: recommended must be true or false"
    return None


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    try:
        round_data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except OSError as err:
        print(f"build_decide.py: cannot read {sys.argv[1]}: {err.strerror}")
        return 2
    except (UnicodeDecodeError, json.JSONDecodeError) as err:
        print(f"build_decide.py: {sys.argv[1]} is not valid JSON: {err}")
        return 2
    bad = shape_problem(round_data)
    if bad:
        print(f"build_decide.py: {sys.argv[1]}: {bad}. See assets/round.example.json for the shape.")
        return 2
    seen = set()
    for group in round_data.get("groups", []):
        for q in group.get("questions", []):
            for key in ("id", "question", "options", "skill"):
                if not q.get(key):
                    raise SystemExit(f"question missing '{key}': {q}")
            if q["id"] in seen:
                raise SystemExit(f"{q['id']}: question ids must be unique")
            seen.add(q["id"])
            recs = sum(1 for o in q["options"] if o.get("recommended"))
            if recs == 0 or (recs > 1 and not q.get("multi")):
                raise SystemExit(f"{q['id']}: needs exactly one recommended option (several only for a pick-any question)")
    card = round_data.get("card", {})
    shared = list(card.get("moves", [])) + [card.get("headline", "")] + [s.get("text", "") for s in round_data.get("summary", [])]
    for text in shared:
        if re.search(r"\d", re.sub(r"(?i)\b(bet|goal|focus|step|question)\s+\d\b|\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b(\s+\d{4})?", "", text)):
            raise SystemExit(f"the card and summary hold no numbers (levels and moves only): {text!r}")
    for text in shared:
        for label, pat in PRIVATE:
            if pat.search(text):
                raise SystemExit(f"the card and summary hold no private details ({label}): {text!r}")
    for group in round_data.get("groups", []):
        for q in group.get("questions", []):  # digits are fine here; keys, emails, phones and a name next to money are not
            fields = [q.get("question", ""), q.get("why", "")] + [o.get("label", "") for o in q.get("options", [])]
            for text in fields:
                if not isinstance(text, str):
                    continue
                for label, pat in PRIVATE:
                    if pat.search(text):
                        raise SystemExit(f"{q['id']}: a question holds private details ({label}): {text!r}")
    page_text = [round_data.get("title", ""), round_data.get("subtitle", ""), card.get("kicker", ""), card.get("foot", "")]
    page_text += [s.get("label", "") for s in round_data.get("summary", [])]
    page_text += [x for g in round_data.get("groups", []) for x in (g.get("title", ""), g.get("intro", ""))]
    for text in page_text:
        for label, pat in PRIVATE:
            if isinstance(text, str) and pat.search(text):
                raise SystemExit(f"the page's titles hold private details ({label}): {text!r}")
    payload = json.dumps(round_data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__ROUND_JSON__", payload)
    try:
        Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
        Path(sys.argv[2]).write_text(html, encoding="utf-8")
    except OSError as err:
        raise SystemExit(f"build_decide.py: cannot write {sys.argv[2]}: {err.strerror}")
    count = sum(len(g.get("questions", [])) for g in round_data.get("groups", []))
    print(f"wrote {sys.argv[2]}: {count} questions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
