---
title: "Business review for founders and AI agents"
description: "A free monthly business review for founders working with AI agents. Run every skill, read across them, and get one page: the top five changes and every open question, grouped by who decides."
slug: review
skill: review
plan: BUSINESS.md
part: review
---

# Business review for founders and AI agents

Each part of your business can look fine on its own. The useful finding is
usually between them: a focus with no owner, a number with no focus, a rule
nobody follows. You only see it when you read the whole file at once.

A review runs every skill in order, so BUSINESS.md gets all seven sections.
Then it reads across them and ends with one page: the top five changes and every
open question, grouped by who decides. People answer in one sitting, not one
interruption at a time. It's written for founders and small teams.

## What goes in it

The review writes no section of its own. It fills every section through the
other skills, as a draft.

| Step | What it does |
|---|---|
| Run the skills | In order: business, goals, metrics, roles, ask-less, lessons |
| Read across | The same gap in two sections, an answer in one that another asks about |
| Check for stale lines | A number older than its latest export, a rule a later decision replaced |
| Top five changes | One line each, tied to a focus, quoting the line it comes from. The biggest becomes that focus's Next move |
| Open questions | Duplicates merged, grouped by who decides, biggest unblock first. Seven in the file at most |

## How to do it

1. **Run the skills in order.** Each writes its own section as a draft.
   Anything that needs a person goes to Open questions, and the run keeps
   going. A fact it can't find is `unknown`.
2. **Read across the sections.** Look for what repeats: the same gap in two
   sections, a focus with no owner, a number with no focus, a rule nobody
   follows.
3. **Check for stale lines.** Any line older than its source becomes an open
   question, or its skill updates it.
4. **Pick the top five changes.** Each one line, plain words, starting with a
   verb. Each names a focus and quotes the line. A change with no source is
   dropped. The one that unblocks the most others comes first. Each focus's
   Next move is set from its most important change.
5. **Settle the questions.** If answering one answers another, keep one. Group
   the rest by who decides, taken from Who owns what, and rank each person's by
   how much the answer unblocks.
6. **Build the pages.** One decision page, grouped by person: each opens it,
   clicks their answers, copies them and pastes them back. It stays local, and the
   summary on top holds no revenue, prices or counts. A second page, from the `business-page` skill, turns BUSINESS.md
   into one clean page to read and share.
7. **Apply the answers.** Each answer goes back to the section it came from.
   The question leaves Open questions.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. A review of it would start with clinics
staying: clinics that left went 1, 2, 3 from August to October and Who owns what
says "Clinics stay | nobody". The same file asks Jo seven questions, from who
owns that to which timezone the numbers use. It would also set each focus's Next move, such
as "an agent starts measuring the no-show rate" for focus 2.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo, or let
the review do it. Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file).

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## When to run it

Monthly, and after any big change: a new focus, a new agent or hire, a launch.
For a first full setup, run it once and answer the page.

## Or let your agent do it

The `review` skill runs the other skills, reads across them, and builds the
page. It decides nothing for anyone.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "review my business".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need the same
plan, and you want the answers kept current,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=review)
keeps it in one place every agent reads.
