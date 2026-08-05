---
name: fly
description: Ship the current work as a pull request with every local check green — read the repo's CHECKS.md (or derive its checks when there is none), branch off the default branch, run the checks and fix what breaks, commit, push, and open or update the PR. Finishes when the PR is open; it does not wait on CI. Use whenever the user says "fly", "ship it", "make a PR", "open a pull request", or asks to get the current work pushed and reviewable. Works in any repo; nothing here is project-specific.
---

# fly — get the work onto a green PR

> **The repo owns what "green" means. The skill owns getting there.**

Every wasted round trip in shipping comes from one of two places: running a check
the repo doesn't have, or skipping one it does. So the check list is not something
you re-infer on every run — it is a file the repo carries, **`CHECKS.md`**, and
this skill reads it.

**Local checks are the gate. CI is the audit.** This skill finishes when the PR is
open and the local checks are green. It takes one instant read of CI status on the
way out and then stops. It never blocks on a workflow run — see
[§7](#7-one-ci-probe-never-a-wait).

| | file |
|---|---|
| The procedure | **this file** |
| Writing a repo's `CHECKS.md` | [adopting-a-repo.md](adopting-a-repo.md) |
| `CHECKS.md` grammar, the report contract | [reference.md](reference.md) |
| When it goes wrong | [troubleshooting.md](troubleshooting.md) |

---

## 0. Preflight

Four facts, gathered before anything is changed. If one fails, **stop and say
which** — do not improvise around it.

```bash
git rev-parse --show-toplevel          # a git repo at all
git symbolic-ref -q HEAD               # not detached
git remote get-url origin              # somewhere to push
gh auth status                         # gh usable
```

The default branch, without a network round trip:

```bash
git symbolic-ref --quiet --short refs/remotes/origin/HEAD | sed 's|^origin/||'
```

Empty means `origin/HEAD` was never set locally (common on a `clone --depth` or an
older clone). Fix it once with `git remote set-head origin --auto`, then re-read.
Do **not** fall back to `git remote show origin` — it is a network call that hangs
offline and behind a proxy.

## 1. Find the checks

Walk this in order and **stop at the first hit**:

| # | Source | What it gives you |
|---|---|---|
| 1 | **`CHECKS.md`** at the repo root | The authority. Read nothing else. |
| 2 | `.github/workflows/*.y*ml` | The commands CI actually runs |
| 3 | `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md`, root **and** per-package | Often the local commands *and why* they're phrased that way |
| 4 | Language & platform inference | Last resort |

Rules that make this deterministic:

- **`CHECKS.md`, exactly.** At `git rev-parse --show-toplevel`. Case-sensitive. Not
  `.github/CHECKS.md`, not `checks.md`, not `server/CHECKS.md` — a monorepo gets
  **one** root file with a section per component.
- A **near-miss** filename (`checks.md`, `CHECKS.MD`, `CI-CHECKS.md`) is reported as
  a near-miss, never silently used. A typo that quietly downgrades you to inference
  is the exact failure this design exists to prevent.
- When `CHECKS.md` is present it is the **sole** authority. Workflows and CLAUDE.md
  are not consulted, not cross-checked, not merged in.
- When it is **absent**, derive from 2 → 3 → 4, and then **offer to write
  `CHECKS.md`** from what you derived. Every repo pays the derivation cost once.
  See [adopting-a-repo.md](adopting-a-repo.md).
- A **broken** section — `Dir:` that doesn't exist, a command that isn't runnable —
  is a **failure**, reported as such. Never silently skipped.

`CHECKS.md` is authority for *what to run*, but it can drift from CI. If CI later
fails on something the file doesn't list, **the file is the bug** — fix it in the
same PR.

## 2. Scope to what changed

```bash
base=$(git merge-base origin/<default> HEAD)
git diff --name-only "$base"...HEAD    # committed on this branch
git status --porcelain                 # not yet committed
```

Take the **union**. A section runs when any changed path matches its `When:` globs;
a section with no `When:` always runs. Report skipped sections *with the reason* —
"skipped, no `admin/**` changes" is information; a silently absent check is not.

**Unrelated dirty files.** Uncommitted work is normally the thing you're shipping,
but a stray edit in an unrelated area is not. List anything that doesn't belong to
this change and ask before staging it. Prefer explicit paths over `git add -A`.

## 3. Get onto a branch

- **On the default branch** → `git checkout -b <short-kebab-name>`. Name it for the
  change, not the ticket.
- **Already on a branch** → stay on it.
- **Behind the base?** Rebase **only** a branch that has never been pushed. Once a
  branch is pushed, rebasing it requires the force-push forbidden below — so either
  leave it, or ask. A stale base is CI's problem to report, not a reason to rewrite
  published history.

## 4. Run the checks, and fix what breaks

Per matched section:

1. Run `Setup:` first. A failed setup fails the whole section — do not run its
   checks against a stale environment. (This is the "green locally, red in CI" case:
   a teammate lands a dep bump, you pull without re-installing, and your checks and
   CI's disagree about which versions exist.)
2. Run its commands. Sections run **in parallel** with each other; a section marked
   `Serial: yes` runs its own commands in order.
3. Every command gets a timeout — `Timeout:` if declared, otherwise 15 minutes. A
   hung test suite is the same failure mode as waiting on CI, and just as fatal.

On failure:

- If the section declares `Fix:`, run it and re-run the check. Formatters and
  autofixable linters are most of what fails; letting a declared command handle it
  is deterministic and free.
- Otherwise fix the cause. **At most 2 attempts per check**, then stop and report.
  Grinding on a check that isn't converging burns the session and buries the signal.
- Re-run the **full matched set** after any fix. Fixes cause failures elsewhere.

**Never suppress to get green.** A disabled rule, a widened ignore, a skipped test
is a pass that lies. If a fix touched linter config (`.eslintrc`, `ruff.toml`,
`clippy.toml`, …) or added `# type: ignore`, `#[allow(…)]`, `eslint-disable`,
`@ts-expect-error`, `skip`/`xfail`, it goes in the report under **Suppressed**,
named. If a check cannot pass for a reason outside the change — a broken upstream
dep, a flaky external service — stop and say so rather than routing around it.

## 5. Commit

Read the style, don't assume it:

```bash
git log --oneline -15
```

Copy what you see: prefix scheme, imperative vs. past, casing, length, whether
bodies are used. Write the body about **why**, and about anything a reviewer would
otherwise have to reverse-engineer. Split into several commits when the work has
genuinely separable parts — but never a split that leaves an intermediate commit
broken.

## 6. Push, then open or update the PR

```bash
git push -u origin <branch>
gh pr view --json number,url,state --jq '.state'   # empty/error ⇒ no PR yet
```

- **No PR** → `gh pr create --base <default> --title … --body-file -` (heredoc).
- **PR already open** → `gh pr edit` the title and body so they describe **all**
  commits on the branch, not just the new ones. A PR whose description covers half
  its diff is worse than one with no description.
- **PR closed/merged** → don't reopen. Say so and stop.

Body leads with **why**, then what changed, then how it was verified, then what's
still open. Be honest in that last part — a named rough edge is worth more than a
clean-looking description. Follow the repo's PR template if it has one.

## 7. One CI probe, never a wait

```bash
gh pr checks --json name,bucket,link    # returns immediately; exit 8 = pending
```

Read it once. Report what it says. **Stop.**

Never `gh pr checks --watch`. Never `gh run watch`. Never a poll loop. The reasons
are concrete, not stylistic:

- `gh run watch` blocks indefinitely on a queued run, an approval gate, or a
  workflow that a path filter meant never to start.
- `gh run list --limit 1` picks *one* run. Repos routinely have several independent
  PR workflows; watching one and declaring green is simply wrong.
- On a change that triggers no workflow at all, `gh run list` returns the *previous*
  branch's run — so the wait watches something unrelated and reports on it.

If the user wants CI shepherded to green, that is a separate, deliberate request —
not the silent tail of every ship.

**A CI failure that the local run should have caught is a bug in `CHECKS.md`**, and
now there is somewhere to fix it. Add the missing check to the file, in the same PR.

## 8. Report

Always close with the block below — same shape every time, so it can be skimmed.
Full spec in [reference.md](reference.md#the-report).

```
🚀 Shipped — <one-line what this change is>

📦  PR #<n> · <pr title>
    <pr url>

🌿  <branch> → <base> · <n> commits · <n> files (+<a> −<d>)

✅  Local checks — <n> passed, <n> skipped · <duration> · source: CHECKS.md
    🖥️  server   format ✓  lint ✓  typecheck ✓  pytest ✓ (701)
    🌐  admin    skipped — no admin/** changes
    🧪  app      skipped — no app/** changes

🔄  CI  <n> workflows queued at push — not waited on
    gh pr checks <n>

📌  Left open
    • <anything unfinished, uncertain, or deferred>
```

Two lines are non-negotiable. **`source:`** names where the checks came from, so a
silent fallback to inference is visible rather than mistaken for a real check run.
And anything **Suppressed** gets its own section — never folded into a ✓.

When it stops short, report that instead, and keep it short enough to read:

```
🛑 Stopped — <what blocked> after <n> fix attempts

🌿  <branch> · <n> commits, not pushed
❌  <section> · <check>
    <the 5–10 lines that actually say what's wrong>
✅  <what did pass>  ·  ⏭️  <what was skipped and why>
```

## Guardrails

- **Never force-push** a branch under review without being asked.
- **Never merge**, and never enable auto-merge, unless the user asks.
- **Never rewrite pushed history** — that includes rebase, amend, and squash of
  commits already on `origin`.
- Don't commit secrets, `.env` files, or local-only config. Check `git status`
  before staging; prefer explicit paths to `git add -A`.
- Don't edit CI configuration to make a check pass.
- If the user asked to ship and the work isn't finished, say so before shipping it.
