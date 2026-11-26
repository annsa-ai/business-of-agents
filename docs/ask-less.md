---
title: "Stop answering the same questions from your AI agents"
description: "A free guide for founders who feel like the message bus between their AI agents. Find the questions your agents keep asking, count them, and turn each repeat into a one-line rule."
slug: ask-less
skill: ask-less
plan: BUSINESS.md#how-we-decide
part: review
---

# Stop answering the same questions from your AI agents

"Can I merge this?" "Should I go ahead?" "Which one first?" Every question an
agent brings you is an answer you never wrote down. You give it again, to the
next agent, tomorrow. You become the message bus between your sessions.

The fix is small. Find the questions that repeat, and write each answer once as
a one-line rule, starting "We", in the "How we decide" section of BUSINESS.md, where
every person and agent on your team reads before they start. It's written for
founders and small teams.

## What goes in it

Everything agents asked you, and what you were already telling them, sorts
into three piles.

| Pile | What happens to it |
|---|---|
| The same question, asked again | Becomes a one-line rule starting "We" |
| A question you answered once ("yes, merge it") | Becomes a row in Decisions |
| What your agents were already told | Quoted, not rewritten. If they keep asking anyway, it moves where they read first |

The rules go in two short lists: what anyone can do without asking, and what
comes to a named person first. Twelve rules at most.

## How to do it

1. **Collect the questions.** Open your last week or two of agent sessions.
   Scroll or search for question marks. Copy every question an agent asked
   you into one list, with the date.
2. **Throw out what isn't an ask.** Skip questions the agent answered itself,
   headings, and example prompts. Keep what was really put to you.
3. **Sort each one** into the three piles: asked again, answered once, or
   already written down.
4. **Find the repeats.** A repeat is the same decision asked twice or more, in
   any words. Count it. Check what you answered each time: if it was the same
   answer, the rule is already in your head.
5. **Check what's already written.** Look in AGENTS.md, CLAUDE.md and any
   memory file your agent keeps. If the answer is already there, agents aren't
   reading it, or it's unclear. Move it where they read first instead of
   writing it twice.
6. **Write one sentence per repeat,** starting "We". Use your own words from
   your replies: "We merge once the tests pass and the reviewer approves."
7. **Leave some questions with you.** Anything that can't be undone stays a
   question: production data, money, sign-in, and words customers will read.
   Put those under "What comes to <who> first", with the name of who decides.
8. **Add the rules to BUSINESS.md** under "How we decide". Run it
   again next week and compare the counts.

## The template

Copy [skills/business/assets/BUSINESS.md](../skills/business/assets/BUSINESS.md) to the root of your repo and
fill in the "How we decide" section. Add a line to AGENTS.md (and to CLAUDE.md, with `@BUSINESS.md`, if you use Claude Code) pointing agents at BUSINESS.md; see [how BUSINESS.md works](how-business-md-works.md#one-file).

## A starter set of rules

Not sure where to start? [plans/AGENTS-rules-starter.md](../plans/AGENTS-rules-starter.md)
holds the rules Cat Williams-Treloar, founder of Annsa, runs her own agents by: when to interrupt,
how to ask, what ships without her, and what always comes to her. Paste the ones
that fit and make the words yours.

## A worked example

[Tidewater's BUSINESS.md](../plans/examples/tidewater/BUSINESS.md) is for a
made-up booking app for physio clinics. Its "How we decide" section
shows the shape: two "We" rules anyone can follow (work on focus 1 before focus
2; add a test with any new code) and three things that go to Jo first (prices
and anything that moves money, the words patients read, and SMS settings and
patient data). It ends with how to ask: one question, the options, and the one
we'd pick.

## When the answer isn't written down

If BUSINESS.md doesn't answer a question, an agent adds it to Open questions
with what it found, then keeps going. You answer them all in one sitting.

## Or let your agent do it

The `ask-less` skill reads the Claude Code and Codex session logs saved on the
computer it runs on, counts every question, sorts them, and shows you the
rules ranked by how many questions each would remove. It writes only the ones
you pick. Cloud agents and Cursor don't leave logs it can read; paste a week of
your agents' questions instead. The skill sends nothing anywhere itself.

```bash
npx skills add annsa-ai/business-of-agents
```

Then ask your agent: "find the questions I keep answering and write rules for them".

## When several agents need it

BUSINESS.md works for one repo. When agents across several tools need the same
rules, and you want to see which rules fire and which get undone,
[Annsa](https://annsa.ai/?utm_campaign=business-of-agents&utm_medium=tool&utm_source=github&utm_content=ask-less)
keeps them as rules every agent reads before it starts.
