---
title: "Lessons learned template: a retrospective and decision log built from what really happened"
description: "A free lessons learned template, retrospective template and decision log template for teams working with AI agents. Built from your git history, plan and numbers, not from memory."
slug: lessons
skill: lessons
plan: BUSINESS.md#decisions
part: review
---

# Lessons learned template: a retrospective and decision log built from what really happened

A retrospective usually asks people to remember the last two weeks. Recent
days loom largest. And when agents do much of the work, it's easy to lose
track of what they did.

This template reads what happened instead: what merged, what was undone, what
the goals said and what the numbers did. It fills the "Decisions" section of
BUSINESS.md in two parts, for founders and small teams. A decision log has one row per decision, so no agent
reopens something you settled. Below it, the lessons for the period.

## What goes in it

| Part | What it answers |
|---|---|
| Decisions table | One row per decision: date, decision, why, who decided, source |
| What we learned | What happened, and what you do differently now |
| Did it work? | For each thing shipped for a focus: the number before and after, or "can't be judged" |
| Sources | Where each fact came from |

Keep the 8 latest decisions and 3 lessons. Older ones move to
BUSINESS-archive.md. Git keeps the rest.

## How to do it

1. **Pick the period.** Two weeks is a good default. Write it as dates.
2. **Read what happened.** Your git log, merged pull requests, failed CI runs,
   any incident notes. Write down what you couldn't read.
3. **Look for lesson candidates.** A change that was reverted. A feature
   followed by a fix within days. The same check failing twice. A task that
   slipped. A decision nobody wrote down. Also look for what went well.
4. **Check whether it worked.** For each ship a focus depended on, find the
   focus's number before and after. Write one of: moved, did not move, too early
   (and when to look again), or not measured yet. One reading proves nothing, and a
   ship that came before a move didn't necessarily cause it.
5. **Find the evidence for each lesson.** A commit, a PR number, a quote.
   It goes in the Sources line, not the lesson. No evidence, no
   lesson.
6. **Write a cause only if you can show it.** A commit message, a review
   comment, a log. Otherwise write "cause unknown". "Rushed" is a guess.
7. **Keep people out of the cause.** Write what happened and what the system
   allowed, not who did it.
8. **Say what each lesson changes.** A rule, one sentence starting "We" that anyone can follow
   without asking, goes to "How we decide". A decision goes in the
   table. Or neither: worth knowing, and that's all. Don't write a rule that
   lets an agent decide alone on anything that can't be undone.
9. **Record decisions only when someone made one.** A date, who decided, and a
   source. If the history only implies it, ask first: it goes to Open
   questions.
10. **Keep three lessons.** Past that, nobody acts on any.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in the "Decisions" section. To change a decision, add a new row that
replaces it.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. Its Decisions section has one row:
deposits only on first visits, always refundable in one click, decided by Jo on
8 Nov 2026. Under "What we learned, 6 to 20 Nov" it has three lessons: deposits went out,
came back and went out again in four days; reminders went out on UTC time and a
hotfix followed; and neither change can be judged because no-shows aren't
measured.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent do it

The `lessons` skill reads your git history, pull requests, focus and numbers,
drafts the lessons and decisions for you to pick from, and writes only what you
pick, in the Decisions section.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "write my lessons learned for the last two weeks".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need the same
history, so none repeats a mistake or reopens a settled decision,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=lessons)
keeps decisions, answers and what agents learned in one place, which every
agent reads before it starts.
