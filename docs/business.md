---
title: "BUSINESS.md: tell your AI agents what business they're in"
description: "A free BUSINESS.md template and guide. AGENTS.md tells your agents how to work in the code. BUSINESS.md tells them who the customer is, what you sell, what you're trying to win and what always needs you."
slug: business
skill: business
plan: BUSINESS.md#what-we-do
part: review
---

# BUSINESS.md: tell your AI agents what business they're in

AGENTS.md tells your agents how to work in the code: the commands, the style,
the tests. It says nothing about the business. So every agent asks you again:
who's the customer, what do we charge, can I change this copy, what are we
actually trying to win this quarter?

BUSINESS.md answers those once, in one file at the root of your repo that every
person and agent on your team reads before they start. The "What we do" section
is where it begins. It is written for founders and small teams.

## What goes in it

BUSINESS.md has seven sections. One skill writes each.

| Section | What it answers |
|---|---|
| Top 3 Business Focus | Up to three ranked goals (profit, customer, people or purpose), each with a number, an owner and the next move |
| What we do | Ideal customer, offer, price, customer benefit, channels, what makes you different, and what you won't do |
| Metrics | Five numbers at most, and how each is counted |
| Who owns what | One owner for each outcome, a person or an agent |
| How we decide | Rules written as "We ...": what anyone can do, and what goes to whom first |
| Decisions | What a person decided, and what you learned |
| Open questions | What's still waiting on a person, for each person by name |

"What we do" has ten fields: Company, Website & socials, Ideal customer, Offer,
Price, Feedback, Customer benefit, Channels & distribution, What makes us
different, and What we won't do.

## How to write it

1. **Start from what's already written.** Your README, your pricing page, your
   AGENTS.md, any plan docs. Most of it is already true somewhere.
2. **Use your customers' words.** Copy a line from a call note or a support
   email instead of your home page's pitch. "Drowning in no-shows" tells an
   agent more than "an all-in-one practice platform".
3. **Write the price and the no.** What you charge, and what customers ask for
   that you turn down. Agents stop proposing those. Say if the price is public.
4. **Name a source for every line.** A file, a page or a person. No source, no
   line.
5. **Leave out what you don't know.** Write `unknown` rather than a guess
   your agents will treat as fact.
6. **Point your agents at it.** Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file).

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in "What we do". The other sections can say "Not written yet" until you
run their skills. Or run the `review` skill to write all of them.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. Its "What we do" section opens with one
line, "We help small physio clinics stop losing money to no-shows." It then
fills the ten fields: customer quotes, two public prices (Solo $29, Clinic $79)
and a won't-do: insurance or Medicare billing. Where it doesn't know, it says
`unknown`.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent write it

The `business` skill reads your repo first, asks only what it can't find (six
questions at most, each with a suggested answer), marks where every line came from, and shows you the section
before it writes. Other sections stay as they were.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "write my BUSINESS.md".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need the same
context, and it should stay current as decisions are made,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=business)
keeps it as one plan: each section becomes a page every agent reads
before it starts.
