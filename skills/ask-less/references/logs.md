# Reading past sessions

Read this when no logs are on this computer, or when another session folder may belong to this business.

## Listing first

`find_asks.py --list` reads only folder names, and the first line of each Codex session (where Codex records the folder). It never reads what was said. Show the person the folders and counts it prints, then ask: "May I read these past Claude Code and Codex sessions on this computer?" Run `--days 14 --yes` only after a yes. Without `--yes` it reads nothing.

## What it reads and writes

It matches this project's folder exactly, plus its worktrees. `--project <path>` names another. It writes `~/.ask-less/asks.jsonl`, outside any repo. Each line has an `id`, the `question`, the time and the person's `next_message`, with keys, emails, phone numbers and passwords replaced by `[redacted]`.

## Other session folders

Other folders are listed by name only. Ask which belong to this business before reading them. Read an approved one with `--project <path>`.

## Fallbacks

- Nobody is there to say yes: skip the read and record an open question.
- No logs (Cursor, or a cloud agent whose past sessions aren't on this computer): ask the person to paste a week of questions and their replies.
- Pasted text is read the same way: count the asks, drop what isn't one, and keep the person's wording.
