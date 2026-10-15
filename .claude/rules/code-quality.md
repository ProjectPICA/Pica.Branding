---
paths:
  - "**/*.{ts,tsx,js,mjs,html,scss,css,cs,tf,py}"
---

# Formatting and linting

A `PostToolUse` hook (`.claude/hooks/format_lint.py`) formats the file you just edited with the owning repo's
own tool and reports lint problems. It rewrites the file on disk, so **re-read a file the hook says it
reformatted before editing it again**. It never auto-fixes lint problems: fix what it reports.

| Files | Formatter | Linter | Config that decides |
|---|---|---|---|
| `.ts .tsx .html .css .scss .js` | Prettier | ESLint (`.ts .tsx .html`) | the repo's `package.json` `prettier` key or `.prettierrc*`; `eslint.config.js` |
| `.cs` | `dotnet format whitespace` (keeps the file's line endings) | the build; style/analyzer rules are enforced only in `PICA` (`EnforceCodeStyleInBuild`, warnings as errors) | `.editorconfig` |
| `.tf` | `terraform fmt` | `terraform validate` | — |
| `.py` | `ruff format` | `ruff check` | only with `ruff` installed, a ruff config in the repo, and a non-generated file |

- **No config, no formatting.** A repo without a resolvable Prettier config is left alone; the hook
  never reformats to Prettier's defaults. Add the config to the repo (and a `format:check` script)
  rather than to this hook.
- **Unformatted repos are only linted.** A tracked file whose committed version was not Prettier-clean
  is linted but not reformatted, so the first touch never reflows a whole file. Format the repo once,
  in its own commit, and the hook starts formatting its files.
- **ESLint warnings count.** The hook reports them; `warn` rules are a burn-down list, so do not add
  to it.
- **The hook is not the gate.** It only sees files you edit through `Edit`/`Write`. Before a push run
  the repo's check: `npm run lint` (and `npm run format:check` where the repo has it), `dotnet build`
  for style and analyzer rules, `terraform fmt -check -recursive` and `terraform validate`.
- **Never loosen a rule to make a warning go away.** Fix the code, or narrow one suppression with a
  reason beside it. ESLint rules that are `warn` are a burn-down list: do not add to it.
- **Do not reformat whole files you did not otherwise change.** A formatting-only change goes in its
  own commit so blame and review stay readable.
- **Worktrees:** the hook uses the worktree's `node_modules` if present, else the main checkout's.
  ESLint plugins resolve from the config's location, so run `npm ci` in a long-lived worktree.
