---
name: business-page
description: >
  Business page: turns BUSINESS.md into one designed HTML page to read and share, with no network calls. Use when someone asks for a page, HTML or report from BUSINESS.md. Trigger on: "make it a page", "turn BUSINESS.md into HTML", "share it with the team".
---

# Business page

You turn BUSINESS.md into one designed page by running the script, so every
team gets the same design and BUSINESS.md stays the source of truth.

## Steps

1. Find BUSINESS.md at the root of the repo. If it's missing, say so and
   suggest the `business` skill, and stop there.
2. Run, from the repo root:

   ```bash
   python3 <skills folder>/business-page/scripts/business_page.py BUSINESS.md <out.html>
   ```

   Default `<out.html>` is `.business/business.html`. Use the name the
   person gives if they give one.
3. Tell the person where the page is. If BUSINESS.md says `draft` or holds
   internal numbers, say so before they share it. Done when you have given the
   path and said so if either applies.
