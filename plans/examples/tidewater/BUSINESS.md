<!-- Worked example for a made-up company, Tidewater. Not a real business. -->

# Tidewater

> How we run Tidewater, for people and agents. Read it before you start.
> If the answer is here, act on it. A decision someone already made is final,
> even while the status says draft. A draft only means: check with the owner
> before you act on a rule nobody has stated yet.
> Open questions wait for their owner; nothing in them is decided yet.
> No answer here? Add the question to Open questions, take the safest option
> and keep going.

Updated 24 Nov 2026 · Status: draft, Jo to confirm

## Top 3 Business Focus

Until 28 Feb 2027. Focus 1 comes first.

1. **Customer · More clinics pay for Tidewater every month.** Number: active clinics, 43 → 60 by 28 Feb. Owner: Jo. Next: Jo calls clinics to win about 4 more a month.
2. **Customer · Fewer no-shows for clinics that take deposits.** Number: no-show rate for those clinics, not measured yet. Owner: Jo, until named. Next: an agent starts measuring it.

Not doing now: Medicare and insurance codes on invoices. One clinic asked; we don't do insurance billing.

Sources: Jo, data/revenue_export.csv.

## What we do

We help small physio clinics stop losing money to no-shows.

- **Company:** Tidewater
- **Website & socials:** unknown
- **Ideal customer:** physio clinics with 1 to 6 practitioners, losing money to no-shows.
- **Offer:** online booking, a text reminder 24 hours before, and a deposit on the first visit.
- **Price:** Solo $29 a month. Clinic $79 a month, up to 6 practitioners. 14-day free trial, no card. Prices are public; every other number here is internal.
- **Feedback:** "No-shows cost us more than the software does." "We just need it to text people, honestly." "Deposit refunds are confusing for front desk."
- **Customer benefit:** fewer empty slots, without chasing patients by phone.
- **Channels & distribution:** Jo sells directly, through calls with clinics. Which channel brings most trials: unknown.
- **What makes us different:** unknown. Clinics ask for reminders that just work and a first-visit deposit.
- **What we won't do:** insurance or Medicare billing. We're not a practice-management system.

Sources: README, docs/pricing.md, feedback/notes.md, Jo.

## Metrics

How we know it's working. Checked 20 Nov 2026.

| Number | Latest | Goal | How it's counted | If it moves, we |
|---|---|---|---|---|
| Active clinics | 43 (Oct), up from 39 | 60 by 28 Feb | Paid clinics at month end, `data/revenue_export.csv` | Fall behind pace: sales and trials before new features |
| No-show rate, deposit clinics | not measured yet | not set yet | No source yet | Judge whether deposits work |
| Trial to paid | 3 of 12 (week of 9 Nov) | none | Paid that week over new trials that week, test signups left out, `data/weekly_signups.csv` | not set yet |

Readings: Active clinics: Aug 34, Sep 39, Oct 43
Readings: Trial to paid: 5 Oct 2 of 8, 12 Oct 1 of 8, 19 Oct 3 of 12, 26 Oct 2 of 12, 2 Nov 4 of 11, 9 Nov 3 of 12

On pace for focus 1: 60 needs about 4 more clinics a month. The last two months added 5 and 4.

Sources: data/revenue_export.csv (monthly), data/weekly_signups.csv (weekly).

## Who owns what

Every outcome has one owner, a person or an agent.

| Outcome | Owner | Source |
|---|---|---|
| Clinics sign up and pay: sales, calls, pricing | Jo | Jo |
| Booking-page copy | Jo | Jo, AGENTS.md |
| Every PR is reviewed before merge | reviewer agent | .claude/agents/reviewer.md |
| Features get built | nobody | Jo |
| Clinics stay | nobody | Jo |
| No-shows fall (focus 2) | Jo, until named | Jo |

Sources: Jo, AGENTS.md, .claude/agents/reviewer.md.

## How we decide

Small, reversible calls are made by whoever holds the work. Big calls come to Jo.

**What anyone can do:**
- We work on focus 1 before focus 2.
- We add a test with any new code. The reviewer agent blocks a PR without one.

**What comes to Jo first:**
- Prices, and anything that moves money.
- Words patients read: the booking page.
- SMS provider settings and patient data.

When something's unclear, we ask one question, with the options and the one we'd pick, and keep going. Once it's decided, it goes in Decisions, so nobody asks again.

Sources: AGENTS.md, .claude/agents/reviewer.md, Jo.

## Decisions

What we've decided, so nobody asks again.

| Date | Decision | Why | Who | Source |
|---|---|---|---|---|
| 8 Nov 2026 | Deposits only on first visits, always refundable in one click | Refunds that need a phone call break the front desk | Jo | Jo; commits 3da9e84, 788e546 |

**What we learned, 6 to 20 Nov:**
- Deposits went out, came back and went out again in four days. The front desk couldn't refund. Now: a change that moves money goes past Jo first.
- Reminders went out on UTC time, not clinic time, and a hotfix followed. Now: we test the send time.
- Neither change can be judged yet: we don't measure no-shows.

Sources: git log, feedback/notes.md, Jo.

## Open questions

What we're still deciding, and who decides.

- **For Jo:** who owns keeping clinics? Clinics that left went 1, 2, 3 from August to October.
- **For Jo:** who owns focus 2, and where will the no-show rate come from?
- **For Jo:** AGENTS.md says "Use pnpm" and "Run `npm test`". Which is right?
- **For Jo:** you said both exports are weekly. The billing export is monthly. Is that expected?
- **For Jo:** may an agent merge once tests pass and the reviewer approves? We'd say yes, with no deploys.
- **For Jo:** where do new clinics first hear about Tidewater?
- **For Jo:** what timezone do the numbers use?
