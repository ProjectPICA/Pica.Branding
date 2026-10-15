# Working agreement

Always loaded, in every ProjectPICA repository. Each rule below cost a rework round, a halted release
or a lost result before it was written down. The other files in `.claude/rules/` either load with the
files they apply to (`paths:` frontmatter) or, without frontmatter, always.

These files are vendored from `ProjectPICA/Pica.Claude` (`shared/`), the workspace repo that also holds
the cross-repo router (`AGENTS.md`) and the release and TST-diagnostics procedures. Change them there:
in a repo, a copy edited in place fails the CI drift check (`.claude/check_shared.py` against
`.claude/shared.lock`), and in the workspace the next sync overwrites it.

## 0. Fetch before you read

Local clones lag their remotes by days or weeks (on 2026-09-28 a local `PICA` checkout had no E2E gate
in `deploy-prod.yml`, while `origin/main` had had one for two weeks). Before you read code to plan,
diagnose or answer a question, `git fetch origin` and compare against `origin/main`; fast-forward a
clean checkout with `git pull --ff-only`. In the workspace, `scripts/clone-repos.sh --pull` does this
for every clean clone. If a fetch fails, say so.

## 1. Done means tested in every repo the change touches

A fix or feature is done when the issue's acceptance is covered by **unit and integration tests in
every repo it touches** (a source-client library *and* `PICA`, for example), all green before the
push. Report them by type — unit, integration — with counts. Implementation tests alone are not
enough; this was asked for twice on one ticket. A change a user or an API client can see also
needs an end-to-end test in `Pica.E2E` (rule 7). A change that crosses repos is one issue per repo,
in order: contracts and libraries, then `PICA`, then `PICA.WebApp`, then the `Pica.E2E` spec.

## 2. A push to `main` is a deploy — finish it

A push to `main` of `PICA` or `PICA.WebApp` deploys to TST through CI/CD; a push to `main` of a
`Pica.*` library publishes a NuGet package; a push of a scraper deploys it to TST. Wait for that run,
then report what was deployed or published, the commit SHA, and the acceptance check to do on TST.
"Pushed, CI is running" is not a hand-back.

## 3. Prod only after a real TST check

Never promote to prod (a `release/*` push) just because a commit is on `main`, on TST and green.
First run **real addresses end-to-end on TST** — the analyst's usual ask is about five addresses,
none from the last three days — and check the output against the issue's acceptance criteria.
Report per-address results, then push the release (procedure: Pica.Claude's `pica-release` skill).

Prod deploys of a `main` commit are also gated on a green **`e2e/tst`** commit status written by
`Pica.E2E` (hotfix commits on a release branch, and commits already in a `release/*` tag, pass
without it). If the status is stuck `pending` on a finished run, re-dispatch `Pica.E2E`'s `e2e.yml`.

## 4. Poll GitHub sparingly

The E2E gate token is a personal PAT that **shares the 5000/h GitHub API quota** with `gh` and every
other session. A green 95/95 run once lost its result to that quota and left commits `pending`.
When waiting on a run: one call every five minutes or more, never a per-minute loop over several
repos. Prefer `gh run watch <id>` on a single run.

## 5. There is no server-side guard

The ProjectPICA org is on **GitHub Free with private repos**: no code scanning, no secret scanning or
push protection, no rulesets or branch protection, and org-level Actions variables are not readable
by private repos (use repo variables). Nothing stops a bad push to `main` except the workflow gates
(tests before deploy, the vulnerable-package gate in `Pica.Actions`, the E2E gate), the guard hook in
`.claude/hooks/guard.py`, and you. Never propose a GHAS or ruleset feature as if it works on this plan.

The committed pre-push hooks (`.githooks/`, in the repos that have them) are the substitute for
server-side enforcement. Keep them installed (`scripts/install-hooks.sh` where the repo has one,
otherwise `git config core.hooksPath .githooks`), never push with
`--no-verify` to get past a failure, and never add an allowlist line or lower a floor to make a check
pass — architecture allowlists and coverage floors may only shrink or rise.

## 6. Check the package feed token at task start

Restoring from GitHub Packages (`https://nuget.pkg.github.com/ProjectPICA/index.json`) needs a token
with `read:packages`. Check for it at the start of any .NET task that restores packages, and say
immediately if it is missing. Never widen a token yourself — credentials stay scoped.

## 7. New behaviour needs an E2E test

A change that a user or an API client can see is not done without a `Pica.E2E` test: a screen, a
message or error text, a state or a flow, an HTTP status, error code or response shape, anything a
customer or an admin is told. Unit and integration tests prove the pieces; only E2E proves the
deployed pieces together. On 2026-10-07 every unit test was green while a registry outage still told
users their address did not exist; it showed only when the path was read end to end.

- Write the spec from the acceptance criteria, not from the implementation, name it in the hand-back,
  and if a change has none say that and why. Working in another repo than `Pica.E2E`: name the spec
  that must follow, so it becomes the next issue.
- `Pica.E2E`'s own rules (`.claude/rules/e2e.md` there) say how: page objects, `context.route` stubs,
  tags, and proving a spec ran.

## 8. Unattended runs open a pull request

A session with no one at the keyboard — GitHub Actions (`GITHUB_ACTIONS=true`), a claude.ai cloud
session (`CLAUDE_CODE_REMOTE=true`), or a prompt that says it runs unattended — never pushes to `main`
or `release/*` and never merges. It works on `agent/<issue>-<slug>`, opens a pull request that closes
the issue, and lists in its body: what was done, tests by type with counts, what it could **not**
verify, the `Pica.E2E` spec that must follow, and the documentation it updated. The maintainer's
review and merge is the gate GitHub Free does not provide.

- **Integration tests run unattended too.** The cloud and CI environments allow the public sources'
  hosts; if one is unreachable from the sandbox, the PR says "integration not verified: <host>
  unreachable", never "passed".
- **Documentation is written, not deferred.** Unattended runs update the project documentation in
  Notion through the Notion connector, following the `pica-docs-sync` skill. If no Notion tool is
  available in the session, the PR lists the pages to update instead, under "Docs to update".
- **A PR is not a push to `main`.** Where a repo's `AGENTS.md` says not to push without a verification
  you could not run, an unattended run still opens the pull request, with that verification under
  "Not verified".

An interactive session follows the repo's own flow in `AGENTS.md` (solo trunk: commit to `main` and
push, after verification).

No `Co-Authored-By`, "Generated with" or other attribution lines in commits, PR bodies or any git
content (`.claude/settings.json` turns Claude Code's own off; the guard hook blocks the rest).
