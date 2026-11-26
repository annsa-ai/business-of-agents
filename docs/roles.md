---
title: "Job description template for people and AI agents"
description: "A free job description template for the people and the AI agents on your team. Write each role as outcomes, limits and a check, plus a short hiring job description example."
slug: roles
skill: roles
plan: BUSINESS.md#who-owns-what
part: review
---

# Job description template for people and AI agents

Your agents already have jobs. One writes features, one reviews pull requests,
one answers support. Each owns some outcomes and has limits, whether or not you
ever wrote them down. When two agents both think a thing is theirs, or neither
does, work gets dropped or done twice.

This template writes the jobs down, for people and agents in the same shape. It
starts with the "Who owns what" section of BUSINESS.md: each outcome and its one
owner. It's written for founders and small teams.

## What goes in it

| Part | What it answers |
|---|---|
| Who owns what | Each outcome, its one owner, whether that's a person or an agent, and where you know that from |
| The role in one line | What this role is for |
| Owns | The outcomes it's answerable for, matching the table |
| May decide alone | What it can do without asking: the "We ..." rules in How we decide |
| Comes back to a person | What it never decides alone: production data, money, sign-in, words customers read |
| Reads before starting | The files it reads first |
| How its work is checked | Who or what looks: a test, a review, a number |
| Hiring (optional) | The same shape for a human hire, plus the outcome they own in 90 days |

The table lives in BUSINESS.md. What each role may decide alone lives in "How
we decide".

## How to do it

1. **List the outcomes.** An outcome is a result someone answers for:
   "customers get an answer within a day", not "support". Take them from your
   top 3 business focus.
2. **Find who does each one now.** A person, an agent, or nobody. Doing the
   work isn't owning it. The owner is the one you say is accountable.
3. **Give each outcome one owner.** Not two. If two want it, pick one. The
   other helps.
4. **Write down where each owner line comes from.** A file, an agent
   definition, or "you said". No source, no line.
5. **List the outcomes nobody owns.** Say so plainly, and say what leaving them
   unowned costs. Don't hand them to an agent just to fill the table.
6. **Write a short description per role,** for people and agents alike, using
   the parts above. A role you know little about gets one line: "role to
   define".
7. **Set the limits.** Whatever can't be undone stays with a person for every
   role: production data, money, sign-in, words customers will read.
8. **Say how each role's work is checked.** If an agent does the work, it needs
   a check too.
9. **Show it to each person.** Nobody gets a role they haven't agreed to.
10. **Point your agents at it.** Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file).
    Anything outside an agent's role, or anything in its "comes back to a
    person", goes to the person.

## A hiring job description example

A job description full of
skills and years tells nobody what the hire needs to get done. Start from the
outcome.

> **Hiring: Clinic growth lead** (made-up example, Tidewater)
> **The role in one line:** bring more physio clinics onto Tidewater and keep them.
> **The outcome you own in 90 days:** active clinics, now 43, target 60 by 28 Feb, read from the monthly billing export (focus 1).
> **Owns:** clinics sign up and pay; more clinics stay.
> **May decide alone:** which clinics to contact and in what order; which trial follow-ups to send, in wording the founder has approved.
> **Comes back to a person:** prices, anything that moves money, patient data, and any new words customers read.
> **Reads before starting:** BUSINESS.md.
> **How your work is checked:** the active-clinics number in Metrics each month, and a weekly review with the founder.
> **Pay, hours, location:** ask the person. Don't invent them.

Leave out years of experience and a list of tools unless you can say why the
outcome needs them.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in the "Who owns what" section.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. Its Who owns what table has six
outcomes. Two have nobody named: features get built, and clinics stay. A third,
no-shows fall (focus 2), is Jo's until someone is named. It shows a person (Jo) and a reviewer agent in the same shape.
Open questions asks Jo who owns keeping clinics, and who owns focus 2.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent do it

The `roles` skill reads how your business actually runs: your files, your agent
definitions and your git history. It drafts the table for you to change and
writes only the Who owns what section. Ask it for a hiring description and it
writes one from the table.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "write who owns what".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need to know
their roles, and you want each person's way of working kept current,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=roles)
keeps each agent's role, and how each person likes to work, in one place.
