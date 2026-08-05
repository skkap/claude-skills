# Reference — `CHECKS.md` grammar, resolution, and the report contract

## Why a markdown file

`CHECKS.md` is read by people as often as by agents. A developer joining the repo
should be able to open one file and know exactly what to run before pushing —
which is also, not coincidentally, exactly what this skill needs. A YAML manifest
would be easier to parse and worse at that job, and a file only a tool reads is a
file that rots.

So: markdown, with just enough shape to be unambiguous.

## Anatomy

````markdown
# Local checks

<optional prose: what this file is, how it relates to CI>

## <Section name>
When: `server/**`, `pyproject.toml`
Dir: `server`
Setup: `poetry install --no-interaction`
Fix: `poetry run ruff format src tests`
Serial: no
Timeout: 20m

```bash
poetry run ruff format --check src tests
poetry run lint
poetry run typecheck
```
````

A **section** is an `##` heading plus the field lines under it and its fenced
`bash` block. One section per independently-scoped unit of the repo — an app, a
package, a toolchain within an app (the Rust half of a Tauri app is its own
section because it scopes and serializes differently from the frontend).

### Fields

All optional. Order doesn't matter. One per line, directly under the heading,
before the fenced block.

| Field | Meaning | Default |
|---|---|---|
| `When:` | Comma-separated globs. The section runs if **any** changed path matches. | always runs |
| `Dir:` | Working directory for every command, relative to the repo root. | repo root |
| `Setup:` | Runs once before the section's checks. Failure fails the section. | none |
| `Fix:` | Autofix command. Run on failure, then the check is retried once. | none |
| `Serial:` | `yes` → run this section's commands in order, not in parallel. | `no` |
| `Timeout:` | Per-command budget (`90s`, `20m`). | `15m` |
| `Needs:` | Prose precondition, e.g. `Docker running (testcontainers)`. Reported, not enforced. | none |

### The fenced block

One command per line. Exactly what a human would type, in `Dir:`. No `&&`
chaining, no `cd` — that's what `Dir:` is for. Each line is a separately
reported check.

Commands should carry their own quiet flags (`-q`, `--tb=short`, `--no-cov`).
Check output lands in an agent's context; a 4,000-line pytest dump displaces the
information needed to fix it.

## Resolution rules

1. **Location.** `CHECKS.md` at `git rev-parse --show-toplevel`. Case-sensitive.
   No aliases, no `.github/` variant, no per-package copies.
2. **Authority.** Present ⇒ sole source. CI configs and CLAUDE.md are not read,
   not merged, not used to cross-check.
3. **Probe.** `git ls-files`, never `ls`/`test -f`/`[ -f ]`. macOS (APFS) and
   Windows (NTFS) are case-insensitive by default, so a filesystem test on a repo
   containing `CHECKS.md` answers *yes* to `checks.md` and `CHECKS.MD` as well —
   every macOS run would report a phantom near-miss, and a warning that fires
   always is a warning nobody reads. Git records the name as tracked, which is
   also the name Linux CI resolves. Cross-check with `stat -f %i` (BSD) or
   `stat -c %i` (GNU) if you need to prove two spellings are one inode.
4. **Near-miss.** A tracked file differing only in case or wording (`checks.md`,
   `CI-CHECKS.md`) is *reported* and *not used*. Silence here converts a typo into
   an invisible downgrade to inference.
5. **Broken section.** `Dir:` missing, or a command that cannot run, is a
   **failure**. Never a skip.
6. **Scope.** Changed paths = `git diff --name-only $(git merge-base origin/<default> HEAD)...HEAD`
   ∪ `git status --porcelain`. Globs match against repo-root-relative paths.
7. **Concurrency.** Sections run in parallel. Within a section, parallel unless
   `Serial: yes`. `Setup:` always precedes its own section's checks and never
   blocks another section.
8. **Fix budget.** `Fix:` once, then at most 2 further attempts, then stop.
9. **Drift.** If CI fails on something absent from `CHECKS.md`, the file is the
   defect. Fix it in the same PR.

## Serial sections

`Serial: yes` exists for real toolchain constraints, not caution. The canonical
case is cargo: it holds a build lock on the target directory, so parallel
invocations don't run concurrently — they queue, and each one can invalidate the
next one's cache. Serial is genuinely faster there.

Use it when commands contend for a lock, a port, a fixture database, or a shared
build directory. Not otherwise: parallel is the default because it's usually a
large win.

## The report

Every run ends with the block in [SKILL.md §8](SKILL.md#8-report). The contract:

| Line | Must contain |
|---|---|
| `🚀`/`🛑` | Outcome in one line — shipped, or what blocked |
| `📦` | PR number, title, **full URL** |
| `🌿` | branch → base, commit count, file/line delta |
| `✅` | per-section results, counts where meaningful, **`source:`** |
| `🔄` | CI state at the instant of the single probe, and that it wasn't waited on |
| `⚠️` | **Suppressed** — every ignore, disable, or skip a fix introduced. Omit only if there were none |
| `📌` | Left open — deferred, uncertain, or unfinished. Omit only if genuinely nothing |

**`source:`** is load-bearing. It reads `CHECKS.md`, `CI workflows`,
`CLAUDE.md`, or `inferred (no CHECKS.md)`. Anything but the first is a standing
invitation to adopt the file, and the last means the checks are a guess — the
report has to say so.

**Suppressed** is the other one. A ✓ obtained by widening an ignore is not the
same fact as a ✓ obtained by fixing the code, and collapsing the two is how a
repo's checks quietly stop meaning anything.

## Exit conditions

`fly` ends in exactly one of three states, and says which:

- **Shipped** — every matched check green, commits pushed, PR open. CI probed once.
- **Stopped** — a check won't pass within budget, or a preflight fact is missing,
  or something needs a decision that isn't the skill's to make. Nothing is pushed
  that shouldn't be; the report says what and why.
- **Nothing to do** — branch is clean, checks green, PR already open and current.
  Re-report; do not manufacture an empty commit.
