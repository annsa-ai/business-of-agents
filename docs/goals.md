---
title: "Goals for founders: your top 3 business focus, one number each"
description: "A free goals template for founders working with AI agents. Your top three goals for the next 90 days, each with one number, an owner and the next move, with a worked example from a made-up company."
slug: goals
skill: goals
plan: BUSINESS.md#top-3-business-focus
part: review
---

# Goals for founders: your top 3 business focus, one number each

A goal list with several numbers per goal and no order leaves an agent to pick
whichever number moved, then ask you which goal comes first, because nothing in
the file says.

A goal here is an outcome with one number that says whether it's happening. You
hold three at most, ranked. The rank sets the working order, so no person or
agent has to ask which thing is first. They live in the "Top 3 Business Focus"
section of BUSINESS.md.

## What goes in it

Each focus is one of four types: Profit, Customer, People or Purpose.

| Part | What it answers |
|---|---|
| Until | The date the focus runs to. Focus 1 comes first |
| Type and outcome | Profit, Customer, People or Purpose, then what becomes true, in plain words |
| Number | The one number that says it's happening: now, target and date |
| Owner | The one person or agent who answers for it |
| Next | The one move that matters most right now |
| Not doing now | What you cut, and why |
| Sources | Where each fact came from |

## How to do it

1. **Pick your period.** The next 90 days. Write the end as a date,
   "28 Feb 2027", not "Q1".
2. **Write what a win looks like.** "What would make the next 90 days a
   win?" Aim for three outcomes at most. "Launch the blog" is an activity.
   "Founders find us without us pitching" is an outcome.
3. **Pick a type for each.** Profit (money in), Customer (what they get or
   say), People (your team) or Purpose (why you exist). It keeps the three
   from all being the same kind of goal.
4. **Give each one number.** The one number that would tell you it's working.
   If you can't think of one, the goal isn't ready. Its first job is to
   measure it.
5. **Say where you can read it today.** A dashboard, a CSV, a database
   query. If you can't read it, write `unknown` for now. Never guess a starting
   point.
6. **Set the target, and say why.** A target is a proposal, not data: "60 by
   28 Feb, because the last two months added 5 and 4". If you can't judge it
   until you have a first reading, write "not measured yet".
7. **Name an owner and the next move.** One owner each. The next move is one
   step, not a plan. An answer you need from someone goes in Open questions.
8. **Rank them, and write what you're not doing.** Focus 1 beats focus 2
   whenever they compete. One line for each thing you cut, and why.
9. **Read the numbers weekly.** Rewrite the focus when one is won, clearly
   lost, or the period ends.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in the "Top 3 Business Focus" section. Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file). The section tells agents to work focus 1 before focus 2.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. It has two focus items, both Customer.
1: "More clinics pay for Tidewater every month", active clinics 43 to 60 by 28
Feb, owner Jo, next Jo calls clinics to win about 4 more a month. 2: "Fewer
no-shows for clinics that take deposits", not measured yet, owner Jo until
named, next an agent starts measuring it. "Not doing now" holds a customer request the founder
has already said no to: Medicare and insurance codes on invoices.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent do it

The `goals` skill reads your repo, issues and recent commits, asks three
questions at most, drafts the focus for you to change, and writes only the Top 3
Business Focus section.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "write my goals".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools work from the
same goals, and you want the ranking kept current from what customers say,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=goals)
keeps your goals and the work under them in one plan every agent reads.
