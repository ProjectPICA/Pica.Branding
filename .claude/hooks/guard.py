#!/usr/bin/env python3
"""PreToolUse guard on Bash for a ProjectPICA repository.

Vendored from `ProjectPICA/Pica.Claude` (`shared/hooks/guard.py`); change it there, not here.

Two jobs, both backed by something that went wrong or nearly did:

1. Commits and pushes in this repo (or, at the workspace root, any repo under it) are scanned for
   what must never be published: credentials (GitHub Free has no secret scanning or push protection
   here), personal machine or vault paths, AI attribution, and browser-automation scratch. These BLOCK.
2. Commands that change shared environments ASK first: Terraform apply/destroy/state surgery,
   Azure write verbs, SQL writes through sqlcmd, and any push to a `release/*` branch (a prod
   deploy — the TST check in Pica.Claude's `pica-release` skill comes first).

The hook runs before the command, so for a one-liner such as `git add -A && git commit … && git push`
it scans what the command *will* publish: the working tree and untracked files as well as the index
and the commits not yet on the upstream.

Fail-soft by design: anything unexpected exits 0 and lets the call through.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# The scope this hook guards: the project the session runs in. That is a single repo in a cloud or
# CI clone, and the workspace root (with every repo cloned inside it) on the maintainer's machine.
WORKSPACE = os.path.realpath(
    os.environ.get("CLAUDE_PROJECT_DIR") or os.path.join(os.path.dirname(__file__), "..", "..")
)

# Credential shapes that are never legitimate in a repo, tests included. (label, pattern, may a
# placeholder word on the line — FAKE_TOKEN=, example, … — excuse it?)
TOKEN_SECRETS = [
    ("private key block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), False),
    ("GitHub token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"), False),
    ("Entra client secret", re.compile(r"\b[A-Za-z0-9_-]{3}8Q~[A-Za-z0-9_.~-]{30,}"), False),
    ("Azure storage key", re.compile(r"AccountKey\s*=\s*[A-Za-z0-9+/=]{40,}"), False),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\."), True),
    ("bearer token", re.compile(r"\b[Bb]earer\s+[A-Za-z0-9._~+/-]{24,}"), True),
    ("instrumentation key", re.compile(r"InstrumentationKey\s*=\s*[0-9a-f-]{36}", re.I), True),
]
# A secret-named key with a *literal* value: "ClientSecret": "…", ApiKey = '…', Password=…; in a
# connection string. Code that moves a password around (`user.Password = request.Password;`) has no
# literal, and a value without a digit (`"smtp-password"`, i18n `"PASSWORD"`) or with `$`
# interpolation is not a secret. Skipped in tests and Markdown, where examples are expected.
LITERAL_SECRETS = [
    ("password in a connection string",
     re.compile(r"(^|[;\"'])\s*(Password|Pwd)\s*=\s*(?=[^;\"'\s]*\d)[^;\"'\s$<{%]{4,}\s*(;|\"|'|$)", re.I),
     True),
    ("secret-named key with a literal value",
     re.compile(r"(client_?secret|api_?key|password|passwd|pwd|secret|access_?token|sas_?token|"
                r"connection_?string)[\"']?\s*[:=]\s*[\"'](?=[^\"']*\d)([^\"'$%{<\s][^\"'$]{7,})[\"']", re.I),
     True),
]
SECRET_SAFE = re.compile(
    r"(\$\(|\$\{|%[A-Z_]+%|<[A-Za-z _-]+>|xxx+|\.\.\.|\*\*\*|REDACTED|PLACEHOLDER|CHANGEME|"
    r"your[-_]|example|dummy|sample|fake|test|UserSecrets|KeyVault|@Microsoft\.KeyVault|"
    r"Configuration\[|GetConnectionString|secrets\.|vars\.|Environment\.GetEnvironmentVariable)",
    re.IGNORECASE,
)
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__|e2e)/|\.(spec|test)\.[jt]s$|Tests?\.cs$|/fixtures?/", re.I)

LOCAL_CONVENTION = re.compile(r"clercq-agents", re.I)
# Any path under a personal home directory: it names the user and their machine layout (stack traces,
# generated `project.assets.json`, pasted configs). Case-sensitive on purpose, so an API route such as
# `/users/{id}/documents` is not mistaken for one; CI runner and container homes are not personal.
HOME_PATH = re.compile(
    r"(?<![\w.-])(/Users|/home)/(?!(runner|user|app|node|vscode|ubuntu|Shared|root)/)[A-Za-z][\w.-]*/"
)
PRIVATE_REF = re.compile(
    r"(Mobile Documents/com~apple~CloudDocs|Notes/ClercqIt|second.brain|notion\.(so|site)/)",
    re.IGNORECASE,
)
ATTRIBUTION = re.compile(
    r"(Co-Authored-By:|Generated with \[?Claude|🤖 Generated|noreply@anthropic\.com)", re.IGNORECASE
)
SCRATCH = re.compile(r"(^|/)\.playwright(-cli|-mcp)?/|(^|/)test-results/|\.(har|webm)$")

GIT = r"\bgit\b(?:\s+-(?:C|c)\s+\S+)*\s+"
PUSH = re.compile(GIT + r"push\b")
COMMIT = re.compile(GIT + r"commit\b")
ADD_ALL = re.compile(GIT + r"add\b|" + GIT + r"commit\b[^;&|]*\s-[a-zA-Z]*a")

INFRA_ASK = [
    (re.compile(r"\bterraform\s+(-chdir=\S+\s+)?(apply|destroy|import|taint|untaint|force-unlock)\b"),
     "Terraform write against a shared state — confirm the backend (env) first"),
    (re.compile(r"\bterraform\s+(-chdir=\S+\s+)?state\s+(rm|mv|push|replace-provider)\b"),
     "Terraform state surgery"),
    (re.compile(r"\baz\s+(?!login\b|account\b|config\b|extension\b|rest\b)[a-z -]*?\s"
                r"(create|delete|update|set|remove|restart|start|stop|purge|deactivate|activate|"
                r"assign|reset|import|swap|scale|exec)\b"),
     "Azure write operation (or a shell inside a container)"),
    (re.compile(r"\baz\s+rest\b.*(--method|-m)\s+[\"']?(put|patch|post|delete)\b"
                r"(?!.*api\.(applicationinsights|loganalytics)\.io)", re.IGNORECASE),
     "Azure REST write"),
    (re.compile(r"\bsqlcmd\b.*(\b(UPDATE|DELETE|INSERT|MERGE|DROP|ALTER|TRUNCATE|CREATE|GRANT|EXEC)\b|"
                r"\s-i\s)", re.IGNORECASE),
     "SQL write (or a script file) through sqlcmd — TST/PROD data is read-only from a session"),
]
# Flags that skip the pre-push gate or rewrite published history. Permission deny rules only match a
# command's prefix, so `git push -u origin x --no-verify` or `git push origin +main` would slip past them.
NO_VERIFY = re.compile(GIT + r"push\b[^;&|]*?\s--no-verify\b|"
                       + GIT + r"commit\b[^;&|]*?\s(--no-verify\b|-[aqsv]*n[aqsv]*(\s|$))")
FORCE_PUSH = re.compile(GIT + r"push\b[^;&|]*?(\s--force(-with-lease|-if-includes)?\b|\s-[a-zA-Z]*f[a-zA-Z]*\b|"
                        r"\s\+[\w./-]+)")
UNATTENDED = os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CLAUDE_CODE_REMOTE") == "true"
MAIN_PUSH = re.compile(GIT + r"push\b[^;&|]*?\s(\S+:)?(refs/heads/)?main\b")
RELEASE_ASK = ("Push to a release/* branch deploys PRODUCTION — the real-address TST check and a "
               "green e2e/tst status come first (the pica-release skill in ProjectPICA/Pica.Claude)")

WORKDIR = ""


def git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, timeout=20, cwd=WORKDIR)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


def untracked_as_diff() -> str:
    out = []
    for path in git("ls-files", "--others", "--exclude-standard").splitlines()[:200]:
        out.append(f"+++ b/{path}")
        try:
            with open(os.path.join(WORKDIR, path), encoding="utf-8", errors="ignore") as fh:
                out.extend("+" + line.rstrip("\n") for line in fh.readlines()[:2000])
        except Exception:
            pass
    return "\n".join(out)


def upstream() -> str:
    return (git("rev-parse", "--verify", "-q", "@{u}").strip()
            or git("rev-parse", "--verify", "-q", "origin/main").strip())


def what_is_published(command: str) -> tuple[str, str]:
    """(diff, commit messages) that this command is about to publish."""
    diff, messages = "", ""
    if COMMIT.search(command):
        messages += command
        diff += git("diff", "-U0", "--cached")
        if ADD_ALL.search(command):  # `git add … && git commit` or `commit -a`: the tree goes too
            diff += "\n" + git("diff", "-U0") + "\n" + untracked_as_diff()
    if PUSH.search(command):
        base = upstream()
        if base:
            diff += "\n" + git("diff", "-U0", base, "HEAD")
            messages += "\n" + git("log", "--format=%B", f"{base}..HEAD")
    return diff, messages


def scan(diff: str, messages: str, setup_repo: bool) -> list[str]:
    problems: list[str] = []
    secret_hits: list[str] = []
    private_hits: list[str] = []
    scratch: set[str] = set()
    path = ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            if SCRATCH.search(path):
                scratch.add(path)
            continue
        if not line.startswith("+") or line.startswith("+++") or not path:
            continue
        if path.startswith((".claude/hooks/", "shared/hooks/")):
            continue  # the guard has to contain the patterns it looks for
        examples_ok = TEST_PATH.search(path) or path.endswith(".md")
        checks = TOKEN_SECRETS if examples_ok else TOKEN_SECRETS + LITERAL_SECRETS
        for label, pattern, excusable in checks:
            if pattern.search(line) and not (excusable and SECRET_SAFE.search(line)):
                secret_hits.append(f"{path}: possible {label}")
                break
        # The setup repo may name the ~/.clercq-agents convention; no repo may name a personal path.
        if (PRIVATE_REF.search(line) or HOME_PATH.search(line)
                or (not setup_repo and LOCAL_CONVENTION.search(line))):
            private_hits.append(f"{path}: {line[1:].strip()[:70]}")

    if secret_hits:
        problems.append(
            "BLOCK: something that looks like a credential is in the diff. This org has no secret\n"
            "  scanning or push protection (GitHub Free) — nothing else will catch it:\n"
            + "\n".join(f"    {h}" for h in list(dict.fromkeys(secret_hits))[:8])
        )
    if private_hits:
        problems.append(
            "BLOCK: reference to a personal/local path or private notes in committed content:\n"
            + "\n".join(f"    {h}" for h in private_hits[:8])
        )
    if scratch:
        problems.append(
            "BLOCK: browser-automation or test-run scratch is included — unstage and gitignore it:\n"
            + "\n".join(f"    {p}" for p in sorted(scratch)[:8])
        )
    if ATTRIBUTION.search(messages or ""):
        problems.append(
            "BLOCK: AI attribution in the commit message (Co-Authored-By / 'Generated with' / "
            "anthropic address).\n  Project rule: no attribution trailers in any git content."
        )
    return problems


def respond(decision: str, reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": decision,
        "permissionDecisionReason": reason}}))


def resolve_workdir(command: str, base: str) -> str:
    m = re.search(r"\bgit\s+-C\s+(?:'([^']+)'|\"([^\"]+)\"|(\S+))", command) or \
        re.search(r"\bcd\s+(?:'([^']+)'|\"([^\"]+)\"|(\S+))", command)
    if not m:
        return base
    t = os.path.expanduser(next(g for g in m.groups() if g))
    return t if os.path.isabs(t) else os.path.join(base, t)


def main() -> int:
    global WORKDIR
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return 0
    tool_input = payload.get("tool_input")
    command = (tool_input.get("command") if isinstance(tool_input, dict) else "") or ""
    if not isinstance(command, str):
        return 0

    asks = [label for pattern, label in INFRA_ASK if pattern.search(command)]
    blocking: list[str] = []

    if COMMIT.search(command) or PUSH.search(command):
        target = resolve_workdir(command, payload.get("cwd") or os.getcwd())
        if os.path.isdir(target):
            WORKDIR = target
            if PUSH.search(command) and ("release/" in command
                                         or git("branch", "--show-current").startswith("release/")):
                asks.append(RELEASE_ASK)
            # Case-folded: the volume is case-insensitive and reached as both Projects/ and projects/.
            top = os.path.realpath(git("rev-parse", "--show-toplevel").strip() or "/nonexistent")
            ws, tp = WORKSPACE.casefold(), top.casefold()
            if tp == ws or tp.startswith(ws + os.sep):
                diff, messages = what_is_published(command)
                # The workspace setup repo is the one carrying the clone list.
                blocking = scan(diff, messages, setup_repo=os.path.isfile(os.path.join(top, "repos.tsv")))
        elif PUSH.search(command) and "release/" in command:
            asks.append(RELEASE_ASK)

    if NO_VERIFY.search(command):
        blocking.append("BLOCK: --no-verify (or `commit -n`) skips the pre-push/pre-commit gate, the only "
                        "enforcement this org has (GitHub Free). Fix what the hook reports instead.")
    if FORCE_PUSH.search(command):
        blocking.append("BLOCK: force push (--force, -f, +ref) rewrites published history.")
    if UNATTENDED and PUSH.search(command) and (
            MAIN_PUSH.search(command) or (WORKDIR and git("branch", "--show-current").strip() == "main")):
        blocking.append("BLOCK: an unattended run never pushes to main — push an agent/<issue>-<slug> branch "
                        "and open a pull request (working agreement rule 8).")

    if blocking:
        respond("deny", "Blocked — this would publish something that must never leave the machine:"
                "\n\n" + "\n\n".join(blocking) + "\n\nFix it and retry. If one is a genuine false "
                "positive, say which line and why; do not route around the guard.")
    elif asks:
        respond("ask", "This changes a shared environment:\n  - " + "\n  - ".join(asks)
                + "\n\nApprove only if this was explicitly asked for in this conversation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
