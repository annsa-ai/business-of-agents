# Apply pasted answers

Read this when someone pastes text that starts "Your decisions, answers". Do it now or in a later session.

1. Each line reads `Q1 · <question> → <answer>`. Match it to the open question by its words, not only its id. If an answer could fit two questions, ask which.
2. Update the section the question came from. The answer is the person's yes to fix the line that caused the question too (an AGENTS.md command, a stale price on the site); fix only that line and tell them what you changed.
3. Remove the question from Open questions and from `.business/decisions.json`. If Open questions now holds fewer than seven, move the next question from `decisions.json` up. Change the status line once a section has nothing open.
4. If AGENTS.md (or CLAUDE.md, GEMINI.md, Copilot's file) doesn't point to BUSINESS.md, add the line from the Business skill's "Point agents at BUSINESS.md" step (`<skills folder>/business/SKILL.md`), and tell the person.
5. Rebuild the page: `python3 <skills folder>/business-page/scripts/business_page.py BUSINESS.md .business/business.html`.

Done when every pasted answer is applied or has a question back to the person, and Open questions holds only what is still open.
