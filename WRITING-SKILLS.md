# How we write skills

For anyone adding or changing a skill. What BUSINESS.md should look like is
in [docs/how-business-md-works.md](docs/how-business-md-works.md); this file is
how the skills themselves are written. In the skills, `<skills folder>`
means the folder the skills are installed in (the one holding `business/`,
`review/` and the rest). `scripts/check_skills.py` checks
every skill against it.

## The parts of a SKILL.md

1. Front matter: `name` (the folder name) and `description`. The description
   leads with what the skill is ("Goals: ..."), then when to use it, one
   trigger per case.
2. **`# Title`** and a stance: one or two sentences, second person, on who the
   agent is in this job and what it won't do. Then the section it writes.
3. `## Before you start`: read BUSINESS.md.
4. `## Hard rules`: what the agent does, each with its reason. Say the
   behavior you want; keep "never" for real guardrails (secrets, production
   data), paired with what to do instead.
5. `## When tempted`: a two-column table, "When tempted to" and "Do this".
6. `## Steps`: numbered. Read the real data first. Ask with a suggestion:
   one round of numbered questions, each with the answer you'd suggest, so the
   person can reply "yes", "yes except 3", or correct it. When the person
   isn't there, record each question with
   `python3 <skills folder>/review/scripts/add_question.py`, which writes it
   to Open questions and `.business/decisions.json`. Each step ends with
   "Done when ...".
7. `## The section it writes`: its exact shape, copied from
   `skills/business/assets/BUSINESS.md`.
8. `## Examples`: one strong line and one weak one, with why. Examples
   come from the Tidewater example and are never copied into a real file.
9. `## The self-check`: run `python3 <skills folder>/review/scripts/lint_plan.py BUSINESS.md`
   (it says whether the repo looks public), then the skill's own checks. A failure is fixed or
   dropped, not softened.
10. `## When to run it again`: on a schedule (weekly, monthly) or after an
    event (a release, a new agent, a new hire).
11. **`## What to run next`.**

SKILL.md stays under 200 lines. Long detail goes in `references/`.

## The description

Lead with what the skill is and a colon ("Goals: ..."). What it does, when to use it, then four or
five phrases people actually say. Under 600 characters.

## Links

Skills never mention Annsa or any other product: they work for the person, not
for us. The README and the docs pages may link to annsa.ai once, at the end,
tagged `?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=<name>`.

## Lines every skill carries

Each skill says these somewhere. The checker looks for the first four; check the
last three by eye:

- It reads BUSINESS.md, and copies `<skills folder>/business/assets/BUSINESS.md` if it's missing.
- Unanswered questions are recorded with `add_question.py`.
- It makes sure agents are pointed at BUSINESS.md, as the Business skill's
  "Point agents at BUSINESS.md" step says.
- Its self-check runs `lint_plan.py`.
- In a Review run it sets `Status: draft`; the note at the top of BUSINESS.md
  tells readers what draft means.
- If the person says to keep it off the repo, it works in the folder they name.
- It changes no other file without the person's yes.

## Adding a skill

1. Make `skills/<name>/SKILL.md` with the parts above, under 200 lines.
2. Give it one section of BUSINESS.md, or make it a tool skill that runs a script (add it to `TOOLS` in the checker).
3. Add a plain-words page at `docs/<name>.md` and a row to the README table.
4. Run the checks below, then a cold run and a before-and-after run.

## Checks to run

```
python3 scripts/check_skills.py
python3 skills/review/scripts/lint_plan.py plans/examples/tidewater/BUSINESS.md
python3 skills/business-page/scripts/business_page.py plans/examples/tidewater/BUSINESS.md /tmp/page.html
```
