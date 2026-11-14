# explain-like-five

An [Agent Skill](https://agentskills.io/specification) that makes your coding agent answer like it is explaining to a five-year-old: smallest true words, one idea per sentence, pictures before prose.

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd).

## What it changes

| Before | After |
|---|---|
| Long, nested sentences | One idea, twelve words at most |
| Jargon | Plain words, real names glossed once |
| Paragraphs describing steps | Lists, tables, arrow chains |
| "Great question! Let me..." | The answer, first line |
| "Hope this helps!" | Nothing |

Code, commands, paths and error text are never simplified.

## Install

Copy the folder into your agent's skills directory:

```sh
# Claude Code
git clone https://github.com/narnoldi82/explain-like-five ~/.claude/skills/explain-like-five

# Kiro
git clone https://github.com/narnoldi82/explain-like-five ~/.kiro/skills/explain-like-five
```

## Use

Say "explain like I am five", "ELI5" or `/explain-like-five`. It stays on for the session. Say "stop eli5" or "normal mode" to turn it off.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest: name, version, and the SkillCentral content hash in `metadata.skillcentral.hash` |

## License

[MIT](LICENSE)
