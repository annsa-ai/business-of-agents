---
title: "KPI dashboard template: the five numbers that show your business is working"
description: "A free KPI dashboard template for founders working with AI agents. Pick the few numbers that matter, define each one exactly, and keep the command that refreshes it, so every reading means the same thing."
slug: metrics
skill: metrics
plan: BUSINESS.md#metrics
part: review
---

# KPI dashboard template: the five numbers that show your business is working

A dashboard with thirty charts answers nothing. A dashboard with three numbers
and no definitions answers differently each week. When an agent updates it, it
may count test accounts, switch from weeks to months, or remember a number
instead of reading it.

This template is one short table in the "Metrics" section of BUSINESS.md. Each
number has its exact definition, the decision it feeds, and how it's
counted, in plain words. Any person or agent can read it again next week and get a
number that means the same thing.

## What goes in it

One table, five numbers at most.

| Column | What it answers |
|---|---|
| Number | The name. One per focus, copied from Top 3 Business Focus |
| Latest | The value, and the period it covers |
| Goal | The target and date, or none |
| How it's counted | The event, the unit, the window, the timezone, what's left out, and which file it comes from |
| If it moves, we | The decision the number feeds. No decision means nobody would act on it: leave it out |

Under the table: a Readings line with past values, one line on whether you're on
pace, and a Sources line with each source's last date. A number you want but can't read yet says
"not measured yet" and gets an open question.

## How to do it

1. **Start with your focus.** Take the one number for each of your top 3
   business focus items. Don't rename them.
2. **Add one value number if no focus says it.** It's the number that says
   customers are getting value. "Teams that sent a report this week" says
   value. "Signups" says interest. If a focus already says it, show it once.
3. **Add health numbers sparingly.** Failed payments, errors, or the share of
   signups that never start. Add one only if someone would act when it moves.
   Keep the total to five or fewer.
4. **Write the definition for each.** Two people reading it should get the
   same number. For a conversion rate, say whether it counts everyone who
   signed up in the period, or only those who acted within their first week. Name the timezone: a database day is usually UTC, yours is
   not.
5. **Leave out your own accounts.** Name how to exclude them: by email domain,
   a flag, or an id.
6. **Get each value by running something.** A query, an export, a CSV. Write
   down the command and the date. Never write a number you remember.
7. **Record the source's last date.** If it's older than one reading cycle,
   mark it stale.
8. **Check one number against something you can see.** A row count, a total
   you know. If it's off, say so. Don't adjust it.
9. **If you can't read it, say so.** Write "not measured yet" and add a question
   to Open questions about where it will come from.
10. **Change a definition on purpose.** Log the date and reason, and mark old
    readings "old definition". Never mix two definitions in one trend.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in the "Metrics" section. Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file). To update the numbers, an agent runs `scripts/metrics.sh`,
read-only, and asks before touching production. It never estimates a number.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. Its Metrics table has three numbers
built from two exports: active clinics (43 in October, up from 39, goal 60 by
28 Feb), trial to paid (3 of 12 in the week of 9 Nov), and a no-show rate that
isn't measured yet. Under it, a Readings line lists past values, and one line
says 60 needs about 4 more clinics a month and the last two months added 5 and
4. Open questions asks Jo which timezone the numbers use.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent do it

The `metrics` skill reads your top 3 focus and your data, writes each definition,
runs read-only commands to get each value, and asks before it touches anything
in production. It writes only the Metrics section.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "write the metrics for my business".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need the same
numbers, and you want each goal to carry its number next to its work,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=metrics)
keeps the metric on the goal itself, and the numbers sit where every agent reads them.
