#!/usr/bin/env python3
"""PostToolUse: run the owning repo's own formatter and linter on the file Claude just edited.

Vendored from `ProjectPICA/Pica.Claude` (`shared/hooks/format_lint.py`); change it there, not here.

Developers get this from format-on-save in their IDE; this hook gives Claude Code the same behaviour,
so what it writes already matches the formatter and a later save does not reflow it.

By file type, using each repo's own tool and config (never a default style of this hook's own):

- `.ts .tsx .js .mjs .html .css .scss` — the repo's Prettier (`package.json` "prettier" key or a
  `.prettierrc*`), then, for `.ts .tsx .html`, its ESLint (`eslint.config.js`, the rules `npm run lint`
  uses; warnings included). Prettier is skipped when the repo has no resolvable config, rather than
  reformatting to defaults, and for a tracked file whose committed version was not Prettier-clean
  (it is only linted), so no first touch reflows a whole file. Format a repo once, in its own commit.
- `.cs` — `dotnet format whitespace` against the repo's `.editorconfig`, keeping the file's existing
  line endings and final newline. Style and analyzer rules are enforced by the build
  (`EnforceCodeStyleInBuild`) only where the repo enables it (PICA); that is the verification step.
- `.tf` — `terraform fmt`.
- `.py` — `ruff format` and `ruff check` when `ruff` is on PATH, the repo has a ruff config, and the
  file is not marked generated.

Formatting is written in place, and the model is told when a file changed because its next Edit must
work from the formatted text. Lint problems are reported back, never auto-fixed.

Works in a repo's worktrees (`<repo>/.claude/worktrees/<name>/…`): tools come from the worktree if it
has `node_modules`, else from the main checkout.

Fail-soft: any error exits 0 silently.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


PRETTIER = {".ts", ".tsx", ".js", ".mjs", ".html", ".css", ".scss"}
ESLINT = {".ts", ".tsx", ".html"}
SKIP_PARTS = {"node_modules", "dist", ".angular", ".playwright-cli", "bin", "obj", ".terraform", "__pycache__"}
TIMEOUT = 15  # per tool call; a file takes at most a handful of calls, within the hook's 60 s


def repo_root(path: Path) -> Path | None:
    for parent in path.parents:
        if (parent / ".git").exists():
            return parent
    return None


def main_checkout(root: Path) -> Path:
    """`<repo>/.claude/worktrees/<name>` -> `<repo>`; any other root is returned unchanged."""
    p = root.parts
    if len(p) >= 3 and p[-3:-1] == (".claude", "worktrees"):
        return Path(*p[:-3])
    return root


def run(args: list[str], cwd: Path, stdin: str | None = None) -> subprocess.CompletedProcess:
    """Run a tool; a timeout or a missing tool yields a non-zero result instead of raising."""
    # `direnv exec <dir>` loads whichever `.envrc` applies to the file's repo (on the maintainer's
    # machine the workspace's devenv shell); in a cloud or CI clone there is no direnv and PATH is used.
    for argv in (args, ["direnv", "exec", str(cwd), *args]):
        try:
            result = subprocess.run(argv, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=TIMEOUT)
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(argv, 124, "", "timed out")
        # node, dotnet, terraform and friends are only on PATH inside the workspace's devenv shell
        if result.returncode != 127:
            return result
    return subprocess.CompletedProcess(args, 127, "", "tool not found")


def was_formatted_in_head(prettier: Path, path: Path, root: Path) -> bool:
    """True for a new file, or one whose committed version already matches Prettier.

    A repo that has never been formatted would otherwise get a whole-file reflow on the first touch of
    every file. Such files are only linted until the repo is formatted once in its own commit.
    """
    rel = path.relative_to(root).as_posix()
    head = run(["git", "show", f"HEAD:{rel}"], root)
    if head.returncode != 0:
        return True  # untracked or new: format it
    return run([str(prettier), "--check", "--stdin-filepath", str(path)], root, stdin=head.stdout).returncode == 0


def node_tool(root: Path, name: str) -> Path | None:
    for base in (root, main_checkout(root)):
        candidate = base / "node_modules" / ".bin" / name
        if candidate.exists():
            return candidate
    return None


def format_node(path: Path, root: Path, messages: list[str]) -> None:
    if path.name in {"package-lock.json", "package.json"}:
        return
    prettier = node_tool(root, "prettier")
    if (
        prettier is not None
        and run([str(prettier), "--find-config-path", str(path)], root).returncode == 0
        and was_formatted_in_head(prettier, path, root)
    ):
        before = path.read_bytes()
        result = run([str(prettier), "--write", "--end-of-line", "auto", str(path)], root)
        changed = path.read_bytes() != before  # judge by the file, not the exit code: a timeout can follow a rewrite
        if result.returncode != 0 and not changed:
            print(f"prettier could not format {path.name}: {result.stderr.strip()[:300]}", file=sys.stderr)
        elif changed:
            messages.append(f"Prettier reformatted {path.name} to the repo's Prettier config. Re-read it before editing it again.")

    eslint = node_tool(root, "eslint")
    if eslint is not None and path.suffix.lower() in ESLINT:
        # exit 0 = clean or warnings only, 1 = errors, 2 = ESLint itself failed (ignore: fail soft).
        # Warnings are reported too: the repo's config uses `warn` for burn-down rules.
        result = run([str(eslint), "--no-warn-ignored", "--format", "json", str(path)], root)
        if result.returncode in (0, 1) and result.stdout.strip():
            problems = [
                f"{path.name}:{m['line']}:{m['column']} {'error' if m.get('severity') == 2 else 'warning'}: "
                f"{m['message']} ({m.get('ruleId') or 'parse error'})"
                for file_report in json.loads(result.stdout)
                for m in file_report["messages"]
            ]
            if problems:
                more = f" (+{len(problems) - 15} more)" if len(problems) > 15 else ""
                messages.append(f"ESLint reports problems in {path.name}{more}; fix them before moving on:\n" + "\n".join(problems[:15]))


def format_dotnet(path: Path, root: Path, messages: list[str]) -> None:
    if not (root / ".editorconfig").exists() and not any(root.glob("*/.editorconfig")):
        return
    before = path.read_bytes()
    # --folder skips MSBuild workspace loading, so this takes about a second instead of ten.
    result = run(["dotnet", "format", "whitespace", str(root), "--folder", "--include", str(path.relative_to(root)), "--verbosity", "quiet"], root)
    after = path.read_bytes()
    if after == before:
        return  # judged by the file, not the exit code: a timeout can follow a rewrite
    # Keep the file's own line endings and final newline: a repo's .editorconfig can disagree with its
    # tree (PICA's asks for CRLF, almost all files are LF), and a whole-file rewrite buries the real diff.
    eol = b"\r\n" if b"\r\n" in before else b"\n"
    text = after.replace(b"\r\n", b"\n")
    text = text.rstrip(b"\n") + (b"\n" if before.endswith(b"\n") else b"")
    fixed = text.replace(b"\n", eol)
    if fixed == before:
        path.write_bytes(before)
        return
    path.write_bytes(fixed)
    messages.append(f"dotnet format reformatted whitespace in {path.name} to the repo's .editorconfig. Re-read it before editing it again.")


def format_terraform(path: Path, root: Path, messages: list[str]) -> None:
    before = path.read_bytes()
    result = run(["terraform", "fmt", str(path)], path.parent)
    changed = path.read_bytes() != before
    if result.returncode != 0 and not changed:
        print(f"terraform fmt could not format {path.name}: {result.stderr.strip()[:300]}", file=sys.stderr)
    elif changed:
        messages.append(f"terraform fmt reformatted {path.name}. Re-read it before editing it again.")


def format_python(path: Path, root: Path, messages: list[str]) -> None:
    if shutil.which("ruff") is None:
        return
    if not any((root / name).exists() for name in ("ruff.toml", ".ruff.toml")) and "[tool.ruff" not in "".join(
        p.read_text(errors="ignore") for p in root.rglob("pyproject.toml") if not SKIP_PARTS & set(p.parts)
    ):
        return  # no ruff config: never format to ruff's defaults
    if any(marker in "".join(path.read_text(errors="ignore").splitlines(keepends=True)[:8]).lower() for marker in ("generated", "do not edit")):
        return
    before = path.read_bytes()
    run(["ruff", "format", str(path)], root)
    if path.read_bytes() != before:
        messages.append(f"ruff reformatted {path.name}. Re-read it before editing it again.")
    result = run(["ruff", "check", "--output-format", "concise", str(path)], root)
    if result.returncode == 1 and result.stdout.strip():
        messages.append(f"ruff reports problems in {path.name}; fix them before moving on:\n" + "\n".join(result.stdout.strip().splitlines()[:15]))


def main() -> None:
    event = json.load(sys.stdin)
    file_path = (event.get("tool_input") or {}).get("file_path")
    if not file_path:
        return
    path = Path(file_path)
    suffix = path.suffix.lower()
    if SKIP_PARTS & set(path.parts) or not path.is_file():
        return
    root = repo_root(path)
    # The workspace setup repo (the one carrying `repos.tsv`) holds no application code; its own files
    # are not formatted here.
    if root is None or (main_checkout(root) / "repos.tsv").is_file():
        return

    messages: list[str] = []
    handler = (
        format_node if suffix in PRETTIER else
        format_dotnet if suffix == ".cs" else
        format_terraform if suffix == ".tf" else
        format_python if suffix == ".py" else None
    )
    try:
        if handler is not None:
            handler(path, root, messages)
    except Exception:
        pass  # keep whatever was already recorded: the model must still hear that the file was rewritten

    if messages:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(messages)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
