---
name: pica-story
description: Take a ProjectPICA GitHub issue from start to finish in the current repo — read it, plan, implement with the engineering agents, test by type, verify independently, document, then commit to main (interactive) or open a PR from an agent/ branch (unattended cloud or CI run). Use when asked to "work on issue #12", "pick up this issue", "implement issue 12", "fix #12", "start this story", "finish this story", "wrap this up", or given a GitHub issue URL.
---

# Pica story

One issue, one repo, start to finish. Every step ends on its **done when** line; do not start the next
step before it holds.

## 0. Mode

**Unattended** when `GITHUB_ACTIONS=true` or `CLAUDE_CODE_REMOTE=true`, or the prompt says so. Nobody
answers questions: take the recommended default, write it down, and carry on. Otherwise **interactive**:
ask in prose, never in a dialog, and keep working on whatever the answer does not block.

Hard rules in both modes:

- No `Co-Authored-By` lines, "Generated with" footers or mentions of agents/AI in commits, PRs, issue
  comments or code comments.
- Never `--no-verify`, never lower `COVERAGE_FLOOR`, never add a line to an architecture allowlist. A hook
  that fails is a finding to fix.
- Never push `release/*`, never tag a release, never touch PROD.
- Plans, contracts and notes go in `.claude/scratch/<issue>/` (never committed) or the issue/PR text.

## 1. Read the issue and the rules

```bash
gh repo view --json nameWithOwner -q .nameWithOwner          # owner/repo from the git remote
gh issue view <n> --comments --json number,title,body,labels,comments,url
```

Accept a number, `#n` or a full issue URL (an issue in another repo than the current one: stop and say so).
Read the repo's `AGENTS.md` (imported by `.claude/CLAUDE.md`), its `CLAUDE.md` if present, and every file in
`.claude/rules/`. Extract the **acceptance criteria verbatim**; if the issue has none, the domain-analyst
derives them in step 3.

**Done when** you can state the criteria, the repo's verification ladder and its commit-subject convention
(`git log --oneline -15`).

## 2. Start from origin/main

```bash
git fetch origin
git status --porcelain                                       # must be clean
```

- **Unattended:** `git switch -c agent/<n>-<slug> origin/main` (slug: 3-5 kebab words from the title).
- **Interactive:** on `main`, `git pull --ff-only`.

Then:

- Keep scratch out of git: `mkdir -p .claude/scratch/<n>` and, if `git check-ignore -q .claude/scratch/<n>`
  fails, add `.claude/scratch/` to `.git/info/exclude` (local only).
- Install the repo's hooks if it ships them: `[ -x scripts/install-hooks.sh ] && scripts/install-hooks.sh`.
- .NET repos: a restore from GitHub Packages needs a token with `read:packages`. If `dotnet restore` fails on
  auth, say so now; never widen a token yourself.
- **Baseline:** run the repo's build, lint and test commands on the unmodified tree and write down the
  counts per type. Without a baseline you cannot tell your breakage from the repo's.
- **A bug is reproduced first** — a failing test or a measured symptom on `origin/main`. If it does not
  reproduce, stop and report that instead of fixing something.

**Done when** the branch is set, the baseline counts are recorded and (for a bug) the reproduction exists.

## 3. Analyse and plan

Check for work in flight first: open PRs and branches touching the same area
(`gh pr list --search <term>`, `git log --all --oneline -S <Term>`).

Scale the team to the issue:

| Issue | Launch |
|---|---|
| Vague, rule-heavy or crossing a bounded context | `domain-analyst` (issue text verbatim, repo), then `solution-architect` with its report |
| Crosses a layer boundary, touches a shared component (`src/app/shared/`, a shared enum, a contract) or needs a decision | `solution-architect` (criteria, repo, `.claude/scratch/<n>/`) |
| Obvious, single-layer | plan it yourself |

Work that belongs in **another repo** (see the router in `AGENTS.md`: contracts in `Pica.Messaging`, a
source in its `Pica.<Source>` library, E2E in `Pica.E2E`) is not done here: it becomes a follow-up issue,
listed in order (contracts/library → backend → WebApp → E2E spec).

- **Interactive:** present the plan in a few lines with any open question and your recommended answer; wait
  for the go-ahead when an answer changes scope, otherwise proceed.
- **Unattended:** take each open question's recommended default and record it for the PR.

**Done when** every criterion maps to a planned change and a planned test.

## 4. Implement, with spec tests in parallel

Launch in **one message**:

- the engineer(s): `dotnet-engineer` (PICA, `Pica.*` libraries, scrapers, `Pica.Messaging`),
  `angular-engineer` (PICA.WebApp), `azure-platform-engineer` (Terraform, Dockerfiles, workflows) — each with
  its plan slice, the criteria verbatim, the baseline and the contract path;
- `spec-test-author` with the **acceptance criteria verbatim**, the component under test, the contract and
  the baseline — never the plan's reasoning or the implementation.

Small changes you make yourself, still with `spec-test-author` alongside. When a backend and a frontend
engineer run in parallel, send each the other's agent id with `SendMessage` so contract questions go
direct; contract changes bump `version:` in `contract.md`.

Read every engineer's report: its *Not verified* and *Deviations* are yours to resolve, not to forward.

**Done when** all slices report and the spec tests exist.

## 5. Run the verification ladder

Run the repo's own commands from its `AGENTS.md`, for example:

| Repo | Unit | Integration | Build / lint |
|---|---|---|---|
| PICA | `dotnet test` with `--filter "FullyQualifiedName!~Integration"`, plus `tests/PICA.Architecture.Tests` | same with `~Integration` (needs the AppHost's infrastructure) | `dotnet build src/PICA.sln` (warnings as errors) |
| PICA.WebApp | `npm run test:ci` | — | `npm run lint`, `npm run build` |
| `Pica.*` libraries, scrapers | the unit test project (offline) | the `*.Integration.Tests` project (live network) | `dotnet build` |
| Terraform | — | — | `terraform fmt -check -recursive && terraform validate` |

Report **by type with counts against the baseline**: "unit 412 passed (baseline 405), integration not run:
no Docker in sandbox". A suite you could not run is listed under *Not verified* with the reason, never
silently skipped.

**Done when** every type is green against the baseline or listed as not run with a reason.

## 6. Verify independently, in parallel

Launch in **one message**. Brief with **inputs only** — never your account of what you changed or why it
works; that narrative is the bias these agents exist to avoid.

| Agent | When | Gets |
|---|---|---|
| `code-reviewer` | every non-trivial diff | diff range (`origin/main...HEAD`, or the commits since the baseline sha), criteria verbatim, plan and contract paths |
| `api-verifier` | backend, messaging, migration, source client, infra | how to run or reach the system and authenticate, criteria verbatim, contract, baseline |
| `ui-verifier` | anything visible in PICA.WebApp | run command or URL and how to reach the screen, criteria verbatim, design reference if any, baseline |

Then reconcile: every FAIL and BLOCKER/MAJOR finding is fixed by the engineer and the ladder (step 5) re-run;
every UNVERIFIED is resolved or carried to *Not verified*. A finding is never argued away because you know
why the code looks that way. After fixes, re-verify with a **new** agent instance.

**Done when** no FAIL or BLOCKER remains and the verification table is complete: one row per criterion →
test (unit / integration) / running app → PASS, FAIL or UNVERIFIED (blocker).

## 7. Name the Pica.E2E spec

A change a user or an API client can see — a screen, a message or error text, a state or flow, an HTTP
status, error code or response shape — is not done without a spec in `ProjectPICA/Pica.E2E` (working
agreement rule 7). Write down: spec file, test title, the criterion it encodes, UI journey (page object +
`data-testid`s) or API contract (`adminRequest`), and any state to force with `context.route`.

- **In the Pica.E2E repo itself:** have `e2e-automation-tester` write and run it (brief: criteria verbatim,
  changed paths, target).
- **From a product repo, interactive:** propose the follow-up and create it when the maintainer agrees
  (`gh issue create -R ProjectPICA/Pica.E2E`); the spec is pushed and run once the change is on TST.
- **Unattended:** list it in the PR under *Follow-ups* as an issue to create in `ProjectPICA/Pica.E2E`.

A change with nothing visible says so in one line, with the reason.

## 8. Document

After verification, launch `documentor` with inputs only: repository (`git remote get-url origin`), diff
range, issue. For a non-trivial change (architecture, service, endpoint, infrastructure, domain rule, or any
page created) then launch `documentation-reviewer` with the same inputs plus the documentor's coverage
report, and have the documentor fix its BLOCKER and MAJOR findings. Both follow the `pica-docs-sync` skill.

If no Notion tool is available in the session, the documentor returns the pages to update; carry them to
*Docs to update* in the PR (unattended) or the hand-back (interactive). A change with nothing to document
says so in one line.

**Done when** the coverage report (or the Docs-to-update list) is in hand.

## 9a. Finish — unattended

1. Commit: subject states what was done, in the repo's convention; one line unless the *why* is not
   obvious. Stage explicitly; `git diff --stat origin/main...HEAD` shows only this issue's change.
2. `git push -u origin agent/<n>-<slug>` — never `main`, never `--force`.
3. Open the PR (draft if anything in *Not verified* blocks a criterion or scope is unfinished):

```bash
gh pr create --base main --head agent/<n>-<slug> --title "<what was done>" --body "$(cat <<'EOF'
Closes #<n>

## Summary
- <what was done, one line each, at most 5>

## Tests
- Unit: <added> added; <passed>/<total> passed (baseline <x>)
- Integration: <counts, or "not run: reason">
- Architecture / lint / build: <result>

## Not verified
- <criterion or suite — blocker>

## Decisions taken
- <open question — default chosen>

## Follow-ups
- ProjectPICA/Pica.E2E: <spec title — criterion>
- <other repo: issue to create>

## Docs to update
- <page title — what is now false or missing>   (only when no Notion tool was available)
EOF
)"
```

   No rationale, no implementation narrative, no checkbox lists. Drop an empty section.
4. `gh issue comment <n> --body "<PR URL>"`.
5. Never merge, never approve, never mark ready a draft you opened as blocked.

## 9b. Finish — interactive

Follow the repo's `AGENTS.md` flow; for ProjectPICA that is solo trunk delivery:

1. Commit on `main` (same subject rules), `git pull --rebase` if `main` moved, re-run the ladder if it did,
   then `git push origin main`. The pre-push hook runs; a failure is fixed, not bypassed.
2. **A push of PICA or PICA.WebApp to `main` is a TST deploy.** Find the run (`gh run list --branch main
   --limit 3`), follow it with `gh run watch <id>` (poll at most every five minutes otherwise — the E2E gate
   shares the API quota), and report which apps were updated, the commit SHA and the acceptance check to do
   on TST.
3. A `Pica.*` library change reaches PICA only through a published package (a code push to `main`) and a
   version bump in PICA: list the PICA bump as a follow-up issue in PICA.
4. Production is out of scope: it needs a real-address check on TST and a green `e2e/tst` first.

## Hand-back (both modes)

First line: the PR URL (unattended) or the pushed SHA and the deploy run (interactive). Then the
verification table, tests by type with counts against the baseline, *Not verified*, the Pica.E2E spec
(or why none), follow-up issues, and the docs coverage or *Docs to update*.

Stop and report instead of finishing when verification failed on something user-visible and cannot be fixed
here, part of the scope is blocked, or the base branch is too broken to judge the change — unattended, that
is a draft PR whose *Not verified* says what is blocking.
